from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django import forms
from django.core.validators import MinValueValidator
from Aplicaciones.cuentas.models import catalogoEmp
# Create your models here.


   
class producto(models.Model):
    codigo = models.CharField(primary_key=True,unique=True,max_length=30)
    descripcion = models.CharField(max_length=100)
    
class Rol(models.Model):
    modulo = models.CharField('Nombre del Rol',max_length=30)

    def __str__(self):
        return self.modulo
class alm(models.Model):
    lugar = models.CharField(max_length=30)

    def __str__(self):
        return self.modulo

class proveedores(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False)
    nombre = models.CharField(max_length=30)
    saldo = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)],null=True, default=0)
    dias_vencimiento = models.IntegerField(null=True)
    saldo_cajas = models.IntegerField(null=True)
    tipo = models.ForeignKey(catalogoEmp, on_delete=models.CASCADE ,null=True)
    def __str__(self):
        return self.nombre


class pagosProv(models.Model):
    nombre = models.ForeignKey(proveedores, on_delete=models.CASCADE ,null=True)
    total = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fechaPago = models.DateField()
    refe =  models.CharField(max_length=30, null=True)
    formaPago = models.CharField(max_length=30, null=True)
    movi = models.CharField(max_length=255, blank=True,null=True) 

class UsuarioManager(BaseUserManager):
    def create_user(self,  username, rol,email ,password=None):
        user = self.model(
            username=username,
            rol=rol,
            email=self.normalize_email(email)
        )

        user.set_password(password)  # Encriptar el password antes de guardarlo
        user.save()
        return user

    def create_superuser(self, username, email, rol, password):
        # Buscar la instancia del rol a partir del ID proporcionado
        try:
            rol_instance = Rol.objects.get(id=rol)
        except Rol.DoesNotExist:
            raise ValueError('El rol especificado no existe.')

        user = self.create_user(
            username=username,
            rol=rol_instance,
            email=email
            
        )
        user.set_password(password)
        user.usuario_administrador = True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser):
    username = models.CharField('Nombre de usuario', unique=True, max_length=100)
    nombres = models.CharField('Nombres', max_length=200, blank=True, null=True)
    apellidos = models.CharField('Apellidos', max_length=200, blank=True, null=True)
    email =models.EmailField("Correo Electronico", max_length=254, unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True, verbose_name='Rol')
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager()
    foto = models.ImageField(upload_to='fotos_perfil/', null=True, blank=True)
    capturando = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['rol','email']

    def __str__(self):
        return f'{self.rol}, {self.nombres}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador

class Nota(models.Model):
    folio = models.IntegerField(primary_key=True, unique=True)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    totalK = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    totalP = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    totalC = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    totalT = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    taraC = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    taraT = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    fecha = models.DateField(null=True)
    kilosB = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    kilosN = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],null=True)
    unidades= models.IntegerField(null=True)
    movi = models.CharField(max_length=255, blank=True,null=True) 
    movi2 = models.CharField(max_length=255, blank=True,null=True) 
    proveedor= models.CharField(max_length=50,null=True)
    nombre = models.CharField(max_length=100,null=True)
    usuario = models.CharField(max_length=100,null=True)
    prov = models.ForeignKey(proveedores, on_delete=models.CASCADE ,null=True)
    vencido = models.BooleanField(default=False)
    en_pago = models.BooleanField(default=False)
    pago = models.ForeignKey(pagosProv, on_delete=models.SET_NULL, null=True, blank=True)





class embalaje(models.Model):
    nombre = models.CharField(max_length=20,null=True)
    peso = models.DecimalField(max_digits=10,null=True, decimal_places=2, validators=[MinValueValidator(0)])

class paleta(models.Model):
    nombre = models.CharField(max_length=20,null=True)
    peso = models.DecimalField(max_digits=10,null=True, decimal_places=2, validators=[MinValueValidator(0)])

class materia(models.Model):
    nombre = models.CharField(max_length=20,null=True)
    codigo = models.CharField(max_length=20,null=True)
    catalogo = models.CharField(max_length=5,null=True)
class SalidaStock(models.Model):
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE)
    unidades = models.IntegerField(validators=[MinValueValidator(0)])
    fecha = models.DateField()
    tipo = models.ForeignKey(embalaje, on_delete=models.CASCADE,null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return f"Salida de {self.unidades} unidades para {self.proveedor.nombre} el {self.fecha}"
class recep(models.Model):
    fruta = models.ForeignKey(materia,max_length=100,null=True,on_delete=models.SET_NULL)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    variedad = models.CharField(max_length=50,null=True)
    productor = models.ForeignKey(proveedores, on_delete=models.SET_NULL, null=True, blank=True)
    brix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    ph = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    muestra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tipoCaja = models.CharField(max_length= 100,null=True)
    #Evaluacion
    mancha = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    tamano = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    caracter = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sMadura = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    defecto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    verde = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    podrida = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    lodo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    #Evaluacion del transporte
    larva = models.CharField(max_length=100,null=True)
    mExtrana = models.CharField(max_length=100,null=True)
    limpieza = models.CharField(max_length=100,null=True)
    aQuimicos = models.CharField(max_length=100,null=True)
    aPlagas = models.CharField(max_length=100,null=True)
    tDefecto = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    descuento = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    muestreo = models.ImageField(upload_to='muestreo/', null=True, blank=True)
     # ... (otros campos)
    en_nota = models.BooleanField(default=False)
    nota = models.ForeignKey(Nota, on_delete=models.SET_NULL, null=True, blank=True)

class fisicoQ(models.Model):
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.CharField(max_length=20)
    productos = models.ForeignKey(materia,on_delete=models.SET_NULL ,null=True)
    lote = models.CharField(max_length=30)
    nTarima = models.IntegerField()
    loTarima = models.CharField(max_length=30)
    cantidad = models.IntegerField()
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True)

class fisico(models.Model):
    productos = models.CharField(max_length=200)
    presentacion = models.CharField (max_length=200)
    tMuestra = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    hora = models.TimeField()
    cliente = models.CharField(max_length=20)
    lote = models.CharField(max_length=30)
    brix = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    ph = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hoja = models.IntegerField()
    podrida = models.CharField(max_length=200)
    sabor = models.CharField(max_length=200)
    defecto = models.IntegerField()
    color = models.IntegerField()
    caracter = models.IntegerField()
    tamano = models.IntegerField()
    mExtrana = models.CharField(max_length=100,null=True)
    empaque = models.CharField(max_length=100,null=True)
    embalaje = models.CharField(max_length=100,null=True)
    producto = models.CharField(max_length=100,null=True)


class fruta(models.Model):
    movimiento = models.IntegerField(primary_key=True,null=False)
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE, null=True)
    nombre= models.ForeignKey(materia,on_delete=models.SET_NULL,null=True )
    almacen = models.ForeignKey(alm, on_delete=models.DO_NOTHING, null=True)
    unidades= models.IntegerField()
    tipoCaja= models.ForeignKey(embalaje,on_delete=models.SET_NULL,null=True )
    tarima = models.ForeignKey(paleta,on_delete=models.SET_NULL,null=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField()
    maq = models.CharField(max_length=100, null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora = models.TimeField(null=True)
    maquila_origen = models.CharField(max_length=30,null=True)
     # ... (otros campos)
    en_nota = models.BooleanField(default=False)
    nota = models.ForeignKey(Nota, on_delete=models.SET_NULL, null=True, blank=True)

    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.movimiento}'
class alfrut(models.Model):
    movimiento = models.IntegerField(primary_key=True,null=False)
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE, null=True)
    almacen = models.ForeignKey(alm, on_delete=models.DO_NOTHING, null=True)
    nombre = models.CharField(max_length=100)
    unidades= models.IntegerField()
    tipoCaja= models.CharField(max_length=10)
    tarima = models.CharField(max_length=30, null=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField()
    maq = models.CharField(max_length=100, null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.movimiento}'
    def __str__(self):
        # Formatea la fecha como "DD/MM/YY"
        return self.fecha1.strftime("%y/%m/%d")  
class frigoe(models.Model):
    movimiento = models.IntegerField(primary_key=True,null=False)
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE, null=True)
    almacen = models.ForeignKey(alm, on_delete=models.DO_NOTHING, null=True)
    nombre = models.CharField(max_length=100)
    unidades= models.IntegerField()
    tipoCaja= models.CharField(max_length=10)
    tarima = models.CharField(max_length=30, null=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField()
    maq = models.CharField(max_length=100, null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.movimiento}'
    def __str__(self):
        # Formatea la fecha como "DD/MM/YY"
        return self.fecha1.strftime("%y/%m/%d")  

class proTer(models.Model):
    movimiento = models.IntegerField(primary_key=True,null=False)
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE, null=True)
    almacen = models.ForeignKey(alm, on_delete=models.DO_NOTHING, null=True)
    nombre = models.CharField(max_length=100)
    unidades= models.IntegerField()
    tipoCaja= models.CharField(max_length=10)
    tarima = models.CharField(max_length=30, null=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField()
    maq = models.CharField(max_length=100, null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.movimiento}'
    def __str__(self):
        # Formatea la fecha como "DD/MM/YY"
        return self.fecha1.strftime("%y/%m/%d")  
    
class ventas(models.Model):
    movimiento = models.IntegerField(primary_key=True,null=False)
    proveedor = models.ForeignKey(proveedores, on_delete=models.CASCADE, null=True)
    almacen = models.ForeignKey(alm, on_delete=models.DO_NOTHING, null=True)
    nombre = models.CharField(max_length=100)
    unidades= models.IntegerField()
    tipoCaja= models.CharField(max_length=10)
    tarima = models.CharField(max_length=30, null=True)
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    fecha = models.DateTimeField()
    maq = models.CharField(max_length=100, null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.movimiento}'
    def __str__(self):
        # Formatea la fecha como "DD/MM/YY"
        return self.fecha1.strftime("%y/%m/%d")  
class Maquila(models.Model):
    lote = models.ForeignKey(fruta, on_delete=models.CASCADE)
    nombre = models.ForeignKey(materia, max_length=30,on_delete=models.CASCADE)
    maquila = models.CharField(max_length=30)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.IntegerField(null=True)
    unidades=models.IntegerField(null=True)
    tipoCaja=models.ForeignKey(embalaje,max_length=30,null=True, on_delete=models.CASCADE)
    tarima = models.ForeignKey(paleta,max_length=30,null=True, on_delete=models.CASCADE)
    horaEnvio = models.DateTimeField()
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora= models.TimeField(null=True)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')
    def __str__(self):
        return f'{self.id}'
    

class despatado(models.Model):
    lote = models.ForeignKey(fruta, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=30)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cantidad = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.CharField(max_length=30)
    unidades=models.CharField(max_length=30,null=True)
    tipoCaja=models.CharField(max_length=30,null=True)
    tarima=models.CharField(max_length=30,null=True)
    horaEnvio = models.DateTimeField()
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')
    def __str__(self):
        return f'{self.id}'


class lavado(models.Model):
    lote = models.ForeignKey(fruta, on_delete=models.CASCADE)
    nombre = models.ForeignKey(materia, max_length=30,on_delete=models.CASCADE)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgDesp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.IntegerField()
    tipoCaja=models.ForeignKey(embalaje,max_length=30,null=True, on_delete=models.CASCADE)
    tarima=models.ForeignKey(paleta,max_length=30,null=True, on_delete=models.CASCADE)
    horaEnvio = models.DateField()
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora =  models.TimeField(null=True)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')

    def __str__(self):
        return f'{self.id}'

class congelado(models.Model):
    lote = models.ForeignKey(lavado, on_delete=models.CASCADE)
    nombre = models.ForeignKey(materia,max_length=30, on_delete=models.CASCADE)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgDesp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.IntegerField()
    tipoCaja=models.ForeignKey(embalaje,max_length=30,null=True, on_delete=models.CASCADE)
    tarima=models.ForeignKey(paleta,max_length=30,null=True, on_delete=models.CASCADE)
    horaEnvio = models.DateField()
    cliente = models.CharField(max_length=30)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora =  models.TimeField(null=True)



    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')
    def __str__(self):
        return f'{self.id}'

class quebrado(models.Model):
    lote = models.ForeignKey(congelado, on_delete=models.CASCADE)
    nombre = models.ForeignKey(materia,max_length=30, on_delete=models.CASCADE)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgDesp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.CharField(max_length=30)
    tipoCaja=models.ForeignKey(embalaje,max_length=30,null=True, on_delete=models.CASCADE)
    tarima=models.ForeignKey(paleta,max_length=30,null=True, on_delete=models.CASCADE)
    horaEnvio = models.DateField()
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    hora =  models.TimeField(null=True)



    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')
    def __str__(self):
        return f'{self.id}'

class Desperdicio(models.Model):
    lote = models.CharField(max_length=30)
    cantidad = models.FloatField(max_length=10)
    #poner fecha de retorno para saber cuando se llevo a cabo


class concervacion(models.Model):
    lote = models.CharField(quebrado,max_length=30)
    tarima = models.IntegerField()
    aceptado = models.BooleanField(default=False)
    nombre = models.ForeignKey(materia,max_length=30, on_delete=models.CASCADE)
    cajas = models.CharField(max_length=30)
    tipoCaja = models.ForeignKey(embalaje,max_length=30, on_delete=models.CASCADE)
    kgT = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    hora =  models.TimeField(null=True)
    cliente = models.CharField(max_length=30)
    destino = models.CharField(max_length=100, blank=True, null=True)
    fecha_aceptacion = models.DateTimeField(blank=True, null=True)
    aceptador = models.CharField(max_length=30,blank=True, null=True)


    
    def __str__(self):
        return f'{self.id}'

class ordenes(models.Model):
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    clave = models.CharField(max_length=30)
    aceptado = models.BooleanField(default=False)
    producto = models.CharField(max_length=30)
    fecha = models.DateField()
    po = models.IntegerField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)
    fecha_aceptacion = models.DateTimeField(blank=True, null=True)
    aceptador = models.CharField(max_length=30,blank=True, null=True)

class compras(models.Model):
    nombre = models.CharField(max_length=30)
    cantidad = models.DecimalField(max_digits=10, decimal_places=3, validators=[MinValueValidator(0)])
    fecha = models.DateField()
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE,null=True)


class congeladoP(models.Model):
    Con = models.IntegerField(primary_key=True)
    pro = models.IntegerField(null=True)
    nombre = models.ForeignKey(materia,max_length=30,on_delete=models.DO_NOTHING)
    kgNetos =models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kg = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    kgDesp = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    cajas = models.CharField(max_length=30)
    unidades=models.CharField(max_length=30,null=True)
    tipoCaja=models.CharField(max_length=30,null=True)
    tarima=models.CharField(max_length=30,null=True)
    horaEnvio = models.DateTimeField()
    status = models.CharField(max_length=30,null=True)
    cliente = models.CharField(max_length=30,null=True)
    en_almacen = models.BooleanField(default=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    horaEnvio = models.DateTimeField(auto_now_add=True)
    fechaOriginal = models.DateTimeField(editable=False, null=True, blank=True)


    ESTADO_FRUTA = (
        ('en_almacen', 'En Almacén'),
        ('en_maquila', 'En Maquila'),
    )
    estado = models.CharField(max_length=20, choices=ESTADO_FRUTA, default='en_almacen')
    def __str__(self):
        return f'{self.id}'



