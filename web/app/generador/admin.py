from django.contrib import admin
from models import 	Configuracion, Estado, TituloValor, Unidad, Version

class Config(admin.StackedInline):
    model = Configuracion
    exclude = ( 'fecha_inicio','valor_energia', 'valor_papel', 'valor_tintas',
                'porcentaje_valuacion', 'unidad', 'ventana_inactividad')

class VersionAdmin(admin.ModelAdmin):
    inlines = [Config]
    list_display = ['info', 'nombre']

admin.site.register(Unidad)
admin.site.register(TituloValor)
admin.site.register(Estado)
admin.site.register(Version, VersionAdmin)
