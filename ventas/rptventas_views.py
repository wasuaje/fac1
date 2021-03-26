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
@user_passes_test(is_in_rptventa_group, login_url='/login/')
def ventas(request):
    data=None    
    data2=None
    model=Documento
    if request.method == 'POST':         
        form =  RptVentasForm(request.POST,request.FILES)        
        if form.is_valid():
            #factura_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            reporte=request.POST['seleccione_reporte']
            
            #Ventas en bolivares
            if reporte == "ventasbs":
                template_name = 'rptventasbs.html'        
                data = model.objects.filter(Q(fecha__gte=form.cleaned_data['fecha_desde']) & \
                                        Q(fecha__lte=form.cleaned_data['fecha_hasta']) & 
                                        Q(tipo_doc__codigo='FV') 
                                        ).order_by('correlativo')            
                data2={}
                data2["fecha_desde"]=request.POST['fecha_desde']          
                data2["fecha_hasta"]=request.POST['fecha_hasta']     
                data2["imponible"]=Decimal(0.00)
                data2["iva"]=Decimal(0.00)
                data2["total"]=Decimal(0.00)
                if data:
                    for rec in data:
                        data2["imponible"]+=rec.imponible
                        data2["iva"]+=rec.tot_impuesto
                        data2["total"]+=rec.total_general
            
            #Ventas por producto
            elif reporte == "ventasprod":
                template_name = 'rptventasprod.html'                        
                kwargs={}
                kwargs["documento__fecha__gte"]=form.cleaned_data['fecha_desde']
                kwargs["documento__fecha__lte"]=form.cleaned_data['fecha_hasta']
                kwargs["documento__tipo_doc__codigo"]="FV"

                data = DocumentoDet.objects.filter(**kwargs)\
                    .values("item__descripcion")\
                    .annotate(total=Sum(F('importe')*F('cantidad')*(1+F('impuesto')/100 ) , \
                                         output_field=FloatField() ), \
                              cantidad=Sum(F('cantidad'))
                             ) \
                    .order_by('-cantidad')
                data2={}
                data2["fecha_desde"]=request.POST['fecha_desde']          
                data2["fecha_hasta"]=request.POST['fecha_hasta']     
                data2["total_cantidad"]=Decimal(0.00)
                data2["total_total"]=Decimal(0.00)
                
                if data:
                    for rec in data:                        
                        data2["total_cantidad"]+=rec["cantidad"]
                        data2["total_total"]+=Decimal(rec["total"])
            
            #Ventas por categoria
            elif reporte == "ventascat":
                template_name = 'rptventascat.html'                        
                kwargs={}
                kwargs["documento__fecha__gte"]=form.cleaned_data['fecha_desde']
                kwargs["documento__fecha__lte"]=form.cleaned_data['fecha_hasta']
                kwargs["documento__tipo_doc__codigo"]="FV"
                
                data = DocumentoDet.objects.filter(**kwargs)\
                    .values("item__categoria__nombre")\
                    .annotate(total=Sum(F('importe')*F('cantidad')*(1+F('impuesto')/100 ) , \
                                         output_field=FloatField() ), \
                              cantidad=Sum(F('cantidad'))
                             ) \
                    .order_by('-cantidad')
                data2={}
                data2["fecha_desde"]=request.POST['fecha_desde']          
                data2["fecha_hasta"]=request.POST['fecha_hasta']     
                data2["total_cantidad"]=Decimal(0.00)
                data2["total_total"]=Decimal(0.00)
                
                if data:
                    for rec in data:                
                        data2["total_cantidad"]+=rec["cantidad"]
                        data2["total_total"]+=Decimal(rec["total"])

        else:
            template_name = 'ventas_form.html'
            form =  RptVentasForm(request.POST,request.FILES)

    else:    
        template_name = 'ventas_form.html'
        form =  RptVentasForm()

    
    return render_to_response(template_name, 
            {'form': form, 'data': data,'data2':data2}, 
            context_instance=RequestContext(request))

