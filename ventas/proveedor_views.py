from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect,JsonResponse
from comunes import *

@login_required(login_url='/login/')
@user_passes_test(is_in_proveedor_group, login_url='/login/')
def index_proveedor(request):
    form_class = GenericSearchForm
    model = Proveedor
    template_name = 'index_proveedor.html'
    paginate_by = 10

    form = form_class(request.POST or None)
    if form.is_valid():
        proveedor_list = model.objects.filter(razon_social__icontains=form.cleaned_data['buscar'])
    else:
        proveedor_list = model.objects.all()

    paginator = Paginator(proveedor_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        proveedors = paginator.page(page)
    except PageNotAnInteger:
        proveedors = paginator.page(1)
    except EmptyPage:
        proveedors = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'proveedors': proveedors,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_proveedor', login_url='/login/')
def add_proveedor(request):
    #import pdb; pdb.set_trace()
    template_name="proveedor.html"
    if request.method == 'POST':
        form = ManageProveedores(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/proveedor/')
    else:
        form = ManageProveedores()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.change_proveedor', login_url='/login/')
def edit_proveedor(request,pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)        
    form = ManageProveedores(instance=proveedor)    
    #print form.nombres
    if request.POST:
        form = ManageProveedores(request.POST,request.FILES,instance=proveedor)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/proveedor/')        

    return render_to_response('proveedor.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_proveedor', login_url='/login/')
def delete_proveedor(request,pk):
	proveedor = get_object_or_404(Proveedor, pk=pk)        
	form = ManageProveedores(instance=proveedor)    
    #print form.nombres
	if request.POST:
		form = ManageProveedores(request.POST,request.FILES,instance=proveedor)    
		if form.is_valid():
			proveedor.delete()            
			messages.add_message(request, messages.SUCCESS, ('Proveedor eliminado'))
			return HttpResponseRedirect('/proveedor/')        

	return render_to_response('proveedor.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


def search_proveedor(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['term'] 
        art=Proveedor.objects.filter(Q(rif__contains=to_search) | Q(razon_social__contains=to_search))        
        for i in range(0,len(art)):
            data[i]={'id':art[i].id,'rif':art[i].rif,
                    'value':art[i].razon_social
                    }

    return JsonResponse(data)    

def search_proveedor_id(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['search'] 
        clt=Proveedor.objects.filter( pk=to_search )         
        data['proveedor']={'id':clt[0].id,'rif':clt[0].rif,
                    'razon_social':clt[0].razon_social
                    }

    return JsonResponse(data)        

def qadd_proveedor(request):
    data={}    
    if request.method == 'GET':
        razon=request.GET['razon'] 
        rif=request.GET['rif'] 
        telefono=request.GET['telefono']         
        clte=Proveedor(razon_social=razon,rif=rif,tlf=telefono)
        clte.save()
        
        data['nuevo_proveedor']={'id':clte.id,'rif':clte.rif,
                    'razon_social':clte.razon_social
                    }

    return JsonResponse(data)        

