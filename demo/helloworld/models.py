from datetime import timezone, datetime, timedelta, date
from django.db import models
from django.core.validators import RegexValidator
from viewflow.models import Process
from django.contrib import auth
from django.contrib.auth.models import User, UserManager, Group
from django import forms
from filer.fields.image import FilerFileField
from django.contrib.auth.models import User


class ProcesoPrueba(Process):
    text = models.CharField(max_length=150)
    approved = models.BooleanField(default=False)
    fecha = models.DateField(null=True)


class CustomUser(User):
    telefono = models.CharField(max_length=10, null=True)

    #class Meta:
    #    abstract = True

class Solicitante(models.Model):
    nombre_solicitate = models.CharField(max_length=200, default='')
    identificacion_solicitate = models.CharField(max_length=12, validators=[RegexValidator(r'^\d{1,12}$')], default='')
    direccion_solicitate = models.CharField(max_length=100, null=True)
    barrio_solicitate = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    #def __str__(self):
    #    return self.id_solicitante


class Balance(models.Model):
    id_balance = models.CharField(primary_key=True, max_length=8, validators=[RegexValidator(r'^\d{1,8}$')])
    descripcion = models.CharField(max_length=200)
    valor_compensado = models.DecimalField(max_digits=15, decimal_places=2, default='0,00')
    valor_afectacion = models.DecimalField(max_digits=15, decimal_places=2, default='0,00')
    valor_balance = models.DecimalField(max_digits=15, decimal_places=2, default='0,00')


class Timestampable(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Informe_tecnico(Timestampable):
    id_informe = models.CharField(primary_key=True, max_length=8, validators=[RegexValidator(r'^\d{1,8}$')])
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    informe = FilerFileField(null=True)

    def __str__(self):
        return self.id_informe


class Expediente(models.Model):
    id_expediente = models.CharField(primary_key=True, max_length=5, validators=[RegexValidator(r'^\d{1,5}$')])
    nombre = models.CharField(max_length=200)
    resolucion = models.CharField(max_length=12, blank=True, null=True)
    autorizacion = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return self.id_expediente



class Recaudo(models.Model):
    numero_recaudo = models.CharField(primary_key=True, max_length=12, validators=[RegexValidator(r'^\d{1,12}$')])
    banco = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=15, decimal_places=2, default='0,00')
    evidencia = FilerFileField(null=True)

    def __str__(self):
        return self.numero_recaudo


class Solicitud(Solicitante, models.Model):
    id_solicitud = models.CharField(primary_key=True, max_length=15)
    nombre = models.CharField(max_length=200, unique=True)  # Agregar en el modelo!!! Importante!!!!
    id_expediente = models.ForeignKey(Expediente, blank=True, null=True, on_delete=models.CASCADE)
    #id_solicitante = models.ForeignKey(Solicitante, blank=True, null=True, on_delete=models.CASCADE)
    direccion_solicitud = models.CharField(max_length=100, default=' ')
    barrio_solicitud = models.CharField(max_length=100, default=' ')
    municipio = models.CharField(max_length=100, default=' ')
    fecha = models.DateField(default=date.today)  # Agregar!
    fecha_respuesta = models.DateField(default=datetime.now()+timedelta(days=18))
    #asignar_a = models.ManyToManyField(Empleado, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.id_solicitud



class Anexo(models.Model):
    id_anexo = models.CharField(primary_key=True, max_length=12)
    nombre = models.CharField(max_length=200)
    anexo = FilerFileField(null=True)
    id_solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre



class Ficha_individuo(models.Model):
    id_arbol = models.CharField(primary_key=True, max_length=8)
    #coordenadas!!! geodjango con point
    #coordenadas = Point(x=...., y=...., z=0, srid=....) #LocationPoint()
    latitud = models.DecimalField(max_digits=15, decimal_places=6, null=True)
    longitud = models.DecimalField(max_digits=15, decimal_places=6, null=True)
    nombre = models.CharField(max_length=100)
    familia = models.CharField(max_length=100)
    estado = models.CharField(max_length=300)
    altura = models.FloatField()
    dap = models.FloatField()
    valor = models.DecimalField(max_digits=15, decimal_places=2, default='0,00')

    def __str__(self):
        return self.id_arbol


class AgendarVisita(models.Model):
    fecha_agendada = models.DateTimeField()


class Visita(AgendarVisita):
    id_visita = models.CharField(primary_key=True, max_length=5, validators=[RegexValidator(r'^\d{1,10}$')])
    detalles = models.CharField(max_length=300)
    id_arbol = models.ManyToManyField(Ficha_individuo)
    id_solicitud = models.ForeignKey(Solicitud, blank=True, null=True, on_delete=models.CASCADE)
    kilogramos_biomasa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return self.id_visita


class Empleado(CustomUser):
    solicitud = models.ManyToManyField(Solicitud, blank=True)
    id_visita = models.ForeignKey(Visita, blank=True, null=True, on_delete=models.CASCADE)
    #g = request.user.groups.values_list('name',flat=True)


    class Meta:
        verbose_name = 'Empleado'
    #rol = models.CharField(max_length=1, choices=COORDINACIONES,default='02')

    # Lo que me va a retornar al hacer un query, para que deje de ser "objeto <tecnico>"
    # def __str__(self):
    #    return self.nombre
    # Necesito nombre de la solicitud!!!! D:


class Seguimiento(models.Model):
    id_seguimiento = models.CharField(primary_key=True, max_length=8, validators=[RegexValidator(r'^\d{1,8}$')])
    id_balance = models.OneToOneField(Balance, blank=True, null=True, on_delete=models.CASCADE)
    id_visita = models.ForeignKey(Visita, blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=300)
    adjunto = FilerFileField(null=True)



class Acta(Timestampable):
    id_acta = models.CharField(primary_key=True, max_length=7)
    id_visita = models.ForeignKey(Visita,on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=300)
    #acta = models.FileField(upload_to='img/profile/%Y/%m/')

    def __str__(self):
        return self.descripcion



class Respuesta(models.Model):
    id_solicitud = models.ForeignKey(Solicitud)
    respuesta = FilerFileField(null=True)

class ProcesoSolicitud(Process):
    usuario = models.ForeignKey(Empleado, blank=True, null=True)
    solicitud = models.ForeignKey(Solicitud, blank=True, null=True)
    approved = models.BooleanField(default=True)
    text = models.CharField(max_length=150, default='')

    verificaInfo = models.BooleanField(default=False)
    infoCompleta = models.BooleanField(default=False)
    pagoRealizado = models.BooleanField(default=False)
    agendarVisita = models.DateField(blank=True, null=True)
    realizaVisita = models.BooleanField(default=False)
    def __str__(self):
        return '%s %s' (self.descripcion, self.text)




class ProcesoVisita(Process):
    #usuario = models.ForeignKey(Empleado, blank=True, null=True)
    solicitud = models.ForeignKey(Solicitud, blank=True, null=True)
    approved = models.BooleanField(default=True)
    visita = models.ForeignKey(Visita, blank=True, null=True)
    text = models.CharField(max_length=150, default='')

    mayor_a_1000 = models.BooleanField(default=False)
    requiere_compensar = models.BooleanField(default=False)
    agendarVisita = models.DateField(blank=True, null=True)
    realizaVisita = models.BooleanField(default=False)






