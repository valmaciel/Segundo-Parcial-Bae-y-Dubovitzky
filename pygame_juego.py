import pygame
from pygame_utils import *
from juego_utils import *
import time

def mostrar_juego_arcade(ventana, estado, eventos):
    if 'pregunta_actual' not in estado:
        estado['preguntas_disponibles'] = obtener_lista_preguntas_por_dificultad(estado['dificultad'])
        estado['pregunta_actual'] = estado['preguntas_disponibles'].pop()
        estado['inicio_tiempo'] = time.time()
    
    ventana.fill(estado['paleta']['fondo'])
    
    # Información de juego
    dibujar_texto(ventana, "Vidas: " + "❤️ " * estado['vidas'], 200, 50, estado['paleta'], centrado=False)
    dibujar_texto(ventana, f"Dificultad: {estado['dificultad']}", 640, 50, estado['paleta'])
    dibujar_texto(ventana, f"Puntaje: {estado['puntaje']}", 1080, 50, estado['paleta'], centrado=False)
    
    # Pregunta
    dibujar_texto(ventana, estado['pregunta_actual']['pregunta'], 640, 150, estado['paleta'])
    
    # Opciones
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
                    
                    if respuesta_usuario == estado['pregunta_actual']['respuesta']:
                        if estado['sonidos']['correcto']:
                            estado['sonidos']['correcto'].play()
                        estado['puntaje'] += int(estado['pregunta_actual']['puntaje'])
                        agregar_estadistica(estado['usuario'], 'aciertos_totales')
                        agregar_monedas(estado['usuario'], int(estado['pregunta_actual']['puntaje']))
                    else:
                        if estado['sonidos']['incorrecto']:
                            estado['sonidos']['incorrecto'].play()
                        estado['vidas'] -= 1
                        agregar_estadistica(estado['usuario'], 'errores_totales')
                    
                    agregar_estadistica(estado['usuario'], 'rondas_jugadas')
                    agregar_estadistica(estado['usuario'], 'tiempo_total', tiempo_total)
                    
                    if estado['vidas'] <= 0:
                        estado['pantalla_actual'] = 'resultado_arcade'
                    else:
                        # Si no hay más preguntas disponibles, obtener nueva lista
                        if not estado['preguntas_disponibles']:
                            estado['preguntas_disponibles'] = obtener_lista_preguntas_por_dificultad(estado['dificultad'])
                        
                        # Obtener siguiente pregunta
                        estado['pregunta_actual'] = estado['preguntas_disponibles'].pop()
                        estado['inicio_tiempo'] = time.time()
                indice += 1

def mostrar_resultado_arcade(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Partida ARCADE terminada", 640, 100, estado['paleta'])
    dibujar_texto(ventana, f"Jugador: {estado['usuario']}", 640, 200, estado['paleta'])
    dibujar_texto(ventana, f"Puntaje final: {estado['puntaje']}", 640, 300, estado['paleta'])
    dibujar_texto(ventana, f"Dificultad: {estado['dificultad']}", 640, 400, estado['paleta'])
    
    boton_volver = crear_boton(440, 500, 400, 60, "Volver al menú", estado['paleta'])
    
    pos_mouse = pygame.mouse.get_pos()
    actualizar_boton(boton_volver, pos_mouse)
    dibujar_boton(ventana, boton_volver, estado['paleta'])
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if actualizar_boton(boton_volver, evento.pos):
                if estado['sonidos']['click']:
                    estado['sonidos']['click'].play()
                estado['pantalla_actual'] = 'menu_principal'
                estado['pregunta_actual'] = None
                estado['inicio_tiempo'] = None
                estado['preguntas_disponibles'] = None