from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect 
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory,inlineformset_factory
#from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Avg,Sum,Count,F,FloatField,Q
from decimal import *
from comunes import *
#import simplejson
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import SafeString

@login_required(login_url='/login/')
@user_passes_test(is_in_factcompra_group, login_url='/login/')
def index_factcompra(request):
    form_class = GenericSearchForm
    model = Documento
    template_name = 'index_factcompra.html'

    if request.method == 'POST': 
        form = form_class(request.POST or None)
        if form.is_valid():
            #factcompra_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            factcompra_list = model.objects.filter(Q(tipo_doc__codigo='FC') & \
                                                (Q(correlativo__contains=form.cleaned_data['buscar']) |\
                                                Q(cliente__razon_social__contains=form.cleaned_data['buscar']))
                                                )
    else:    
        
        #factcompra_list = model.objects.all()
        factcompra_list = model.objects.filter(Q(tipo_doc__codigo='FC') )
        form = GenericSearchForm()

    factcompra_list=factcompra_list.annotate(sub_total=( Sum( F('documentodet__total') ) ) )
    factcompra_list=factcompra_list.annotate(iva=( Sum( F('documentodet__total') ) ) )

    paginator = Paginator(factcompra_list, 11) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        factcompras = paginator.page(page)
    except PageNotAnInteger:
        factcompras = paginator.page(1)
    except EmptyPage:
        factcompras = paginator.page(paginator.num_pages)
    
    return render_to_response(template_name, 
            {'form': form, 'factcompras': factcompras,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_documento', login_url='/login/')
def add_factcompra(request):
    template_name="factcompra.html"
    if request.method == 'POST':
        form = ManageFactCompras(request.POST,request.FILES)        
        if form.is_valid():
            fact_nueva = form.save(commit=False)            
            fact_nueva.usuario=request.user
            tipodoc = TipoDoc.objects.get( Q(codigo='FC'))
            print "asdasdadas",tipodoc.nombre
            #fact_nueva.tipo_doc=tipodoc.id
            fact_nueva.tipo_doc=tipodoc
            fact_nueva.save()
            #messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/detallefc/%s' % fact_nueva.pk)
    else:
        form = ManageFactCompras()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permission_required('ventas.add_documento', login_url='/login/')
def detallefc(request,pk):
    factcompra = get_object_or_404(Documento, pk=pk)        
    #form = ManageDocumentos(instance=documento)    
    form_class = GenericSearchForm
    model = DocumentoDet        
    if request.method == 'POST':
        form = ManageLineas(request.POST,request.FILES)                
        if form.is_valid():            
            nueva = form.save(commit=False)            
            nueva.documento=factcompra
            nueva.save()
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/detallefc/%s' % pk)
    else:
        form = ManageLineas(instance=factcompra)        
        lineas = model.objects.filter(documento=pk)        

    return render_to_response('detallefc.html',
        {'form': form,'id': pk,'factcompra':factcompra,'lineas':lineas},
                              context_instance=RequestContext(request))

@permission_required('ventas.delete_documento', login_url='/login/')
def delete_detallefc(request,pk,fact):
    #linea a borrar
    linea = get_object_or_404(DocumentoDet, pk=pk)            
    factcompra = get_object_or_404(Documento, pk=fact)        
    #borro linea
    linea.delete()

    messages.add_message(request, messages.SUCCESS, ('linea eliminada'))
    return HttpResponseRedirect('/detallefc/%s' % fact)

@login_required(login_url='/login/')
@permission_required('ventas.change_documento', login_url='/login/')
def edit_factcompra(request,pk):
    factcompra = get_object_or_404(Documento, pk=pk)        
    form = ManageFactCompras(instance=factcompra)    
    #print form.nombres
    if request.POST:
        form = ManageFactCompras(request.POST,request.FILES,instance=factcompra)    
        if form.is_valid():
            form.save()            

            messages.add_message(request, messages.SUCCESS, ('factcompra editada.'))            
            return HttpResponseRedirect('/detallefc/%s' % pk) 

    return render_to_response('factcompra.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_documento', login_url='/login/')
def delete_factcompra(request,pk):
	factcompra = get_object_or_404(Documento, pk=pk)        
	form = ManageFactCompras(instance=factcompra)        
	if request.POST:
		form = ManageFactCompras(request.POST,request.FILES,instance=factcompra)    
		if form.is_valid():
			factcompra.delete()            
			messages.add_message(request, messages.SUCCESS, ('FactCompra eliminada'))
			return HttpResponseRedirect('/factcompra/')        

	return render_to_response('factcompra.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))

