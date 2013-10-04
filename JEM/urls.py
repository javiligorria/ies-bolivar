from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from django.conf import settings
from principal.views import *
admin.autodiscover()

urlpatterns = patterns('principal.views',
	     url(r'^$', 'vista_index'),
		 url(r'^contacto/', 'contacto'),
		 url(r'^ingresar/', 'ingresar'),
		 url(r'^privado/', 'privado'),
		 url(r'^cerrar/$', 'cerrar'),
		 url(r'^institucional/', 'institucional'),
		 url(r'^carreras/', 'carreras'),
		 url(r'^carrera/(?P<carrera>.*)/', 'carrera'),
		 #COORDINADOR:
			#ALUMNOS
		 url(r'^registrarusuarioAlumno/', 'registrarusuarioAlumno'),
		 url(r'^registrarAlumno/(?P<usuario>.*)/', 'registrarAlumno'),
		 url(r'^editarAlumno/(?P<legajo>.*)/', 'editarAlumno', name='editarAlumno'),
		 url(r'^consultarLegajoAlumno/', 'consultarLegajoAlumno'),
		 url(r'^consultarAlumno/', 'consultarAlumno'),
		 url(r'^datosAlumno/(?P<nom>.*)/(?P<ape>.*)/', 'datosAlumno', name='datosAlumno'),
		 
		 
		 url(r'^registrarCuota/', 'registrarCuota'),
		 url(r'^pagocuota/(?P<nom>.*)/(?P<ape>.*)/(?P<anio>.*)/', 'pagocuota'),
		 
			#PROFESOR
		 url(r'^registrarusuarioProfesor/', 'registrarusuarioProfesor'),
		 url(r'^registrarProfesor/(?P<usuario>.*)/', 'registrarProfesor'),
		 url(r'^editarProfesor/(?P<carrera>\d+)/(?P<legajo>\d+)/', 'editarProfesor', name='editarProfesor'),
		 url(r'^consultarLegajoProfesor/', 'consultarLegajoProfesor'),
		 url(r'^consultarProfesor/', 'consultarProfesor'),
		 url(r'^datosProfesor/(?P<nom>.*)/(?P<ape>.*)/', 'datosProfesor', name='datosProfesor'),
		 
			#CREAR
		 url(r'^registrarusuarioCoordinador/', 'registrarusuarioCoordinador'),
		 url(r'^crearCoordinador/', 'crearCoordinador'),
		 url(r'^crearLibroAula/', 'crearLibroAula'),
		 url(r'^crearCarrera/', 'crearCarrera'),
		 url(r'^agregarmateria/', 'agregarmateria'),
		 url(r'^crearPlanEstudio/', 'crearPlanEstudio'),
		 url(r'^crearTurnoExamen/', 'crearTurnoExamen'),
		 url(r'^crearItemTurnoExamen/(?P<turno>.*)/', 'crearItemTurnoExamen'),
		
		 url(r'^datoscargados/', 'datoscargados'),
		 url(r'^datoscargados2/', 'datoscargados2'),
		 
			#CONSULTAR	
		url(r'^consultaListadoFinales/', 'consultaListadoFinales'),
		url(r'^consultaTurnoExamen/', 'consultaTurnoExamen'),
		url(r'^consultaMatricula/', 'consultaMatricula'),
		url(r'^consultarAlumnoAnalitico/', 'consultarAlumnoAnalitico'),
		url(r'^consultaColoquio/', 'consultaColoquio', name='consultaColoquio'),
		url(r'^consultaLibroAula/', 'consultaLibroAula', name='consultaLibroAula'),
		url(r'^consultaAlumnos/', 'consultaAlumnos', name='consultaAlumnos'),	
		url(r'^consultaInscripcion/', 'consultaInscripcion', name='consultaInscripcion'),	
		url(r'^listadoAlumnos/(?P<carrera>.*)/(?P<curso>.*)/(?P<anio>.*)/', 'listadoAlumnos', name='listadoAlumnos'),
		url(r'^alumnosInscriptos/(?P<materia>.*)/(?P<anio>.*)/', 'alumnosInscriptos', name='alumnosInscriptos'),
		url(r'^libroAula/(?P<materia>.*)/(?P<anio>.*)/', 'libroAula', name='libroAula'),
		url(r'^actaColoquio/(?P<materia>.*)/(?P<anio>.*)/', 'actaColoquio', name='actaColoquio'),
		url(r'^analiticoAlumno/(?P<carrera>.*)/(?P<legajo>.*)/', 'analiticoAlumno', name='analiticoAlumno'),
		url(r'^actaMatricula/(?P<materia>.*)/(?P<anio>.*)/', 'actaMatricula', name='actaMatricula'),
		url(r'^turnoExamen/(?P<carrera>.*)/(?P<anio>.*)/(?P<numero>.*)/', 'turnoExamen', name='turnoExamen'),
		url(r'^listadoFinales/(?P<anio>.*)/(?P<turno>.*)/(?P<materia>.*)/', 'listadoFinales', name='listadoFinales'),
			
			#SITIO WEB
		url(r'^editarNoticia/', 'editarNoticia'),
		url(r'^noticias/', 'noticias'),
		

		#27 / 05 / 2013 
		#Monzon Edaurdo URL
		#SUBMENU Examen 
		url(r'^Registrar_parcial/', 'Registrar_parcial'),
		url(r'^Consultar_parcial/', 'Consultar_parcial', name='Consultar_parcial'),
		url(r'^Editar_parcial/(?P<materia>.*)/(?P<legajo>.*)/(?P<tipo_examen>.*)/', 'Editar_parcial', name='Editar_parcial'),
		url(r'^Registrar_coloquio/', 'Registrar_coloquio'),
		url(r'^Consultar_coloquio/', 'Consultar_coloquio', name='Consultar_coloquio'),
		url(r'^Editar_coloquio/(?P<materia>.*)/(?P<legajo>.*)/', 'Editar_coloquio', name='Editar_coloquio'),

		# SUBMENU Informes
		url(r'^consultar_notas/', 'consultar_notas'),
		url(r'^consultar_finales/', 'consultar_finales'),
		url(r'^informenotas/(?P<materia>.*)/(?P<anio>.*)/(?P<curso>.*)/', 'informenotas'), 	 
		url(r'^informefinales/(?P<materia>.*)/(?P<anio>.*)/(?P<curso>.*)/', 'informefinales'), 	 
 	    url(r'^consultarAlumno2/', 'consultarAlumno2'),
		url(r'^datosAlumno2/(?P<nom>.*)/(?P<ape>.*)/', 'datosAlumno2', name='datosAlumno'),
		url(r'^actaColoquio2/(?P<materia>.*)/(?P<anio>.*)/', 'actaColoquio2', name='actaColoquio2'),
		url(r'^consultaColoquio2/', 'consultaColoquio2', name='consultaColoquio2'),
		url(r'^consultaMatricula2/', 'consultaMatricula2'),
		url(r'^actaMatricula2/(?P<materia>.*)/(?P<anio>.*)/', 'actaMatricula2', name='actaMatricula2'), 
		url(r'^Consultar_final/', 'Consultar_final'),
		url(r'^Editar_final/(?P<materia>.*)/(?P<anio>.*)/(?P<turno>.*)/(?P<legajo>.*)/', 'Editar_final', name='Editar_final'),

		
		url(r'^cambiarPassword2/', 'cambiarPassword2'), 
 	 

		 
		# SUBMENU AULA
		 
	    url(r'^registrar_asistencia/', 'registrar_asistencia'), 
		url(r'^crearPrograma/', 'crearPrograma'),
		url(r'^crearContenido/(?P<programa>.*)/', 'crearContenido'),
		url(r'^consultar_asistencia/', 'consultar_asistencia'),
		url(r'^Editar_asistencia/(?P<legajo>.*)/(?P<materia>.*)/(?P<anio>.*)/', 'Editar_asistencia'),
				 
		# FIN DE MODIFICACION   #
		 
		 
		 
		######### MENU ALUMNO#######
		
		url(r'^consultaTurnoExamenAlumno/', 'consultaTurnoExamenAlumno'),
		url(r'^turnoExamenAlumno/(?P<carrera>.*)/(?P<anio>.*)/(?P<numero>.*)/', 'turnoExamenAlumno'), 
		url(r'^consultarPlanEstudio/', 'consultarPlanEstudio'), 
		url(r'^planEstudio/(?P<nom>.*)/', 'planEstudio'),
		url(r'^consultarPrograma/', 'consultarPrograma'), 
		url(r'^programa/(?P<materia>.*)/(?P<anio>.*)/', 'programa'),
		url(r'^consultarExamenParcial/', 'consultarExamenParcial'), 
		url(r'^notasParciales/(?P<materia>.*)/(?P<anio>.*)/', 'notasParciales'),
		url(r'^consultarExamenFinal/', 'consultarExamenFinal'), 
		url(r'^notasFinales/(?P<materia>.*)/(?P<anio>.*)/', 'notasFinales'),
		url(r'^consultarColoquios/', 'consultarColoquios'), 
		url(r'^notasColoquios/(?P<materia>.*)/(?P<anio>.*)/', 'notasColoquios'),
		url(r'^consultarCorrelativas/', 'consultarCorrelativas'), 
		url(r'^correlativas/(?P<carrera>.*)/', 'correlativas'),
		url(r'^cambiarPassword/', 'cambiarPassword'), 
		url(r'^inscribirMateria/', 'inscribirMateria'), 
		url(r'^inscripcionMaterias/(?P<carrera>.*)/(?P<curso>.*)/', 'inscripcionMaterias'),
		url(r'^inscripcionMat/(?P<mat>.*)/', 'inscripcionMat'),
		url(r'^inscribirFinal/', 'inscribirFinal'), 
		url(r'^inscripcionFinales/(?P<carrera>.*)/(?P<curso>.*)/(?P<turno>.*)/', 'inscripcionFinales'),
		url(r'^inscripcionExamenFinal/(?P<mat>.*)/(?P<turnoexamen_id>.*)/', 'inscripcionExamenFinal'),
		
		
		url(r'^admin/', include(admin.site.urls)),
		url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
		#url(r'^media/(?P<path>.*)', 'django.views.statics.serve', {'document_root':settings.MEDIA_ROOT,}),
		# url(r'^JEM/', include('JEM.foo.urls')),
		
		# url(r'^datosasistencia/', 'datosasistencia'),
		# url(r'^datosasistencia2/', 'datosasistencia2'),
)
