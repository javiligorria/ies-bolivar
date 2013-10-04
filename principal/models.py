from django.db import models
from django.contrib.auth.models import User

class Noticia(models.Model):
	
	def url(self,filename):
		ruta = 'MultimediaData/Noticia/%s'%(str(filename))
		return ruta
	
	titulo = models.CharField(max_length=765,  blank=True)
	contenido = models.TextField(max_length=765,  blank=True)
	imagen = models.ImageField(upload_to=url,blank=True )

	def __unicode__(self):
		return u"%s"%(self.titulo)

		
class Carrera(models.Model):
	nombre         = models.CharField(max_length=60)
	observaciones  = models.CharField(max_length=765,  blank=True)
    
	class Meta:
		db_table = u'Carrera'
		verbose_name_plural = 'Carrera'	
	def __unicode__(self):
		return u"%s"%(self.nombre)
			


class Persona(models.Model):
	legajo         =  models.IntegerField(verbose_name='Legajo', primary_key=True)
	usuario        =  models.OneToOneField(User, unique=True)
	nombre1        =  models.CharField(max_length=30, verbose_name='Primer Nombre')
	nombre2        =  models.CharField(max_length=30, verbose_name='Segundo Nombre', blank=True)
	apellido       =  models.CharField(max_length=30, verbose_name='Apellido')
	dni            =  models.IntegerField(verbose_name='DNI')
	calle          =  models.CharField(max_length=765, verbose_name='Calle')
	numero         =  models.IntegerField(verbose_name='Numero')
	barrio         =  models.CharField(max_length=765, verbose_name='Barrio')
	ciudad         =  models.CharField(max_length=135, verbose_name='Ciudad')
	fecha_nac      =  models.DateField(verbose_name='Fecha_nacimiento')
	email          =  models.EmailField()
		
	class Meta:
		db_table = u'Persona'
		verbose_name_plural = 'Persona'
	def __unicode__(self):
		return u"%s, %s %s" % (self.apellido, self.nombre1, self.nombre2)	
    
class Alumno(Persona):
	carrera        =  models.ForeignKey(Carrera)
	anio_ingreso   =  models.IntegerField(verbose_name='Anio de Ingreso', blank=True, null=True)
	sec_completo   =  models.BooleanField(verbose_name='Secundario Completo')
	titulo         =  models.CharField(verbose_name='Titulo',max_length=135,blank=True)
	fotocopia_dni  =  models.BooleanField(verbose_name='Fotocopia DNI')
	ficha_medica   =  models.BooleanField(verbose_name='Ficha Medica')
	foto_carnet    =  models.BooleanField(verbose_name='Foto Carnet')
	partida_nac    =  models.BooleanField(verbose_name='Partida de Nacimiento')
	
	
	class Meta:
		db_table = u'Alumno'
		verbose_name_plural = 'Alumno'
	class Meta:
		ordering = ["apellido"]
	def __unicode__(self):
		return u"%s, %s %s" % (self.apellido, self.nombre1, self.nombre2)
		

class Profesor(Persona):	
	titulo_hab    =  models.CharField('Titulo_habilitante',max_length=30,blank=True)
	num_mat       =  models.IntegerField('Numero de Matricula', null=True)
	
	
	class Meta:
		db_table = u'Profesor'
		verbose_name_plural = 'Profesor'
	def __unicode__(self):
		return u"%s, %s %s" % (self.apellido, self.nombre1, self.nombre2)
		

class Coordinador(Persona):	
	titulo_hab     =  models.CharField('Titulo_habilitante',max_length=30, blank=True)
	num_mat       =  models.IntegerField('Numero de Matricula', null=True)
	
	
	class Meta:
		db_table = u'Coordinador'
		verbose_name_plural = 'Coordinador'
	def __unicode__(self):
		return u"%s, %s %s" % (self.apellido, self.nombre1, self.nombre2)
		
		
class Telefonos(models.Model):
	persona        = models.ForeignKey(Persona,null=True,blank=True)
	caracteristica = models.IntegerField('Caracteristica', null=True)
	numero         = models.IntegerField('Numero')
	tipo           = models.CharField('Tipo',max_length=60, blank=True)
	
	class Meta:
		db_table = u'Telefono'
		verbose_name_plural = 'Telefono'
	def __unicode__(self):
		 return u"%s, %s  - %s" % (self.persona.Apellido, self.persona.nombre1, self.tipo)

		 
class PlanEstudio(models.Model):
	nombre         =  models.CharField('Nombre',max_length=30)
	carrera        =  models.ForeignKey(Carrera)
	duracion       =  models.CharField('Duracion de la Carrera',max_length=30, blank=True)
	modalidad      =  models.CharField('Modalidad de Dictado',max_length=30, blank=True)
	carga_horaria  =  models.CharField('Carga Horaria Total',max_length=30, blank=True)
	regimen        =  models.CharField('Regimen de Cursado',max_length=30, blank=True)
	observaciones  =  models.CharField(max_length=765,  blank=True)
	   
	class Meta:
		db_table = u'Plan de Estudio'
		verbose_name_plural = 'Plan de Estudio'	
	def __unicode__(self):
		return self.nombre		 

		
class Condicion(models.Model):
	nombre = models.CharField('Nombre', max_length=30)
	descripcion = models.CharField('Descripcion',blank=True, max_length=30, null=True)
	
	class Meta:
		db_table = u'Condicion'
		verbose_name_plural = 'Condicion'	
	def __unicode__(self):
		return self.nombre

	
		
class Materia(models.Model):
	nombre         =  models.CharField('Nombre',max_length=60)
	curso          =  models.IntegerField('Curso',null=True)
	plan_de_estudio=  models.ForeignKey(PlanEstudio) 
	carrera        =  models.ForeignKey(Carrera)
	observaciones  =  models.CharField(max_length=765,  blank=True)
	correlativas   =  models.ManyToManyField('Materia', related_name="bloquea",  null=True, blank=True)
	condicion      =  models.ForeignKey(Condicion)
   
	class Meta:
		db_table = u'Materia'
		verbose_name_plural = 'Materia'	
	def __unicode__(self):
		return self.nombre
	
	
class Programa(models.Model):
	objetivos  =  models.CharField('Objetivos',max_length=150)
	eje_conceptual = models.TextField('Ejes Conceptuales',blank=True)
	met_trabajo    = models.CharField('Metodologia de trabajo',max_length=150, blank=True)
   
	class Meta:
		db_table = u'Programa'
		verbose_name_plural = 'Programa'

		
class Contenidos(models.Model):
	programa     =  models.ForeignKey(Programa)
	unidad       =  models.IntegerField('Unidad')
	item         =  models.CharField('Item',blank=True, max_length=150)
	   
	class Meta:
		db_table = u'Contenidos'
		verbose_name_plural = 'Contenidos'	
	
		
		
class LibroAula(models.Model):
	materia          =  models.ForeignKey(Materia)
	profesor         =  models.ForeignKey(Profesor)
	programa         =  models.ForeignKey(Programa, null=True, blank=True)
	anio             =  models.IntegerField('Anio')
	horas            =  models.IntegerField('Horas Catedra',null=True)
	plan_estudios    =  models.ForeignKey(PlanEstudio)
	cantidad_clases  =  models.IntegerField('Cantidad_clases',null=True)
	observaciones    =  models.CharField('Observaciones',max_length=765, blank=True) 
   
	class Meta:
		db_table = u'LibroAula'
		verbose_name_plural = 'Libro de Aula'
	def __unicode__(self):
		 return u"%s %s" %(self.materia, self.anio)

	
	
class Asistencia(models.Model):
	alumno        =  models.ForeignKey(Alumno)
	libro_aula    =  models.ForeignKey(LibroAula)
	presentes     =  models.IntegerField('Cantidad de Presentes',null=True)
	ausentes      =  models.IntegerField('Cantidad de Ausentes',null=True)
	porcentaje    =  models.FloatField('Porcentaje de Asistencia',null=True)
  
	class Meta:
		db_table = u'Asistencia'
		verbose_name_plural = 'Asistencia'
	def __unicode__(self):
		return u"%s - %s"  % (self.alumno, self.libro_aula)

			
class InscripcionMateria(models.Model):
	materia              =  models.ForeignKey(Materia)
	alumno               =  models.ForeignKey(Alumno)
	fecha_inscripcion    =  models.DateField('Fecha Inscripcion')
	fecha_regularizacion =  models.DateField('Fecha Regularizacion',null=True, blank=True)
	condicion            =  models.ForeignKey(Condicion)
	fecha_aprobacion     =  models.DateField('Fecha Aprobacion',null=True, blank=True)
	aprobado             =  models.BooleanField('Aprobado')
	nota                 =  models.IntegerField('Nota',null=True, blank=True)
	nota_letra           =  models.CharField('Nota(Letras)',max_length=30,null=True,blank=True)
	
	class Meta:
		db_table = u'InscripcionMateria'
		verbose_name_plural = 'Inscripcion Materia'
	def __unicode__(self):
		return u"%s,  %s - %s"  % (self.materia, self.alumno, self.fecha_inscripcion)
		

	
class TipoExamenParcial(models.Model):
	nombre         =  models.CharField(max_length=30) 
	observaciones  =  models.CharField(max_length=765,  blank=True)
    
	class Meta:
		db_table = u'TipoExamen'
		verbose_name_plural = 'Tipo de Examen'
	def __unicode__(self):
		return self.nombre

		
class TurnoExamen(models.Model):
	numero       =  models.IntegerField('Numero') 
	fecha_inicio =  models.DateField('Fecha de Inicio')
	fecha_fin    =  models.DateField('Fecha de Cierre')
	carrera      =  models.ForeignKey(Carrera)
	descripcion  =  models.CharField('Descripcion',max_length=30,null=True,blank=True)
	
	class Meta:
		db_table = u'TurnoExamen'
		verbose_name_plural = 'Turno de Examen'
	def __unicode__(self):
		return u"%s"  % (self.numero)
	
	
class ItemTurnoExamen(models.Model):
	turno        =  models.ForeignKey(TurnoExamen)
	fecha        =  models.DateField('Fecha')
	hora         =  models.CharField('Hora', max_length=30,null=True,blank=True)
	materia      =  models.ForeignKey(Materia)
	tribunal     =  models.ManyToManyField('Profesor', related_name="pertenece") 
	
	class Meta:
		db_table = u'ItemTurnoExamen'
		verbose_name_plural = 'Item Turno de Examen'
	def __unicode__(self):
		return u"%s,  %s "  % (self.fecha, self.materia)
		

		
class Examen(models.Model):
	materia        =  models.ForeignKey(Materia) 
	alumno         =  models.ForeignKey(Alumno)
	fecha          =  models.DateField('Fecha',null=True) 
	nota           =  models.IntegerField('Nota',null=True, blank=True)
	nota_letra     =  models.CharField('Nota(Letras)',max_length=30,null=True,blank=True)
	observaciones  =  models.TextField('Observaciones', blank=True) 

    
	class Meta:
		db_table = u'Examen'
		verbose_name_plural = 'Examen'	
	def __unicode__(self):
		return u"%s,  %s - %s"  % (self.materia, self.alumno, self.fecha)
	
class Parcial(Examen):
	tipo_examen_parcial   =  models.ForeignKey(TipoExamenParcial)
	
    
	class Meta:
		db_table = u'Parcial'
		verbose_name_plural = 'Parcial'	
	def __unicode__(self):
		return u"%s,  %s - %s"  % (self.materia, self.alumno, self.tipo_examen_parcial)
	
	
class Final(Examen): 
	fecha_inscripcion =  models.DateField('Fecha de Inscripcion')
	turno             =  models.ForeignKey(TurnoExamen,null=True)
	condicion         =  models.ForeignKey(Condicion)
	ausente           =  models.BooleanField('Ausente') 
    
	class Meta:
		db_table = u'Final'
		verbose_name_plural = 'Final'	
	def __unicode__(self):
		return u"%s,  %s - %s"  % (self.materia, self.alumno, self.fecha)

		
class Coloquio(Examen):
	ausente        =  models.BooleanField('Ausente') 
    
	class Meta:
		db_table = u'Coloquio'
		verbose_name_plural = 'Coloquio'	
	def __unicode__(self):
		return u"%s,  %s - %s"  % (self.materia, self.alumno, self.fecha)
		

		
class Cuotas(models.Model):
	alumno       =  models.ForeignKey(Alumno)
	monto        =  models.FloatField('Monto',null=True,blank=True) 
	pagado       =  models.BooleanField('Pagado') 
	anio         =  models.IntegerField('Anio') 
	numero_recibo = models.IntegerField('Numero de recibo', null=True,blank=True) 
    
	class Meta:
		db_table = u'Cuotas'
		verbose_name_plural = 'Cuotas'
	def __unicode__(self):
		return u"%s,  %s"  % (self.alumno, self.anio)
	