from django.db import transaction
from ventas.models import *
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg,Sum,Count,F,FloatField,Q
from django.db import connection
from decimal import *


@transaction.atomic
def get_new_correlativo(tipo):
    #
    correlativo = TipoDoc.objects.select_for_update().get(codigo=tipo)    
    correlativo.correlativo+=1        
    correlativo.save()
    nuevo=correlativo.correlativo    
    return nuevo

def is_in_articulo_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Articulo').count() == 1        
    return False   

def is_in_categoria_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Categoria').count() == 1        
    return False   

def is_in_cliente_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Cliente').count() == 1        
    return False   

def is_in_banco_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Banco').count() == 1        
    return False   

def is_in_cuentabanco_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='CuentaBanco').count() == 1        
    return False   

def is_in_empresa_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Empresa').count() == 1        
    return False       

def is_in_factura_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Factura').count() == 1        
    return False   

def is_in_factcompra_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='FactCompra').count() == 1
    return False   

def is_in_formapago_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='FormaPago').count() == 1        
    return False   

def is_in_inventario_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Inventario').count() == 1        
    return False   


def is_in_caja_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Caja').count() == 1
    return False   

def is_in_postext_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Postext').count() == 1
    return False   

def is_in_proveedor_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='Proveedor').count() == 1
    return False   

def is_in_tipocaja_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='TipoCaja').count() == 1
    return False   

def is_in_tipodoc_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='TipoDoc').count() == 1
    return False   

def is_in_tipoimpuesto_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='TipoImpuesto').count() == 1
    return False   

def is_in_rptventa_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='RptVenta').count() == 1
    return False   

def is_in_rptcompra_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='RptCompra').count() == 1
    return False   

def is_in_rptinventario_group(user):
    if user:
        #print user,user.groups.filter(name='Postext').count() == 1
        return user.groups.filter(name='RptInventario').count() == 1
    return False       


def get_data_detalle(fact):
    model = DocumentoDet        
    lineas = model.objects.filter(documento=fact)
    #lineas=lineas.annotate(sub_impuesto=( F('importe') * F('cantidad') )*( F('impuesto')/100 ) )
    #lineas=lineas.annotate(sub_descuento=( F('importe') * F('cantidad') )*( F('descuento')/100 ) )
    data={}
        
    excento=0
    imponible=0
    tot_impuesto=0    
    tot_descuento=0
    sujeto_dcto=0
    subtotal=0
    total_general=0
    for lin in lineas:        
        subtotal+=lin.total        
        
        #con impuesto y con descuento
        if lin.impuesto>0 and  lin.descuento>0:                        
            imponible+=lin.total * (1 - (lin.descuento/100) )
            tot_impuesto+=lin.total * (1 - (lin.descuento/100) ) * (lin.impuesto/100)
            tot_descuento+=lin.total * (lin.descuento/100)
            sujeto_dcto+=lin.total
            
        #con impuesto y sin descuento
        elif lin.impuesto>0 and  lin.descuento==0:                        
            imponible+=lin.total
            tot_impuesto+=lin.total *  (lin.impuesto/100)
            
        #sin impuesto y con descuento
        elif lin.impuesto==0 and  lin.descuento>0:                        
            excento+=lin.total
            tot_descuento+=lin.total * (lin.descuento/100)
            sujeto_dcto+=excento            
        
        #sin impuesto y sin descuento
        elif lin.impuesto==0 and  lin.descuento==0:                        
            excento+=lin.total            
    
    if imponible > 0:
        total_general=excento+imponible+tot_impuesto
    else:
        total_general=excento+imponible+tot_impuesto-tot_descuento

#    print subtotal,imponible,excento,tot_impuesto,tot_descuento,sujeto_dcto
    #totales=lineas.aggregate(Sum('total'), Avg('impuesto') )
    
    if excento > 0:
        data['excento']=excento
    if sujeto_dcto > 0:
        data['sujeto_dcto']=sujeto_dcto
        data['tot_descuento']=tot_descuento
        data['pct_descuento']=(tot_descuento/sujeto_dcto)*100
    if imponible > 0:
        data['imponible']=imponible
        data['pct_impuesto']=lin.impuesto
        data['tot_impuesto']=tot_impuesto

    data['subtotal']=subtotal
    data['total_general']=total_general
    
    data_json=json.dumps(data, cls=DjangoJSONEncoder)

    return data,data_json    


def get_cobros(ini,fin,usr=None,opc=None):
    kwargs = {}
    kwargs["fecha_hora__gte"]=ini
    kwargs["fecha_hora__lte"]=fin        

    if usr:            
        kwargs["usuario"]=User( pk = usr)
            
    if opc == "total":        #obtengo el total cobrado
        q = Cobros.objects.filter(**kwargs )\
            .aggregate(total=Sum('monto'))
    elif opc == "efectivo":
        kwargs["forma_pago__efectivo"]=True         
        q = Cobros.objects.filter(**kwargs).aggregate(total=Sum('monto'))
    else:                       #cobrado por forma pago
        q = Cobros.objects.filter(**kwargs)\
            .values("forma_pago__nombre").annotate(total=Sum('monto')).order_by("forma_pago__nombre")        

    return q

def get_ventas(ini,fin,usr=None,opc=None):    
    
    kwargs = {}
    kwargs["fecha_hora__gte"]=ini
    kwargs["fecha_hora__lte"]=fin    
    kwargs["documento__fecha_hora__gte"]=ini
    kwargs["documento__fecha_hora__lte"]=fin    

    if usr:    
        usuario=User( pk = usr)
        kwargs["usuario"]=usuario
        kwargs["documento__usuario"] = usuario

    
    if opc == "total":        #obtengo el total cobrado
        kwargs.pop("documento__usuario",None)
        kwargs.pop("documento__fecha_hora__gte",None)
        kwargs.pop("documento__fecha_hora__lte",None)
        q = Documento.objects.filter(**kwargs)\
            .aggregate(total=Sum('total_general'))                
    
    elif opc == "categoria":        #obtengo el total cobrado
        kwargs.pop("usuario",None)
        kwargs.pop("fecha_hora__gte",None)
        kwargs.pop("fecha_hora__lte",None)

        q = DocumentoDet.objects.filter(**kwargs)\
            .values("item__categoria__nombre").annotate(total=Sum(F('importe')*F('cantidad')*(1+F('impuesto')/100 ) , output_field=FloatField() ) ).order_by('item__categoria__nombre')
    
    else:                      
        kwargs.pop("usuario",None)
        kwargs.pop("fecha_hora__gte",None)
        kwargs.pop("fecha_hora__lte",None)
        q = DocumentoDet.objects.filter(**kwargs)\
            .values("item__descripcion").annotate(total=Sum(F('importe')*F('cantidad')*(1+F('impuesto')/100 ) , output_field=FloatField() ) ).order_by('item__descripcion')
        
    return q


def facturas_sin_cobrar(ini,fin,usr=None):
    kwargs = {}

    kwargs["fecha_hora__gte"]=ini
    kwargs["fecha_hora__lte"]=fin    

    if usr:            
        kwargs["usuario"]=User( pk = usr)
    
    q = Documento.objects.select_related('cobro').filter(**kwargs)\
            .values("correlativo").annotate(Facturado=Sum('total_general')).annotate(Cobrado=Sum('cobros__monto')).order_by()    
     
    return q                

def get_mov_caja(ini,fin,usr=None,opc=None,tipo=None):
    #opc= total, detalles
    #tipo=1 manual, 0 automaticos, None todos
    #para crear el query dinamicamente segun vengas los parametros
    kwargs = {}
    
    if tipo:
        if tipo == "manual":
            kwargs["manual"]=1
        else:
            kwargs["manual"]=0 
        
    if usr:            
        kwargs["turno__usuario"]=User( pk = usr)

    kwargs["fecha_hora__gte"]=ini
    kwargs["fecha_hora__lte"]=fin

    if opc:
        if opc=='total':
            q = TurnoDet.objects.filter(**kwargs)\
                .aggregate(total_ingreso=Sum('ingreso'),total_egreso=Sum('egreso'))
    else:
        q = TurnoDet.objects.filter(**kwargs)\
            .values('fecha_hora','descripcion','ingreso','egreso').order_by('fecha_hora')
    # print q
    # for i in  connection.queries:
    #     print i["sql"]
    return q                    

def get_caja_turnos(caja_abierta):    
    q = Turno.objects.filter(caja=caja_abierta)
    return q

def get_data_cierre(inicio,fin,usuario=None,turno_abierto=None,caja_abierta=None):
    data={}
    data["cobros_total"] = get_cobros(inicio,fin,usuario,"total") #cobros totales
    data["cobros_detalle"] = get_cobros(inicio,fin,usuario) #cobros por forma de pago                        
    data["ventas_detalle"] = get_ventas(inicio,fin,usuario) #ventas por producto
    data["ventas_categoria"] = get_ventas(inicio,fin,usuario,"categoria") #ventas categoria                
    data["total_efectivo"] = get_cobros(inicio,fin,usuario,"efectivo") #cobros en efectivo                
    if turno_abierto:
        data["saldo_inicial"] = turno_abierto.saldo_apertura                
    if caja_abierta:
        data["saldo_inicial"] = caja_abierta.saldo_apertura
        data["turnos"] = get_caja_turnos(caja_abierta)
    #tot=0
    #for i in data["ventas_detalle"] :
    #    tot+=i["total"]
    #data["ventas_total"] = tot
    data["ventas_total"] = get_ventas(inicio,fin,usuario,"total")
    
    data["total_movimientos_manuales"] = get_mov_caja(inicio,fin,usuario,"total","manual")
    data["detalle_movimientos_manuales"] = get_mov_caja(inicio,fin,usuario,None,"manual")
    #print data["entradas_manuales"]


    if  data["ventas_total"]["total"] and data["cobros_total"]["total"]:                
        data["falta_sobra"]=data["cobros_total"]["total"]-data["ventas_total"]["total"]                      
    else:
        data["falta_sobra"]=Decimal(0.00)
        data["ventas_total"]["total"]=Decimal(0.00)
        data["cobros_total"]["total"]=Decimal(0.00)



    if len(data["detalle_movimientos_manuales"]) == 0:
        data["total_movimientos_manuales"]={'total_ingreso':Decimal(0.00),'total_egreso':Decimal(0.00)}
        

    if turno_abierto:
        try:
            data["saldo_final"] = turno_abierto.saldo_apertura + data["falta_sobra"] + \
            data["ventas_total"]["total"] + \
            data["total_movimientos_manuales"]["total_ingreso"] - \
            data["total_movimientos_manuales"]["total_egreso"] 
        except:
            data["saldo_final"] = Decimal(0.00)
        # data["saldo_final"] = turno_abierto.saldo_apertura + data["falta_sobra"] + \
        # data["ventas_total"]["total"] + \
        # data["total_movimientos_manuales"]["total_ingreso"] -\
        # data["total_movimientos_manuales"]["total_egreso"]
        #print data["saldo_final"]

    if caja_abierta:
        try:
            data["saldo_final"] = caja_abierta.saldo_apertura + data["falta_sobra"] + \
            data["ventas_total"]["total"]  + \
            data["total_movimientos_manuales"]["total_ingreso"]  - \
            data["total_movimientos_manuales"]["total_egreso"]  
        except:
            data["saldo_final"] = Decimal(0.00)

    #else:
    #    data=None

    
    return data
    #for i in  connection.queries:
    #    print i["sql"]
    #print data["ventas_detalle"]    