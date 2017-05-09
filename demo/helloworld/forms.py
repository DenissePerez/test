from django import forms
from django.forms import formset_factory
from material.base import Layout, Row, Span2
from . import models


# Formularios que importan los modelos, creando una conexión
# entre el proceso y el modelo real.
# Su fin es mostrar un formulario con los campos de la tabla
# correspondiente al modelo deseado
# y no al modelo de tipo proceso.


class ProcesoSolicitudF(forms.ModelForm):
    class Meta:
        model = models.Solicitud
        fields = ['nombre_solicitate', 'identificacion_solicitate',
                  'direccion_solicitate', 'barrio_solicitate',
                  'id_solicitud', 'nombre', 'id_expediente',
                  'direccion_solicitud', 'barrio_solicitud', 'municipio',
                  'fecha', 'fecha_respuesta']



class ProcesoSolicitudForm(ProcesoSolicitudF):
    patient = forms.ModelChoiceField(queryset=models.Solicitud.objects.all())


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Solicitud #Modelo al que referencio
        fields = '__all__'


class VisitaForm(forms.ModelForm):
    class Meta:
        model = models.Visita #Modelo al que referencio
        fields = '__all__'

 
class ProcesoVisita(forms.ModelForm):
    class Meta:
        model = models.ProcesoVisita
        fields = ['titulo']


class Acta(forms.ModelForm):
    class Meta:
        model = models.Acta
        fields = ['id_acta', 'id_visita', 'descripcion']
        
class Subir_acta(forms.ModelForm):
    class Meta:
        model = models.Subir_acta
        fields = ['id_acta']


class Informe(forms.ModelForm):
    class Meta:
        model = models.Informe_tecnico
        fields = ['id_informe', 'nombre', 'descripcion']


class Resolucion(forms.ModelForm):
    class Meta:
        model = models.Resolucion
        fields = '__all__'
        

class Balance(forms.ModelForm):
    class Meta:
        model = models.Balance
        fields = '__all__'


class Respuesta(forms.ModelForm):
    class Meta:
        model = models.Respuesta
        fields = '__all__'


class Recaudo(forms.ModelForm):
    class Meta:
        model = models.Recaudo
        fields = '__all__'


class paz_y_salvo(forms.ModelForm):
    class Meta:
        model = models.paz_y_salvo
        fields = '__all__'
        
class Seguimiento(forms.ModelForm):
	class Meta:
		model = models.Seguimiento
		fields = '__all__'


class Notificacion(forms.ModelForm):
	class Meta:
		model = models.Notificacion
		fields = '__all__'

class ActaRequerimiento(forms.ModelForm):
    class Meta:
        model = models.ActaRequerimiento
        fields = '__all__'
        
        
