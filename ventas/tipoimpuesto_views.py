from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_tipoimpuesto_group, login_url='/login/')
def index_tipoimpuesto(request):
    form_class = GenericSearchForm
    model = TipoImpuesto
    template_name = 'index_tipoimpuesto.html'
    paginate_by = 5

    form = form_class(request.POST or None)
    if form.is_valid():
        tipoimpuesto_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
    else:
        tipoimpuesto_list = model.objects.all()

    paginator = Paginator(tipoimpuesto_list, 5) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        tipoimpuestos = paginator.page(page)
    except PageNotAnInteger:
        tipoimpuestos = paginator.page(1)
    except EmptyPage:
        tipoimpuestos = paginator.page(paginator.num_pages)

    return render_to_response(template_name, 
            {'form': form, 'tipoimpuestos': tipoimpuestos,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_tipoimpuesto', login_url='/login/')
def add_tipoimpuesto(request):
    template_name="tipoimpuesto.html"
    if request.method == 'POST':
        form = ManageTipoImpuestos(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/tipoimpuesto/')
    else:
        form = ManageTipoImpuestos()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_tipoimpuesto', login_url='/login/')
def edit_tipoimpuesto(request,pk):
    tipoimpuesto = get_object_or_404(TipoImpuesto, pk=pk)        
    form = ManageTipoImpuestos(instance=tipoimpuesto)    
    #print form.nombres
    if request.POST:
        form = ManageTipoImpuestos(request.POST,request.FILES,instance=tipoimpuesto)    
        if form.is_valid():
            form.save()
            #persona = form.save()
            #this is where you might choose to do stuff.
            #contact.name = 'test'
            #persona.save()
            messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
            return HttpResponseRedirect('/tipoimpuesto/')        

    return render_to_response('tipoimpuesto.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_tipoimpuesto', login_url='/login/')
def delete_tipoimpuesto(request,pk):
	tipoimpuesto = get_object_or_404(TipoImpuesto, pk=pk)        
	form = ManageTipoImpuestos(instance=tipoimpuesto)    
    #print form.nombres
	if request.POST:
		form = ManageTipoImpuestos(request.POST,request.FILES,instance=tipoimpuesto)    
		if form.is_valid():
			tipoimpuesto.delete()            
			messages.add_message(request, messages.SUCCESS, ('TipoImpuesto eliminada'))
			return HttpResponseRedirect('/tipoimpuesto/')        

	return render_to_response('tipoimpuesto.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))