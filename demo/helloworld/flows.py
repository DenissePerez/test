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
            fields=['titulo']
        ).Next(this.Iniciar)
    )

    Iniciar = (
        flow.View(
            views.solicitud,
            fields='__all__'
        ).Permission(
            auto_create=True
        ).Next(this.setDependencia)
    )

    setDependencia = (
        flow.View(
            UpdateProcessView,
            fields=['coordinacion']
        ).Permission(
            auto_create=True
        )
            #.Assign(username='secretaria')
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
            #.Assign(username='coordinador_flora')
            .Next(this.Verificar)
    )

    # check_approve3 = (
    #     flow.If(lambda
    #                 activation: activation.process.usuario.username == 'tecnico_flora')  # toca verificar si es un tecnico
    #         .Then(this.Verificar)
    #         .Else(this.end)
    # )

    Verificar = (
        flow.View(
            UpdateProcessView,
            fields=["informacion_Completa", "pago_Realizado"]
        ).Permission(
            auto_create=True
        )
            #.Assign(lambda activation: activation.process.usuario)
            .Next(this.check_approve2)
    )

    check_approve2 = (
        flow.If(lambda activation: activation.process.informacion_Completa and activation.process.pago_Realizado)
            .Then(this.AgVisita)
            .Else(this.actaRequerimiento)
    )

    actaRequerimiento = (
        flow.View(
            views.ActaRequerimiento,
        )
            #.Assign(lambda activation: activation.process.usuario)
            .Next(this.Verificar)

    )

    AgVisita = (
        flow.View(
            UpdateProcessView,
            fields=["agendar_Visita"])
            #.Assign(lambda activation: activation.process.usuario)
            .Next(this.end)

    )


    end = flow.End()


@frontend.register
class HelloWorldFlow(Flow):
    """    
    Proceso visita.
    """
    process_class = models.ProcesoVisita
    # lock_impl = lock.select_for_update_lock

    summary_template = "'{{ process.titulo }}'"

    Iniciar = (
        flow.Start(
            CreateProcessView,
            fields=['titulo']
        )
            .Next(this.Inicio)
    )

    Inicio = (
        flow.View(
            views.visita,
        )#.Assign(username__contains='tecnico_flora')
            .Next(this.approve)
    )

    approve = (
        flow.View(
            views.Acta,
            task_description="Requiere aprobacion",
            task_result_summary="La tarea ha sido {{ process.approved|yesno:'Approbada,Rechazada' }}"
        )
            .Permission(auto_create=True)
            .Next(this.biomasa)
    )


    biomasa = (  # La solicitud es de más de 1000 kiligramos?
        flow.View(
            UpdateProcessView,
            fields=["mayor_a_1000"]
        ).Permission(auto_create=True)
         .Next(this.check_approve)
    )

    check_approve = (
        flow.If(lambda activation: activation.process.mayor_a_1000)
            .Then(this.informe) #De ser así hacer informe técnico
            .Else(this.compensa) #De lo contrario, preguntar si se requiere compensación
    )

    informe = (
        flow.View(
            views.Informe,
        )#.Assign(username='tecnico_flora')
         .Next(this.aprobar_informe)
    )

    aprobar_informe = (
        flow.View(
            UpdateProcessView,
            fields=["visto_bueno"]
        )#.Assign(username='coodinador_flora')
         .Next(this.verificar_visto_informe)
    )

    verificar_visto_informe = (
        flow.If(lambda act: act.process.visto_bueno)
            .Then(this.resolucion)
            .Else(this.informe)
    )

    resolucion = (
        flow.View(
            views.Resolucion,
        )#.Assign(username='tecnico_flora')
         .Next(this.compensar)
    )

    compensar = (
        flow.View(
            views.balance,
        ).Next(this.end)
    )

    check_viabilidad = (
        flow.If(lambda activation: activation.process.requiere_compensar)
            .Then(this.compensa)
            .Else(this.end)
    )

    compensa = ( #Si la solicitud requiere compensación, vaya a compensaciones
        flow.View(
            UpdateProcessView,
            fields=["requiere_compensar"]
        ).Permission(
            auto_create=True
        )
         #.Assign(lambda activation: activation.process.requiere_compensar)
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


# )

@frontend.register
class Compensacion(Flow):
    """    
    Proceso de Compensacion.
    """
    process_class = models.ProcesoCompensacion
    # lock_impl = lock.select_for_update_lock

    summary_template = "'{{ process.titulo }}'"

    Iniciar = (
        flow.Start(
            CreateProcessView,
            fields=['titulo']
        )
            .Next(this.tipo_compensacion)
    )

    tipo_compensacion = (
        flow.View(
            UpdateProcessView,
            fields=["compensacion_economica"]
        ).Permission(
            auto_create=True
        )#.Assign(username__contains='tecnico_flora')
         .Next(this.check_compensacion)
    )

    check_compensacion = (
        flow.If(lambda activation: activation.process.compensacion_economica)
            .Then(this.recaudar)
            .Else(this.agendar_visita)
    )
    recaudar = (
        flow.View(
            views.Recaudo,
        )
            .Next(this.balance)
    )

    balance = (
        flow.View(
            views.balance,
            task_description="Requiere aprobacion",
            task_result_summary="La tarea ha sido {{ process.approved|yesno:'Approved,Rejected' }}")
            .Permission(auto_create=True)
            .Next(this.balance_en_cero)
    )

    balance_en_cero = (
        flow.View(
            UpdateProcessView,
            fields=["balance_en_cero"]
        ).Permission(
            auto_create=True
        )#.Assign(lambda activation: activation.process.balance_en_cero)
          .Next(this.check_balance_en_cero)
    )

    check_balance_en_cero = (
        flow.If(lambda activation: activation.process.balance_en_cero)
            .Then(this.paz_y_salvo)
            .Else(this.agendar_visita)
    )

    paz_y_salvo = (
        flow.View(
            views.paz_y_salvo,
        ).Next(this.end)
    )

    agendar_visita = (
        flow.View(
            views.seguimiento,
        ).Next(this.end)
    )

    end = flow.End()

@frontend.register
class Seguimiento(Flow):
    """    
    Seguimiento a Compensaciones.
    """
    process_class = models.ProcesoSeguimiento
    # lock_impl = lock.select_for_update_lock

    summary_template = "'{{ process.titulo }}'"

    Iniciar = (
        flow.Start(
            CreateProcessView,
            fields=['titulo']
        ).Next(this.estado)
        )

    estado = (
        flow.View(
            UpdateProcessView,
            fields=["arboles_en_buen_estado"]
        ).Permission(
            auto_create=True
        )  # .Assign(username__contains='tecnico_flora')
            .Next(this.check_compensacion)
    )

    check_compensacion = (
        flow.If(lambda activation: activation.process.arboles_en_buen_estado)
            .Then(this.verificar_tiempo)
            .Else(this.notificar)
    )

    notificar = (
        flow.View(
            views.notificacion,
        ).Permission(
            auto_create=True
        ).Next(this.end)
    )

    verificar_tiempo = (
        flow.View(
            UpdateProcessView,
            fields=["tiempo_cumplido"]
        ).Permission(
            auto_create=True
        )  # .Assign(username__contains='tecnico_flora')
            .Next(this.check_tiempo)
    )


    check_tiempo = (
        flow.If(lambda activation: activation.process.tiempo_cumplido)
            .Then(this.paz_y_salvo)
            .Else(this.agendar_visita)
    )

    paz_y_salvo = (
        flow.View(
            views.paz_y_salvo,
        )
            #task_description="Requiere aprobacion",
            #task_result_summary="La tarea ha sido {{ process.approved|yesno:'Approved,Rejected' }}")
            .Permission(auto_create=True)
            .Next(this.end)
    )

    agendar_visita = (
        flow.View(
            UpdateProcessView,
            fields=["agendarVisita"]
        ).Permission(
            auto_create=True
        )  # .Assign(lambda activation: activation.process.balance_en_cero)
            .Next(this.end)
    )


    end = flow.End()

    def send_hello_world_request(self, activation):
        with open(os.devnull, "w") as world:
            world.write(activation.process.titulo)

    end = flow.End()

