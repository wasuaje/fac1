from django.shortcuts import render

# Create your views here.
from django.http import *
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from ventas.models import *
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect    
from django.contrib import auth                 
from django.core.context_processors import csrf 
from forms import *
from django.views.generic import CreateView
#para separar cada pantalla o grupos
from categoria_views import *
from articulo_views import *
from cliente_views import *
from empresa_views import *
from proveedor_views import *
from tipodoc_views import *
from tipocaja_views import *
from cuentabanco_views import *
from factura_views import *
from factcompra_views import *
from tipoimpuesto_views import *
from postext_views import *
from formapago_views import *
from banco_views import *
from opercaja_views import *
from operturno_views import *
from rptventas_views import *
from rptcompras_views import *
from inventario_views import *
from rptinventarios_views import *

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, ('Ha salido con exito'))
    return HttpResponseRedirect('/')

def login_user(request):    
	error=""
	msg=""
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']	
		user = authenticate(username=username, password=password)			
		if user is not None:
			if user.is_active:
				login(request, user)
				messages.add_message(request, messages.SUCCESS, ('Se ha logueado correctamente!'))
				return HttpResponseRedirect('/')                            
			else:
				msg="El usuario esta inactivo"
				messages.add_message(request, messages.ERROR, ('No se pudo loguear'))
		else:
			msg="usuario no existe"				
			error="No se pudo loguear, %s" % msg

	if request.GET:
		next = request.GET['next']
		if  next == "/":
			pass
		else:
			error="No tiene permisos para esta funcionalidad"

	form = MyLoginForm()	
	return render(request,'login.html', {'form':form, 'error':error})


@login_required(login_url='/login/')
def main(request):
	#valido si la empresa esta creada, debe estarlo
	mensaje=[]
	_count=Empresa.objects.count()
	
	if _count==0:
		mensaje.append("No ha configurado su empresa. Vaya a Opciones->Configurar Empresa")	
	elif _count>1:
		mensaje.append("Error de configuracion de empresa")
	else:
		empresa=Empresa.objects.all()[:1]
		empresa=empresa[0]
		request.session['empresa'] = {'razon_social':empresa.razon_social,'rif':empresa.rif,
								'logo':empresa.ruta_foto.url,'nit':empresa.nit,'tlf':empresa.tlf,
								'fax':empresa.fax,'email':empresa.email,'direccion':empresa.direccion,
								'p1':empresa.p1,'p2':empresa.p2,'p3':empresa.p3,'p4':empresa.p4,
								'p5':empresa.p5
									}
		# return HttpResponseRedirect('/empresa/')
	
	try:
		impuesto=TipoImpuesto.objects.get(codigo='G')
	except TipoImpuesto.DoesNotExist:
		mensaje.append("Necesita configurar el impuesto Al menos uno debe tener codigo G. Click en Configurar->Tipo de Impuestos")
	else:
		request.session['impuesto'] = {'G':str(impuesto.valor)}
	#print request.session['impuesto']['G']
	#
	
	return render(request, 'index.html', {
            'mensaje': mensaje,            
        })


def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)     # create form object

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
        else:
        	print "error salvando"

    #args = {}
    #args.update(csrf(request))
    form = MyRegistrationForm()
    #print args
    return render(request, 'register.html', {'form':form})	

