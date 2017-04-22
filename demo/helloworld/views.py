from django.views import generic
from django.shortcuts import render, redirect
from formtools.wizard.views import SessionWizardView

from viewflow.decorators import flow_start_view, flow_view
from viewflow.flow.views import StartFlowMixin, FlowMixin
from viewflow.flow.views.utils import get_next_task_url

from . import forms, models
from django.shortcuts import render, get_object_or_404
#https://www.youtube.com/watch?v=KbOei4IRinc

from .forms import PostForm
from .models import Solicitud



class FirstBoodSampleView(StartFlowMixin, SessionWizardView):
    template_name = 'sample.html'


    form_list = [forms.PatientForm, forms.ProcesoSolicitudF]
    #form = form_list(request.POST or None)

    def done(self, form_list, form_dict, **kwargs):
        nombre = form_dict['0'].save()

        sample = form_dict['1'].save(commit=False)
        sample.nombre = nombre
        sample.nombre_solicitate = self.request.user
        sample.save()

        self.activation.process.sample = sample
        self.activation.done()

        return redirect(get_next_task_url(self.request, self.activation.process))



@flow_start_view
def second_blood_sample(request, **kwargs):
    request.activation.prepare(request.POST or None, user=request.user)
    form = forms.ProcesoSolicitudF(request.POST or None)

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





class GenericTestFormView(FlowMixin, generic.CreateView):
    """A generic view to save blood test data.
    Assumes that test data model have FK `sample` field. The view can
    be parametrized directly in flow definition.
    """
    def form_valid(self, form):
        test_data = form.save(commit=False)
        test_data.sample = self.activation.process.sample
        test_data.save()
        self.activation_done()
        return redirect(self.get_success_url())