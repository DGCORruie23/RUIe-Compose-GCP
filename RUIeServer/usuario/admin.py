from django.contrib import admin

from .models import Usuario, Paises, EstadoFuerza, Frases, Municipios, PuntosInternacion, RescatePunto, ConteoRapidoPunto, MsgUpdate, DisuadidosPunto

class RescateAdmin(admin.ModelAdmin):
    list_display = ['idRescate', 'oficinaRepre', 'puntoEstra']
    list_editable = ['puntoEstra']
    list_filter = ['oficinaRepre', 'puntoEstra']
    search_fields = ['oficinaRepre', 'puntoEstra']

class EstadoAdmin(admin.ModelAdmin):
    list_display = ['idEdoFuerza', 'oficinaR', 'nomPuntoRevision', 'tipoP']
    list_filter = ['oficinaR', 'tipoP']
    search_fields = ['oficinaR', 'nomPuntoRevision']

class InternacionAdmin(admin.ModelAdmin):
    list_display = ['idPuntoInter', 'estadoPunto', 'nombrePunto', 'tipoPunto']
    list_filter = ['estadoPunto', 'tipoPunto']
    search_fields = ['nombrePunto']

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['idUser','estado', 'nombre', 'apellido', 'nickname', 'str_pass','tipo_disp']
    list_editable = ['estado','nombre', 'apellido', 'nickname','str_pass','tipo_disp']
    list_filter = ['str_pass','tipo_disp']
    search_fields = ['nickname','nombre','idUser', 'tipo_disp']

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Paises)
admin.site.register(EstadoFuerza, EstadoAdmin)
admin.site.register(Frases)
admin.site.register(Municipios)
admin.site.register(PuntosInternacion, InternacionAdmin)
admin.site.register(RescatePunto, RescateAdmin)
admin.site.register(DisuadidosPunto)
admin.site.register(ConteoRapidoPunto)
admin.site.register(MsgUpdate)
