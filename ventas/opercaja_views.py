from django.contrib.auth.decorators import login_required,user_passes_test
from forms import *
from django.core.paginator import Paginator,PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect    
from comunes import *

from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMessage

@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def opencaja(request):
    template_name="opercaja.html"       
    error=None
    success=None
    if  "caja" not in request.session.keys():          
        if request.method == 'POST':
            form = OpenCaja(request.POST,request.FILES)
            if form.is_valid():
                nueva_caja=form.save(commit=False)
                nueva_caja.usuario=request.user                
                nueva_caja.save()
                request.session['caja'] = {'id':nueva_caja.id,'nombre':nueva_caja.tipocaja.nombre,
                                    'fecha':nueva_caja.fecha.strftime('%Y-%m-%d'),'hora_ini':nueva_caja.fecha_hora_ini.strftime('%Y-%m-%d %H:%M:%S')
                                        }                
                # If the save was successful, redirect to another page                            
                success="Caja abierta con exito"
                return render_to_response(template_name,
                              {'form': form,'error':error,'success':success},
                              context_instance=RequestContext(request))
            else:
                error="La combinacion caja/fecha ya esta cerrada para el dia de hoy"
                return render_to_response(template_name,
                              {'form': form,'error':error,'success':success},
                              context_instance=RequestContext(request))

        else:
            ultimo_turno=Turno.objects.filter().order_by('-id')[0]                        
            form = OpenCaja(initial={'saldo_apertura': ultimo_turno.saldo_cierre})
                        

    else:
        form = None        
        error ="Ya hay una caja abierta, verifique, fecha: %s" % request.session["caja"]["fecha"]
        #tal vez una verificacion contra BD si de verdad la caja existe para evitar que se 
        #borre el registro por bbdd y quede la sesion abierta de la caja        
    return render_to_response(template_name,
                              {'form': form,'error':error},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def closecaja(request):
    template_name="closecaja.html"    
    error=None
    success=None    
    caja_abierta=None     
    data=None  
    #print request.session["turno"]   
    #del request.session['turno']     
    #request.session.pop('turno',None)
    #break;
    #request.session["turno"]["id"]=1
        #request.session.pop('caja',None)
        #return HttpResponseRedirect('/opencaja/')            
    if  "caja" in request.session.keys():
        
        caja_abierta = Caja.objects.get( pk=request.session["caja"]["id"] )             
        inicio = caja_abierta.fecha_hora_ini
        fin =datetime.now()
        usuario = request.user.id
        template_name="closecaja.html"    
        if request.method == 'POST':        #puede ser un form.form personalizado !!!    
            form = CloseCajaDet(request.POST,request.FILES)                
            if form.is_valid():
                template_name="closecaja_no_menu.html"    
                data=get_data_cierre(inicio,fin,caja_abierta=caja_abierta) 
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
                                    
                
                #print type(turno_abierto.saldo_apertura),type(t_ventas),type(ent_man),type(faltasobra),type(retiro),type(sal_man)
                caja_abierta.saldo_cierre=caja_abierta.saldo_apertura+t_ventas+ent_man+faltasobra-retiro-sal_man
                caja_abierta.estado=1
                caja_abierta.fecha_hora_fin=datetime.now()                    
                caja_abierta.save()
                #print retiro,faltasobra                    

                #ENCENDER LUEGO
                #del request.session["caja"]     
                # If the save was successful, redirect to another page            
                success="Caja cerrada con exito "
                data=get_data_cierre(inicio,fin,caja_abierta=caja_abierta) 
                if data:
                    data["saldo_final"]=caja_abierta.saldo_cierre
                    data["faltasobra"]=faltasobra
                    data["retirobanco"]=retiro
                
                #MEJORAR REPORTE
                #print data

                subject = "Informacion de Cierre de Caja als %s " % request.session["caja"]["fecha"]
                to = ['wasuaje@eluniversal.com']
                from_email = 'systema@eluniversal.com'

                ctx = {'form': form,'error':error,'success':success,'data':data}

                message = get_template("closecaja_table.html").render(Context(ctx,request))
                msg = EmailMessage(subject, message, to=to, from_email=from_email)
                msg.content_subtype = 'html'
                msg.send()
                
                return render_to_response("closecaja_table.html",
                                  {'form': form,'error':error,'success':success,'data':data},
                                  context_instance=RequestContext(request))
        else:                                        
                                 
            data=get_data_cierre(inicio,fin,caja_abierta=caja_abierta)            
            if data:
                form=CloseCajaDet(initial={'faltante_sobrante': data["falta_sobra"]})                                    
                if data["falta_sobra"] > 0:
                    error="Cobro superior a ventas verifique"
                elif data["falta_sobra"] < 0:
                    fact=facturas_sin_cobrar(inicio,fin)
                    #print fact
                    facts= [x["correlativo"] for x in fact if x["Cobrado"] <> x["Facturado"] ]                    
                    #print facts
                    error="Existen facturas sin cobrar, verifique facturas %s" % "".join(str(facts))                    
            else:
                form=None       
    else:        
        form = None        
        error ="No hay caja abierta, verifique"        
        
    return render_to_response(template_name,
                              {'form': form,'error':error, "data":data },
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def movcaja(request):
    form_class = DateSearchForm
    model = TurnoDet
    form=DateSearchForm()    
    template_name = 'index_movcaja.html'
    movimientos=None
    error=None    
    if  "turno" not in request.session.keys():
        error="No hay caja o turno operativo para agregarle movimientos"    
    else:
        if request.method == 'POST': 
            form = form_class(request.POST or None)
            if form.is_valid():
                #movimiento_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
                #movimiento_list = model.objects.filter( kwargs.pop("fecha_hora__lte",None))            
                fecha=form.cleaned_data['fecha']
                if not fecha:
                    fecha=datetime.now()
                return HttpResponseRedirect( reverse('search_mc' , args=(fecha.year,fecha.month,fecha.day) ) )            
        else:    
            kwargs={}        
            kwargs["manual"]=1
            movimiento_list = model.objects.filter(**kwargs)\
                    .values("descripcion","fecha_hora","ingreso","egreso") \
                    .order_by('fecha_hora')        
            form = DateSearchForm()    

            paginator = Paginator(movimiento_list, 11) # Show 10 contacts per page

            page = request.GET.get('page')
            try:
                movimientos = paginator.page(page)
            except PageNotAnInteger:
                movimientos = paginator.page(1)
            except EmptyPage:
                movimientos = paginator.page(paginator.num_pages)
    
    return render_to_response(template_name, 
            {'form': form, 'movimientos': movimientos,'error':error}, 
            context_instance=RequestContext(request))


@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def search_movcaja(request,year,month,day):
    form_class = DateSearchForm
    template_name = 'index_movcaja.html'
    model = TurnoDet

    if request.method == 'POST': 
        form = form_class(request.POST or None)
        if form.is_valid():
            #inventario_list = model.objects.filter(correlativo__icontains=form.cleaned_data['buscar'])
            #inventario_list = model.objects.filter( kwargs.pop("fecha_hora__lte",None))            
            fecha=form.cleaned_data['fecha']
            if fecha:
                return HttpResponseRedirect( reverse('search_mc' , args=(fecha.year,fecha.month,fecha.day) ) )                   
            else:
                return HttpResponseRedirect( '/movcaja/' )
    else:
        kwargs={}
        kwargs["fecha_hora__year"]=int(year)
        kwargs["fecha_hora__month"]=int(month)
        kwargs["fecha_hora__day"]=int(day)
        kwargs["manual"]=1
        movimiento_list = model.objects.filter(**kwargs)\
                .values("descripcion","fecha_hora","ingreso","egreso") \
                .order_by('fecha_hora')   

        paginator = Paginator(movimiento_list, 11) # Show 10 contacts per page
        
        page = request.GET.get('page')
        
        try:
            movimientos = paginator.page(page)
        except PageNotAnInteger:
            movimientos = paginator.page(1)
        except EmptyPage:
            movimientos = paginator.page(paginator.num_pages)
                
        form = DateSearchForm()    

    return render_to_response(template_name, 
            {'form': form, 'movimientos': movimientos,}, 
            context_instance=RequestContext(request))          

@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def add_movcaja(request):
    template_name="movcaja.html"
    if request.method == 'POST':
        form = MovCajaEnt(request.POST,request.FILES)        
        if form.is_valid():
            mov_nueva = form.save(commit=False)            
            mov_nueva.usuario=request.user
            mov_nueva.manual=1
            mov_nueva.turno=Turno(pk=request.session["turno"]["id"])            
            mov_nueva.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/movcaja/')
    else:
        form = MovCajaEnt()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
@user_passes_test(is_in_caja_group, login_url='/login/')
def sub_movcaja(request):
    template_name="movcaja.html"
    if request.method == 'POST':
        form = MovCajaSal(request.POST,request.FILES)        
        if form.is_valid():
            mov_nueva = form.save(commit=False)            
            mov_nueva.usuario=request.user
            mov_nueva.manual=1
            mov_nueva.turno=Turno(pk=request.session["turno"]["id"])            
            mov_nueva.save()
            messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
            # If the save was successful, redirect to another page            
            return HttpResponseRedirect('/movcaja/')
    else:
        form = MovCajaSal()
    return render_to_response(template_name,
                              {'form': form},
                              context_instance=RequestContext(request))
