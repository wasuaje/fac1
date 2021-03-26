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
@user_passes_test(is_in_inventario_group, login_url='/login/')
def index_inventario(request):
    form_class = DateSearchForm
    model = Inventario
    template_name = 'index_inventario.html'
    inventarios=None

    if request.method == 'POST': 
        form = form_class(request.POST or None)
        if form.is_valid():
            #inventario_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            #inventario_list = model.objects.filter( kwargs.pop("fecha_hora__lte",None))            
            fecha=form.cleaned_data['fecha']            
            return HttpResponseRedirect( reverse('search_inv' , args=(fecha.year,fecha.month,fecha.day) ) )            
    else:    
        kwargs={}        
        inventario_list = kwargs["tipo__in"]=["E","S"]
        inventario_list = Inventario.objects.filter(**kwargs)\
                .values("articulo__descripcion","fecha_hora","cantidad","articulo__importe").annotate( \
                valor= Sum(F('cantidad') * F('articulo__importe') , output_field=FloatField() ) ) \
                .order_by('fecha_hora')        
        form = DateSearchForm()    

        paginator = Paginator(inventario_list, 11) # Show 10 contacts per page

        page = request.GET.get('page')
        try:
            inventarios = paginator.page(page)
        except PageNotAnInteger:
            inventarios = paginator.page(1)
        except EmptyPage:
            inventarios = paginator.page(paginator.num_pages)
    
    return render_to_response(template_name, 
            {'form': form, 'inventarios': inventarios,}, 
            context_instance=RequestContext(request))

@login_required(login_url='/login/')
@user_passes_test(is_in_inventario_group, login_url='/login/')
def search_inventario(request,year,month,day):
    form_class = DateSearchForm
    template_name = 'index_inventario.html'
    if request.method == 'POST': 
        form = form_class(request.POST or None)
        if form.is_valid():
            #inventario_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            #inventario_list = model.objects.filter( kwargs.pop("fecha_hora__lte",None))            
            fecha=form.cleaned_data['fecha']
            if fecha:
                return HttpResponseRedirect( reverse('search_inv' , args=(fecha.year,fecha.month,fecha.day) ) )                   
            else:
                return HttpResponseRedirect( '/inventario/' )
    else:
        kwargs={}
        kwargs["fecha"]=datetime(int(year),int(month),int(day))
        kwargs["tipo__in"]=["E","S"]
        inventario_list = Inventario.objects.filter(**kwargs)\
                    .values("articulo__descripcion","fecha_hora","cantidad","articulo__importe").annotate( \
                        valor= Sum(F('cantidad') * F('articulo__importe') , output_field=FloatField() ) ) \
                    .order_by('fecha_hora')  

        paginator = Paginator(inventario_list, 11) # Show 10 contacts per page

        page = request.GET.get('page')
        
        try:
            inventarios = paginator.page(page)
        except PageNotAnInteger:
            inventarios = paginator.page(1)
        except EmptyPage:
            inventarios = paginator.page(paginator.num_pages)
        
        #args.update(csrf(request))
        form = DateSearchForm(initial={'fecha':kwargs["fecha"]})    

    return render_to_response(template_name, 
            {'form': form, 'inventarios': inventarios,}, 
            context_instance=RequestContext(request))                

@login_required(login_url='/login/')
@permission_required('ventas.add_inventario', login_url='/login/')
def add_inventario(request):
    template_name="inventario.html"
    if request.method == 'POST':
        form = ManageInventarios(request.POST,request.FILES)        
        if form.is_valid():
            inv_nueva = form.save(commit=False)
            if inv_nueva.tipo=="S":
                inv_nueva.cantidad=inv_nueva.cantidad*-1
            inv_nueva.usuario=request.user
            inv_nueva.articulo=Articulo(pk=request.POST["articulo"])
            inv_nueva.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/inventario/')
    else:
        form = ManageInventarios()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))
