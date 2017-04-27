from viewflow import flow, frontend
from viewflow.base import this, Flow
from viewflow.flow.views import CreateProcessView, UpdateProcessView
from . import views, models


@frontend.register
class ProcesoSolicitud(Flow):
    process_class = models.ProcesoSolicitud
    summary_template = "'{{ process.titulo }}'"


    Iniciar_Proceso = (
        flow.Start(
            CreateProcessView,
            fields = ['titulo']
        ).Next(this.Iniciar)
    )

    Iniciar = (
        flow.View(
            views.second_blood_sample,
            fields = '__all__'
        ).Permission(
                auto_create=True
        ).Next(this.setDependencia)
    )

    setDependencia = (
        flow.View(
            UpdateProcessView,
            fields=["coordinacion"]
        ).Permission(
            auto_create=True
        )
        .Assign(username='sec')
        .Next(this.setDependencia2)
    )

    setDependencia2 = (
        flow.If(lambda activation: activation.process.coordinacion == '1')
        .Then(this.asignar)
        .Else(this.end)
           )

    asignar = (
        flow.View(
            UpdateProcessView,
            fields=["usuario"]
        ).Permission(
            auto_create=True
        )
        .Assign(username='coo')
        .Next(this.Verificar)
    )

    check_approve3 = (
        flow.If(lambda activation: activation.process.usuario.username == 'yurs')  # toca verificar si es un tecnico
        .Then(this.Verificar)
        .Else(this.end)
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


# ---------- Metodos -----------
    imprimir = (
        flow.Handler(
            this.print_message_Ys
        ).Next(setDependencia2)
    )


    def print_message_Ys(self, activation):
        print(type(activation.process.coordinacion))
        print(activation.process.coordinacion)
        print(activation.process.coordinacion=="1")


@frontend.register
class HelloWorldFlow(Flow):
    """    
    Proceso visita.
    """
    process_class = models.ProcesoVisita
    #lock_impl = lock.select_for_update_lock

    summary_template = "'{{ process.titulo }}'"

    Iniciar = (
        flow.Start(
            CreateProcessView,
            fields=['titulo']
        ).Next(this.Inicio)
    )


    Inicio = (
        flow.View(
            views.visita,
            )
            .Next(this.approve)
        )

    approve = (
        flow.View(
            views.Acta,
            task_description ="Requiere aprobacion",
            task_result_summary="La tarea ha sido {{ process.approved|yesno:'Approved,Rejected' }}")
            .Permission(auto_create=True)
            .Next(this.check_approve)
    )
    # biomasa = (  # La solicitud es de más de 1000 kiligramos?
    #     flow.View(
    #         UpdateProcessView,
    #
    #         fields=["mayor_a_1000"]
    #         ).Permission(auto_create=True)
    #         .Next(this.check_approve)
    #     )

    check_approve = (
        flow.View(
            views.Acta,
            flow.If(lambda act: act.process.kilogramos_biomasa)
                .Then(this.inform)
                .Else(this.viabilidad)
            )

        )
    #     flow.If(cond=lambda act: act.process.views.Acta.kilogramos_biomasa>1000)
    #         .Then(this.inform)
    #         .Else(this.viabilidad)
    # )
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
            .Assign(lambda activation: activation.process.requiere_compensar)
            .Next(this.check_approve)
    )

    check_viabilidad = (
        flow.If(lambda activation: activation.process.requiere_compensar)
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
            .Assign(lambda activation: activation.process.requiere_compensar)
            .Next(this.check_approve)
    )

    check_compensacion = (
        flow.If(lambda activation: activation.process.requiere_compensar)
            .Then(this.compensar)
            .Else(this.respuesta)
    )

    respuesta = (
        flow.View(
            views.respuesta,
        ).Next(this.end)
    )

    end = flow.End()

    def send_hello_world_request(self, activation):
        with open(os.devnull, "w") as world:
            world.write(activation.process.titulo)

#     )


    end = flow.End()

