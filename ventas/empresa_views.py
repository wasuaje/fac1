from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *

@login_required(login_url='/login/')
@user_passes_test(is_in_empresa_group, login_url='/login/')
def index_empresa(request):
    form_class = GenericSearchForm
    model = Empresa
    template_name = 'index_empresa.html'
    paginate_by = 10
    #numero de registros existente, solo debe haber uno
    _count=Empresa.objects.count()

    form = form_class(request.POST or None)
    if form.is_valid():
        empresa_list = model.objects.filter(razon_social__icontains=form.cleaned_data['buscar'])
    else:
        empresa_list = model.objects.all()

    paginator = Paginator(empresa_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        empresas = paginator.page(page)
    except PageNotAnInteger:
        empresas = paginator.page(1)
    except EmptyPage:
        empresas = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'empresas': empresas,'registros':_count}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_empresa', login_url='/login/')
def add_empresa(request):
    #import pdb; pdb.set_trace()
    template_name="empresa.html"
    if request.method == 'POST':
        form = ManageEmpresas(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/empresa/')
    else:
        form = ManageEmpresas()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.change_empresa', login_url='/login/')
def edit_empresa(request,pk):
    empresa = get_object_or_404(Empresa, pk=pk)        
    form = ManageEmpresas(instance=empresa)    
    #print form.nombres
    if request.POST:
        form = ManageEmpresas(request.POST,request.FILES,instance=empresa)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/empresa/')        

    return render_to_response('empresa.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_empresa', login_url='/login/')
def delete_empresa(request,pk):
	empresa = get_object_or_404(Empresa, pk=pk)        
	form = ManageEmpresas(instance=empresa)    
    #print form.nombres
	if request.POST:
		form = ManageEmpresas(request.POST,request.FILES,instance=empresa)    
		if form.is_valid():
			empresa.delete()            
			messages.add_message(request, messages.SUCCESS, ('Empresa eliminado'))
			return HttpResponseRedirect('/empresa/')        

	return render_to_response('empresa.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))