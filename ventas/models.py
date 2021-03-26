from __future__ import unicode_literals
from django.db import models
from datetime import *
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
# Create your models here.
# into your database.

class Empresa(models.Model):    
    razon_social = models.CharField(max_length=200, blank=False, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    rif = models.CharField(max_length=15, blank=True, null=True)
    nit = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tlf = models.CharField(max_length=45, blank=True, null=True)
    fax = models.CharField(max_length=45, blank=True, null=True)
    ruta_foto = models.ImageField(upload_to='empresas/', null=True)
    p1 = models.CharField(max_length=25, blank=True, null=True)
    p2 = models.CharField(max_length=25, blank=True, null=True)
    p3 = models.CharField(max_length=25, blank=True, null=True)
    p4 = models.CharField(max_length=25, blank=True, null=True)
    p5 = models.CharField(max_length=25, blank=True, null=True)

    class Meta:        
        db_table = 'empresa'

    def __unicode__(self):
        return self.razon_social

class TipoImpuesto(models.Model):
    nombre       = models.CharField(max_length=50, blank=False, null=True)    
    codigo       = models.CharField(max_length=50, blank=False, null=True)    
    valido_desde = models.DateField( blank=False, null=False)
    valido_hasta = models.DateField( blank=True, null=True)
    valor        = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default="0.00")    

    class Meta:        
        db_table = 'tipo_impuesto'

    def __unicode__(self):
        return "(%s) - %s" % (self.codigo, self.valor)


class Categoria(models.Model):
    nombre = models.CharField(max_length=250, blank=False, null=False)
    ruta_foto = models.ImageField(upload_to='categorias/', null=True)

    class Meta:        
        db_table = 'categoria'

    def __unicode__(self):
        return self.nombre
        
class Articulo(models.Model):
    codigo = models.CharField(max_length=50, blank=False, null=True)    
    descripcion = models.CharField(max_length=250, blank=False, null=True)    
    importe = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True, default="0.00")
    descuento = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default="0.00")    
    inventar = models.NullBooleanField(null=False)
    #impuesto = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, default="0.00")        
    ruta_foto = models.ImageField(upload_to='articulos/', null=True)
    categoria = models.ForeignKey('Categoria')
    tipoimpuesto = models.ForeignKey('TipoImpuesto', null=True)

    class Meta:        
        db_table = 'articulo'
    
    def __unicode__(self):
        return self.descripcion

class Cliente(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    razon_social = models.CharField(max_length=200, blank=False, null=False)
    direccion = models.CharField(max_length=500, blank=False, null=True)
    rif = models.CharField(max_length=15, blank=False, null=False)
    nit = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tlf = models.CharField(max_length=45, blank=True, null=True)
    fax = models.CharField(max_length=45, blank=True, null=True)        

    class Meta:        
        db_table = 'cliente'
    
    def __unicode__(self):
        return self.razon_social


class Banco(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'banco'

    def __unicode__(self):
        return self.nombre

class TipoDoc(models.Model):
    codigo = models.CharField(max_length=2, blank=True, null=True)   
    nombre = models.CharField(max_length=45, blank=True, null=True)
    correlativo = models.IntegerField(blank=True, null=True)

    class Meta:        
        db_table = 'tipo_doc'
    
    def __unicode__(self):
        return self.nombre

class Proveedor(models.Model):
    nombre = models.CharField(max_length=200, blank=True, null=True)
    razon_social = models.CharField(max_length=200, blank=True, null=True)
    direccion = models.CharField(max_length=500, blank=True, null=True)
    rif = models.CharField(max_length=15, blank=True, null=True)
    nit = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    tlf = models.CharField(max_length=45, blank=True, null=True)
    fax = models.CharField(max_length=45, blank=True, null=True)
    ruta_foto = models.ImageField(upload_to='proveedores/', null=True)

    class Meta:        
        db_table = 'proveedor'

    def __unicode__(self):
        return self.razon_social

class Documento(models.Model):
    correlativo = models.IntegerField(blank=True, null=True)
    fecha = models.DateField(default=datetime.now,blank=True)
    fecha_vencimiento = models.DateField(default=datetime.now,blank=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)
    contacto = models.CharField(max_length=45, blank=True, null=True)
    nota_superior = models.CharField(max_length=500, blank=True, null=True)
    nota_detalle = models.CharField(max_length=500, blank=True, null=True)
    referencia = models.IntegerField(blank=True, null=True)    
    tipo_doc = models.ForeignKey(TipoDoc,blank=False, null=True)
    proveedor = models.ForeignKey(Proveedor, blank=False, null=True)
    cliente = models.ForeignKey(Cliente, blank=False, null=True)
    total_general = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    pct_descuento = models.DecimalField(blank=True, null=True,max_digits=5, decimal_places=2,default=0.00)    
    pct_impuesto  = models.DecimalField(blank=True, null=True,max_digits=5, decimal_places=2,default=0.00)    
    subtotal = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    tot_impuesto = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    excento = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    imponible = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    tot_descuento = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    sujeto_dcto = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    estado  = models.NullBooleanField(null=False,default=False)
    usuario = models.ForeignKey(User)

    class Meta:        
        db_table = 'documento'

    
class DocumentoDet(models.Model):
    descripcion = models.CharField(max_length=200, blank=True, null=True)
    cantidad = models.IntegerField(blank=False, null=True,default=1)
    importe = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    descuento = models.DecimalField(blank=True, null=False,max_digits=5, decimal_places=2,default=0.00)
    impuesto = models.DecimalField(blank=True, null=True,max_digits=5, decimal_places=2,default=0.00)    
    total = models.DecimalField(blank=True, null=True,max_digits=10, decimal_places=2,default=0.00)
    nota = models.CharField(max_length=45, blank=True, null=True)
    documento = models.ForeignKey(Documento)
    item = models.ForeignKey(Articulo)

    class Meta:        
        db_table = 'documento_det'


class FormaPago(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    efectivo = models.NullBooleanField(null=False,default=False)
    monetizable = models.NullBooleanField(null=False,default=True)

    class Meta:        
        db_table = 'forma_pago'
    
    def __unicode__(self):
        return self.nombre

class Cobros(models.Model):
    fecha = models.DateField(default=datetime.now,blank=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)
    aprobacion = models.CharField(max_length=45, blank=True, null=True)
    monto = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    descripcion = models.CharField(max_length=45, blank=True, null=True)    
    forma_pago = models.ForeignKey(FormaPago)
    documento = models.ForeignKey(Documento)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    usuario = models.ForeignKey(User)
    estado  = models.NullBooleanField(null=False,default=False)

    class Meta:        
        db_table = 'cobros'


class Pagos(models.Model):
    fecha = models.DateField(blank=True, null=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)
    aprobacion = models.CharField(max_length=45, blank=True, null=True)
    monto = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    documento = models.ForeignKey(Documento)
    forma_pago = models.ForeignKey(FormaPago)
    banco = models.ForeignKey(Banco, blank=True, null=True)
    usuario = models.ForeignKey(User)

    class Meta:        
        db_table = 'pagos'


class Inventario(models.Model):
    tipo = models.CharField(max_length=1)
    descripcion = models.CharField(max_length=45, blank=True, null=True)
    fecha = models.DateField(default=datetime.now,blank=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)
    cantidad = models.BigIntegerField(blank=False, null=False, default=1)    
    articulo = models.ForeignKey(Articulo) 
    usuario = models.ForeignKey(User)

    class Meta:        
        db_table = 'inventario'
    
    def __unicode__(self):
        return self.descripcion

    @receiver(post_save, sender=DocumentoDet)
    def creating(sender, **kwargs):
        #en caso de creacion de detalle de factura
        linea=kwargs.get("instance",'None')
        created=kwargs.get("created",'None')
        articulo=linea.item    
        #print kwargs,created
        if linea.documento.tipo_doc.codigo=='FV':
            if articulo.inventar and created:
                invent = Inventario(tipo="V",descripcion="Salida de articulos Ventas, POS, etc ",\
                            cantidad=linea.cantidad*-1,articulo=articulo,usuario=linea.documento.usuario)
                invent.save()
        
        if linea.documento.tipo_doc.codigo=='FC':
            if articulo.inventar and created:
                invent = Inventario(tipo="C",descripcion="Entrada por compra de productos",\
                         cantidad=linea.cantidad,articulo=articulo,usuario=linea.documento.usuario)
                invent.save()
        
    
    @receiver(post_delete, sender=DocumentoDet)
    def deleting(sender, **kwargs):
        #en caso de eliminacion de detalle de factura
        linea=kwargs.get("instance",'None')
        articulo=linea.item  

        if linea.documento.tipo_doc.codigo=='FV':
            if articulo.inventar:        
                invent = Inventario(tipo="V",descripcion="Entrada por reverso de salida de articulos Ventas, POS, etc ",cantidad=linea.cantidad,articulo=articulo,usuario=linea.documento.usuario)
                invent.save()        

        if linea.documento.tipo_doc.codigo=='FC':
            if articulo.inventar:        
                invent = Inventario(tipo="C",descripcion="Salida por reverso de compra ",cantidad=linea.cantidad*-1,articulo=articulo,usuario=linea.documento.usuario)
                invent.save()        

class TipoCaja(models.Model):       
    codigo = models.CharField(max_length=5, blank=True, null=True)   
    nombre = models.CharField(max_length=45, blank=True, null=True)
    
    class Meta:        
        db_table = 'tipo_caja'
        
    def __unicode__(self):
        return "%s - %s" % (self.codigo , self.nombre)

class Caja(models.Model):       
    descripcion = models.CharField(max_length=100, blank=True, null=True)    
    fecha = models.DateField(default=datetime.now,blank=True)
    fecha_hora_ini = models.DateTimeField(default=datetime.now,blank=True)    
    fecha_hora_fin = models.DateTimeField(default=datetime.now,blank=True)    
    saldo_apertura = models.DecimalField(default=0.00,blank=False, null=False,max_digits=9, decimal_places=2)
    saldo_cierre  = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    estado  = models.NullBooleanField(null=False,default=False)
    usuario = models.ForeignKey(User)
    tipocaja = models.ForeignKey(TipoCaja,null=False)
    
    class Meta:        
        db_table = 'caja'
        unique_together = ( ("tipocaja","fecha") )

    def __unicode__(self):
        return "Caja del %s" % self.fecha

class Turno(models.Model):
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_hora_ini = models.DateTimeField(default=datetime.now,blank=True)    
    fecha_hora_fin = models.DateTimeField(default=datetime.now,blank=True)    
    saldo_apertura = models.DecimalField(default=0.00,blank=False, null=False,max_digits=9, decimal_places=2)
    saldo_cierre  = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    estado  = models.NullBooleanField(null=False,default=False)
    usuario = models.ForeignKey(User,null=True)
    caja = models.ForeignKey(Caja,null=True)
    
    class Meta:        
        db_table = 'turno'        

    def __unicode__(self):
        return "%s: %s - %s" % (self.usuario.username, self.fecha_hora_ini, self.fecha_hora_fin)

class TurnoDet(models.Model):
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)   
    ingreso = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    egreso = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)        
    turno = models.ForeignKey(Turno)
    manual = models.NullBooleanField(null=False,default=False)
    
    class Meta:        
        db_table = 'turno_det'
    
class CuentaBanco(models.Model):
    numero = models.CharField(max_length=20, blank=True, null=True)
    contacto = models.CharField(max_length=100, blank=True, null=True)
    banco = models.ForeignKey(Banco)
    
    class Meta:        
        db_table = 'cuenta_banco'

    def __unicode__(self):
        return "%s : %s" % (self.numero, self.banco.nombre)

class BancoDet(models.Model):
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fecha_hora = models.DateTimeField(default=datetime.now,blank=True)   
    ingreso = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)
    egreso = models.DecimalField(blank=True, null=True,max_digits=9, decimal_places=2)        
    cuentabanco = models.ForeignKey(CuentaBanco)
    manual = models.NullBooleanField(null=False,default=False)

    class Meta:        
        db_table = 'banco_det'

class Vehiculo(models.Model):
    placa = models.CharField(max_length=45, blank=True, null=True)
    color = models.CharField(max_length=45, blank=True, null=True)
    serial_motor = models.CharField(max_length=45, blank=True, null=True)
    serial_caja = models.CharField(max_length=45, blank=True, null=True)
    serial_carroceria = models.CharField(max_length=45, blank=True, null=True)
    nro_ejes = models.IntegerField(blank=True, null=True)
    nro_ruedas = models.IntegerField(blank=True, null=True)
    kilometraje = models.IntegerField(blank=True, null=True)
    ruta_foto = models.ImageField(upload_to='vehiculo/', null=True)
    vehiculo_modelo = models.ForeignKey('VehiculoModelo')
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    class Meta:        
        db_table = 'vehiculo'


class VehiculoMarca(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)

    class Meta:        
        db_table = 'vehiculo_marca'


class VehiculoModelo(models.Model):
    nombre = models.CharField(max_length=45, blank=True, null=True)
    vehiculo_marca = models.IntegerField()

    class Meta:        
        db_table = 'vehiculo_modelo'

