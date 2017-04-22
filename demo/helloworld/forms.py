from django import forms
from material.base import Layout, Row, Span2
from . import models



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



#class BiochemistryForm(forms.ModelForm):
#    class Meta:
#        model = models.Biochemistry
#        fields = ['hemoglobin', 'lymphocytes']


class ProcesoSolicitudForm(ProcesoSolicitudF):
    patient = forms.ModelChoiceField(queryset=models.Solicitud.objects.all())


class PostForm(forms.ModelForm):
    class Meta:
        model = models.Solicitud #Modelo al que referencio
        fields = '__all__'
