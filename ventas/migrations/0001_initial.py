# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=50, null=True)),
                ('descripcion', models.CharField(max_length=250, null=True)),
                ('importe', models.DecimalField(default='0.00', null=True, max_digits=9, decimal_places=2, blank=True)),
                ('descuento', models.DecimalField(default='0.00', null=True, max_digits=5, decimal_places=2, blank=True)),
                ('inventar', models.BooleanField()),
                ('ruta_foto', models.ImageField(null=True, upload_to='articulos/')),
            ],
            options={
                'db_table': 'articulo',
            },
        ),
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'banco',
            },
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, unique=True, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('tot_ingresos', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('tot_egresos', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('tota_general', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('estado', models.BooleanField()),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'caja',
            },
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=250)),
                ('ruta_foto', models.ImageField(null=True, upload_to='categorias/')),
            ],
            options={
                'db_table': 'categoria',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200, null=True, blank=True)),
                ('razon_social', models.CharField(max_length=200)),
                ('direccion', models.CharField(max_length=500, null=True)),
                ('rif', models.CharField(max_length=15)),
                ('nit', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('tlf', models.CharField(max_length=45, null=True, blank=True)),
                ('fax', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Cobros',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('aprobacion', models.CharField(max_length=45, null=True, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('descripcion', models.CharField(max_length=45, null=True, blank=True)),
                ('estado', models.BooleanField()),
                ('banco', models.ForeignKey(blank=True, to='ventas.Banco', null=True)),
            ],
            options={
                'db_table': 'cobros',
            },
        ),
        migrations.CreateModel(
            name='Documento',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('correlativo', models.IntegerField(null=True, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, blank=True)),
                ('fecha_vencimiento', models.DateField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('contacto', models.CharField(max_length=45, null=True, blank=True)),
                ('nota_superior', models.CharField(max_length=500, null=True, blank=True)),
                ('nota_detalle', models.CharField(max_length=500, null=True, blank=True)),
                ('referencia', models.IntegerField(null=True, blank=True)),
                ('status', models.IntegerField(null=True, blank=True)),
                ('total_general', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('pct_descuento', models.DecimalField(default=0.0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('pct_impuesto', models.DecimalField(default=0.0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('subtotal', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('tot_impuesto', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('excento', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('imponible', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('tot_descuento', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('sujeto_dcto', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('estado', models.BooleanField()),
                ('cliente', models.ForeignKey(to='ventas.Cliente', null=True)),
            ],
            options={
                'db_table': 'documento',
            },
        ),
        migrations.CreateModel(
            name='DocumentoDet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=200, null=True, blank=True)),
                ('cantidad', models.IntegerField(default=1, null=True)),
                ('importe', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('descuento', models.DecimalField(default=0.0, max_digits=5, decimal_places=2, blank=True)),
                ('impuesto', models.DecimalField(default=0.0, null=True, max_digits=5, decimal_places=2, blank=True)),
                ('total', models.DecimalField(default=0.0, null=True, max_digits=10, decimal_places=2, blank=True)),
                ('nota', models.CharField(max_length=45, null=True, blank=True)),
                ('documento', models.ForeignKey(to='ventas.Documento')),
                ('item', models.ForeignKey(to='ventas.Articulo')),
            ],
            options={
                'db_table': 'documento_det',
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('razon_social', models.CharField(max_length=200, null=True)),
                ('direccion', models.CharField(max_length=500, null=True, blank=True)),
                ('rif', models.CharField(max_length=15, null=True, blank=True)),
                ('nit', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('tlf', models.CharField(max_length=45, null=True, blank=True)),
                ('fax', models.CharField(max_length=45, null=True, blank=True)),
                ('ruta_foto', models.ImageField(null=True, upload_to='empresas/')),
                ('p1', models.CharField(max_length=25, null=True, blank=True)),
                ('p2', models.CharField(max_length=25, null=True, blank=True)),
                ('p3', models.CharField(max_length=25, null=True, blank=True)),
                ('p4', models.CharField(max_length=25, null=True, blank=True)),
                ('p5', models.CharField(max_length=25, null=True, blank=True)),
            ],
            options={
                'db_table': 'empresa',
            },
        ),
        migrations.CreateModel(
            name='FormaPago',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'forma_pago',
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tipo', models.CharField(max_length=1)),
                ('descripcion', models.CharField(max_length=45, null=True, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('cantidad', models.BigIntegerField(null=True, blank=True)),
                ('articulo', models.ForeignKey(to='ventas.Articulo')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'inventario',
            },
        ),
        migrations.CreateModel(
            name='Pagos',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(null=True, blank=True)),
                ('fecha_hora', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('aprobacion', models.CharField(max_length=45, null=True, blank=True)),
                ('monto', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('descripcion', models.CharField(max_length=45, null=True, blank=True)),
                ('banco', models.ForeignKey(blank=True, to='ventas.Banco', null=True)),
                ('documento', models.ForeignKey(to='ventas.Documento')),
                ('forma_pago', models.ForeignKey(to='ventas.FormaPago')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'pagos',
            },
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=200, null=True, blank=True)),
                ('razon_social', models.CharField(max_length=200, null=True, blank=True)),
                ('direccion', models.CharField(max_length=500, null=True, blank=True)),
                ('rif', models.CharField(max_length=15, null=True, blank=True)),
                ('nit', models.CharField(max_length=15, null=True, blank=True)),
                ('email', models.EmailField(max_length=254, null=True, blank=True)),
                ('tlf', models.CharField(max_length=45, null=True, blank=True)),
                ('fax', models.CharField(max_length=45, null=True, blank=True)),
                ('ruta_foto', models.ImageField(null=True, upload_to='proveedores/')),
            ],
            options={
                'db_table': 'proveedor',
            },
        ),
        migrations.CreateModel(
            name='TipoDoc',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=2, null=True, blank=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
                ('correlativo', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'tipo_doc',
            },
        ),
        migrations.CreateModel(
            name='TipoImpuesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=50, null=True)),
                ('codigo', models.CharField(max_length=50, null=True)),
                ('valido_desde', models.DateField()),
                ('valido_hasta', models.DateField(null=True, blank=True)),
                ('valor', models.DecimalField(default='0.00', null=True, max_digits=5, decimal_places=2, blank=True)),
            ],
            options={
                'db_table': 'tipo_impuesto',
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('descripcion', models.CharField(max_length=100, null=True, blank=True)),
                ('ingreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('egreso', models.DecimalField(null=True, max_digits=9, decimal_places=2, blank=True)),
                ('fecha', models.DateField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora_inicio', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('fecha_hora_fin', models.DateTimeField(default=datetime.datetime.now, blank=True)),
                ('estado', models.BooleanField()),
                ('caja', models.ForeignKey(to='ventas.Caja')),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'turno',
            },
        ),
        migrations.CreateModel(
            name='Vehiculo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('placa', models.CharField(max_length=45, null=True, blank=True)),
                ('color', models.CharField(max_length=45, null=True, blank=True)),
                ('serial_motor', models.CharField(max_length=45, null=True, blank=True)),
                ('serial_caja', models.CharField(max_length=45, null=True, blank=True)),
                ('serial_carroceria', models.CharField(max_length=45, null=True, blank=True)),
                ('nro_ejes', models.IntegerField(null=True, blank=True)),
                ('nro_ruedas', models.IntegerField(null=True, blank=True)),
                ('kilometraje', models.IntegerField(null=True, blank=True)),
                ('ruta_foto', models.ImageField(null=True, upload_to='vehiculo/')),
                ('cliente', models.ForeignKey(blank=True, to='ventas.Cliente', null=True)),
            ],
            options={
                'db_table': 'vehiculo',
            },
        ),
        migrations.CreateModel(
            name='VehiculoMarca',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
            ],
            options={
                'db_table': 'vehiculo_marca',
            },
        ),
        migrations.CreateModel(
            name='VehiculoModelo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=45, null=True, blank=True)),
                ('vehiculo_marca', models.IntegerField()),
            ],
            options={
                'db_table': 'vehiculo_modelo',
            },
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='vehiculo_modelo',
            field=models.ForeignKey(to='ventas.VehiculoModelo'),
        ),
        migrations.AddField(
            model_name='documento',
            name='proveedor',
            field=models.ForeignKey(to='ventas.Proveedor', null=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='tipo_doc',
            field=models.ForeignKey(to='ventas.TipoDoc', null=True),
        ),
        migrations.AddField(
            model_name='documento',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='cobros',
            name='documento',
            field=models.ForeignKey(to='ventas.Documento'),
        ),
        migrations.AddField(
            model_name='cobros',
            name='forma_pago',
            field=models.ForeignKey(to='ventas.FormaPago'),
        ),
        migrations.AddField(
            model_name='cobros',
            name='usuario',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='articulo',
            name='categoria',
            field=models.ForeignKey(to='ventas.Categoria'),
        ),
        migrations.AddField(
            model_name='articulo',
            name='tipoimpuesto',
            field=models.ForeignKey(to='ventas.TipoImpuesto', null=True),
        ),
    ]
