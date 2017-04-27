from django.views import generic
from django.shortcuts import render, redirect
from django.forms import formset_factory
from formtools.wizard.views import SessionWizardView

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
def second_blood_sample(request, **kwargs):
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
def check_biomasa(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.VisitaForm(request.POST or None)
    #g = request.user.groups.values_list('Coordinador', flat=True)

    if form.is_valid():
        sample = form.save(commit=False)
        sample.patient = form.cleaned_data['kilogramos_biomasa']
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
    form = forms.respuesta(request.POST or None)

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

