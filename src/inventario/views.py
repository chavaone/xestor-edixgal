from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import Usuario, Equipo, Asignacion
from incidencias.models import Incidencia, ComentarioIncidencia
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.core.paginator import Paginator
from django.db.models import Q

class VistaCreacionUsuario(CreateView):
    model = Usuario
    fields = ['nome', 'apelidos','nivel',  'curso']
    template_name = 'crear-usuario.html'
    success_url = reverse_lazy('lista-usuarios')

class VistaCreacionEquipo(CreateView):
    model = Equipo
    fields = ['numeroDeSerie', 'info']
    template_name = 'crear-equipo.html'
    success_url = reverse_lazy('lista-equipos')

class VistaCreacionAsignacion(CreateView):
    model = Asignacion
    fields = ['equipo', 'usuario', 'manual']
    template_name = 'crear-asignacion.html'

    def get_success_url(self):
        query_usuario = self.request.GET.get('usuario','')
        query_equipo = self.request.GET.get('equipo','')

        if query_usuario:
            return reverse("vista-usuario", kwargs={"pk": query_usuario})

        if query_equipo:
            return reverse("vista-equipo", kwargs={"pk": query_equipo})

        return reverse_lazy('lista-equipos')

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(VistaCreacionAsignacion, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        query_usuario = self.request.GET.get('usuario','')
        query_equipo = self.request.GET.get('equipo','')
        if query_usuario: initial['usuario'] = query_usuario
        if query_equipo: initial['equipo'] = query_equipo
        return initial

class VistaEdicionUsuario(UpdateView):
    model = Usuario
    fields = '__all__'
    template_name = 'editar-usuario.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("vista-usuario", kwargs={"pk": pk})

class VistaEdicionEquipo(UpdateView):
    model = Equipo
    fields = '__all__'
    template_name = 'editar-equipo.html'

    def get_success_url(self):
        pk = self.kwargs["pk"]
        return reverse("vista-equipo", kwargs={"pk": pk})

class VistaBorradoUsuario(DeleteView):
    model = Usuario
    success_url = reverse_lazy('lista-alumnos')

class VistaBorradoEquipo(DeleteView):
    model = Equipo
    success_url = reverse_lazy('lista-equipos')
    template_name = 'eliminar-equipo.html'


def listaUsuarios (request):
    numPaxina = request.GET.get('paxina', '1')
    orderBy = request.GET.get('order-by', 'nivel curso apelidos').split(' ')
    filter = request.GET.get('filter', '').split(' ')
    busca = request.GET.get('busca', '')

    usuarios = Usuario.objects.all()
    if filter:
        if filter[0]: usuarios = usuarios.filter(nivel=filter[0])
        if len(filter) == 2: usuarios = usuarios.filter(curso=filter[1])
    if busca:
        usuarios = usuarios.filter(Q(nome__contains=busca) | Q(apelidos__contains=busca))
    if orderBy:
        usuarios = usuarios.order_by(*orderBy)


    paxinador = Paginator(usuarios, 30)
    paxina = paxinador.page(int(numPaxina))

    data = {
        'usuarios': [{
            "pk": usuario.pk,
            "nome": usuario.nome,
            "apelidos": usuario.apelidos,
            "nivel": usuario.nivel,
            "curso": usuario.curso,
            "equipos": [ {
                "pk": asignacion.equipo.pk,
                "sn": asignacion.equipo.numeroDeSerie
                } for asignacion in Asignacion.objects.filter(usuario=usuario).exclude(data_fin__isnull=False)
                ],
            "incidencias": [ {
                "pk": incidencia.pk,
                } for incidencia in Incidencia.objects.filter(usuario=usuario)
            ],
        } for usuario in paxina.object_list],
        'lista_paxinas': paxinador.page_range,
        'paxina': paxina,
        'opcions_filtro': sorted([' '.join(a) for a in Usuario.objects.values_list('nivel', 'curso').distinct()]),
        'filtro_activo': ' '.join(filter),
        'busca': busca
    }

    return render(request, 'lista-usuarios.html', data)

def vistaUsuario (request, pk):
    usuario = Usuario.objects.get(pk=pk)
    usuario_plus = {
        "pk": usuario.pk,
        "nome": usuario.nome,
        "apelidos": usuario.apelidos,
        "nivel": usuario.nivel,
        "curso": usuario.curso,
        "equipos": [ {
            "pk": asignacion.equipo.pk,
            "pk_asignacion": asignacion.pk,
            "sn": asignacion.equipo.numeroDeSerie,
            "info": asignacion.equipo.info,
            "data_ini": asignacion.data_ini,
            "data_fin": asignacion.data_fin
            } for asignacion in Asignacion.objects.filter(usuario=usuario).order_by('data_fin')
            ],
        "incidencias": [ {
            "pk": incidencia.pk,
            "aberta": incidencia.aberta,
            "data": incidencia.data,
            "comentarios": [{
                    "desc": comentario.descricion,
                    "ten_fincheiro": comentario.ficheiro is not None,
                    "data": comentario.data
                } for comentario in ComentarioIncidencia.objects.filter(incidencia=incidencia)[:2]]
            } for incidencia in Incidencia.objects.filter(usuario=usuario)
        ],
    }
    return render(request, 'vista-usuario.html', {'usuario': usuario_plus})

def listaEquipos (request):
    busca = request.GET.get('busca', '')

    equipos = Equipo.objects.all()
    if busca:
        equipos = equipos.filter(numeroDeSerie__contains=busca)

    datos = {
     'equipos': [{
         "pk": equipo.pk,
         "sn": equipo.numeroDeSerie,
         "info": equipo.info,
         "activo": equipo.enActivo,
         "usuarios": [ {
             "pk": asignacion.usuario.pk,
             "nome": asignacion.usuario.apelidos + ", "  + asignacion.usuario.nome
             } for asignacion in Asignacion.objects.filter(equipo=equipo).exclude(data_fin__isnull=False)
         ],
         "incidencias": [ {
             "pk": incidencia.pk,
             } for incidencia in Incidencia.objects.filter(equipo=equipo).exclude(aberta=False)
         ],
     } for equipo in equipos],
     'busca': busca
    }
    return render(request, 'lista-equipos.html', datos)


def vistaEquipo (request, pk):
    equipo = Equipo.objects.get(pk=pk)
    equipo_plus = {
        "pk": equipo.pk,
        "sn": equipo.numeroDeSerie,
        "info": equipo.info,
        "activo": equipo.enActivo,
        "usuarios": [ {
            "pk": asignacion.usuario.pk,
            "pk_asignacion": asignacion.pk,
            "nome": asignacion.usuario.apelidos + ", "  + asignacion.usuario.nome,
            "nivel": asignacion.usuario.nivel + " " + asignacion.usuario.curso,
            "data_ini": asignacion.data_ini,
            "data_fin": asignacion.data_fin
            } for asignacion in Asignacion.objects.filter(equipo=equipo).order_by('data_fin')
        ],
        "incidencias": [ {
            "pk": incidencia.pk,
            "aberta": incidencia.aberta,
            "data": incidencia.data,
            "comentarios": [{
                    "desc": comentario.descricion,
                    "ten_fincheiro": comentario.ficheiro is not None,
                    "data": comentario.data
                } for comentario in ComentarioIncidencia.objects.filter(incidencia=incidencia)[:2]]
            } for incidencia in Incidencia.objects.filter(equipo=equipo).order_by('-aberta')
        ],
    }
    return render(request, 'vista-equipo.html', {'equipo': equipo_plus})


def cambiarEstadoEquipo(request, pk):
    equipo = Equipo.objects.get(pk=pk)

    equipo.enActivo = not equipo.enActivo
    equipo.save()

    return vistaEquipo(request, pk)

def darDeBaixaUsuario(request, pk):
    usuario = Usuario.objects.get(pk=pk)

    if usuario.nivel == 'PR':
        usuario.nivel = 'eP'
        usuario.curso = ''
    elif usuario.nivel:
        usuario.nivel = 'eA'
        usuario.curso = ''
    usuario.save()

    return vistaUsuario (request, pk)

def terminarAsignacion(request, pk):
    asignacion = Asignacion.objects.get(pk=pk)
    asignacion.data_fin = timezone.now()
    asignacion.save()

    query_usuario = request.GET.get('usuario','')
    query_equipo = request.GET.get('equipo','')

    if query_equipo:
        return vistaEquipo(request, query_equipo)

    if query_usuario:
        return vistaUsuario(request, query_usuario)
    return listaEquipos(request)
