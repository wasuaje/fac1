from django.contrib.auth.decorators import login_required, user_passes_test
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
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
import datetime



@login_required(login_url='/login/')
@user_passes_test(is_in_postext_group, login_url='/login/')
def postext(request):    
    error=None
    formaspago=FormaPago.objects.all()
    bancos=Banco.objects.all()

    if  "caja" not in request.session.keys() or  "turno" not in request.session.keys():
        error="No hay caja o turno operativo para comenzar a facturar"    

    return render_to_response('postext.html', {"formaspago":formaspago,"banco":bancos,"error":error},
                                   context_instance=RequestContext(request))
    
        
def add_postext(request):
    data={}    
    if request.method == 'POST':
        cantidad=int(request.POST['cantidad']) ;
        id_articulo=request.POST['id_articulo'] ;
        id_cliente=request.POST['id_cliente'] ;
        id_factura=request.POST['id_factura'] ;

        #algunas instancias que necesito ya seteadas
        cliente = Cliente.objects.get( pk=id_cliente )                 
        tipodoc = TipoDoc.objects.get( codigo='FV' )
        articulo = Articulo.objects.get( pk=id_articulo )

        #VALIDAR QUE ES FACTURA NUEVA O VIENE YA UN ID FACTURA
        if id_factura != "":
            fact_nueva=Documento.objects.get( pk=id_factura )
        else:
            #agrego nueva factura            
            fact_nueva=Documento(correlativo=get_new_correlativo('FV'),cliente=cliente,tipo_doc=tipodoc,usuario=request.user)
            fact_nueva.save()        
        
        #agrego la linea que viene
        linea=DocumentoDet(cantidad=cantidad,item=articulo,documento=fact_nueva, \
                            importe=articulo.importe,total=cantidad*articulo.importe, \
                            impuesto=articulo.tipoimpuesto.valor,descuento=articulo.descuento
                            )
        linea.save()

        #actualizo los totales de factura segun la lineas que tenga
        total_fact,data_json=get_data_detalle( fact_nueva.id )
        
        #actualizo los totales de lafactura
        
        for dt in total_fact:                                
            setattr(fact_nueva, dt, total_fact[dt])
        fact_nueva.save()                        
        
        #genero la data a devolve via json
        #obtengo lo cobrado ya por la factura a efectos de ir calculando en el visor

        cobros = Cobros.objects.filter( documento=fact_nueva.id )
        total_cobro=0
        for ln in cobros:            
            total_cobro+=ln.monto  
        

        #obtengo las lineas        
        lineas = DocumentoDet.objects.filter(documento=fact_nueva.id)
    

        llist=[]
        for ln in lineas:
            llist.append({"id":ln.id, "cantidad":ln.cantidad,"importe":ln.importe,"total":ln.total,"articulo":ln.item.descripcion})
        
        data["lineas"]=llist
        data["totales"] = total_fact

        facfecha=datetime.datetime.strftime(fact_nueva.fecha,'%d - %b - %Y')
        data["factura"] = {"correlativo":fact_nueva.correlativo,"id":fact_nueva.id,"fecha":facfecha}

        data["cobros"]={"total":total_cobro}

    return JsonResponse(data)      

def del_postext(request):
    data={}    
    if request.method == 'POST':
        lineaid=request.POST['lineaid'] 
        linea=DocumentoDet.objects.get( pk=lineaid )
        documento=linea.documento
        articulo=linea.item
        cantidad=linea.cantidad
        linea.delete()

        total_fact,data_json=get_data_detalle( documento.id )
        
        #actualizo los totales de lafactura
        
        for dt in total_fact:                                
            setattr(documento, dt, total_fact[dt])
        documento.save()                                

        #genero la data a devolve via json
        #obtengo los cobros
        cobros = Cobros.objects.filter( documento=documento.id )
        total_cobro=0
        for ln in cobros:            
            total_cobro+=ln.monto 

        #obtengo las lineas        
        lineas = DocumentoDet.objects.filter(documento=documento.id)
        
        llist=[]
        for ln in lineas:
            llist.append({"id":ln.id, "cantidad":ln.cantidad,"importe":ln.importe,"total":ln.total,"articulo":ln.item.descripcion})
        
        data["lineas"]=llist
        data["totales"] = total_fact

        facfecha=datetime.datetime.strftime(documento.fecha,'%d - %b - %Y')
        data["factura"] = {"correlativo":documento.correlativo,"id":documento.id,"fecha":facfecha}
        data["cobros"]={"total":total_cobro}

    return JsonResponse(data)      

def add_cobro(request):
    data={}    
    if request.method == 'POST':
        id_formapago=request.POST["id_formapago"]
        id_banco=request.POST["id_banco"]
        monto=request.POST["monto"]
        id_factura=request.POST["id_factura"]
        aprobacion=request.POST["aprobacion"]

        #algunas instancias que necesito ya seteadas
        formapago = FormaPago.objects.get( pk=id_formapago )                         
        factura = Documento.objects.get( pk=id_factura )        

        descripcion= "Cobro de Factura %s" % factura.correlativo        

        #agrego la linea que viene
        if id_banco == "":
            cobro=Cobros(monto=monto,forma_pago=formapago,documento=factura, \
                            aprobacion=aprobacion,descripcion=descripcion,usuario=request.user
                             )
        else:
            banco = Banco.objects.get( pk=id_banco )
            cobro=Cobros(monto=monto,forma_pago=formapago,documento=factura, \
                            banco=banco,aprobacion=aprobacion,descripcion=descripcion,usuario=request.user
                            )
        cobro.save()
        
        #obtengo las lineas        
        cobros = Cobros.objects.filter( documento=factura.id )
        
        llist=[]
        total_cobro=0
        for ln in cobros:
            llist.append({"id":ln.id, "monto":ln.monto,"aprobacion":ln.aprobacion, \
                        "forma_pago":ln.forma_pago.nombre})
            total_cobro+=ln.monto        

        
        data["lineas"]=llist
        data["totales"] = {"total_cobro":total_cobro,"total_fact":factura.total_general,"pendiente":factura.total_general-total_cobro}


    return JsonResponse(data)         

def del_cobro(request):
    data={}    
    if request.method == 'POST':
        cobroid=request.POST['cobroid'] ;
        cobro=Cobros.objects.get( pk=cobroid )
        documento=cobro.documento        
        cobro.delete()

        #traigo la data de factura
        total_fact,data_json=get_data_detalle( documento.id )
                

        #genero la data a devolve via json
        #obtengo las lineas        
        cobros = Cobros.objects.filter( documento=documento.id )
        
        llist=[]
        total_cobro=0
        for ln in cobros:
            llist.append({"id":ln.id, "monto":ln.monto,"aprobacion":ln.aprobacion, \
                        "forma_pago":ln.forma_pago.nombre})
            total_cobro+=ln.monto   
        
        data["lineas"]=llist
        
        data["totales"] = total_fact

        data["totales"] = {"total_cobro":total_cobro,"total_fact":documento.total_general,"pendiente":documento.total_general-total_cobro}

    return JsonResponse(data)        