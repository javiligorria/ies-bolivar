from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext, loader
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import *
from principal.forms import *
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from principal.models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
import datetime

#PDF

#import reportlab
#from reportlab.pdfgen import canvas
#import ho.pisa as pisa
#import cStringIO as StringIO
#from cgi import escape
#from django.template.loader import render_to_string

inscripcionMateria =True

def vista_index(request):
    return HttpResponseRedirect('/noticias/')

def institucional(request):
    return render_to_response('institucional.html', context_instance=RequestContext(request))	

def carreras(request):
	carrera = Carrera.objects.all()
	return render_to_response('carreras.html', {'carrera': carrera}, context_instance=RequestContext(request))


def carrera(request, carrera):
	lista1 = []
	lista2 = []
	lista3 = []
	todas1 = Materia.objects.filter(carrera__nombre=carrera, curso=1)
	todas2 = Materia.objects.filter(carrera__nombre=carrera, curso=2)
	todas3 = Materia.objects.filter(carrera__nombre=carrera, curso=3)
	
	for elem in todas1:
		lista1.append(Materia.objects.get(nombre=elem.nombre))
	for elem in todas2:
		lista2.append(Materia.objects.get(nombre=elem.nombre))
	for elem in todas3:
		lista3.append(Materia.objects.get(nombre=elem.nombre))
	return render_to_response('carrera.html', {'carrera': carrera, 'lista1': lista1, 'lista2': lista2, 'lista3': lista3 }, context_instance=RequestContext(request))		
	
	
def ingresar(request):
	if not request.user.is_anonymous():
		return HttpResponseRedirect('/privado') 
	if request.method == 'POST':
		formulario = AuthenticationForm(request.POST)
		if formulario.is_valid:
			usuario = request.POST['username']
			clave = request.POST['password']
			acceso = authenticate(username=usuario, password=clave)
			if acceso is not None:
				if acceso.is_active:
					login(request, acceso)
					return HttpResponseRedirect('/privado')
				else:
					return render_to_response('noactivo.html', context_instance=RequestContext(request))
			else:
				return render_to_response('nousuario.html', context_instance=RequestContext(request))
	else:
		formulario = AuthenticationForm()
	return render_to_response('ingresar.html', {'formulario':formulario}, context_instance=RequestContext(request))
	
	

def contacto(request):
	if request.method=='POST':
		formulario = ContactoForm(request.POST)
		if formulario.is_valid():
			titulo = 'Mensaje desde la web de Simon Bolivar'
			contenido = formulario.cleaned_data['mensaje'] + "\n"
			contenido+= 'Comunicarse a: ' + formulario.cleaned_data['correo']
			correo = EmailMessage(titulo, contenido, to=['javiligorria@gmail.com'])
			correo.send()
			return HttpResponseRedirect('/')
	else:
		formulario = ContactoForm()
	return render_to_response('contacto.html',{'formulario':formulario}, context_instance=RequestContext(request))


def __castPersona(persona):
	out = persona
	try:
		out = persona.alumno
	except Alumno.DoesNotExist:
		pass
	try:
		out = persona.coordinador
	except Coordinador.DoesNotExist:
		pass
	try:
		out = persona.profesor
	except Profesor.DoesNotExist:
		pass
	
	return out
	
@login_required(login_url='/ingresar')
def privado(request):
	usuario = request.user
	persona = __castPersona(usuario.persona)
	if isinstance(persona, Alumno):
		html = 'privadoAlumno.html'
	elif isinstance(persona, Coordinador):
		html = 'privadoCoordinador.html'
	elif isinstance(persona, Profesor):
		html = 'privadoProfesor.html'
	return render_to_response(html, {'usuario':usuario}, context_instance=RequestContext(request))
	
		
	
@login_required(login_url='/ingresar')
def cerrar(request):
		logout(request)
		return HttpResponseRedirect('/')


################# MENU COORDINADOR!!!!######################		

@login_required
def registrarusuarioAlumno(request):
	titulo = 'Registrar Alumno'
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid():
			usuario = formulario.save()
			return HttpResponseRedirect('/registrarAlumno/%s/'%(usuario.id))
	else:
		formulario = UserCreationForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 
	
	
@login_required
def registrarusuarioProfesor(request):
	titulo = 'Registrar Profesor'
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid():
			usuario = formulario.save()
			return HttpResponseRedirect('/registrarProfesor/%s/'%(usuario.id))
	else:
		formulario = UserCreationForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	

		
@login_required
def registrarAlumno(request, usuario):
	lista=[]
	titulo = 'Registrar Alumno'
	if request.method == 'POST':
		formulario = AlumnoForm(request.POST)
		if formulario.is_valid():
			u = User.objects.get(id=usuario)
			add = formulario.save(commit=False)
			add.usuario = u
			add.save()
			formulario.save()
			legajo = formulario.cleaned_data['legajo']
			carrera = formulario.cleaned_data['carrera']
			formulario.save()
			usuarionuevo = Alumno.objects.get(legajo=legajo)
			fecha_actual = datetime.date.today()
			cuota = Cuotas(alumno=usuarionuevo, anio=fecha_actual.year)
			cuota.save()
			materias = Materia.objects.filter(carrera__nombre=carrera, curso=1)
			for elem in materias:
				lista.append(Materia.objects.get(nombre=elem.nombre))
			for mat in lista:
				insc = InscripcionMateria(materia=mat, alumno=usuarionuevo, condicion=mat.condicion, fecha_inscripcion=fecha_actual)
				insc.save()
			return render_to_response('datoscargadosregistro.html', context_instance=RequestContext(request))
	else:
		formulario = AlumnoForm()
	return render_to_response('formularios.html', {'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 


@login_required
def registrarProfesor(request, usuario):
	titulo = 'Registrar Profesor'
	if request.method == 'POST':
		formulario = ProfesorForm(request.POST)
		if formulario.is_valid():
			u = User.objects.get(id=usuario)
			add = formulario.save(commit=False)
			add.usuario = u
			add.save()
			formulario.save()
			return render_to_response('datoscargadosregistro.html', context_instance=RequestContext(request))
	else:
		formulario = ProfesorForm()
	return render_to_response('formularios.html', {'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))
	
@login_required	
def datoscargados2(request):
    return render_to_response('datoscargados.html', context_instance=RequestContext(request))	


@login_required	
def datoscargados(request):
    return render_to_response('datoscargados.html', context_instance=RequestContext(request))	

	

@login_required
def registrarCuota(request):
	titulo = 'Registrar Pago de Cuota'
	if request.method == 'POST':
		formulario = CuotaAlumnoForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			ape = formulario.cleaned_data['apellido']
			anio= formulario.cleaned_data['anio']
			return HttpResponseRedirect('/pagocuota/%s/%s/%s/'%(nom,ape,anio))
			
	else:
		formulario = CuotaAlumnoForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


	
@login_required
def pagocuota(request, nom, ape, anio):
	titulo = 'Registrar Pago de Cuota'
	alumno = Alumno.objects.get(nombre1=nom, apellido=ape)
	cuota = Cuotas.objects.get(alumno=alumno, anio=anio)
	if request.method == 'POST':
		formulario = CuotasForm(request.POST, instance=cuota)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = CuotasForm(instance=cuota)
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 


@login_required
def agregarmateria(request):
	titulo = 'Crear Materia'
	if request.method == 'POST':
		formulario = MateriaForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			nombre = formulario.cleaned_data['nombre']
			plan_de_estudio = formulario.cleaned_data['plan_de_estudio']
			mat = Materia.objects.filter(carrera=carrera, nombre=nombre, plan_de_estudio=plan_de_estudio)
			if len(mat)>0:
				return render_to_response('yaExiste.html', {'nombre':nombre}, context_instance=RequestContext(request))
			else:	
				formulario.save()
				return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = MateriaForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))


@login_required
def crearPlanEstudio(request):
	titulo = 'Crear Plan de Estudio'
	if request.method == 'POST':
		formulario = PlanEstudioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = PlanEstudioForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 

@login_required
def crearCarrera(request):
	titulo = 'Crear Carrera'
	if request.method == 'POST':
		formulario = CarreraForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = CarreraForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))


@login_required
def crearTurnoExamen(request):
	titulo = 'Crear Turno de Examen'
	if request.method == 'POST':
		formulario = TurnoExamenForm(request.POST)
		if formulario.is_valid():
			numero = formulario.cleaned_data['numero']
			fecha_inicio = formulario.cleaned_data['fecha_inicio']
			carrera = formulario.cleaned_data['carrera']
			nombre = '%s - %s'%(numero,fecha_inicio.year)
			tur = TurnoExamen.objects.filter(numero=numero, fecha_inicio=fecha_inicio, carrera=carrera)
			if len(tur)>0:
				return render_to_response('yaExiste.html', {'nombre':nombre}, context_instance=RequestContext(request))
			else:	
				add = formulario.save()
				turno = add.id
				return HttpResponseRedirect('/crearItemTurnoExamen/%s/'%(turno))
	else:
		formulario = TurnoExamenForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

@login_required
def crearItemTurnoExamen(request, turno):
	titulo = 'Crear Items Turno de Examen'
	if request.method == 'POST':
		formulario = ItemTurnoExamenForm(request.POST)
		if formulario.is_valid():
			item = formulario.save(commit=False)
			turnoExamen = TurnoExamen.objects.get(id=turno)
			item.turno = turnoExamen
			item.save()
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = ItemTurnoExamenForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))


	
	

@login_required
def crearLibroAula(request):
	titulo = 'Crear Libro de Aula'
	if request.method == 'POST':
		formulario = LibroAulaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			nombre=materia.nombre
			mat = LibroAula.objects.filter(materia=materia, anio=anio)
			if len(mat)>0:
				return render_to_response('yaExiste.html', {'nombre':nombre}, context_instance=RequestContext(request))
			else:
				formulario.save()
				return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = LibroAulaForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))


@login_required
def registrarusuarioCoordinador(request):
	titulo = 'Registrar Coordinador'
	if request.method == 'POST':
		formulario = UserCreationForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/crearCoordinador/')
	else:
		formulario = UserCreationForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 
	
	
	
@login_required
def crearCoordinador(request):
	titulo = 'Registrar Coordinador'
	if request.method == 'POST':
		formulario = CoordinadorForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario = CoordinadorForm()
	return render_to_response('formularios.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))



@login_required
def consultarLegajoAlumno(request):
	titulo = 'Buscar Alumno'
	if request.method == 'POST':
		formulario = ConsultaForm(request.POST)
		if formulario.is_valid():
			legajo = formulario.cleaned_data['legajo']
			return HttpResponseRedirect('/editarAlumno/%s/'%(legajo))
			
	else:
		formulario = ConsultaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	

	
	
@login_required
def editarAlumno(request, legajo):
	titulo = 'Modificar Alumno'
	alumno = get_object_or_404(Alumno, legajo=legajo)
	user = User.objects.get(username=alumno.usuario.username)
	if request.method == 'POST':
		formulario1 = UserForm(request.POST, instance=user)
		formulario2 = AlumnoForm(request.POST, instance=alumno)
		if formulario1.is_valid() and formulario2.is_valid():
			formulario1.save()
			formulario2.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario1 = UserForm(instance=user)
		formulario2 = AlumnoForm(instance=alumno)
	return render_to_response('formularios_edicion.html', { 'formulario1': formulario1, 'formulario2': formulario2, 'titulo': titulo }, context_instance=RequestContext(request)) 


@login_required
def consultarLegajoProfesor(request):
	titulo = 'Buscar Profesor'
	if request.method == 'POST':
		formulario = ConsultaForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			legajo = formulario.cleaned_data['legajo']
			return HttpResponseRedirect('/editarAlumno/%s/%s/'%(carrera,legajo))
			
	else:
		formulario = ConsultaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	

	
	
@login_required
def editarProfesor(request, carrera, legajo):
	titulo = 'Modificar Profesor'
	profesor = get_object_or_404(Profesor, legajo=legajo)
	username = User.objects.get(username=profesor.usuario.username)
	if request.method == 'POST':
		formulario1 = UserCreationForm(request.POST, instance=username)
		formulario2 = ProfesorForm(request.POST, instance=profesor)
		if formulario1.is_valid() and formulario2.is_valid():
			formulario1.save()
			formulario2.save()
			return HttpResponseRedirect('/datoscargados/')
	else:
		formulario1 = UserCreationForm(instance=username)
		formulario2 = ProfesorForm(instance=profesor)
	return render_to_response('formularios_edicion.html', { 'formulario1': formulario1, 'formulario2': formulario2, 'titulo': titulo}, context_instance=RequestContext(request)) 



@login_required
def consultaAlumnos(request):
	titulo = 'Listado de Alumnos'
	if request.method == 'POST':
		formulario = CursoForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			curso = formulario.cleaned_data['curso']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/listadoAlumnos/%s/%s/%s/'%(carrera,curso,anio))
			
	else:
		formulario = CursoForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))


@login_required			
def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))
	
@login_required
def listadoAlumnos(request, carrera, curso, anio):

	titulo1 = carrera
	if curso == '1':
		titulo2 = 'Listado de Alumnos de Primer Año'
	if curso == '2':
		titulo2 = 'Listado de Alumnos de Segundo Año'
	if curso == '3':
		titulo2 = 'Listado de Alumnos de Tercer Año'
	list=[]
	listaalumnos=[]
	lista = InscripcionMateria.objects.filter(materia__carrera__nombre=carrera, materia__curso=curso, fecha_inscripcion__year=anio).order_by('alumno')
	for elem in lista:
		listaalumnos.append(elem.alumno)
	for i in listaalumnos:
		if i not in list:
			list.append(i)

	return render_to_response('form-opcion.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 
	#return render_to_pdf('form-opcion.html', { 'pagesize':'A4', 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 })



	
	
	
@login_required
def consultarAlumno(request):
	titulo = 'Consultar Alumno'
	if request.method == 'POST':
		formulario = ConsultarAlumnoForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			ape = formulario.cleaned_data['apellido']
			return HttpResponseRedirect('/datosAlumno/%s/%s/'%(nom,ape))
			
	else:
		formulario = ConsultarAlumnoForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def datosAlumno(request,nom,ape):
	titulo = 'Consultar Alumno'
	alumno = Alumno.objects.get(nombre1=nom, apellido=ape)
	formulario = AlumnoForm(instance=alumno)
	return render_to_response('consultas.html',{ 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	
	
	
@login_required
def consultarProfesor(request):
	titulo = 'Consultar Profesor'
	if request.method == 'POST':
		formulario = ConsultarAlumnoForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			ape = formulario.cleaned_data['apellido']
			return HttpResponseRedirect('/datosProfesor/%s/%s/'%(nom,ape))
			
	else:
		formulario = ConsultarAlumnoForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def datosProfesor(request,nom,ape):
	titulo = 'Consultar Profesor'
	profesor = Profesor.objects.get(nombre1=nom, apellido=ape)
	formulario = ProfesorForm(instance=profesor)
	return render_to_response('consultas.html',{ 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	
	
	
@login_required
def consultaInscripcion(request):
	titulo = 'Consulta de Alumnos Inscriptos'
	if request.method == 'POST':
		formulario = InscripcionMateriaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/alumnosInscriptos/%s/%s/'%(materia,anio))
	else:
		formulario = InscripcionMateriaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def alumnosInscriptos(request, materia, anio):
	titulo2 = materia
	titulo1 = 'Listado de Alumnos Inscriptos'
	list=[]
	lista = InscripcionMateria.objects.filter(materia__nombre=materia, fecha_inscripcion__year=anio).order_by('alumno')
	for elem in lista:
		list.append(elem.alumno)

	return render_to_response('form-opcion.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 
	
	
@login_required
def consultaLibroAula(request):
	titulo = 'Consulta de Libro de Aula'
	if request.method == 'POST':
		formulario = ConsultaLibroAulaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/libroAula/%s/%s/'%(materia,anio))
	else:
		formulario = ConsultaLibroAulaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))		
	

@login_required
def libroAula(request, materia, anio):
	titulo = 'Libro de Aula'
	libro = get_object_or_404(LibroAula, materia__nombre=materia, anio=anio)
	formulario = LibroAulaForm(instance=libro)
	return render_to_response('consultas.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 


@login_required
def consultaColoquio(request):
	titulo = 'Acta de Alumnos a Coloquio'
	if request.method == 'POST':
		formulario = InscripcionMateriaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/actaColoquio/%s/%s/'%(materia,anio))
	else:
		formulario = InscripcionMateriaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def actaColoquio(request, materia, anio):
	titulo2 = materia
	titulo1 = 'Acta de Alumnos a Coloquio'
	list=[]
	lista = Coloquio.objects.filter(materia__nombre=materia, fecha__year=anio).order_by('alumno')
	for elem in lista:
		list.append(Coloquio.objects.get(alumno=elem.alumno))

	return render_to_response('tablaColoquio.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 


	
@login_required
def consultarAlumnoAnalitico(request):
	titulo = 'Analitico de  Alumno:'
	if request.method == 'POST':
		formulario = ConsultaForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			legajo = formulario.cleaned_data['legajo']
			return HttpResponseRedirect('/analiticoAlumno/%s/%s/'%(carrera,legajo))
			
	else:
		formulario = ConsultaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def analiticoAlumno(request, carrera, legajo):
	establecimiento = 'I.E.S. Simón Bolivar'
	lista1=[]
	lista2=[]
	lista3=[]
	lista11=[]
	lista22=[]
	lista33=[]
	alumno = get_object_or_404(Alumno, legajo=legajo)
	materias1 = InscripcionMateria.objects.filter(alumno=alumno, materia__curso=1)
	materias2 = InscripcionMateria.objects.filter(alumno=alumno, materia__curso=2)
	materias3 = InscripcionMateria.objects.filter(alumno=alumno, materia__curso=3)
	
	todas1 = Materia.objects.filter(carrera__nombre=carrera, curso=1)
	todas2 = Materia.objects.filter(carrera__nombre=carrera, curso=2)
	todas3 = Materia.objects.filter(carrera__nombre=carrera, curso=3)
	
	for elem in materias1:
		lista1.append(InscripcionMateria.objects.get(materia=elem.materia))
	for elem in materias2:
		lista2.append(InscripcionMateria.objects.get(materia=elem.materia))
	for elem in materias3:
		lista3.append(InscripcionMateria.objects.get(materia=elem.materia))
	
	for elem in todas1:
		lista11.append(Materia.objects.get(nombre=elem.nombre))
	for elem in todas2:
		lista22.append(Materia.objects.get(nombre=elem.nombre))
	for elem in todas3:
		lista33.append(Materia.objects.get(nombre=elem.nombre))
	
	for insc in lista1:
		for mat in lista11:
			if insc.materia == mat:
				lista11.remove(mat)
	for insc in lista2:
		for mat in lista22:
			if insc.materia == mat:
				lista22.remove(mat)
	for insc in lista3:
		for mat in lista33:
			if insc.materia == mat:
				lista33.remove(mat)
	
	return render_to_response('tablaAnalitico.html', { 'lista1': lista1, 'lista2': lista2, 'lista3': lista3, 'establecimiento': establecimiento, 'lista11': lista11, 'lista22': lista22, 'lista33': lista33 }, context_instance=RequestContext(request)) 


def editarNoticia(request):
	titulo = 'Editar una Noticia'
	if request.method == 'POST':
		formulario = NoticiaForm(request.POST, request.FILES)
		if formulario.is_valid():
			formulario.save()
			return HttpResponseRedirect('/datoscargados/')
			
	else:
		formulario = NoticiaForm()
	return render_to_response('formularioNoticias.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


def noticias(request):
	
	list=[]
	lista = Noticia.objects.all()
	for elem in lista:
		list.append(Noticia.objects.get(id=elem.id))
	list.reverse()
	return render_to_response('noticias.html', { 'list': list }, context_instance=RequestContext(request)) 



@login_required
def consultaMatricula(request):
	titulo = 'Acta de Matricula'
	if request.method == 'POST':
		formulario = InscripcionMateriaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/actaMatricula/%s/%s/'%(materia,anio))
	else:
		formulario = InscripcionMateriaForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def actaMatricula(request, materia, anio):
	mat = Materia.objects.get(nombre=materia)
	titulo1 = 'Acta de Matricula'
	titulo2 = '%s' %(mat.carrera)
	titulo3 = '%s' %(materia)
	lista = []
	list=[]
	list1 = InscripcionMateria.objects.filter(materia__nombre=materia, fecha_inscripcion__year=anio).order_by('alumno')
	for elem in list1:
		list.append(InscripcionMateria.objects.get(id=elem.id))
	list2 = Asistencia.objects.filter(libro_aula__materia__nombre=materia, libro_aula__anio=anio)
	for elem in list2:
		lista.append(Asistencia.objects.get(id=elem.id))
	return render_to_response('actaMatricula.html', { 'list': list, 'lista': lista, 'titulo1': titulo1, 'titulo2': titulo2, 'titulo3': titulo3 }, context_instance=RequestContext(request)) 
		
		
		
@login_required
def consultaTurnoExamen(request):
	titulo = 'Turno de Exámen'
	if request.method == 'POST':
		formulario = ConsultarTurnoExamenForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			anio = formulario.cleaned_data['anio']
			numero = formulario.cleaned_data['numero']
			return HttpResponseRedirect('/turnoExamen/%s/%s/%s/'%(carrera,anio,numero))
	else:
		formulario = ConsultarTurnoExamenForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
		

@login_required
def turnoExamen(request, carrera, anio, numero):
	titulo2 = 'Turno de Examen Nro: %s'%(numero)
	titulo1 = '%s'%(carrera)
	turnoExamen = TurnoExamen.objects.get(numero=numero, fecha_inicio__year=anio, carrera__nombre=carrera)
	list1=[]
	list2=[]
	list3=[]
	lista1 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=1).order_by('fecha')
	lista2 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=2).order_by('fecha')
	lista3 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=3).order_by('fecha')
	
	for elem in lista1:
		list1.append(ItemTurnoExamen.objects.get(id=elem.id))
	for elem in lista2:
		list2.append(ItemTurnoExamen.objects.get(id=elem.id))
	for elem in lista3:
		list3.append(ItemTurnoExamen.objects.get(id=elem.id))
			
	return render_to_response('turnoExamen.html', { 'list1': list1, 'list2': list2, 'list3': list3, 'turnoExamen': turnoExamen, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 
		
	
@login_required
def consultaListadoFinales(request):
	titulo = 'Listado de Exámen Final'
	if request.method == 'POST':
		formulario = ConsultaFinalesForm(request.POST)
		if formulario.is_valid():
			anio   = formulario.cleaned_data['anio']
			turno   = formulario.cleaned_data['turno']
			materia = formulario.cleaned_data['materia']
			return HttpResponseRedirect('/listadoFinales/%s/%s/%s/'%(anio,turno,materia))
	else:
		formulario = ConsultaFinalesForm()
		return render_to_response('formulario_consulta.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
				
@login_required
def listadoFinales(request, anio, turno, materia):
	titulo2 = 'Turno de Examen Nro: %s'%(turno)
	titulo1 = 'Listado de Alumnos Inscriptos para %s'%(materia)
	list = []
	lista = Final.objects.filter(materia__nombre=materia, turno__numero=turno, fecha_inscripcion__year=anio).order_by('alumno')
	for elem in lista:
		list.append(Final.objects.get(id=elem.id))
	return render_to_response('listadoFinales.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 

	



##############################		
#  27 / 05 /2013
#  MONZON EDUARDO	
##############################

#MENU EXAMEN
 
##REGISTRO CONSULTA Y MODIFICACION DE NOTAS PARCIALES ####

@login_required	
def Registrar_parcial(request):
	titulo = 'Registrar Exámen Parcial o Práctico'
	if request.method == 'POST':
		formulario = RegistrarParcialForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))
	else:
		formulario= RegistrarParcialForm()
		return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

@login_required
def Consultar_parcial(request):
	titulo = 'Consultar Parcial'
	if request.method == 'POST':
		formulario = ConsultaParcialForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			legajo = formulario.cleaned_data['legajo']
			tipo_examen = formulario.cleaned_data['tipo']
			return HttpResponseRedirect('/Editar_parcial/%s/%s/%s/'%(materia,legajo,tipo_examen))

			
	else:
		formulario = ConsultaParcialForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))		
		
@login_required
def Editar_parcial(request,materia,legajo,tipo_examen):
	titulo = 'Editar Parcial'
	Objeto = get_object_or_404(Parcial, materia__nombre=materia, alumno__legajo=legajo, tipo_examen_parcial__nombre=tipo_examen)
	if request.method == 'POST':
		formulario = ParcialForm(request.POST, instance=Objeto)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('datoscargados2.html', context_instance=RequestContext(request))
	else:
		formulario = ParcialForm(instance=Objeto)
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 
		

##REGISTRO CONSULTA Y MODIFICACION DE NOTAS COLOQUIOS ####

@login_required	
def Registrar_coloquio(request):
	titulo = 'Registrar coloquio'
	if request.method == 'POST':
		formulario = RegistrarColoquioForm(request.POST)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('datoscargados2.html', context_instance=RequestContext(request))

	else:
		formulario= RegistrarColoquioForm()
		return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

@login_required
def Consultar_coloquio(request):
	titulo = 'Consultar Coloquio'
	if request.method == 'POST':
		formulario = ConsultaColoquioForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			legajo = formulario.cleaned_data['legajo']
			return HttpResponseRedirect('/Editar_coloquio/%s/%s/'%(materia,legajo))

			
	else:
		formulario = ConsultaColoquioForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))		
		
@login_required
def Editar_coloquio(request,materia,legajo):
	titulo = 'Editar Coloquio'
	Objeto = get_object_or_404(Coloquio, materia__nombre=materia, alumno__legajo=legajo)
	if request.method == 'POST':
		formulario = ColoquioForm(request.POST, instance=Objeto)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('datoscargados2.html', context_instance=RequestContext(request))
	else:
		formulario = ColoquioForm(instance=Objeto)
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 


# ASISTENCIA#

@login_required	
def registrar_asistencia(request):
	titulo = 'Registrar Asistencia'
	if request.method == 'POST':
		formulario = AsistenciaForm(request.POST)
		if formulario.is_valid():
			asis = formulario.save(commit=False)
			presentes = formulario.cleaned_data['presentes']
			ausentes = formulario.cleaned_data['ausentes']
			libro_aula = formulario.cleaned_data['libro_aula']
			total_clases = libro_aula.cantidad_clases
			porcentaje = (presentes+ausentes)/total_clases
			asis.porcentaje = porcentaje
			asis.save()
			formulario.save()
			return render_to_response('datosasistencia.html', context_instance=RequestContext(request))
	else:
		formulario= AsistenciaForm()
		return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

@login_required
def consultar_asistencia(request):
	titulo = 'Consultar Asistencia'
	if request.method == 'POST':
		formulario = ConsultaAsisForm(request.POST)
		if formulario.is_valid():
			legajo	   = formulario.cleaned_data['legajo']
			materia    = formulario.cleaned_data['materia']
			anio       = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/Editar_asistencia/%s/%s/%s/'%(legajo,materia,anio))
			
	else:
		formulario = ConsultaAsisForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))		

		
@login_required
def Editar_asistencia(request,legajo, materia, anio):
	titulo = 'Editar Asistencia'
	libro = LibroAula.objects.get(materia__nombre=materia, anio=anio)
	Objeto = Asistencia.objects.get(alumno__legajo=legajo, libro_aula=libro)
	if request.method == 'POST':
		formulario = AsistenciaForm(request.POST, instance=Objeto)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('datosasistencia.html', context_instance=RequestContext(request))
	else:
		formulario = AsistenciaForm(instance=Objeto)
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	


	



###### MENU INFORMES ######

# EXAMEN PARCIAL #
@login_required
def consultar_notas(request):
	titulo = 'Informe de notas Parciales'
	if request.method == 'POST':
		formulario = ConsultanotasForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio    = formulario.cleaned_data['anio']
			curso   = formulario.cleaned_data['curso']
			return HttpResponseRedirect('/informenotas/%s/%s/'%(materia,anio,curso))
			
	else:
		formulario = ConsultanotasForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	

@login_required
def informenotas(request, materia, anio, curso):
	titulo2 = materia
	titulo1 = 'Informe de Parciales'
	list=[]
	lista = Parcial.objects.filter(materia__nombre=materia, fecha__year=anio, materia__curso=curso).order_by('alumno')
	for elem in lista:
		list.append(Parcial.objects.get(alumno=elem.alumno))

	return render_to_response('tablaExamenparcial.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 
		
		
### EXAMEN FINAL ###

@login_required
def consultar_finales(request):
	titulo = 'Informe de notas Finales'
	if request.method == 'POST':
		formulario = ConsultanotasForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio    = formulario.cleaned_data['anio']
			curso   = formulario.cleaned_data['curso']
			return HttpResponseRedirect('/informefinales/%s/%s/'%(materia,anio,curso))
			
	else:
		formulario = ConsultanotasForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))			

@login_required
def informefinales(request, materia, anio, curso):
	titulo2 = materia
	titulo1 = 'Informe de Finales'
	list=[]
	lista = Final.objects.filter(materia__nombre=materia, fecha__year=anio, materia__curso=curso).order_by('alumno')
	for elem in lista:
		list.append(Final.objects.get(alumno=elem.alumno))

	return render_to_response('tablaExamenfinal.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 		


@login_required
def consultarAlumno2(request):
	titulo = 'Consultar Alumno'
	if request.method == 'POST':
		formulario = ConsultarAlumnoForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			ape = formulario.cleaned_data['apellido']
			return HttpResponseRedirect('/datosAlumno2/%s/%s/'%(nom,ape))
			
	else:
		formulario = ConsultarAlumnoForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def datosAlumno2(request,nom,ape):
	titulo = 'Consultar Alumno'
	alumno = Alumno.objects.get(nombre1=nom, apellido=ape)
	formulario = AlumnoForm(instance=alumno)
	return render_to_response('consultas2.html',{ 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	
	
## INFORME DE COLOQUIO	

@login_required
def consultaColoquio2(request):
	titulo = 'Acta de Alumnos a Coloquio'
	if request.method == 'POST':
		formulario = InscripcionMateriaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/actaColoquio2/%s/%s/'%(materia,anio))
	else:
		formulario = InscripcionMateriaForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def actaColoquio2(request, materia, anio):
	titulo2 = materia
	titulo1 = 'Acta de Alumnos a Coloquio'
	list=[]
	lista = Coloquio.objects.filter(materia__nombre=materia, fecha__year=anio).order_by('alumno')
	for elem in lista:
		list.append(Coloquio.objects.get(alumno=elem.alumno))

	return render_to_response('tablaColoquio2.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 

	
## MATRICULA
	
@login_required
def consultaMatricula2(request):
	titulo = 'Acta de Matricula'
	if request.method == 'POST':
		formulario = InscripcionMateriaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/actaMatricula2/%s/%s/'%(materia,anio))
	else:
		formulario = InscripcionMateriaForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	


@login_required
def actaMatricula2(request, materia, anio):
	mat = Materia.objects.get(nombre=materia)
	titulo1 = 'Acta de Matricula'
	titulo2 = '%s' %(mat.carrera)
	titulo3 = '%s' %(materia)
	
	list=[]
	lista = InscripcionMateria.objects.filter(materia__nombre=materia, fecha_inscripcion__year=anio).order_by('alumno')
	for elem in lista:
		list.append(InscripcionMateria.objects.get(id=elem.id))

	return render_to_response('actaMatricula2.html', { 'list': list, 'titulo1': titulo1, 'titulo2': titulo2, 'titulo3': titulo3 }, context_instance=RequestContext(request)) 
## EDITAR FINAL###

@login_required
def Consultar_final(request):
	titulo = 'Consultar Final'
	if request.method == 'POST':
		formulario = ConsultafinalForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio 	= formulario.cleaned_data['anio']
			turno	= formulario.cleaned_data['turno']
			legajo  = formulario.cleaned_data['legajo']
			
			return HttpResponseRedirect('/Editar_final/%s/%s/%s/%s/'%(materia,anio,turno,legajo))
			
	else:
		formulario = ConsultafinalForm()
		return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))		

@login_required
def Editar_final(request, materia,anio,turno,legajo):
	titulo = 'Editar Final'
	Objeto = get_object_or_404(Final, materia__nombre=materia, turno__fecha_inicio__year=anio, turno__numero=turno, alumno__legajo=legajo)
	if request.method == 'POST':
		formulario = FinalForm(request.POST, instance=Objeto)
		if formulario.is_valid():
			formulario.save()
			return render_to_response('datoscargados2.html', context_instance=RequestContext(request))
	else:
		formulario = FinalForm(instance=Objeto)
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 



###3######CONTRASEÑA PROFESOR #########
@login_required
def cambiarPassword2(request):
	titulo = 'Cambiar Contraseña'
	usuario = request.user
	if request.method == 'POST':
		formulario = CambioPasswordForm(request.POST)
		if formulario.is_valid():
			password_one = formulario.cleaned_data['password_one']
			password_two = formulario.cleaned_data['password_two']
			usuario.set_password(password_two)
			usuario.save()
			return render_to_response('passwordCambiado2.html', context_instance=RequestContext(request))
			
		else:
			return render_to_response('passwordNoCambiado2.html', context_instance=RequestContext(request))
	else:
		formulario = CambioPasswordForm()
		return render_to_response('formularios_profesor.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def crearPrograma(request):
	titulo = 'Crear Programa'
	if request.method == 'POST':
		formulario = CrearProgramaForm(request.POST)
		if formulario.is_valid():
			add = formulario.save()
			programa = add.id
			return HttpResponseRedirect('/crearContenido/%s/'%(programa))
	else:
		formulario = CrearProgramaForm()
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

@login_required
def crearContenido(request, programa):
	titulo = 'Crear Contenido de Programa'
	if request.method == 'POST':
		formulario = CrearContenidoForm(request.POST)
		if formulario.is_valid():
			contenido = formulario.save(commit=False)
			programa = Programa.objects.get(id=programa)
			contenido.programa = programa
			contenido.save()
			formulario.save()
			return render_to_response('formulario_consulta2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	

	else:
		formulario = CrearContenidoForm()
	return render_to_response('formulario2.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))

	
################# MENU ALUMNOS!!!!################
	

@login_required
def consultaTurnoExamenAlumno(request):
	titulo = 'Turno de Exámen'
	if request.method == 'POST':
		formulario = ConsultarTurnoExamenForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			anio = formulario.cleaned_data['anio']
			numero = formulario.cleaned_data['numero']
			return HttpResponseRedirect('/turnoExamenAlumno/%s/%s/%s/'%(carrera,anio,numero))
	else:
		formulario = ConsultarTurnoExamenForm()
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
		

@login_required
def turnoExamenAlumno(request, carrera, anio, numero):
	titulo2 = 'Turno de Examen Nro: %s'%(numero)
	titulo1 = '%s'%(carrera)
	turnoExamen = TurnoExamen.objects.get(numero=numero, fecha_inicio__year=anio, carrera__nombre=carrera)
	list1=[]
	list2=[]
	list3=[]
	lista1 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=1).order_by('fecha')
	lista2 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=2).order_by('fecha')
	lista3 = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__carrera__nombre=carrera, materia__curso=3).order_by('fecha')
	
	for elem in lista1:
		list1.append(ItemTurnoExamen.objects.get(id=elem.id))
	for elem in lista2:
		list2.append(ItemTurnoExamen.objects.get(id=elem.id))
	for elem in lista3:
		list3.append(ItemTurnoExamen.objects.get(id=elem.id))
			
	return render_to_response('turnoExamenAlumno.html', { 'turnoExamen': turnoExamen, 'list1': list1, 'list2': list2, 'list3': list3, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 
		

@login_required
def consultarPlanEstudio(request):
	titulo = 'Consultar Plan de Estudio'
	if request.method == 'POST':
		formulario = ConsultarPlanEstudioForm(request.POST)
		if formulario.is_valid():
			nom = formulario.cleaned_data['nombre']
			return HttpResponseRedirect('/planEstudio/%s/'%(nom))
			
	else:
		formulario = ConsultarPlanEstudioForm
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def planEstudio(request,nom):
	titulo = 'Consultar Plan de Estudio'
	plan = PlanEstudio.objects.get(nombre=nom)
	formulario = PlanEstudioForm(instance=plan)
	return render_to_response('consultas_alumno.html',{ 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	
		

@login_required
def consultarPrograma(request):
	titulo = 'Consultar Programa'
	if request.method == 'POST':
		formulario = ConsultaLibroAulaForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/programa/%s/%s/'%(materia,anio))
			
	else:
		formulario = ConsultaLibroAulaForm
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
@login_required
def programa(request,materia,anio):
	titulo = 'Consultar Programa'
	libro = LibroAula.objects.get(materia__nombre=materia, anio=anio)
	Objeto = get_object_or_404(Programa, id=libro.programa.id)
	formulario = ProgramaForm(instance=programa)
	return render_to_response('consultas_alumno.html',{ 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request)) 	
			

		
@login_required
def consultarExamenParcial(request):
	titulo = 'Consultar Exámenes Parciales'
	if request.method == 'POST':
		formulario = ConsultaExamenForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/notasParciales/%s/%s/'%(materia,anio))
			
	else:
		formulario = ConsultaExamenForm
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
	
@login_required
def notasParciales(request,materia,anio):
	titulo1 = 'Consulta Notas Exámenes Parciales'
	titulo2 = materia
	list=[]
	usuario = request.user.persona
	parciales = Parcial.objects.filter(materia__nombre=materia, fecha__year=anio, alumno=usuario).order_by('fecha')
	for examen in parciales:
		list.append(Parcial.objects.get(id=examen.id))
	
	return render_to_response('consulta_parciales.html',{ 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 	
		


@login_required
def consultarExamenFinal(request):
	titulo = 'Consultar Exámen Final'
	if request.method == 'POST':
		formulario = ConsultaExamenForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/notasFinales/%s/%s/'%(materia,anio))
			
	else:
		formulario = ConsultaExamenForm
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
	
@login_required
def notasFinales(request,materia,anio):
	titulo1 = 'Consulta Notas Exámen Final'
	titulo2 = materia
	list=[]
	usuario = request.user.persona
	finales = Final.objects.filter(materia__nombre=materia, fecha__year=anio, alumno=usuario).order_by('fecha')
	for examen in finales:
		list.append(Final.objects.get(id=examen.id))
	
	return render_to_response('consulta_finales.html',{ 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 	

	
@login_required
def consultarColoquios(request):
	titulo = 'Consultar Notas Coloquio'
	if request.method == 'POST':
		formulario = ConsultaExamenForm(request.POST)
		if formulario.is_valid():
			materia = formulario.cleaned_data['materia']
			anio = formulario.cleaned_data['anio']
			return HttpResponseRedirect('/notasColoquios/%s/%s/'%(materia,anio))
			
	else:
		formulario = ConsultaExamenForm
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
	
@login_required
def notasColoquios(request,materia,anio):
	titulo1 = 'Consulta Notas Coloquio'
	titulo2 = materia
	list=[]
	usuario = request.user.persona
	finales = Coloquio.objects.filter(materia__nombre=materia, fecha__year=anio, alumno=usuario).order_by('fecha')
	for examen in finales:
		list.append(Coloquio.objects.get(id=examen.id))
	
	return render_to_response('consulta_coloquios.html',{ 'list': list, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 	
	

@login_required
def consultarCorrelativas(request):
	titulo = 'Consultar Correlativas'
	if request.method == 'POST':
		formulario = ConsultarCorrelativaForm(request.POST)
		if formulario.is_valid():
			carrera = formulario.cleaned_data['carrera']
			return HttpResponseRedirect('/correlativas/%s/'%(carrera))
			
	else:
		formulario = ConsultarCorrelativaForm()
		return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	
	
@login_required
def correlativas(request,carrera):
	titulo1 = 'Consulta Materias Correlativas'
	titulo2 = carrera
	list1=[]
	list2=[]
	list3=[]
	materias1 = Materia.objects.filter(carrera__nombre=carrera, curso=1)
	materias2 = Materia.objects.filter(carrera__nombre=carrera, curso=2)
	materias3 = Materia.objects.filter(carrera__nombre=carrera, curso=3)
	
	for mat in materias1:
		list1.append(Materia.objects.get(id=mat.id))
	for mat in materias2:
		list2.append(Materia.objects.get(id=mat.id))
	for mat in materias3:
		list3.append(Materia.objects.get(id=mat.id))

	return render_to_response('consulta_correlativas.html',{ 'list1': list1, 'list2': list2, 'list3': list3, 'titulo1': titulo1, 'titulo2': titulo2 }, context_instance=RequestContext(request)) 	
		
	
@login_required
def cambiarPassword(request):
	titulo = 'Cambiar Contraseña'
	usuario = request.user
	if request.method == 'POST':
		formulario = CambioPasswordForm(request.POST)
		if formulario.is_valid():
			password_one = formulario.cleaned_data['password_one']
			password_two = formulario.cleaned_data['password_two']
			usuario.set_password(password_two)
			usuario.save()
			# CODIGO NUEVO
			persona = __castPersona(usuario.persona)
			if isinstance(persona, Alumno):
				html = 'passwordCambiado.html'
			elif isinstance(persona, Coordinador):
				html = 'passwordCambiado3.html'
			elif isinstance(persona, Profesor):
				html = 'passwordCambiado2.html'
			return render_to_response(html,{'usuario':usuario}, context_instance=RequestContext(request))
			#return render_to_response('passwordCambiado.html', context_instance=RequestContext(request))
			
		else:
			return render_to_response('passwordNoCambiado.html', context_instance=RequestContext(request))
	else:
		formulario = CambioPasswordForm()
		return render_to_response('formularios_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
		
@login_required
def inscribirMateria(request):
	if inscripcionMateria == True:
		titulo = 'Inscripción a Materias'
		if request.method == 'POST':
			formulario = InscribirMateriaForm(request.POST)
			if formulario.is_valid():
				carrera = formulario.cleaned_data['carrera']
				curso = formulario.cleaned_data['curso']
				return HttpResponseRedirect('/inscripcionMaterias/%s/%s/'%(carrera,curso))
			
		else:
			formulario = InscribirMateriaForm()
			return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	else:
		return render_to_response('privadoAlumno.html', context_instance=RequestContext(request)) 

@login_required
def inscripcionMaterias(request,carrera,curso):
	titulo1 = 'Inscripción a Materias'
	lista1 = []
	lista = Materia.objects.filter(carrera__nombre=carrera, curso=curso).order_by('nombre')
	for mat in lista:
		lista1.append(Materia.objects.get(id=mat.id))
	return render_to_response('inscripcionMaterias.html',{ 'lista1': lista1, 'titulo1': titulo1 }, context_instance=RequestContext(request)) 	


@login_required
def inscripcionMat(request,mat):
	usuario = request.user.persona
	fecha_actual = datetime.date.today()
	materia = Materia.objects.get(nombre=mat)
	alumno = Alumno.objects.get(legajo=usuario.legajo)
	condicion = Condicion.objects.get(nombre='Regular')
	correlativa =  materia.correlativas.all()
	consulta = InscripcionMateria.objects.filter(materia=materia, alumno=alumno, condicion=condicion, fecha_inscripcion=fecha_actual).values()
	if len(consulta) > 0:
		return render_to_response('inscripcionInvalida.html',{ 'materia': materia }, context_instance=RequestContext(request)) 	
	else:
		for x in correlativa:
			consultar = InscripcionMateria.objects.filter(materia=x, alumno=alumno, condicion=condicion, fecha_inscripcion=fecha_actual, aprobado=True).values()
			if len(consultar) == 0:
				return render_to_response('inscripcionInvalidoCorrelativa.html',{ 'materia': materia }, context_instance=RequestContext(request))

		insc = InscripcionMateria(materia=materia, alumno=alumno, condicion=condicion, fecha_inscripcion=fecha_actual)
		insc.save()
		consultaCuota = Cuotas.objects.filter(alumno=alumno, anio=fecha_actual.year)
		if len(consultaCuota) == 0:
			cuota = Cuotas(alumno=alumno, anio=fecha_actual.year)
			cuota.save()
		return render_to_response('inscripcionValida.html',{ 'materia': materia }, context_instance=RequestContext(request)) 	


@login_required
def inscribirFinal(request):
	if inscripcionMateria == True:
		titulo = 'Inscripción a Exámenes'
		if request.method == 'POST':
			formulario = InscribirExamenForm(request.POST)
			if formulario.is_valid():
				carrera = formulario.cleaned_data['carrera']
				curso = formulario.cleaned_data['curso']
				turno = formulario.cleaned_data['turno']
				return HttpResponseRedirect('/inscripcionFinales/%s/%s/%s/'%(carrera,curso,turno))
			
		else:
			formulario = InscribirExamenForm()
			return render_to_response('formulario_consulta_alumno.html', { 'formulario': formulario, 'titulo': titulo }, context_instance=RequestContext(request))	
	else:
		return render_to_response('privadoAlumno.html', context_instance=RequestContext(request)) 

@login_required
def inscripcionFinales(request,carrera,curso,turno):
	titulo1 = 'Inscripción a Exámenes'
	lista1 = []
	fecha_actual = datetime.date.today()
	turnoExamen = TurnoExamen.objects.get(numero=turno, fecha_inicio__year=fecha_actual.year)#fecha_inicio__lt=fecha_actual
	if fecha_actual > turnoExamen.fecha_inicio and fecha_actual < turnoExamen.fecha_fin:
		lista = ItemTurnoExamen.objects.filter(turno=turnoExamen, materia__curso=curso, materia__carrera__nombre=carrera)
		for tur in lista:
			lista1.append(ItemTurnoExamen.objects.get(id=tur.id))
		return render_to_response('inscripcionExamenes.html',{ 'lista1': lista1, 'turnoExamen':turnoExamen, 'titulo1': titulo1 }, context_instance=RequestContext(request)) 	
	else: 
		return render_to_response('Noinscribir.html', context_instance=RequestContext(request))

@login_required
def inscripcionExamenFinal(request,mat,turnoexamen_id):
	usuario = request.user.persona
	fecha_actual = datetime.date.today()
	materia = Materia.objects.get(nombre=mat)
	alumno = Alumno.objects.get(legajo=usuario.legajo)
	condicion = Condicion.objects.get(nombre='Regular')
	correlativa =  materia.correlativas.all()
	turno = TurnoExamen.objects.get(id=turnoexamen_id)
	consulta = Final.objects.filter(materia=materia, alumno=alumno, condicion=condicion, turno=turno).values()
	if len(consulta) > 0:
		return render_to_response('inscripcionInvalida.html',{ 'materia': materia }, context_instance=RequestContext(request)) 	
	else:
		for x in correlativa:
			consultar = InscripcionMateria.objects.filter(materia=x, alumno=alumno, condicion=condicion, fecha_inscripcion=fecha_actual, aprobado=True).values()
			if len(consultar) == 0:
				return render_to_response('inscripcionInvalidoCorrelativa.html',{ 'materia': materia }, context_instance=RequestContext(request))

		insc = Final(materia=materia, alumno=alumno, condicion=condicion, fecha_inscripcion=fecha_actual, turno=turno)
		insc.save()
		return render_to_response('inscripcionValida.html',{ 'materia': materia }, context_instance=RequestContext(request)) 	
		

			

	
	