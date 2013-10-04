#enconding:utf-8
from django.forms import ModelForm
from django import forms
from models import *
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


	

class AlumnoForm(forms.ModelForm):
	class Meta:
		model = Alumno
		exclude = ('usuario')
		

class ProfesorForm(forms.ModelForm):
	class Meta:
		model = Profesor
		exclude = ('usuario')

class CoordinadorForm(forms.ModelForm):
    class Meta:
        model = Coordinador
		

class ContactoForm(forms.Form):
	correo = forms.EmailField(label="Tu correo electronico")
	mensaje = forms.CharField(widget=forms.Textarea)

class CuotaAlumnoForm(forms.Form):
	nombre   = forms.CharField(label="Nombre")
	apellido = forms.CharField(label="Apellido")
	anio     = forms.CharField(label='Año')
	
class CuotasForm(forms.ModelForm):
    class Meta:
        model = Cuotas


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
	
		
class PlanEstudioForm(forms.ModelForm):
    class Meta:
        model = PlanEstudio

class ProgramaForm(forms.ModelForm):
    class Meta:
        model = Programa		
		
class TurnoExamenForm(forms.ModelForm):
    class Meta:
        model = TurnoExamen
		
class ItemTurnoExamenForm(forms.ModelForm):
    class Meta:
		model = ItemTurnoExamen	
		exclude = ('turno')
		
class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
		
class LibroAulaForm(forms.ModelForm):
    class Meta:
        model = LibroAula
		
class ConsultaForm(forms.Form):
	legajo = forms.IntegerField(label="Legajo")
	
class ConsultarAlumnoForm(forms.Form):
	nombre   = forms.CharField(label="Nombre")
	apellido = forms.CharField(label="Apellido")
	
class CursoForm(forms.ModelForm):
	class Meta:
		model=Materia
		fields = ('carrera', 'curso')	
	anio  = forms.IntegerField(label='Año')
	
class InscripcionMateriaForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	anio  = forms.IntegerField(label='Año')	

class ConsultaLibroAulaForm(forms.ModelForm):
	class Meta:
		model = LibroAula
		fields = ('materia', 'anio')

		
class NoticiaForm(forms.ModelForm):
	class Meta:
		model = Noticia

class ConsultarTurnoExamenForm(forms.Form):
	carrera= forms.ModelChoiceField(queryset=Carrera.objects.all(), label='Carrera')
	anio  = forms.IntegerField(label='Año')
	numero  = forms.IntegerField(label='Turno Número')

class ConsultaFinalesForm(forms.Form):
	anio = forms.IntegerField(label='Año Lectivo')
	turno = forms.IntegerField(label='Turno Nro')
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	
	
class RegistrarParcialForm(forms.ModelForm):
	class Meta:
		model = Parcial
		
class ConsultaParcialForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	legajo  = forms.IntegerField(label='Legajo')
	tipo	= forms.ModelChoiceField(queryset=TipoExamenParcial.objects.all(), label='Tipo de Examen')
			
class ParcialForm(forms.ModelForm):
	class Meta:
		model = Parcial		
	
# COLOQUIO		
class RegistrarColoquioForm(forms.ModelForm):
	class Meta:
		model = Coloquio
		
class ConsultaColoquioForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	legajo  = forms.IntegerField(label='Legajo')
		
class ColoquioForm(forms.ModelForm):
	class Meta:
		model = Coloquio	

# MENU AULA 

	
# Asitencia

class ConsultaAsisForm(forms.Form):
	legajo = forms.IntegerField(label='Legajo')
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	anio 	= forms.IntegerField(label='Año')
	
class AsistenciaForm(forms.ModelForm):
	class Meta:
		model  = Asistencia
		exclude = ('porcentaje')
		
#####INFORMES ###


# NOTAS PARCIALES #
class ConsultanotasForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	anio 	= forms.IntegerField(label='Año')
	curso	= forms.IntegerField(label='Curso')

	
	
class ConsultafinalForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	anio 	= forms.IntegerField(label='Año')
	turno	= forms.IntegerField(label='Turno Nro.')
	legajo  = legajo = forms.IntegerField(label='Legajo')
	
	
class FinalForm(forms.ModelForm):
	class Meta:
		model	= Final
		
class CrearProgramaForm(forms.ModelForm):
	class Meta:
		model = Programa
		
class CrearContenidoForm(forms.ModelForm):
	class Meta:
		model = Contenidos
		exclude = ('programa')
		
		
############## MENU ALUMNOS!!!############

class ConsultarPlanEstudioForm(forms.Form):
	nombre= forms.ModelChoiceField(queryset=PlanEstudio.objects.all(), label='Nombre')
	
class ConsultaExamenForm(forms.Form):
	materia = forms.ModelChoiceField(queryset=Materia.objects.all(), label='Materia')
	anio = forms.IntegerField(label='Año')
	
class ConsultarCorrelativaForm(forms.Form):
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), label='Carrera')	
	
class CambioPasswordForm(forms.Form):
	password_one = forms.CharField(label="Nueva Contraseña", widget=forms.PasswordInput(render_value=False))
	password_two = forms.CharField(label="Confirmar Contraseña", widget=forms.PasswordInput(render_value=False))
	
	def clean_password_two(self):
		password_one = self.cleaned_data['password_one']
		password_two = self.cleaned_data['password_two']
		if password_one == password_two:
			return password_two
		else:
			raise forms.ValidationError('Las contraseñas no coinciden')


class InscribirMateriaForm(forms.Form):
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), label='Carrera')
	curso = forms.IntegerField(label='Curso')
	
class InscribirExamenForm(forms.Form):
	carrera = forms.ModelChoiceField(queryset=Carrera.objects.all(), label='Carrera')
	curso = forms.IntegerField(label='Curso')
	turno = forms.IntegerField(label='Turno de Exámen Nro')
			