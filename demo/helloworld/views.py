from django.views import generic
from django.shortcuts import render, redirect
from django.forms import formset_factory
#from formtools.wizard.views import SessionWizardView

from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url

from . import forms, models
from django.shortcuts import render, get_object_or_404
#https://www.youtube.com/watch?v=KbOei4IRinc

from .forms import PostForm, VisitaForm, ProcesoVisita, VisitaForm
from .models import Solicitud

#Las vistas a continuación descritas, importan uno de los formularios creados
#Buscando sobreescribir la vista de viewflow


@flow_view
def solicitud(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.ProcesoSolicitudF(request.POST or None)
    #g = request.user.groups.values_list('Coordinador', flat=True)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.patient = form.cleaned_data['id_solicitud']
        sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })

@flow_view
def visita(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.VisitaForm(request.POST or None)
    #g = request.user.groups.values_list('Coordinador', flat=True)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.patient = form.cleaned_data['id_visita']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })


@flow_view
def Acta(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Acta(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.acta = form.cleaned_data['id_acta']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })


@flow_view
def Informe(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Informe(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.acta = form.cleaned_data['id_informe']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })


@flow_view
def Resolucion(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Resolucion(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.acta = form.cleaned_data['id_resolucion']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })

@flow_view
#vista que importa el formulario balance
def balance(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Balance(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['id_balance']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })

@flow_view
#vista que importa el formulario respuesta
def respuesta(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Respuesta(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['id_solicitud']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })



@flow_view
#vista que importa el formulario respuesta
def Recaudo(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Recaudo(request.POST or None, request.FILES)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['numero_recaudo']
        #sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })
    
    
@flow_view
#vista que importa el formulario respuesta
def balance(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Balance(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['id_balance']
        sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })
    
@flow_view
#vista que importa el formulario respuesta
def paz_y_salvo(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.paz_y_salvo(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['id_paz_y_salvo']
        sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })


@flow_view
#vista que importa el formulario respuesta
def seguimiento(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.Seguimiento(request.POST or None)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.balance = form.cleaned_data['id_balance']
        sample.taken_by = request.user
        sample.save()

        request.activation.process.sample = sample
        request.activation.done()

        return redirect(get_next_task_url(request, request.activation.process))

    return render(request, 'sample2.html', {
        'form': form,
        'activation': request.activation
    })
    
    
    
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

@flow_view
def Subir_acta(request, **kwargs):	
	if request.method == 'POST':
		form = Subir_acta(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			
			return redirect(get_next_task_url(request))
	
	else:
		form = Subir_acta()
		
	return render(request, 'sample2.html', {
	    'form': form,
    })
