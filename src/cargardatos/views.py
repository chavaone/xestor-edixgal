from django.shortcuts import render
import requests as req
from bs4 import BeautifulSoup
from inventario.models import Usuario, Equipo, Asignacion
from django.http import HttpResponse
import json
from django.utils import timezone

def _eliminarNonVistos(obx_alumnos, obx_profesores):
    return ""

def _procesar_datos (sn, nome=None, apelidos=None, curso_raw=None):
    log = ""
    obx_vistos = {'equipos':[], 'usuarios': []}
    equipo, equipo_creado = Equipo.objects.get_or_create(numeroDeSerie=sn)

    obx_vistos['equipos'].append(equipo)

    if equipo_creado:
        log += '<p class="creacion">Equipo con SN %s creado.</p>' % (sn)

    if not (nome and apelidos): #Equipo sen asignar. Eliminanse as asignacions existentes.
        asignacions = Asignacion.objects.filter(equipo=equipo, manual=False).exclude(data_fin__isnull=False)
        for asignacion in asignacions:
            asignacion.data_fin = timezone.now()
            asignacion.save()
            log += '<p class="eliminacion">Asignacion de equipo con SN %s e usuario <em>%s, %s</em> eliminada.</p>' % (sn, asignacion.usuario.apelidos, asignacion.usuario.nome)
        return log, obx_vistos

    usuario, usuario_creado = Usuario.objects.get_or_create(nome = nome, apelidos=apelidos)

    obx_vistos['usuarios'].append(usuario)

    if curso_raw:
        nivel = 'S' + curso_raw[0]
        curso = curso_raw[-1]
    else:
        nivel = 'PR'
        curso = ''

    if usuario_creado:
        log += '<p class="creacion">Usuario <em>%s, %s</em> creado.</p>' % (apelidos, nome)
        usuario.nivel = nivel
        usuario.curso = curso
        usuario.save()
    elif usuario.nivel != nivel or usuario.curso != curso:
        log += '<p class="actualizacion">Datos usuario <em>%s, %s</em> actualizados.</p>' % (apelidos, nome)
        usuario.nivel = nivel
        usuario.curso = curso
        usuario.save()

    asignacion, asignacion_creada = Asignacion.objects.get_or_create(equipo=equipo, usuario=usuario)

    if asignacion_creada:
        log += '<p class="creacion">Asignacion de equipo con SN %s e usuario <em>%s, %s</em> creada.</p>' % (sn, apelidos, nome)

    return log, obx_vistos

def _cargarDatos(text, alumnado):
    log = ""
    obx_vistos = {'equipos':[], 'usuarios': []}

    soup = BeautifulSoup(text, 'html.parser')
    if alumnado:
        filas = soup.select("table.listado2 tr")[2:]
    else:
        filas = soup.select("table.listado tr")[2:]

    for fila in filas:
        columnas = fila.select("td")
        if alumnado:
            sn = columnas[2].text.strip()
            nome = columnas[3].text.strip().title()
            apelidos = columnas[4].text.strip().title()
            curso_raw = columnas[5].text.strip()
        else:
            sn = columnas[1].text.strip()
            nome = columnas[2].text.strip().title()
            apelidos = columnas[3].text.strip().title()
            curso_raw = None

        log_fila, obxs_fila =  _procesar_datos (sn, nome=nome, apelidos=apelidos, curso_raw=curso_raw)
        log += log_fila
        obx_vistos['equipos'] += obxs_fila['equipos']
        obx_vistos['usuarios'] += obxs_fila['usuarios']

    return log, obx_vistos


def cargarDatosXestor(request):

    usuario = request.GET.get('usuario', '')
    contrasinal = request.GET.get('contrasinal', '')

    if not (usuario and contrasinal):
        ret_data = {
            'status': 'DATA_MISSING'
        }
        return HttpResponse(json.dumps(ret_data), content_type='application/json')

    sesion = req.Session()

    res_login = sesion.post("https://www.edu.xunta.gal/uac/premium/admin/acceso_usuarios_ldap.php",
                            data= {
                                    'action': "validate_captcha",
                                    'usuario': usuario,
                                    'clave': contrasinal
                            })

    if res_login.text.find("ventanaLogin") != -1:
        ret_data = {
            'status': 'LOGIN_FAIL'
        }
        return HttpResponse(json.dumps(ret_data), content_type='application/json')

    res_alumnos = sesion.get("https://www.edu.xunta.gal/uac/premium/admin/equipos_colegio.php")
    log_alumnos, obx_vistos_alumnos = _cargarDatos(res_alumnos.text, True)

    res_profesores = sesion.get("https://www.edu.xunta.gal/uac/premium/admin/equiposProfesorado_colegio.php")
    log_profesores, obx_vistos_profesores =  _cargarDatos(res_profesores.text, False)

    #log_eliminacion = _eliminarNonVistos(obx_vistos_alumnos, obx_vistos_profesores)

    ret_data = {
        'status': 'OK',
        'log': log_alumnos + log_profesores  + "<p>Terminado!</p>"#+ log_eliminacion
    }
    return HttpResponse(json.dumps(ret_data), content_type='application/json')
