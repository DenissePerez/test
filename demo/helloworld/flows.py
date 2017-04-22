from viewflow import flow
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from . import views, models
from viewflow import frontend




@frontend.register
class ProcesoPrueba(Flow):
    process_class = models.ProcesoPrueba

    start = (
        flow.Start(
            CreateProcessView,
            fields=["text", "fecha"]
        ).Permission(
            auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        ).Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)


@frontend.register
class ProcesoSolicitud(Flow):
    process_class = models.ProcesoSolicitud

    Iniciar = (
        flow.Start(
            views.second_blood_sample,
            fields = '__all__'
        ).Permission(
                auto_create=True
        ).Next(this.approve)
    )

    approve = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(

            auto_create=True
        )
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.check_approve)
    )


    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.send)
        .Else(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)


#@frontend.register
#class Visita(Flow):
#    process_class = Visita

#    start = (
#        flow.Start(
#            CreateProcessView,
#            fields=["id_visita", "detalles", "id_arbol", "id_solicitud", "fecha"]
#        ).Permission(
#           auto_create=False
#        ).Next(this.approve)
#   )

#    approve = (
#        flow.View(
#            UpdateProcessView,
#            fields=["approved"]
#        ).Permission(
#            auto_create=True
#        ).Next(this.check_approve)
#    )

#    check_approve = (
#        flow.If(lambda activation: activation.process.approved)
#        .Then(this.send)
#        .Else(this.end)
#    )

#    send = (
#        flow.Handler(
#            this.send_hello_world_request
#        ).Next(this.end)
#    )

#    end = flow.End()

#    def send_hello_world_request(self, activation):
#        print(activation.process.text)