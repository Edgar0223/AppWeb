# Generated by Django 4.2.4 on 2024-06-21 11:52

import Aplicaciones.Trabajo.models
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cuentas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='alm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lugar', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='congelado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgDesp', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.IntegerField()),
                ('horaEnvio', models.DateField()),
                ('cliente', models.CharField(max_length=30)),
                ('en_almacen', models.BooleanField(default=True)),
                ('hora', models.TimeField(null=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Desperdicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lote', models.CharField(max_length=30)),
                ('cantidad', models.FloatField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='embalaje',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, null=True)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='fisico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productos', models.CharField(max_length=200)),
                ('presentacion', models.CharField(max_length=200)),
                ('tMuestra', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('cliente', models.CharField(max_length=20)),
                ('lote', models.CharField(max_length=30)),
                ('brix', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('ph', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('hoja', models.IntegerField()),
                ('podrida', models.CharField(max_length=200)),
                ('sabor', models.CharField(max_length=200)),
                ('defecto', models.IntegerField()),
                ('color', models.IntegerField()),
                ('caracter', models.IntegerField()),
                ('tamano', models.IntegerField()),
                ('mExtrana', models.CharField(max_length=100, null=True)),
                ('empaque', models.CharField(max_length=100, null=True)),
                ('embalaje', models.CharField(max_length=100, null=True)),
                ('producto', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='fruta',
            fields=[
                ('movimiento', models.IntegerField(primary_key=True, serialize=False)),
                ('unidades', models.IntegerField()),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateTimeField()),
                ('maq', models.CharField(max_length=100, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('hora', models.TimeField(null=True)),
                ('maquila_origen', models.CharField(max_length=30, null=True)),
                ('en_nota', models.BooleanField(default=False)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('almacen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.alm')),
            ],
        ),
        migrations.CreateModel(
            name='materia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, null=True)),
                ('codigo', models.CharField(max_length=20, null=True)),
                ('catalogo', models.CharField(max_length=5, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Nota',
            fields=[
                ('folio', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('totalK', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('totalP', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('totalC', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('totalT', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('taraC', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('taraT', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField(null=True)),
                ('kilosB', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('kilosN', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('unidades', models.IntegerField(null=True)),
                ('movi', models.CharField(blank=True, max_length=255, null=True)),
                ('movi2', models.CharField(blank=True, max_length=255, null=True)),
                ('proveedor', models.CharField(max_length=50, null=True)),
                ('nombre', models.CharField(max_length=100, null=True)),
                ('usuario', models.CharField(max_length=100, null=True)),
                ('vencido', models.BooleanField(default=False)),
                ('en_pago', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='paleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=20, null=True)),
                ('peso', models.DecimalField(decimal_places=2, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
            ],
        ),
        migrations.CreateModel(
            name='producto',
            fields=[
                ('codigo', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True)),
                ('descripcion', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='proveedores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=30)),
                ('saldo', models.DecimalField(decimal_places=3, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('dias_vencimiento', models.IntegerField(null=True)),
                ('saldo_cajas', models.IntegerField(null=True)),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cuentas.catalogoemp')),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.CharField(max_length=30, verbose_name='Nombre del Rol')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=100, unique=True, verbose_name='Nombre de usuario')),
                ('nombres', models.CharField(blank=True, max_length=200, null=True, verbose_name='Nombres')),
                ('apellidos', models.CharField(blank=True, max_length=200, null=True, verbose_name='Apellidos')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo Electronico')),
                ('usuario_activo', models.BooleanField(default=True)),
                ('usuario_administrador', models.BooleanField(default=False)),
                ('foto', models.ImageField(blank=True, null=True, upload_to='fotos_perfil/')),
                ('capturando', models.BooleanField(default=False)),
                ('rol', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.rol', verbose_name='Rol')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ventas',
            fields=[
                ('movimiento', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('unidades', models.IntegerField()),
                ('tipoCaja', models.CharField(max_length=10)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateTimeField()),
                ('maq', models.CharField(max_length=100, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('almacen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.alm')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SalidaStock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unidades', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='recep',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('variedad', models.CharField(max_length=50, null=True)),
                ('brix', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('ph', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('muestra', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('tipoCaja', models.CharField(max_length=100, null=True)),
                ('mancha', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('tamano', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('caracter', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('sMadura', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('defecto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('verde', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('podrida', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('lodo', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('larva', models.CharField(max_length=100, null=True)),
                ('mExtrana', models.CharField(max_length=100, null=True)),
                ('limpieza', models.CharField(max_length=100, null=True)),
                ('aQuimicos', models.CharField(max_length=100, null=True)),
                ('aPlagas', models.CharField(max_length=100, null=True)),
                ('tDefecto', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('descuento', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('muestreo', models.ImageField(blank=True, null=True, upload_to='muestreo/')),
                ('en_nota', models.BooleanField(default=False)),
                ('fruta', models.ForeignKey(max_length=100, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.materia')),
                ('nota', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.nota')),
                ('productor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.proveedores')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='quebrado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgDesp', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.CharField(max_length=30)),
                ('horaEnvio', models.DateField()),
                ('en_almacen', models.BooleanField(default=True)),
                ('hora', models.TimeField(null=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.congelado')),
                ('nombre', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.materia')),
                ('tarima', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.paleta')),
                ('tipoCaja', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='proTer',
            fields=[
                ('movimiento', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('unidades', models.IntegerField()),
                ('tipoCaja', models.CharField(max_length=10)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateTimeField()),
                ('maq', models.CharField(max_length=100, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('almacen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.alm')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='pagosProv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total', models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fechaPago', models.DateField()),
                ('refe', models.CharField(max_length=30, null=True)),
                ('formaPago', models.CharField(max_length=30, null=True)),
                ('movi', models.CharField(blank=True, max_length=255, null=True)),
                ('nombre', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
            ],
        ),
        migrations.CreateModel(
            name='ordenes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('clave', models.CharField(max_length=30)),
                ('aceptado', models.BooleanField(default=False)),
                ('producto', models.CharField(max_length=30)),
                ('fecha', models.DateField()),
                ('po', models.IntegerField()),
                ('fecha_aceptacion', models.DateTimeField(blank=True, null=True)),
                ('aceptador', models.CharField(blank=True, max_length=30, null=True)),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='nota',
            name='pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.pagosprov'),
        ),
        migrations.AddField(
            model_name='nota',
            name='prov',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores'),
        ),
        migrations.CreateModel(
            name='Maquila',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maquila', models.CharField(max_length=30)),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.IntegerField(null=True)),
                ('unidades', models.IntegerField(null=True)),
                ('horaEnvio', models.DateTimeField()),
                ('en_almacen', models.BooleanField(default=True)),
                ('hora', models.TimeField(null=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.fruta')),
                ('nombre', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.materia')),
                ('tarima', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.paleta')),
                ('tipoCaja', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='lavado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgDesp', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.IntegerField()),
                ('horaEnvio', models.DateField()),
                ('en_almacen', models.BooleanField(default=True)),
                ('hora', models.TimeField(null=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.fruta')),
                ('nombre', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.materia')),
                ('tarima', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.paleta')),
                ('tipoCaja', models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='fruta',
            name='nombre',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.materia'),
        ),
        migrations.AddField(
            model_name='fruta',
            name='nota',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.nota'),
        ),
        migrations.AddField(
            model_name='fruta',
            name='proveedor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores'),
        ),
        migrations.AddField(
            model_name='fruta',
            name='tarima',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.paleta'),
        ),
        migrations.AddField(
            model_name='fruta',
            name='tipoCaja',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.embalaje'),
        ),
        migrations.AddField(
            model_name='fruta',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='frigoe',
            fields=[
                ('movimiento', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('unidades', models.IntegerField()),
                ('tipoCaja', models.CharField(max_length=10)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateTimeField()),
                ('maq', models.CharField(max_length=100, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('almacen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.alm')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='fisicoQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.TimeField()),
                ('cliente', models.CharField(max_length=20)),
                ('lote', models.CharField(max_length=30)),
                ('nTarima', models.IntegerField()),
                ('loTarima', models.CharField(max_length=30)),
                ('cantidad', models.IntegerField()),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('productos', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Trabajo.materia')),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='despatado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cantidad', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.CharField(max_length=30)),
                ('unidades', models.CharField(max_length=30, null=True)),
                ('tipoCaja', models.CharField(max_length=30, null=True)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('horaEnvio', models.DateTimeField()),
                ('en_almacen', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('lote', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.fruta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='congeladoP',
            fields=[
                ('Con', models.IntegerField(primary_key=True, serialize=False)),
                ('pro', models.IntegerField(null=True)),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgDesp', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('cajas', models.CharField(max_length=30)),
                ('unidades', models.CharField(max_length=30, null=True)),
                ('tipoCaja', models.CharField(max_length=30, null=True)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('status', models.CharField(max_length=30, null=True)),
                ('cliente', models.CharField(max_length=30, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('horaEnvio', models.DateTimeField(auto_now_add=True)),
                ('fechaOriginal', models.DateTimeField(blank=True, editable=False, null=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('nombre', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.materia')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='congelado',
            name='lote',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Trabajo.lavado'),
        ),
        migrations.AddField(
            model_name='congelado',
            name='nombre',
            field=models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.materia'),
        ),
        migrations.AddField(
            model_name='congelado',
            name='tarima',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.paleta'),
        ),
        migrations.AddField(
            model_name='congelado',
            name='tipoCaja',
            field=models.ForeignKey(max_length=30, null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje'),
        ),
        migrations.AddField(
            model_name='congelado',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='concervacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lote', models.CharField(max_length=30, verbose_name=Aplicaciones.Trabajo.models.quebrado)),
                ('tarima', models.IntegerField()),
                ('aceptado', models.BooleanField(default=False)),
                ('cajas', models.CharField(max_length=30)),
                ('kgT', models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('hora', models.TimeField(null=True)),
                ('cliente', models.CharField(max_length=30)),
                ('destino', models.CharField(blank=True, max_length=100, null=True)),
                ('fecha_aceptacion', models.DateTimeField(blank=True, null=True)),
                ('aceptador', models.CharField(blank=True, max_length=30, null=True)),
                ('nombre', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.materia')),
                ('tipoCaja', models.ForeignKey(max_length=30, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.embalaje')),
            ],
        ),
        migrations.CreateModel(
            name='compras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('cantidad', models.DecimalField(decimal_places=3, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateField()),
                ('usuario', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='alfrut',
            fields=[
                ('movimiento', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=100)),
                ('unidades', models.IntegerField()),
                ('tipoCaja', models.CharField(max_length=10)),
                ('tarima', models.CharField(max_length=30, null=True)),
                ('kg', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('kgNetos', models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)])),
                ('fecha', models.DateTimeField()),
                ('maq', models.CharField(max_length=100, null=True)),
                ('en_almacen', models.BooleanField(default=True)),
                ('estado', models.CharField(choices=[('en_almacen', 'En Almacén'), ('en_maquila', 'En Maquila')], default='en_almacen', max_length=20)),
                ('almacen', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Trabajo.alm')),
                ('proveedor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Trabajo.proveedores')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]