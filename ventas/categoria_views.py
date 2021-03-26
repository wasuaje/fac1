from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_categoria_group, login_url='/login/')
def index_categoria(request):
    form_class = GenericSearchForm
    model = Categoria
    template_name = 'index_categoria.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        categoria_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
    else:
        categoria_list = model.objects.all()

    paginator = Paginator(categoria_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        categorias = paginator.page(page)
    except PageNotAnInteger:
        categorias = paginator.page(1)
    except EmptyPage:
        categorias = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'categorias': categorias,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_categoria', login_url='/login/')
def add_categoria(request):
    template_name="categoria.html"
    if request.method == 'POST':
        form = ManageCategorias(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/categoria/')
    else:
        form = ManageCategorias()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_categoria', login_url='/login/')
def edit_categoria(request,pk):
    categoria = get_object_or_404(Categoria, pk=pk)        
    form = ManageCategorias(instance=categoria)    
    #print form.nombres
    if request.POST:
        form = ManageCategorias(request.POST,request.FILES,instance=categoria)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/categoria/')        

    return render_to_response('categoria.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_categoria', login_url='/login/')
def delete_categoria(request,pk):
	categoria = get_object_or_404(Categoria, pk=pk)        
	form = ManageCategorias(instance=categoria)    
    #print form.nombres
	if request.POST:
		form = ManageCategorias(request.POST,request.FILES,instance=categoria)    
		if form.is_valid():
			categoria.delete()            
			messages.add_message(request, messages.SUCCESS, ('Categoria eliminada'))
			return HttpResponseRedirect('/categoria/')        

	return render_to_response('categoria.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))