from parser import *
from juego_utils import *
from usuarios import iniciar_sesion_consola_restringido
from input_utils import obtener_cadena_de_numeros

def jugar_versus(usuario1:str, password1:str):
    usuario2, password2 = iniciar_sesion_consola_restringido(usuario1)
    categorias_restantes_usuario1 = ["antigua", "clasica", "medieval", "renacimiento", "industrial", "moderna", "atomica", "informacion"]
    categorias_restantes_usuario2 = ["antigua", "clasica", "medieval", "renacimiento", "industrial", "moderna", "atomica", "informacion"]
    puntos_corona_usuario1 = 0
    puntos_corona_usuario2 = 0
    rondas_jugadas_usuario1 = 0
    aciertos_usuario1 = 0
    errores_usuario1 = 0
    rondas_jugadas_usuario2 = 0
    aciertos_usuario2 = 0
    errores_usuario2 = 0

    turno_usuario1 = random.choice([True, False])

    while categorias_restantes_usuario1 and categorias_restantes_usuario2:
        if turno_usuario1:
            (rondas_jugadas_usuario1, aciertos_usuario1, errores_usuario1, turno_usuario1, puntos_corona_usuario1
            ) = jugar_ronda_versus(usuario1, puntos_corona_usuario1, categorias_restantes_usuario1,
                                   rondas_jugadas_usuario1, aciertos_usuario1, errores_usuario1, turno_usuario1)
        elif not turno_usuario1:
            (rondas_jugadas_usuario2, aciertos_usuario2, errores_usuario2, turno_usuario1, puntos_corona_usuario2
            ) = jugar_ronda_versus(usuario2, puntos_corona_usuario2, categorias_restantes_usuario2,
                                   rondas_jugadas_usuario2, aciertos_usuario2, errores_usuario2, turno_usuario1)
    
    if not categorias_restantes_usuario1:
        printear_pantalla_consola_estadisticas_partida(usuario1, rondas_jugadas_usuario1, aciertos_usuario1, errores_usuario1, usuario2, rondas_jugadas_usuario2, aciertos_usuario2, errores_usuario2, usuario1, True)
    else:
        printear_pantalla_consola_estadisticas_partida(usuario1, rondas_jugadas_usuario1, aciertos_usuario1, errores_usuario1, usuario2, rondas_jugadas_usuario2, aciertos_usuario2, errores_usuario2, usuario2, True)


def jugar_ronda_versus(usuario:str, puntos_corona:int, categorias_restantes:list, rondas_jugadas_usuario:int, aciertos_usuario:int, errores_usuario:int, turno_perdido:bool):
    lista_preguntas = obtener_lista_preguntas_por_dificultad("Versus")
    if puntos_corona >= 3:
        categorias_restantes, rondas_jugadas_usuario, aciertos_usuario, errores_usuario, turno_perdido = jugar_ronda_corona(
    usuario, categorias_restantes, rondas_jugadas_usuario, aciertos_usuario, errores_usuario, turno_perdido
    )
        puntos_corona = 0
    else:
        pregunta = hacer_pregunta(lista_preguntas, 0, "Versus", usuario, puntos_corona, categorias_restantes, modo_versus = True)
        bandera_correcto, tiempo_total = obtener_y_validar_respuesta_pregunta(pregunta)
        if bandera_correcto:
            print("\n✅ ¡Correcto!")
            aciertos_usuario += 1
            puntos_corona += 1
            agregar_estadistica(usuario, "aciertos_totales")
        else:
            print("\n❌ Incorrecto...")
            errores_usuario += 1
            turno_perdido = not turno_perdido
            agregar_estadistica(usuario, "errores_totales")
        rondas_jugadas_usuario += 1
        agregar_estadistica(usuario, "rondas_jugadas")
        agregar_estadistica(usuario, "tiempo_total", tiempo_total)
    input("\nPresiona ENTER para continuar... ")
    return rondas_jugadas_usuario, aciertos_usuario, errores_usuario, turno_perdido, puntos_corona

def elegir_categoria_ronda_corona(categorias_restantes:list, rondas_jugadas_usuario:int, aciertos_usuario:int, errores_usuario:int, turno_perdido:bool):
    os.system("cls")
    print("¡Estás en una ronda corona!\n\nElige tu época a coronar:")
    n = 0
    for i in range(len(categorias_restantes)):
        n += 1
        print(f"{i+1}) {categorias_restantes[i].capitalize()}")
    opciones = obtener_cadena_de_numeros(n)
    ingreso_usuario = obtener_opcion_numero(opciones, "Elije la categoría: ", "Error de lectura, elije la categoría: ")
    categoria_electa = categorias_restantes[ingreso_usuario - 1]
    categorias_restantes.remove(categoria_electa)
    return categoria_electa, categorias_restantes

def jugar_ronda_corona(usuario:str, categorias_restantes:list, rondas_jugadas_usuario:int, aciertos_usuario:int, errores_usuario:int, turno_perdido:bool):
    os.system("cls")
    categoria_electa, categorias_restantes = elegir_categoria_ronda_corona(categorias_restantes, rondas_jugadas_usuario, aciertos_usuario, errores_usuario, turno_perdido)
    lista_preguntas_validas = obtener_lista_preguntas_por_dificultad("Versus", categoria_electa)
    pregunta = hacer_pregunta(lista_preguntas_validas, 0, "RONDA CORONA", usuario, 0, categorias_restantes, True, True, categoria_electa)
    bandera_correcto, tiempo_total = obtener_y_validar_respuesta_pregunta(pregunta)
    if bandera_correcto:
        print("\n✅ ¡Correcto!")
        aciertos_usuario += 1
        agregar_estadistica(usuario, "aciertos_totales")
    else:
        print("\n❌ Incorrecto...")
        errores_usuario += 1
        turno_perdido = not turno_perdido
        agregar_estadistica(usuario, "errores_totales")
    rondas_jugadas_usuario += 1
    agregar_estadistica(usuario, "rondas_jugadas")
    agregar_estadistica(usuario, "tiempo_total", tiempo_total)   
    return categorias_restantes, rondas_jugadas_usuario, aciertos_usuario, errores_usuario, turno_perdido

