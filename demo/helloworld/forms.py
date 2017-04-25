from django import forms
from material.base import Layout, Row, Span2
from . import models

# Formularios que importan los modelos, creando una conexión
# entre el proceso y el modelo real.
# Su fin es mostrar un formulario con los campos de la tabla
# correspondiente al modelo deseado
# y no al modelo de tipo proceso.


class PatientForm(forms.ModelForm):
    layout = Layout(
        Row('nombre', 'nombre_solicitate'),
        Row('direccion_solicitud', 'barrio_solicitud'),
        Row('municipio','fecha',)
    )

    class Meta:
        model = models.Solicitud
        fields = '__all__'


class ProcesoSolicitudF(forms.ModelForm):
    layout = Layout(
        Row('nombre', 'nombre_solicitate'),
        Row('direccion_solicitud', 'barrio_solicitud'),
        Row('municipio', 'fecha', )
    )

    class Meta:
        model = models.Solicitud
        fields = '__all__'

class ProcesoVisitaF(forms.ModelForm):
    layout = Layout(
        Row('id_visita', 'fecha_agendada', 'kilogramos_biomasa'),
        Row('detalles'),
        Row('id_arbol', 'id_solicitud')
    )

    class Meta:
        model = models.Visita
        fields = '__all__'



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
