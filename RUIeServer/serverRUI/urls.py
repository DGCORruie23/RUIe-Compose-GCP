"""
URL configuration for serverRUI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler404
from usuario import views
from usuarioL.views import index, pagina404
from dashboard import views as viewsDash
from django.contrib.auth import views as viewsL

urlpatterns = [
    path('', index, name="index"),

    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('log-in/', viewsL.LoginView.as_view(template_name= 'base/log_in.html'), name='log-in'),
    path('log-out', viewsL.LogoutView.as_view(), name="logout" ),

    path('login/', include('usuario.urls')),
    path('info/cargarPais', views.cargarPais, name="cargar_pais"),
    path('info/cargarFuerza', views.cargarEdoFuerza, name="cargar_fuerza"),
    #path('dashboard/', views.cargarEdoF, name="cargar_f"),
    path('info/cargarMunicipios', views.cargarMunicipios, name="cargar_municipios"),
    path('info/cargarPuntosI', views.cargarPuntoI, name="cargar_puntoI"),
    path('cargar/Usuarios', views.cargaMasivaUser, name="cargar_usuarios"),
    path('info/Paises', views.infoPaises),
    path('info/Fuerza', views.infoEstadoFuerza),
    path('info/Municipios', views.infoMunicipios),
    path('info/PuntosI', views.infoPuntosInterna),
    path('info/frases', views.infoFrases),
    path('info/descargaN', views.generarExcelNombres),
    path('info/descargaC', views.generarExcelConteo),
    path('info/descargaD', views.pagDuplicados),
    path('info/fechas', views.generarExcelFechas, name="fechas_descarga"),
    path('info/fechasOR', views.generarExcelFechasOR, name="fechas_OR"),
    path('info/descargaD_a', views.downloadDuplicados, name="descarga_duplicados"),
    path('info/descargaTab22', views.generarExcelTab),
    path('info/descargaExcel', views.generarExcelORs, name="descarga_excel"),
    path('info/descargaExcelUsuarios', views.generarExcelUsuarios, name="descarga_excelUsuarios"),
    path('info/descargaExcelEdoFuerza', views.generarExcelEdoFuerza, name="descarga_excelEdoFuerza"),
    path('info/descargaExcelPuntosI', views.generarExcelPuntosI, name="descarga_excelPuntosI"),
    path('info/updateApp', views.msgUpdateUrl, name="info_app"),

    path('info/politica_privacidad', views.politica_privacidad, name="info_politica_privacidad"),

    path('registro/insertR', views.insert_rescates),
    path('registro/insertC', views.insert_conteo),
    path('registro/insertD', views.insert_disuadidos),
    path('descargas/', views.servirApps, name="descargas"),
    path('descargas/apk', views.downloadAPK, name="descarga_android"),

    path('estadistica/', include('estadistica.urls')),

    # path('info/pruebas/edoFuerza', viewsDash.edoFuerza, name="pagina_pruebas_edoFuerza"),
    # path('info/pruebas/edoFuerza/editarEdoFuerza/<int:id_edo_fuerza>', viewsDash.editar_estado_fuerza, name='editar_estado_fuerza'),
    # path('info/pruebas/edoFuerza/eliminarEdoFuerza/<int:id_edo_fuerza>', viewsDash.eliminarEdoFuerza, name='eliminar_estado_fuerza'),
    # path('info/pruebas/edoFuerza/anadirPunto', viewsDash.agregar_punto, name='agregar_punto'),


    # path('info/pruebas/usuarios', viewsDash.Usuarios, name="pagina_pruebas_usuarios"),
    # path('info/pruebas/usuarios/editarUsuario/<int:id_usuario>', viewsDash.editar_usuario, name='editar_usuario'),
    # path('info/pruebas/usuarios/anadirUsuario', viewsDash.agregar_usuario, name='agregar_usuario'),
    # path('info/pruebas/usuarios/eliminarUsuario/<int:id_usuario>', viewsDash.eliminarUsuario, name='eliminar_usuario'),
]

handler404 = pagina404