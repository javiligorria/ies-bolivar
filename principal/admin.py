from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from principal.models import *


admin.site.register(Persona, admin.ModelAdmin)
admin.site.register(Noticia, admin.ModelAdmin)
admin.site.register(Carrera, admin.ModelAdmin)
admin.site.register(Coordinador, admin.ModelAdmin)
admin.site.register(Condicion, admin.ModelAdmin)
admin.site.register(Coloquio, admin.ModelAdmin)
admin.site.register(Parcial, admin.ModelAdmin)
admin.site.register(Final, admin.ModelAdmin)
admin.site.register(Profesor, admin.ModelAdmin)
admin.site.register(Alumno, admin.ModelAdmin)
admin.site.register(PlanEstudio, admin.ModelAdmin)
admin.site.register(Telefonos, admin.ModelAdmin)
admin.site.register(Materia, admin.ModelAdmin)
admin.site.register(LibroAula, admin.ModelAdmin)
admin.site.register(Asistencia, admin.ModelAdmin)
admin.site.register(InscripcionMateria, admin.ModelAdmin)
admin.site.register(TipoExamenParcial, admin.ModelAdmin)
admin.site.register(Examen, admin.ModelAdmin)
admin.site.register(Cuotas, admin.ModelAdmin)
admin.site.register(Programa, admin.ModelAdmin)
admin.site.register(Contenidos, admin.ModelAdmin)
admin.site.register(TurnoExamen, admin.ModelAdmin)
