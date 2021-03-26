from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from django.http import JsonResponse
from django.db.models import Avg,Sum,Count,F,FloatField,Q
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from comunes import *

@login_required(login_url='/login/')
@user_passes_test(is_in_articulo_group, login_url='/login/')
def index_articulo(request):
    form_class = GenericSearchForm
    model = Articulo
    template_name = 'index_articulo.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        articulo_list = model.objects.filter(descripcion__icontains=form.cleaned_data['buscar'])
    else:
        articulo_list = model.objects.all()

    paginator = Paginator(articulo_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        articulos = paginator.page(page)
    except PageNotAnInteger:
        articulos = paginator.page(1)
    except EmptyPage:
        articulos = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'articulos': articulos,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_articulo', login_url='/login/')
def add_articulo(request):
    template_name="articulo.html"

    if request.method == 'POST':
        form = ManageArticulos(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/articulo/')
    else:
        form = ManageArticulos()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_articulo', login_url='/login/')
def edit_articulo(request,pk):
    articulo = get_object_or_404(Articulo, pk=pk)        
    form = ManageArticulos(instance=articulo)    
    #print form.nombres
    if request.POST:
        form = ManageArticulos(request.POST,request.FILES,instance=articulo)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/articulo/')        

    return render_to_response('articulo.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_articulo', login_url='/login/')
def delete_articulo(request,pk):
	articulo = get_object_or_404(Articulo, pk=pk)        
	form = ManageArticulos(instance=articulo)    
    #print form.nombres
	if request.POST:
		form = ManageArticulos(request.POST,request.FILES,instance=articulo)    
		if form.is_valid():
			articulo.delete()            
			messages.add_message(request, messages.SUCCESS, ('Articulo eliminada'))
			return HttpResponseRedirect('/articulo/')        

	return render_to_response('articulo.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


def search_articulo(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['term']        
        art=Articulo.objects.filter(Q(codigo__contains=to_search) | Q(descripcion__contains=to_search))        
        for i in range(0,len(art)):
            data[i]={'id':art[i].id,'codigo':art[i].codigo,
                    'value':art[i].descripcion,'importe':art[i].importe,
                    'descuento':art[i].descuento,'impuesto':art[i].tipoimpuesto.valor
                    }

    return JsonResponse(data)    

def search_articulo_codigo(request):
    data={}    
    if request.method == 'GET':
        to_search=request.GET['codigo'] 
        try:
            art=Articulo.objects.get( codigo=to_search )         
        except Articulo.DoesNotExist:
            data['articulo'] = {"error":"No se encontro el registro"}
        else:
            data['articulo']={'id':art.id,'descripcion':art.descripcion}

    return JsonResponse(data)      