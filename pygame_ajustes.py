import pygame
from pygame_utils import *
from parser import *

def mostrar_ajustes(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes", 640, 100, estado['paleta'])
    
    botones = crear_botones_menu([
        "Sonido",
        "Accesibilidad",
        "Volver"
    ])
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['pantalla_actual'] = 'ajustes_sonido'
                        case 1:
                            estado['pantalla_actual'] = 'ajustes_accesibilidad'
                        case 2:
                            estado['pantalla_actual'] = 'menu_principal' if estado['usuario'] else 'pre_menu'
                indice += 1

def mostrar_ajustes_sonido(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes de Sonido", 640, 100, estado['paleta'])
    
    config = estado['config']['volumen']
    
    # Crear y mostrar botones para cada tipo de sonido
    y_pos = 200
    botones_volumen = crear_botones_ajuste_sonido(config, y_pos, estado['paleta'])
    
    # Crear botón volver
    boton_volver = crear_boton(440, 550, 400, 60, "Volver", estado['paleta'])
    
    # Actualizar estado de botones con posición del mouse
    pos_mouse = pygame.mouse.get_pos()
    for grupo in botones_volumen.values():
        actualizar_boton(grupo['menos'], pos_mouse)
        actualizar_boton(grupo['mas'], pos_mouse)
    actualizar_boton(boton_volver, pos_mouse)
    
    # Dibujar botones y valores
    dibujar_controles_sonido(ventana, botones_volumen, config, estado['paleta'])
    dibujar_boton(ventana, boton_volver, estado['paleta'])
    
    # Manejar eventos
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            procesar_eventos_sonido(evento, pos_mouse, estado, botones_volumen, boton_volver)

def crear_botones_ajuste_sonido(config, y_inicial, paleta):
    botones_volumen = {}
    y_pos = y_inicial
    
    for tipo in ['general', 'musica', 'efectos']:
        botones_volumen[tipo] = {
            'menos': crear_boton(440, y_pos, 50, 50, "-", paleta),
            'mas': crear_boton(790, y_pos, 50, 50, "+", paleta)
        }
        y_pos += 100
        
    return botones_volumen

def dibujar_controles_sonido(ventana, botones_volumen, config, paleta):
    y_pos = 200
    
    for tipo in ['general', 'musica', 'efectos']:
        # Dibujar texto del tipo y valor
        dibujar_texto(ventana, f"{tipo.capitalize()}: {config[tipo]}%", 
                     640, y_pos, paleta)
        
        # Dibujar botones + y -
        dibujar_boton(ventana, botones_volumen[tipo]['menos'], paleta)
        dibujar_boton(ventana, botones_volumen[tipo]['mas'], paleta)
        
        y_pos += 100

def procesar_eventos_sonido(evento, pos_mouse, estado, botones_volumen, boton_volver):
    for tipo in ['general', 'musica', 'efectos']:
        if actualizar_boton(botones_volumen[tipo]['menos'], pos_mouse):
            actualizar_volumen(estado, tipo, -5)
        elif actualizar_boton(botones_volumen[tipo]['mas'], pos_mouse):
            actualizar_volumen(estado, tipo, 5)
    
    if actualizar_boton(boton_volver, pos_mouse):
        reproducir_sonido_click(estado)
        estado['pantalla_actual'] = 'ajustes'

def actualizar_volumen(estado, tipo, cambio):
    # Actualizar valor del volumen
    nuevo_volumen = max(0, min(100, estado['config']['volumen'][tipo] + cambio))
    estado['config']['volumen'][tipo] = nuevo_volumen
    
    # Guardar configuración
    escribir_archivo_json(estado['config'], 'configfiles/config.json')
    
    # Aplicar cambios en tiempo real
    aplicar_cambios_volumen(estado, tipo, nuevo_volumen)

def aplicar_cambios_volumen(estado, tipo, nuevo_volumen):
    volumen_normalizado = nuevo_volumen / 100
    
    if tipo == 'general':
        pygame.mixer.music.set_volume(volumen_normalizado)
    elif tipo == 'musica' and estado['sonidos']['musica']:
        estado['sonidos']['musica'].set_volume(volumen_normalizado)
    elif tipo == 'efectos':
        for efecto in ['click', 'correcto', 'incorrecto']:
            if estado['sonidos'][efecto]:
                estado['sonidos'][efecto].set_volume(volumen_normalizado)

def reproducir_sonido_click(estado):
    if estado['sonidos']['click']:
        estado['sonidos']['click'].play()

def mostrar_ajustes_accesibilidad(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes de Accesibilidad", 640, 100, estado['paleta'])
    
    botones = crear_botones_menu([
        "Daltonismo",
        "TDAH",
        "TEA",
        "Volver"
    ])
    
    config = estado['config']['accesibilidad']
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['pantalla_actual'] = 'ajustes_daltonismo'
                        case 1:
                            estado['pantalla_actual'] = 'ajustes_tdah'
                        case 2:
                            estado['pantalla_actual'] = 'ajustes_tea'
                        case 3:
                            estado['pantalla_actual'] = 'ajustes'
                indice += 1

def mostrar_ajustes_daltonismo(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes de Daltonismo", 640, 100, estado['paleta'])
    
    tipo_actual = estado['config']['accesibilidad']['daltonismo']
    dibujar_texto(ventana, f"Tipo actual: {tipo_actual.capitalize()}", 
                640, 160, estado['paleta'])
    
    botones = crear_botones_menu([
        "Protanopía",
        "Deuteranopía",
        "Tritanopía",
        "Ninguno",
        "Volver"
    ])
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['config']['accesibilidad']['daltonismo'] = 'protanopia'
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 1:
                            estado['config']['accesibilidad']['daltonismo'] = 'deuteranopia'
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 2:
                            estado['config']['accesibilidad']['daltonismo'] = 'tritanopia'
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 3:
                            estado['config']['accesibilidad']['daltonismo'] = 'ninguno'
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 4:
                            estado['pantalla_actual'] = 'ajustes_accesibilidad'
                indice += 1

def mostrar_ajustes_tdah(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes TDAH", 640, 100, estado['paleta'])
    dibujar_texto(ventana, "Adaptaciones para personas con TDAH:", 640, 160, estado['paleta'])
    
    y_pos = 220
    adaptaciones = [
        "- Temporizador visual",
        "- Instrucciones más claras y concisas",
        "- Menos elementos distractores en pantalla",
        "- Feedback inmediato y más visual",
        "- Pausas automáticas entre preguntas"
    ]
    
    for adaptacion in adaptaciones:
        dibujar_texto(ventana, adaptacion, 640, y_pos, estado['paleta'])
        y_pos += 40
    
    estado_actual = "ON" if estado['config']['accesibilidad']['tdah'] else "OFF"
    dibujar_texto(ventana, f"Estado actual: {estado_actual}", 640, y_pos + 20, estado['paleta'])
    
    botones = crear_botones_menu([
        "Activar adaptaciones",
        "Desactivar adaptaciones",
        "Volver"
    ], y_inicial=y_pos + 80)
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['config']['accesibilidad']['tdah'] = True
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 1:
                            estado['config']['accesibilidad']['tdah'] = False
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 2:
                            estado['pantalla_actual'] = 'ajustes_accesibilidad'
                indice += 1

def mostrar_ajustes_tea(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Ajustes TEA", 640, 100, estado['paleta'])
    dibujar_texto(ventana, "Adaptaciones para personas con TEA:", 640, 160, estado['paleta'])
    
    y_pos = 220
    adaptaciones = [
        "- Interfaz más predecible y estructurada",
        "- Lenguaje literal y directo",
        "- Apoyo visual en instrucciones",
        "- Rutinas claras y consistentes",
        "- Transiciones suaves entre pantallas"
    ]
    
    for adaptacion in adaptaciones:
        dibujar_texto(ventana, adaptacion, 640, y_pos, estado['paleta'])
        y_pos += 40
    
    estado_actual = "ON" if estado['config']['accesibilidad']['tea'] else "OFF"
    dibujar_texto(ventana, f"Estado actual: {estado_actual}", 640, y_pos + 20, estado['paleta'])
    
    botones = crear_botones_menu([
        "Activar adaptaciones",
        "Desactivar adaptaciones",
        "Volver"
    ], y_inicial=y_pos + 80)
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, evento.pos):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['config']['accesibilidad']['tea'] = True
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 1:
                            estado['config']['accesibilidad']['tea'] = False
                            escribir_archivo_json(estado['config'], 'configfiles/config.json')
                        case 2:
                            estado['pantalla_actual'] = 'ajustes_accesibilidad'
                indice += 1