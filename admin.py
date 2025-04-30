from django.contrib import admin
from .models import Cuidador, Usuario, Medicamento, Recordatorio, Historial

admin.site.register(Cuidador)
admin.site.register(Usuario)
admin.site.register(Medicamento)
admin.site.register(Recordatorio)
admin.site.register(Historial)
