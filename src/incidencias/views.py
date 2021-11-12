from django.shortcuts import render,redirect
from django.views.generic import CreateView, DeleteView
from .models import Incidencia, ComentarioIncidencia
from inventario.models import Equipo, Usuario, Asignacion
from django.urls import reverse_lazy, reverse
from .forms import ComentarioIncidenciaForm, EstadoIncidenciaForm

class VistaCreacionIncidencia(CreateView):
    model = Incidencia
    fields = ['equipo', 'usuario']
    template_name = 'crear-incidencia.html'
    success_url = reverse_lazy('lista-incidencias')

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(VistaCreacionIncidencia, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        query_usuario = self.request.GET.get('usuario','')
        query_equipo = self.request.GET.get('equipo','')
        if query_usuario:
            initial['usuario'] = query_usuario
            asignacion = Asignacion.objects.filter(usuario=query_usuario, data_fin__isnull=True)
            if asignacion:
                initial['equipo']= asignacion[0].equipo
        if query_equipo:
            initial['equipo'] = query_equipo
            asignacion = Asignacion.objects.filter(equipo=query_equipo, data_fin__isnull=True)
            if asignacion:
                initial['usuario']= asignacion[0].usuario
        return initial

    def get_success_url(self):
        return reverse("vista-incidencia", kwargs={"pk": self.object.pk})

class VistaBorradoIncidencia(DeleteView):
    model = Incidencia
    template_name = 'eliminar-incidencia.html'
    success_url = reverse_lazy('lista-incidencias')

class VistaBorradoComentario(DeleteView):
    model = ComentarioIncidencia
    template_name = 'eliminar-comentario.html'

    def get_success_url(self):
        query_pk = self.request.GET.get('incidencia_pk','')
        if query_pk:
            return reverse("vista-incidencia", kwargs={"pk": query_pk})
        else:
            return reverse("lista-incidencias")

def listaIncidencias (request):
    incidencias_plus = [ {
        "pk": incidencia.pk,
        "estado": incidencia.estado,
        "equipo": incidencia.equipo,
        "usuario": incidencia.usuario,
        "numServizoExterno": incidencia.numServizoExterno,
        "tipoServizoExterno": incidencia.tipoServizoExterno,
        "data": incidencia.data,
        "comentarios": [{
                "desc": comentario.descricion,
                "ten_fincheiro": comentario.ficheiro is not None,
                "data": comentario.data
            } for comentario in ComentarioIncidencia.objects.filter(incidencia=incidencia)[:3]]
        } for incidencia in Incidencia.objects.all().order_by('estado','-data')
    ]
    return render(request, 'lista-incidencias.html', {'incidencias': incidencias_plus})


def vistaIncidencia (request, pk):
    incidencia = Incidencia.objects.get(pk=pk)
    incidencia_plus = {
        "pk": incidencia.pk,
        "estado": incidencia.estado,
        "data": incidencia.data,
        "equipo": incidencia.equipo,
        "usuario": incidencia.usuario,
        "numServizoExterno": incidencia.numServizoExterno,
        "tipoServizoExterno": incidencia.tipoServizoExterno,
        "comentarios": [{
                "pk": comentario.pk,
                "desc": comentario.descricion,
                "ficheiro": comentario.ficheiro,
                "data": comentario.data
            } for comentario in ComentarioIncidencia.objects.filter(incidencia=incidencia)]
        }

    return render(request, 'vista-incidencia.html', {
        'incidencia': incidencia_plus,
        'form_comentario': ComentarioIncidenciaForm(initial={'incidencia': incidencia}), 'form_estado': EstadoIncidenciaForm()})

def engadirComentario (request):
    if request.method != 'POST':
        return
    form_data = ComentarioIncidenciaForm(request.POST, request.FILES)
    form_data.save()

    return vistaIncidencia(request, request.POST['incidencia'])

def cambiarEstadoIncidencia(request, pk):
    if request.method != 'POST':
        return
    incidencia = Incidencia.objects.get(pk=pk)
    form_data = EstadoIncidenciaForm(request.POST, request.FILES, instance=incidencia)
    form_data.save()

    return redirect(reverse('vista-incidencia', kwargs={'pk': pk}))
