from django.contrib import admin
from .models import Empleado
from .models import Acta, Anexo, Balance, Ficha_individuo, Expediente, Solicitud, \
    Seguimiento, Visita, Informe_tecnico, Recaudo, Timestampable


admin.site.register(Acta)
admin.site.register(Anexo)
admin.site.register(Balance)
#admin.site.register(UserAdmin)
#admin.site.register(Coordinacion)
admin.site.register(Empleado)
admin.site.register(Informe_tecnico)
admin.site.register(Ficha_individuo)
admin.site.register(Expediente)
admin.site.register(Recaudo)
admin.site.register(Seguimiento)
#admin.site.register(Solicitante)
admin.site.register(Solicitud)
admin.site.register(Visita)

