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
@user_passes_test(is_in_factura_group, login_url='/login/')
def index_factura(request):
    form_class = GenericSearchForm
    model = Documento
    template_name = 'index_factura.html'

    if request.method == 'POST': 
        form = form_class(request.POST or None)
        if form.is_valid():
            #factura_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            factura_list = model.objects.filter(Q(tipo_doc__codigo='FV') & \
                                               (Q(correlativo__contains=form.cleaned_data['buscar']) |\
                                                Q(cliente__razon_social__contains=form.cleaned_data['buscar'])) 
                                                )
    else:    
        #factura_list = model.objects.all()
        factura_list = model.objects.filter(Q(tipo_doc__codigo='FV') )        
        form = GenericSearchForm()

    factura_list=factura_list.annotate(sub_total=( Sum( F('documentodet__total') ) ) )
    factura_list=factura_list.annotate(iva=( Sum( F('documentodet__total') ) ) )

    paginator = Paginator(factura_list, 11) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        facturas = paginator.page(page)
    except PageNotAnInteger:
        facturas = paginator.page(1)
    except EmptyPage:
        facturas = paginator.page(paginator.num_pages)
    
    return render_to_response(template_name, 
            {'form': form, 'facturas': facturas,}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_documento', login_url='/login/')
def add_factura(request):
    template_name="factura.html"
    if request.method == 'POST':
        form = ManageFacturas(request.POST,request.FILES)        
        if form.is_valid():
            fact_nueva = form.save(commit=False)
            fact_nueva.correlativo=get_new_correlativo('FV')
            fact_nueva.usuario=request.user
            tipodoc = TipoDoc(codigo='FV')
            fact_nueva.tipo_doc=tipodoc.id
            fact_nueva.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/detalle/%s' % fact_nueva.pk)
    else:
        form = ManageFacturas()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
@permission_required('ventas.add_documento', login_url='/login/')
def detalle(request,pk):
    factura = get_object_or_404(Documento, pk=pk)        
    #form = ManageDocumentos(instance=documento)    
    form_class = GenericSearchForm
    model = DocumentoDet        
    if request.method == 'POST':
        form = ManageLineas(request.POST,request.FILES)                
        if form.is_valid():            
            nueva = form.save(commit=False)            
            nueva.documento=factura
            a=nueva.save()
            data,data_json=get_data_detalle(pk)

            #actualizo la data de factura
            for dt in data:                                
                setattr(factura, dt, data[dt])
            factura.save()                        

            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/detalle/%s' % pk)
    else:
        form = ManageLineas(instance=factura)        
        lineas = model.objects.filter(documento=pk)
        data,data_json=get_data_detalle(pk)

    return render_to_response('detalle.html',
        {'form': form,'id': pk,'factura':factura,'lineas':lineas,'data':data,'data_json':SafeString(data_json)},
                              context_instance=RequestContext(request))

@permission_required('ventas.delete_documento', login_url='/login/')
def delete_detalle(request,pk,fact):
    #linea a borrar
    linea = get_object_or_404(DocumentoDet, pk=pk)            
    factura = get_object_or_404(Documento, pk=fact)        
    #borro linea
    linea.delete()
    
    #nuevas lineas de la factura para recalcular
    data,data_json=get_data_detalle(fact)
    
    #actualizo la data de factura con la nueva info de lineas    
    for dt in data:                                
        setattr(factura, dt, data[dt])
    factura.save()

    messages.add_message(request, messages.SUCCESS, ('linea eliminada'))
    return HttpResponseRedirect('/detalle/%s' % fact)

@login_required(login_url='/login/')
@permission_required('ventas.change_documento', login_url='/login/')
def edit_factura(request,pk):
    factura = get_object_or_404(Documento, pk=pk)        
    form = ManageFacturas(instance=factura)    
    #print form.nombres
    if request.POST:
        form = ManageFacturas(request.POST,request.FILES,instance=factura)    
        if form.is_valid():
            form.save()            

            messages.add_message(request, messages.SUCCESS, ('factura editada.'))            
            return HttpResponseRedirect('/detalle/%s' % pk) 

    return render_to_response('factura.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_documento', login_url='/login/')
def delete_factura(request,pk):
	factura = get_object_or_404(Documento, pk=pk)        
	form = ManageFacturas(instance=factura)        
	if request.POST:
		form = ManageFacturas(request.POST,request.FILES,instance=factura)    
		if form.is_valid():
			factura.delete()            
			messages.add_message(request, messages.SUCCESS, ('Factura eliminada'))
			return HttpResponseRedirect('/factura/')        

	return render_to_response('factura.html',
                              {'form': form,
                               'id': pk},
                              context_instance=RequestContext(request))

