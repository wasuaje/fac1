# -*- coding: utf-8 -*-
from forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render_to_response,redirect,get_object_or_404
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test,permission_required
from comunes import *

@login_required(login_url='/login/')
@user_passes_test(is_in_banco_group, login_url='/login/')
def index_banco(request):
    form_class = GenericSearchForm
    model = Banco
    template_name = 'index_banco.html'
    paginate_by = 5

    if request.method == 'POST':
        form = form_class(request.POST or None)
        if form.is_valid():
             banco_list = model.objects.filter(nombre__icontains=form.cleaned_data['buscar'])
        else:
             banco_list = model.objects.all()
    else:
        banco_list = model.objects.all()
        form = form_class()

    paginator = Paginator(banco_list, 10) # Show 10 contacts per page

    page = request.GET.get('page')
    try:
        bancos = paginator.page(page)
    except PageNotAnInteger:
        bancos = paginator.page(1)
    except EmptyPage:
        bancos = paginator.page(paginator.num_pages)

    return render_to_response(template_name,     {'form': form, 'bancos': bancos,}, 
        context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.add_banco', login_url='/login/')
def add_banco(request):
    template_name=u"banco.html"
    if request.method == 'POST':
        form = ManageBancos(request.POST,request.FILES)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, ('Operacion exitosa'))
    # If the save was successful, redirect to another page
        return HttpResponseRedirect('/banco/')
    else:
        form = ManageBancos()
    return render_to_response(template_name,      {'form': form},      context_instance=RequestContext(request))




@login_required(login_url='/login/')
@permission_required('ventas.change_banco', login_url='/login/')
def edit_banco(request,pk):
    banco = get_object_or_404(Banco, pk=pk)
    form = ManageBancos(instance=banco)
    #print form.nombres
    if request.POST:
        form = ManageBancos(request.POST,request.FILES,instance=banco)
    if form.is_valid():
        form.save()
    #persona = form.save()
    #this is where you might choose to do stuff.
    #contact.name = 'test'
    #persona.save()
        messages.add_message(request, messages.SUCCESS, ('Persona editada.'))
        return HttpResponseRedirect('/banco/')

    return render_to_response('banco.html',  {'form': form,   'id': pk},  context_instance=RequestContext(request))


@login_required(login_url='/login/')
@permission_required('ventas.delete_banco', login_url='/login/')
def delete_banco(request,pk):
	banco = get_object_or_404(Banco, pk=pk)
	form = ManageBancos(instance=banco)
#print form.nombres
	if request.POST:
		form = ManageBancos(request.POST,request.FILES,instance=banco)
		if form.is_valid():
			banco.delete()
			messages.add_message(request, messages.SUCCESS, ('Banco eliminada'))
			return HttpResponseRedirect('/banco/')

	return render_to_response('banco.html',  {'form': form,   'id': pk},
  context_instance=RequestContext(request))


def bulk_insert2(request):  ##se cambio el nombre para que no se ejcute de nuevo, funciona bello
    bancos=[u"Banco de Venezuela",
    u"Banesco",
    u"BBVA Banco Provincial",
    u"Banco Mercantil",
    u"Bicentenario Banco Universal",
    u"Banco Occidental de Descuento",
    u"Banco Fondo Común",
    u"Banco Exterior",
    u"Banco del Tesoro",
    u"Banco Industrial de Venezuela",
    u"Banco Nacional de Crédito",
    u"Corp Banca (Venezuela)",
    u"BanCaribe",
    u"Venezolano de Crédito",
    u"Banco Caroní",
    u"Banco Agrícola de Venezuela",
    u"Banco Sofitasa",
    u"Banco Plaza",
    u"Banco del Sur",
    u"Citibank Venezuela",
    u"100% Banco",
    u"Banco Activo",
    u"Banplus",
    u"Banco Espíritu Santo (Venezuela)",
    u"Banco Internacional de Desarrollo",
    u"Banco de Exportación y Comercio",
    u"BanCaribe"]

    bulk=[]
    for i in bancos:
        bulk.append(Banco(nombre=i))

    Banco.objects.bulk_create(bulk)

    return HttpResponseRedirect('/banco/')