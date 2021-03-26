from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from django.db.models import Q
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_cliente_group, login_url='/login/')
def index_cliente(request):
    form_class = GenericSearchForm
    model = Cliente
    template_name = 'index_cliente.html'
    paginate_by = 10

    form = form_class(request.POST or None)
    if form.is_valid():
        cliente_list = model.objects.filter(razon_social__icontains=form.cleaned_data['buscar'])
    else:
        cliente_list = model.objects.all()

    paginator = Paginator(cliente_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        clientes = paginator.page(page)
    except PageNotAnInteger:
        clientes = paginator.page(1)
    except EmptyPage:
        clientes = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'clientes': clientes,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_cliente', login_url='/login/')
def add_cliente(request):
    #import pdb; pdb.set_trace()
    template_name="cliente.html"
    if request.method == 'POST':
        form = ManageClientes(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/cliente/')
    else:
        form = ManageClientes()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.change_cliente', login_url='/login/')
def edit_cliente(request,pk):
    cliente = get_object_or_404(Cliente, pk=pk)        
    form = ManageClientes(instance=cliente)    
    #print form.nombres
    if request.POST:
        form = ManageClientes(request.POST,request.FILES,instance=cliente)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/cliente/')        

    return render_to_response('cliente.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_cliente', login_url='/login/')
def delete_cliente(request,pk):
	cliente = get_object_or_404(Cliente, pk=pk)        
	form = ManageClientes(instance=cliente)    
    #print form.nombres
	if request.POST:
		form = ManageClientes(request.POST,request.FILES,instance=cliente)    
		if form.is_valid():
			cliente.delete()            
			messages.add_message(request, messages.SUCCESS, ('Cliente eliminado'))
			return HttpResponseRedirect('/cliente/')        

	return render_to_response('cliente.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))

def search_cliente(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['term'] 
        art=Cliente.objects.filter(Q(rif__contains=to_search) | Q(razon_social__contains=to_search))        
        for i in range(0,len(art)):
            data[i]={'id':art[i].id,'rif':art[i].rif,
                    'value':art[i].razon_social
                    }

    return JsonResponse(data)    

def search_cliente_id(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['search'] 
        clt=Cliente.objects.filter( pk=to_search )         
        data['cliente']={'id':clt[0].id,'rif':clt[0].rif,
                    'razon_social':clt[0].razon_social
                    }

    return JsonResponse(data)        

def qadd_cliente(request):
    data={}    
    if request.method == 'GET':
        razon=request.GET['razon'] 
        rif=request.GET['rif'] 
        telefono=request.GET['telefono']         
        clte=Cliente(razon_social=razon,rif=rif,tlf=telefono)
        clte.save()
        
        data['nuevo_cliente']={'id':clte.id,'rif':clte.rif,
                    'razon_social':clte.razon_social
                    }

    return JsonResponse(data)        

