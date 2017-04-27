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

class BiomasaForm(forms.ModelForm):
    class Meta:
        model = models.Visita #Modelo al que referencio
        fields = ['kilogramos_biomasa']

class ProcesoVisita(forms.ModelForm):
    class Meta:
        model = models.ProcesoVisita
        fields = ['titulo']


class Acta(forms.ModelForm):
    class Meta:
        model = models.Acta
        fields = ['id_acta', 'id_visita', 'descripcion']


class Informe(forms.ModelForm):
    class Meta:
        model = models.Informe_tecnico
        fields = '__all__'


class Balance(forms.ModelForm):
    class Meta:
        model = models.Balance
        fields = '__all__'


class respuesta(forms.ModelForm):
    class Meta:
        model = models.Respuesta
        fields = '__all__'
