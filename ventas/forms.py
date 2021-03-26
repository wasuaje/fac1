from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from models import *
from django.forms import ModelForm,Textarea,TextInput,HiddenInput
from django.forms.extras.widgets import SelectDateWidget


class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)    


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2','first_name','last_name')        

    def save(self,commit = True):   
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']        

        if commit:
            user.save()

        return user


class MyLoginForm(AuthenticationForm):
    username = forms.CharField(required = True)
    password = forms.CharField(required = True,widget=forms.PasswordInput)
   

    class Meta:
        model = User
        fields = ('username',  'password')        

class GenericSearchForm(forms.Form):
    buscar = forms.CharField(required=False)    

class DateSearchForm(forms.Form):
    fecha = forms.DateField(required=False, label="Busca fecha") 

class ManageCategorias(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'          

class ManageArticulos(ModelForm):
    class Meta:
        model = Articulo
        fields = ['categoria','codigo','descripcion','importe','descuento','tipoimpuesto','inventar','ruta_foto']
 
class ManageClientes(ModelForm):
	class Meta:
		model = Cliente
		fields = ['razon_social','nombre','rif','nit','direccion','email','tlf','fax']
		widgets = {
			'direccion': Textarea(attrs={'cols': 40, 'rows': 5}),
		}

class ManageEmpresas(ModelForm):
    class Meta:
        model = Empresa
        fields = ['razon_social','rif','nit','direccion','email','tlf','fax','ruta_foto','p1','p2','p3','p4','p5']
        widgets = {
            'direccion': Textarea(attrs={'cols': 40, 'rows': 5}),
        }        

class ManageProveedores(ModelForm):
    class Meta:
        model = Proveedor
        fields = ['razon_social','nombre','rif','nit','direccion','email','tlf','fax']
        widgets = {
            'direccion': Textarea(attrs={'cols': 40, 'rows': 5}),
        }        

class ManageTipoDocs(ModelForm):
    class Meta:
        model = TipoDoc
        fields = ['codigo','nombre','correlativo']

class ManageTipoImpuestos(ModelForm):
    class Meta:
        model = TipoImpuesto
        fields = ['codigo','nombre','valor','valido_desde','valido_hasta']

class ManageFormaPagos(ModelForm):
    class Meta:
        model = FormaPago
        fields = ['nombre','efectivo','monetizable']

class ManageBancos(ModelForm):
    class Meta:
        model = Banco
        fields = ['nombre']


class ManageFacturas(ModelForm):
    class Meta:
        model = Documento
        fields = ['cliente', 'fecha','fecha_vencimiento','contacto','nota_superior','nota_detalle']
        widgets = {
            'cliente': HiddenInput(attrs={'size': 10, 'class': 'special'}),            
            'nota_superior': Textarea(attrs={'cols': 40, 'rows': 5}),
            'nota_detalle': Textarea(attrs={'cols': 40, 'rows': 5}),            
        }  

class ManageFactCompras(ModelForm):
    correlativo = forms.CharField(widget=forms.TextInput, label='Fact. Nro.:')
    class Meta:
        model = Documento        
        fields = ['proveedor', 'correlativo','fecha','fecha_vencimiento','contacto', \
                'nota_superior','nota_detalle','pct_descuento','tot_descuento',\
                'pct_impuesto','tot_impuesto' ,'subtotal','imponible','total_general']        
        widgets = {
            'proveedor': HiddenInput(attrs={'size': 10, 'class': 'special'}),            
            'nota_superior': Textarea(attrs={'cols': 40, 'rows': 5}),
            'nota_detalle': Textarea(attrs={'cols': 40, 'rows': 5}),            
        }  

class ManageLineas(ModelForm):
    class Meta:
        model = DocumentoDet
        fields = ['item','cantidad', 'importe','descuento','impuesto','total']        
        widgets = {
            'item': HiddenInput(attrs={'size': 10, 'class': 'special'}),            
            'cantidad': TextInput(attrs={'size': 5,}),
            'importe': TextInput(attrs={'size': 15,}),
            'descuento':  TextInput(attrs={'size': 15,}),
            'impuesto':  TextInput(attrs={'size': 15,}),
            'total':  TextInput(attrs={'size': 15,}),
        }   

class ManageTipoCajas(ModelForm):
    class Meta:
        model = TipoCaja
        fields = ['codigo','nombre']

class ManageCuentaBancos(ModelForm):
    class Meta:
        model = CuentaBanco
        fields = ['banco','numero','contacto']        


class OpenCaja(ModelForm):
    class Meta:
        model = Caja
        fields = ['tipocaja','fecha','saldo_apertura','descripcion']        

class CloseCaja(ModelForm):
    class Meta:
        model = Caja
        fields = ['saldo_cierre','descripcion']        

class CloseCajaDet(forms.Form):
    faltante_sobrante = forms.DecimalField(max_digits=9, decimal_places=2, label='Faltante o Sobrante')
    retiro_banco = forms.DecimalField(max_digits=9, decimal_places=2, label='Retiro al banco')    


class OpenTurno(ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_hora_ini','saldo_apertura','descripcion']  

class CloseTurno(ModelForm):
    class Meta:
        model = Turno
        fields = ['fecha_hora_fin','descripcion']      


class CloseTurnoDet(forms.Form):
    #saldo_inicial = forms.DecimalField(max_digits=9, decimal_places=2, label='Saldo Apertura')
    #ventas_efectivo = forms.DecimalField(max_digits=9, decimal_places=2, label='Ventas Efectivo')
    faltante_sobrante = forms.DecimalField(max_digits=9, decimal_places=2, label='Faltante o Sobrante')
    retiro_banco = forms.DecimalField(max_digits=9, decimal_places=2, label='Retiro al banco')
    #saldo_final = forms.DecimalField(max_digits=9, decimal_places=2, label='Saldo Final')


REPORTES = (
    ('ventasbs', 'Ventas en Bolivares'),
    ('ventasprod', 'Ventas por Producto'),
    ('ventascat', 'Ventas por Categorias'),
)
class RptVentasForm(forms.Form):
    seleccione_reporte = forms.ChoiceField(required=True, choices=REPORTES)
    fecha_desde = forms.DateField( label='Fecha Inicio de reporte')
    fecha_hasta = forms.DateField( label='Fecha Fin de reporte')


REPORTESC = (
    ('comprasbs', 'Compras en Bolivares'),
    ('comprasprod', 'Compras por Producto'),
    ('comprascat', 'Compras por Categorias'),
)
class RptComprasForm(forms.Form):
    seleccione_reporte = forms.ChoiceField(required=True, choices=REPORTESC)
    fecha_desde = forms.DateField( label='Fecha Inicio de reporte')
    fecha_hasta = forms.DateField( label='Fecha Fin de reporte')


TIPOINVENTARIO = (    
    ('E', 'Entrada Manual'),
    ('S', 'Salida Manual'),
)

class ManageInventarios(ModelForm):
    tipo =  forms.ChoiceField(required=True, choices=TIPOINVENTARIO, label="Tipo Mov")
    class Meta:
        model = Inventario
        fields = ['tipo','fecha','articulo','descripcion','cantidad']      
        
REPORTESINV = (
    ('existencias', 'Existencias'),
    ('valorizado', 'Existencias Valorizadas'),
    ('tomafisica', 'Toma de inventario Fisico'),
    
)
class RptInventariosForm(forms.Form):
    seleccione_reporte = forms.ChoiceField(required=True, choices=REPORTESINV)
    

class MovCajaEnt(ModelForm):
    class Meta:
        model = TurnoDet
        fields = ['descripcion','ingreso']      

class MovCajaSal(ModelForm):
    class Meta:
        model = TurnoDet
        fields = ['descripcion','egreso']      
