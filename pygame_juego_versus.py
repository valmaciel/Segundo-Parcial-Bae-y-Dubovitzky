import pygame
from pygame_utils import *
from juego_utils import *
import time
import random

def mostrar_juego_versus(ventana, estado, eventos):
    # Verificar que tengamos un versus_estado válido con usuario2
    if not estado.get('versus_estado') or not estado['versus_estado'].get('usuario2'):
        estado['pantalla_actual'] = 'menu_versus'
        return
    else:
        # Asegurarse que todas las claves necesarias existan
        claves_necesarias = {
            'usuario2': '',
            'turno_usuario1': True,
            'aciertos_consecutivos1': 0,
            'aciertos_consecutivos2': 0,
            'categorias_restantes1': ["antigua", "clasica", "medieval", "renacimiento", 
                                    "industrial", "moderna", "atomica", "informacion"],
            'categorias_restantes2': ["antigua", "clasica", "medieval", "renacimiento", 
                                    "industrial", "moderna", "atomica", "informacion"],
            'categorias_coronadas1': [],
            'categorias_coronadas2': [],
            'ronda_corona': False,
            'categoria_a_coronar': None
        }
        for key, default in claves_necesarias.items():
            if key not in estado['versus_estado']:
                estado['versus_estado'][key] = default

    if 'pregunta_actual' not in estado:
        estado['pregunta_actual'] = None
        estado['inicio_tiempo'] = time.time()
        estado['preguntas_disponibles'] = []

    ventana.fill(estado['paleta']['fondo'])

    # Información de jugadores
    dibujar_texto(ventana, f"{estado['usuario']}: {len(estado['versus_estado']['categorias_coronadas1'])} épocas coronadas", 
                200, 30, estado['paleta'], centrado=False)
    dibujar_texto(ventana, f"Aciertos consecutivos: {estado['versus_estado']['aciertos_consecutivos1']}/3", 
                200, 60, estado['paleta'], centrado=False)

    dibujar_texto(ventana, f"{estado['versus_estado']['usuario2']}: {len(estado['versus_estado']['categorias_coronadas2'])} épocas coronadas", 
                800, 30, estado['paleta'], centrado=False)
    dibujar_texto(ventana, f"Aciertos consecutivos: {estado['versus_estado']['aciertos_consecutivos2']}/3", 
                800, 60, estado['paleta'], centrado=False)

    usuario_actual = estado['usuario'] if estado['versus_estado']['turno_usuario1'] else estado['versus_estado']['usuario2']
    dibujar_texto(ventana, f"Turno de: {usuario_actual}", 640, 100, estado['paleta'])

    aciertos_consecutivos = (estado['versus_estado']['aciertos_consecutivos1'] 
                            if estado['versus_estado']['turno_usuario1'] 
                            else estado['versus_estado']['aciertos_consecutivos2'])
    
    categorias_restantes = (estado['versus_estado']['categorias_restantes1'] 
                            if estado['versus_estado']['turno_usuario1'] 
                            else estado['versus_estado']['categorias_restantes2'])

    # Verificar fin del juego
    if (len(estado['versus_estado']['categorias_coronadas1']) >= 8 or 
        len(estado['versus_estado']['categorias_coronadas2']) >= 8):
        estado['pantalla_actual'] = 'resultado_versus'
        return

    # Determinar qué pantalla mostrar
    if estado['versus_estado']['ronda_corona']:
        mostrar_seleccion_categoria_versus(ventana, estado, eventos)
    elif estado['versus_estado']['categoria_a_coronar'] is not None:
        mostrar_pregunta_corona(ventana, estado, eventos)
    else:
        mostrar_pregunta_versus(ventana, estado, eventos)

def mostrar_pregunta_versus(ventana, estado, eventos):

    if estado['pregunta_actual']:
        print("\nDebug info:")
        print(f"Pregunta actual: {estado['pregunta_actual']['pregunta']}")
        print(f"Respuesta correcta: {estado['pregunta_actual']['respuesta']}")
        print(f"Opciones: {estado['pregunta_actual']['opciones']}")
        print(f"Categoría: {estado['pregunta_actual']['categoria']}")

    # Preparar pregunta si no existe
    if estado['pregunta_actual'] is None:
        estado['preguntas_disponibles'] = obtener_lista_preguntas_por_dificultad("Versus")
        if estado['preguntas_disponibles']:
            estado['pregunta_actual'] = estado['preguntas_disponibles'].pop()
            estado['inicio_tiempo'] = time.time()
        else:
            return  # No hay preguntas disponibles

    dibujar_texto(ventana, estado['pregunta_actual']['pregunta'], 640, 150, estado['paleta'])
    opciones = estado['pregunta_actual']['opciones']
    botones_opciones = []
    indice = 0
    for opcion in opciones:
        boton = crear_boton(340, 250 + indice * 100, 600, 80, opcion, estado['paleta'])
        botones_opciones.append(boton)
        indice += 1

    pos_mouse = pygame.mouse.get_pos()
    for boton in botones_opciones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones_opciones:
                if actualizar_boton(boton, evento.pos):
                    respuesta_usuario = chr(97 + indice)
                    tiempo_total = time.time() - estado['inicio_tiempo']
                    usuario_actual = estado['usuario'] if estado['versus_estado']['turno_usuario1'] else estado['versus_estado']['usuario2']

                    if respuesta_usuario == estado['pregunta_actual']['respuesta']:
                        if estado['sonidos']['correcto']:
                            estado['sonidos']['correcto'].play()
                        if estado['versus_estado']['turno_usuario1']:
                            estado['versus_estado']['aciertos_consecutivos1'] += 1
                            if estado['versus_estado']['aciertos_consecutivos1'] >= 3:
                                estado['versus_estado']['ronda_corona'] = True
                        else:
                            estado['versus_estado']['aciertos_consecutivos2'] += 1
                            if estado['versus_estado']['aciertos_consecutivos2'] >= 3:
                                estado['versus_estado']['ronda_corona'] = True
                        agregar_estadistica(usuario_actual, 'aciertos_totales')
                    else:
                        if estado['sonidos']['incorrecto']:
                            estado['sonidos']['incorrecto'].play()
                        if estado['versus_estado']['turno_usuario1']:
                            estado['versus_estado']['aciertos_consecutivos1'] = 0
                        else:
                            estado['versus_estado']['aciertos_consecutivos2'] = 0
                        estado['versus_estado']['turno_usuario1'] = not estado['versus_estado']['turno_usuario1']
                        agregar_estadistica(usuario_actual, 'errores_totales')

                    agregar_estadistica(usuario_actual, 'rondas_jugadas')
                    agregar_estadistica(usuario_actual, 'tiempo_total', tiempo_total)
                    estado['pregunta_actual'] = None
                    estado['inicio_tiempo'] = time.time()
                    break
                indice += 1

def mostrar_seleccion_categoria_versus(ventana, estado, eventos):
    categorias_disponibles = (estado['versus_estado']['categorias_restantes1'] 
                            if estado['versus_estado']['turno_usuario1'] 
                            else estado['versus_estado']['categorias_restantes2'])

    dibujar_texto(ventana, "¡RONDA CORONA!", 640, 150, estado['paleta'])
    dibujar_texto(ventana, "Elige la época que quieres coronar:", 640, 200, estado['paleta'])

    botones = []
    y_pos = 250
    for categoria in categorias_disponibles:
        boton = crear_boton(440, y_pos, 400, 50, categoria.capitalize(), estado['paleta'])
        botones.append((boton, categoria))
        y_pos += 70

    pos_mouse = pygame.mouse.get_pos()
    for boton, _ in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            for boton, categoria in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    estado['versus_estado']['categoria_a_coronar'] = categoria
                    estado['versus_estado']['ronda_corona'] = False
                    estado['preguntas_disponibles'] = obtener_lista_preguntas_por_dificultad("Versus", categoria)
                    if estado['preguntas_disponibles']:
                        estado['pregunta_actual'] = estado['preguntas_disponibles'].pop()
                        estado['inicio_tiempo'] = time.time()
                    break

def mostrar_pregunta_corona(ventana, estado, eventos):

    if estado['pregunta_actual']:
        print("\nDebug info:")
        print(f"Pregunta actual: {estado['pregunta_actual']['pregunta']}")
        print(f"Respuesta correcta: {estado['pregunta_actual']['respuesta']}")
        print(f"Opciones: {estado['pregunta_actual']['opciones']}")
        print(f"Categoría: {estado['pregunta_actual']['categoria']}")

    categoria = estado['versus_estado']['categoria_a_coronar']
    dibujar_texto(ventana, f"Pregunta para coronar: {categoria.capitalize()}", 640, 120, estado['paleta'])
    dibujar_texto(ventana, estado['pregunta_actual']['pregunta'], 640, 170, estado['paleta'])

    opciones = estado['pregunta_actual']['opciones']
    botones_opciones = []
    indice = 0
    for opcion in opciones:
        boton = crear_boton(340, 250 + indice * 100, 600, 80, opcion, estado['paleta'])
        botones_opciones.append(boton)
        indice += 1

    pos_mouse = pygame.mouse.get_pos()
    for boton in botones_opciones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])

    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones_opciones:
                if actualizar_boton(boton, evento.pos):
                    respuesta_usuario = chr(97 + indice)
                    tiempo_total = time.time() - estado['inicio_tiempo']
                    usuario_actual = estado['usuario'] if estado['versus_estado']['turno_usuario1'] else estado['versus_estado']['usuario2']
                    # Comparación de respuestas ignorando mayúsculas/minúsculas
                    if respuesta_usuario.lower() == estado['pregunta_actual']['respuesta'].lower():
                        if estado['sonidos']['correcto']:
                            estado['sonidos']['correcto'].play()
                        if estado['versus_estado']['turno_usuario1']:
                            estado['versus_estado']['categorias_coronadas1'].append(categoria)
                            estado['versus_estado']['categorias_restantes1'].remove(categoria)
                            estado['versus_estado']['aciertos_consecutivos1'] = 0
                        else:
                            estado['versus_estado']['categorias_coronadas2'].append(categoria)
                            estado['versus_estado']['categorias_restantes2'].remove(categoria)
                            estado['versus_estado']['aciertos_consecutivos2'] = 0
                        agregar_estadistica(usuario_actual, 'aciertos_totales')
                    else:
                        if estado['sonidos']['incorrecto']:
                            estado['sonidos']['incorrecto'].play()
                        if estado['versus_estado']['turno_usuario1']:
                            estado['versus_estado']['aciertos_consecutivos1'] = 0
                        else:
                            estado['versus_estado']['aciertos_consecutivos2'] = 0
                        estado['versus_estado']['turno_usuario1'] = not estado['versus_estado']['turno_usuario1']
                        agregar_estadistica(usuario_actual, 'errores_totales')

                    agregar_estadistica(usuario_actual, 'rondas_jugadas')
                    agregar_estadistica(usuario_actual, 'tiempo_total', tiempo_total)
                    estado['pregunta_actual'] = None
                    estado['versus_estado']['categoria_a_coronar'] = None
                    estado['inicio_tiempo'] = time.time()
                    break
                indice += 1

def mostrar_resultado_versus(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    if 'scroll_y' not in estado:
        estado['scroll_y'] = 0
        
    categorias_coronadas1 = len(estado['versus_estado']['categorias_coronadas1'])
    categorias_coronadas2 = len(estado['versus_estado']['categorias_coronadas2'])
    
    ganador = estado['usuario'] if categorias_coronadas1 > categorias_coronadas2 else estado['versus_estado']['usuario2']
    agregar_estadistica(ganador, 'partidas_ganadas')
    
    # Crear una superficie para el contenido scrolleable
    superficie_stats = pygame.Surface((800, 1000))
    superficie_stats.fill(estado['paleta']['fondo'])
    
    # Dibujar título
    dibujar_texto(superficie_stats, "Partida VERSUS terminada", 400, 20, estado['paleta'])
    dibujar_texto(superficie_stats, f"¡{ganador} es el ganador!", 400, 70, estado['paleta'])
    
    # Estadísticas jugador 1
    y_pos = 150
    dibujar_texto(superficie_stats, f"Jugador: {estado['usuario']}", 400, y_pos, estado['paleta'])
    dibujar_texto(superficie_stats, f"Épocas coronadas: {categorias_coronadas1}", 400, y_pos + 40, estado['paleta'])
    
    dibujar_texto(superficie_stats, "Épocas conquistadas:", 400, y_pos + 80, estado['paleta'])
    for categoria in estado['versus_estado']['categorias_coronadas1']:
        y_pos += 30
        dibujar_texto(superficie_stats, categoria.capitalize(), 400, y_pos + 90, estado['paleta'])
    
    # Estadísticas jugador 2
    y_pos += 150
    dibujar_texto(superficie_stats, f"Jugador: {estado['versus_estado']['usuario2']}", 400, y_pos, estado['paleta'])
    dibujar_texto(superficie_stats, f"Épocas coronadas: {categorias_coronadas2}", 400, y_pos + 40, estado['paleta'])
    
    dibujar_texto(superficie_stats, "Épocas conquistadas:", 400, y_pos + 80, estado['paleta'])
    for categoria in estado['versus_estado']['categorias_coronadas2']:
        y_pos += 30
        dibujar_texto(superficie_stats, categoria.capitalize(), 400, y_pos + 90, estado['paleta'])
    
    # Área visible
    area_visible = pygame.Rect(240, 100, 800, 450)
    ventana.blit(superficie_stats, area_visible, (0, estado['scroll_y'], 800, 450))
    
    # Barra de scroll
    total_altura = y_pos + 150  # Altura total del contenido
    if total_altura > 450:  # Si el contenido es más alto que el área visible
        altura_barra = (450 * 450) / total_altura
        pos_barra = (estado['scroll_y'] * 450) / total_altura
        pygame.draw.rect(ventana, estado['paleta']['boton'], 
                        (1050, 100, 20, 450))
        pygame.draw.rect(ventana, estado['paleta']['resaltado'],
                        (1050, 100 + pos_barra, 20, altura_barra))
    
    # Botón volver
    boton_volver = crear_boton(440, 600, 400, 60, "Volver al menú", estado['paleta'])
    
    pos_mouse = pygame.mouse.get_pos()
    actualizar_boton(boton_volver, pos_mouse)
    dibujar_boton(ventana, boton_volver, estado['paleta'])
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 4:  # Scroll arriba
                estado['scroll_y'] = max(0, estado['scroll_y'] - 30)
            elif evento.button == 5:  # Scroll abajo
                estado['scroll_y'] = min(total_altura - 450, estado['scroll_y'] + 30)
            elif actualizar_boton(boton_volver, pos_mouse):
                if estado['sonidos']['click']:
                    estado['sonidos']['click'].play()
                estado['pantalla_actual'] = 'menu_principal'
                # Limpiar el estado
                estado['versus_estado'] = None
                estado['scroll_y'] = 0
                estado['pregunta_actual'] = None
                estado['inicio_tiempo'] = None 
                estado['preguntas_disponibles'] = None