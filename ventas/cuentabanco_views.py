from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_cuentabanco_group, login_url='/login/')
def index_cuentabanco(request):
    form_class = GenericSearchForm
    model = CuentaBanco
    template_name = 'index_cuentabanco.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        cuentabanco_list = model.objects.filter(banco__nombre__icontains=form.cleaned_data['buscar'])
    else:
        cuentabanco_list = model.objects.all()

    paginator = Paginator(cuentabanco_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        cuentabancos = paginator.page(page)
    except PageNotAnInteger:
        cuentabancos = paginator.page(1)
    except EmptyPage:
        cuentabancos = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'cuentabancos': cuentabancos,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_cuentabanco', login_url='/login/')
def add_cuentabanco(request):
    template_name="cuentabanco.html"
    if request.method == 'POST':
        form = ManageCuentaBancos(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/cuentabanco/')
    else:
        form = ManageCuentaBancos()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_cuentabanco', login_url='/login/')
def edit_cuentabanco(request,pk):
    cuentabanco = get_object_or_404(CuentaBanco, pk=pk)        
    form = ManageCuentaBancos(instance=cuentabanco)    
    #print form.nombres
    if request.POST:
        form = ManageCuentaBancos(request.POST,request.FILES,instance=cuentabanco)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/cuentabanco/')        

    return render_to_response('cuentabanco.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_cuentabanco', login_url='/login/')
def delete_cuentabanco(request,pk):
	cuentabanco = get_object_or_404(CuentaBanco, pk=pk)        
	form = ManageCuentaBancos(instance=cuentabanco)    
    #print form.nombres
	if request.POST:
		form = ManageCuentaBancos(request.POST,request.FILES,instance=cuentabanco)    
		if form.is_valid():
			cuentabanco.delete()            
			messages.add_message(request, messages.SUCCESS, ('CuentaBanco eliminada'))
			return HttpResponseRedirect('/cuentabanco/')        

	return render_to_response('cuentabanco.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))