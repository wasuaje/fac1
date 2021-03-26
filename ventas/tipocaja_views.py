from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_tipocaja_group, login_url='/login/')
def index_tipocaja(request):
    form_class = GenericSearchForm
    model = TipoCaja
    template_name = 'index_tipocaja.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        tipocaja_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
    else:
        tipocaja_list = model.objects.all()

    paginator = Paginator(tipocaja_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        tipocajas = paginator.page(page)
    except PageNotAnInteger:
        tipocajas = paginator.page(1)
    except EmptyPage:
        tipocajas = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'tipocajas': tipocajas,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_tipocaja', login_url='/login/')
def add_tipocaja(request):
    template_name="tipocaja.html"
    if request.method == 'POST':
        form = ManageTipoCajas(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/tipocaja/')
    else:
        form = ManageTipoCajas()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.change_tipocaja', login_url='/login/')
def edit_tipocaja(request,pk):
    tipocaja = get_object_or_404(TipoCaja, pk=pk)        
    form = ManageTipoCajas(instance=tipocaja)    
    #print form.nombres
    if request.POST:
        form = ManageTipoCajas(request.POST,request.FILES,instance=tipocaja)    
        if form.is_valid():
            form.save()            
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/tipocaja/')        

    return render_to_response('tipocaja.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_tipocaja', login_url='/login/')
def delete_tipocaja(request,pk):
	tipocaja = get_object_or_404(TipoCaja, pk=pk)        
	form = ManageTipoCajas(instance=tipocaja)    
    #print form.nombres
	if request.POST:
		form = ManageTipoCajas(request.POST,request.FILES,instance=tipocaja)    
		if form.is_valid():
			tipocaja.delete()            
			messages.add_message(request, messages.SUCCESS, ('TipoCaja eliminada'))
			return HttpResponseRedirect('/tipocaja/')        

	return render_to_response('tipocaja.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))