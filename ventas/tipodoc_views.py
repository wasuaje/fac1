from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_tipodoc_group, login_url='/login/')
def index_tipodoc(request):
    form_class = GenericSearchForm
    model = TipoDoc
    template_name = 'index_tipodoc.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        tipodoc_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
    else:
        tipodoc_list = model.objects.all()

    paginator = Paginator(tipodoc_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        tipodocs = paginator.page(page)
    except PageNotAnInteger:
        tipodocs = paginator.page(1)
    except EmptyPage:
        tipodocs = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'tipodocs': tipodocs,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_tipodoc', login_url='/login/')
def add_tipodoc(request):
    template_name="tipodoc.html"
    if request.method == 'POST':
        form = ManageTipoDocs(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/tipodoc/')
    else:
        form = ManageTipoDocs()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_tipodoc', login_url='/login/')
def edit_tipodoc(request,pk):
    tipodoc = get_object_or_404(TipoDoc, pk=pk)        
    form = ManageTipoDocs(instance=tipodoc)    
    #print form.nombres
    if request.POST:
        form = ManageTipoDocs(request.POST,request.FILES,instance=tipodoc)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/tipodoc/')        

    return render_to_response('tipodoc.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_tipodoc', login_url='/login/')
def delete_tipodoc(request,pk):
	tipodoc = get_object_or_404(TipoDoc, pk=pk)        
	form = ManageTipoDocs(instance=tipodoc)    
    #print form.nombres
	if request.POST:
		form = ManageTipoDocs(request.POST,request.FILES,instance=tipodoc)    
		if form.is_valid():
			tipodoc.delete()            
			messages.add_message(request, messages.SUCCESS, ('TipoDoc eliminada'))
			return HttpResponseRedirect('/tipodoc/')        

	return render_to_response('tipodoc.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))