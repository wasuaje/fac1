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
@user_passes_test(is_in_rptinventario_group, login_url='/login/')
def rptinventarios(request):
    data=None    
    data2=None
    model=Inventario
    if request.method == 'POST':         
        form =  RptInventariosForm(request.POST,request.FILES)        
        if form.is_valid():            
            reporte=request.POST['seleccione_reporte']            
            if reporte == "existencias":
                template_name = 'rptexistencias.html'                                                        
                data = Inventario.objects.filter()\
                        .values("articulo__descripcion").annotate(total=Sum( F('cantidad') )\
                                                       ).order_by('articulo__descripcion')
                                    
                data2={}                
                data2["fecha_desde"]=datetime.now().strftime('%d - %b - %Y')
                data2["total"]=Decimal(0.00)                
                if data:
                    for rec in data:
                        data2["total"]+=rec["total"]
            
            #Ventas por producto
            elif reporte == "valorizado":
                template_name = 'rptexistenciasvalor.html'                                        

                data = Inventario.objects.filter()\
                    .values("articulo__descripcion")\
                    .annotate(cantidad=Sum( F('cantidad') ), \
                            total=Sum(F('articulo__importe')*F('cantidad')*(1+F('articulo__tipoimpuesto__valor')/100 ) , \
                                         output_field=FloatField() )
                             ).order_by('articulo__descripcion')

                data2={}                
                data2["fecha_desde"]=datetime.now().strftime('%d - %b - %Y')
                data2["total_cantidad"]=Decimal(0.00)
                data2["total_total"]=Decimal(0.00)
                
                if data:
                    for rec in data:                        
                        data2["total_cantidad"]+=rec["cantidad"]
                        data2["total_total"]+=Decimal(rec["total"])
            
            #Ventas por categoria
            elif reporte == "tomafisica":                
                template_name = 'rpttomafisica.html'                                                           
                data = Inventario.objects.filter()\
                        .values("articulo__descripcion").annotate(total=Sum( F('cantidad') )\
                                                       ).order_by('articulo__descripcion')
                                    
                data2={}                
                data2["fecha_desde"]=datetime.now().strftime('%d - %b - %Y')
                data2["total"]=Decimal(0.00)                
                if data:
                    for rec in data:
                        data2["total"]+=rec["total"]

        else:
            template_name = 'inventarios_form.html'
            form =  RptInventariosForm(request.POST,request.FILES)

    else:    
        template_name = 'inventarios_form.html'
        form =  RptInventariosForm()

    
    return render_to_response(template_name, 
            {'form': form, 'data': data,'data2':data2}, 
            context_instance=RequestContext(request))


