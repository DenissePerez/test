from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from . import views, models





@frontend.register
class Solicitud(Flow):
    process_class = models.ProcesoSolicitud

    Iniciar = (
        flow.Start(
            views.second_blood_sample,
            fields = '__all__'
        ).Permission(
                auto_create=True
        ).Next(this.asignar)
    )


    setDependencia = (
        flow.View(
            UpdateProcessView,
            fields=["approved"]
        ).Permission(
            auto_create=True
        )
        .Assign(username='CoordinadorFlora')
        .Next(this.asignar)
    )

    asignar = (
        flow.View(
            UpdateProcessView,
            #fields=["approved"]
            fields=["approved","solicitud","usuario"]
        ).Permission(
            auto_create=True
        )
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.check_approve)
    )


    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.Verificar)
        .Else(this.setDependencia)
    )


    Verificar = (
        flow.View(
            UpdateProcessView,
            fields=["verificaInfo", "infoCompleta", "pagoRealizado"]
        ).Permission(
            auto_create=True
        )
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.check_approve2)
    )

    check_approve2 = (
        flow.If(lambda activation: activation.process.infoCompleta and activation.process.pagoRealizado )
        .Then(this.AgVisita)
        .Else(this.actaRequerimiento)
    )

    actaRequerimiento = (
        flow.View(
            UpdateProcessView,
            fields=["infoCompleta", "pagoRealizado"]
        )
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.Verificar)

        )


    AgVisita = (
         flow.View(
            UpdateProcessView,
            fields=["agendarVisita"])
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.DoVisita)

        )


    DoVisita = (
         flow.View(
            UpdateProcessView,
            fields=["realizaVisita"])
        .Assign(lambda activation: activation.process.usuario)
        .Next(this.end)

        )

    end = flow.End()

@frontend.register
#Nombre del modelo
class ProcesoVisita(Flow):
    process_class = models.ProcesoVisita #debe importar un modelo tipo Process de viewflow

    Iniciar = (
        flow.Start( #Inicio en Viewflow
            views.visita, #vista crada para tener un formulario
        ).Next(this.act)
    )

    act = ( #se procede al acta
        flow.View(
            views.Acta, #Vista creada para mostrar el formulario del acta
        ).Next(this.biomasa)
    )

    biomasa = ( #Preguntar si la solicitud es de más de 1000 kiligramos
        flow.View(
            UpdateProcessView,
            fields=["mayor_a_1000"]
        ).Permission(
            auto_create=True
            )
            .Assign(lambda activation: activation.process.usuario)
            .Next(this.check_approve)
    )


    check_approve = (
        flow.If(lambda activation: activation.process.approved)
        .Then(this.inform)
        .Else(this.viabilidad)
    )

    inform = (
        flow.View(
            views.Informe,
        ).Next(this.compensar)
    )

    compensar = (
        flow.View(
            views.balance,
        ).Next(this.end)
    )

    viabilidad = (
        flow.View(
            UpdateProcessView,
            fields=["requiere_compensar"]
        ).Permission(
            auto_create=True
        )
            .Assign(lambda activation: activation.process.usuario)
            .Next(this.check_approve)
    )

    check_viabilidad = (
        flow.If(lambda activation: activation.process.approved)
            .Then(this.compensa)
            .Else(this.end)
    )

    compensa = (
        flow.View(
            UpdateProcessView,
            fields=["requiere_compensar"]
        ).Permission(
            auto_create=True
        )
            .Assign(lambda activation: activation.process.usuario)
            .Next(this.check_approve)
    )

    check_compensacion = (
        flow.If(lambda activation: activation.process.approved)
            .Then(this.compensar)
            .Else(this.respuesta)
    )

    respuesta = (
        flow.View(
            views.respuesta,
        ).Next(this.end)
    )

    send = (
        flow.Handler(
            this.send_hello_world_request
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        print(activation.process.text)


