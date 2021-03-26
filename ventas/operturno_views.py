from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect    
from django.db import IntegrityError
from comunes import *
from django.db import connection
from django.http import HttpResponse
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage
from comunes import *


@login_required(login_url='/login/')
@user_passes_test(is_in_postext_group, login_url='/login/')
def openturno(request):
    template_name="operturno.html"       
    error=None
    success=None    
    if  "caja" in request.session.keys():          
        if  "turno" not in request.session.keys():          
            if request.method == 'POST':
                form = OpenTurno(request.POST,request.FILES)
                if form.is_valid():
                    caja_abierta = Caja.objects.get( pk=request.session["caja"]["id"] ) 
                    nuevo_turno=form.save(commit=False)
                    nuevo_turno.usuario=request.user   
                    nuevo_turno.caja=caja_abierta 
                    #try:       
                    nuevo_turno.save()
                    #except IntegrityError :
                    #    error="Ya la combinacion caja/turno/usuario fue cerrada"
                    #else:
                    request.session['turno'] = {'id':nuevo_turno.id,'usuario':nuevo_turno.usuario.username,
                                        'hora_ini':nuevo_turno.fecha_hora_ini.strftime('%Y-%m-%d %H:%M:%S')
                                            }                
                        # If the save was successful, redirect to another page                            
                    success="Turno abierto con exito"
                    return render_to_response(template_name,
                                  {'form': form,'error':error,'success':success},
                                  context_instance=RequestContext(request))
                else:
                    error="Se encontraron errores, corrija y continue, de lo contrario: "
                    return render_to_response(template_name,
                                  {'form': form,'error':error,'success':success},
                                  context_instance=RequestContext(request))

            else:
                ultimo_turno=Turno.objects.filter().order_by('-id')[0]                        
                form = OpenTurno(initial={'saldo_apertura': ultimo_turno.saldo_cierre})                                        
        else:
            form = None 
            error="Ya hay un turno abierto para este usuario"
            return render_to_response(template_name,
                                  {'form': form,'error':error,'success':success},
                                  context_instance=RequestContext(request))
    else:
        form = None        
        error ="No hay una caja abierta, verifique." 
        #tal vez una verificacion contra BD si de verdad la caja existe para evitar que se 
        #borre el registro por bbdd y quede la sesion abierta de la caja        
    return render_to_response(template_name,
                              {'form': form,'error':error},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@user_passes_test(is_in_postext_group, login_url='/login/')
def closeturno(request):    
    template_name="closeturno.html"    
    error=None
    success=None    
    turno_abierto=None     
    data=None  
    #print request.session["turno"]   
    #del request.session['turno']     
    #request.session.pop('turno',None)
    #break;
    #request.session["turno"]["id"]=1
        #request.session.pop('caja',None)
        #return HttpResponseRedirect('/opencaja/')            
    if  "caja" in request.session.keys():
        if "turno" in request.session.keys():               
            turno_abierto = Turno.objects.get( pk=request.session["turno"]["id"] )             
            inicio = turno_abierto.fecha_hora_ini
            fin =datetime.now()
            usuario = request.user.id
            template_name="closeturno.html"    
            if request.method == 'POST':        #puede ser un form.form personalizado !!!    
                form = CloseTurnoDet(request.POST,request.FILES)                
                if form.is_valid():
                    template_name="closeturno_no_menu.html"    
                    data=get_data_cierre(inicio,fin,usuario,turno_abierto) 
                    #si hubo ventas
                    if data:
                        t_ventas=data["ventas_total"]["total"]                                   
                        ent_man=data["total_movimientos_manuales"]["total_ingreso"] or Decimal(0)
                        sal_man=data["total_movimientos_manuales"]["total_egreso"] or Decimal(0)
                    else:
                        t_ventas=Decimal(0)
                        ent_man=Decimal(0)
                        sal_man=Decimal(0)
                    
                    retiro = Decimal(request.POST["retiro_banco"])
                    faltasobra = Decimal(request.POST["faltante_sobrante"])                    
                    #Rgistro de los movimiento de caja generados por el cierra
                    

                    ventas=TurnoDet(descripcion="Ventas del turno",ingreso=t_ventas,turno=turno_abierto)
                    ventas.save()
                        #hubo faltante
                    if faltasobra < 0.00:
                        salidas=TurnoDet(descripcion="Registro de faltante en turno",egreso=faltasobra*-1,turno=turno_abierto)
                        salidas.save()                    
                        #sobrante
                    if faltasobra > 0.00:
                        salidas=TurnoDet(descripcion="Registro de sobrante en turno",ingreso=faltasobra,turno=turno_abierto)
                        salidas.save()                    
        
                    #retiro a banco
                    if retiro > 0:
                        retiro_b=TurnoDet(descripcion="Retiro de efectivo a banco en turno",egreso=retiro,turno=turno_abierto)
                        retiro_b.save()                 
                                        
                    
                    #print type(turno_abierto.saldo_apertura),type(t_ventas),type(ent_man),type(faltasobra),type(retiro),type(sal_man)
                    turno_abierto.saldo_cierre=turno_abierto.saldo_apertura+t_ventas+ent_man+faltasobra-retiro-sal_man
                    turno_abierto.estado=1
                    turno_abierto.fecha_hora_fin=datetime.now()                    
                    turno_abierto.save()
                    #print retiro,faltasobra                    


                    #ENCENDER LUEGO
                    del request.session["turno"]     
                    # If the save was successful, redirect to another page            
                    success="Turno cerrado con exito "
                    data=get_data_cierre(inicio,fin,usuario,turno_abierto) 
                    if data:
                        data["saldo_final"]=turno_abierto.saldo_cierre
                        data["faltasobra"]=faltasobra
                        data["retirobanco"]=retiro


                    #AGREGAR AQUI FALTA SOBRA Y RETIRO BANCO DESDE REQUEST POST
                    #MEJORAR REPORTE
                    #print data

                    subject = "Informacion de Cierre de Turno"
                    to = ['wasuaje@eluniversal.com']
                    from_email = 'systema@eluniversal.com'

                    ctx = {'form': form,'error':error,'success':success,'data':data}

                    message = get_template("closeturno_table.html").render(Context(ctx,request))
                    msg = EmailMessage(subject, message, to=to, from_email=from_email)
                    msg.content_subtype = 'html'
                    msg.send()
                    
                    return render_to_response("closeturno_table.html",
                                      {'form': form,'error':error,'success':success,'data':data},
                                      context_instance=RequestContext(request))
            else:                                        
                
                data=get_data_cierre(inicio,fin,usuario,turno_abierto)
                          
                if data:
                    form=CloseTurnoDet(initial={'faltante_sobrante': data["falta_sobra"]})                                    
                    if data["falta_sobra"] > 0:
                        error="Cobro superior a ventas verifique"
                    elif data["falta_sobra"] < 0:
                        fact=facturas_sin_cobrar(inicio,fin,usuario)
                        #print fact
                        facts= [x["correlativo"] for x in fact if x["Cobrado"] <> x["Facturado"] ]                    
                        #print facts
                        error="Existen facturas sin cobrar, verifique facturas %s" % "".join(str(facts))                    
                else:
                    form=None
        else:            
            form = None        
            error ="No hay turno activo, verifique"    
    else:        
        form = None        
        error ="No hay ningun turno abierto, verifique"        
        #tal vez una verificacion contra BD si de verdad la caja existe para evitar que se 
        #borre el registro por bbdd y quede la sesion abierta de la caja        
    return render_to_response(template_name,
                              {'form': form,'error':error, "data":data },
                              context_instance=RequestContext(request))

