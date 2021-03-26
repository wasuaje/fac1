from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_formapago_group, login_url='/login/')
def index_formapago(request):
    form_class = GenericSearchForm
    model = FormaPago
    template_name = 'index_formapago.html'
    paginate_by = 5

    if request.method == 'POST':
        form = form_class(request.POST or None)
        if form.is_valid():
            formapago_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
        else:
            formapago_list = model.objects.all()
    else:
        formapago_list = model.objects.all()
        form = form_class()
    
    paginator = Paginator(formapago_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        formapagos = paginator.page(page)
    except PageNotAnInteger:
        formapagos = paginator.page(1)
    except EmptyPage:
        formapagos = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'formapagos': formapagos,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_formapago', login_url='/login/')
def add_formapago(request):
    template_name="formapago.html"
    if request.method == 'POST':
        form = ManageFormaPagos(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/formapago/')
    else:
        form = ManageFormaPagos()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_formapago', login_url='/login/')
def edit_formapago(request,pk):
    formapago = get_object_or_404(FormaPago, pk=pk)        
    form = ManageFormaPagos(instance=formapago)    
    #print form.nombres
    if request.POST:
        form = ManageFormaPagos(request.POST,request.FILES,instance=formapago)    
        if form.is_valid():
            form.save()            
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/formapago/')        

    return render_to_response('formapago.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_formapago', login_url='/login/')
def delete_formapago(request,pk):
	formapago = get_object_or_404(FormaPago, pk=pk)        
	form = ManageFormaPagos(instance=formapago)    
    #print form.nombres
	if request.POST:
		form = ManageFormaPagos(request.POST,request.FILES,instance=formapago)    
		if form.is_valid():
			formapago.delete()            
			messages.add_message(request, messages.SUCCESS, ('FormaPago eliminada'))
			return HttpResponseRedirect('/formapago/')        

	return render_to_response('formapago.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))