import pygame
from parser import *
import random

def crear_boton(x, y, ancho, alto, texto, paleta, tamano_fuente=36):
    boton = {
        'rect': pygame.Rect(x, y, ancho, alto),
        'texto': texto,
        'hover': False,
        'fuente': pygame.font.Font(None, tamano_fuente)
    }
    return boton

def dibujar_boton(ventana, boton, paleta):
    color = obtener_color_boton(boton, paleta)
    pygame.draw.rect(ventana, color, boton['rect'], border_radius=12)
    renderizar_texto_boton(ventana, boton, paleta)

def obtener_color_boton(boton, paleta):
    color_boton = paleta['resaltado'] if boton['hover'] else paleta['boton']
    return color_boton

def renderizar_texto_boton(ventana, boton, paleta):
    texto_surface = boton['fuente'].render(boton['texto'], True, paleta['texto_boton'])
    texto_rect = texto_surface.get_rect(center=boton['rect'].center)
    ventana.blit(texto_surface, texto_rect)

def actualizar_boton(boton, pos_mouse):
    boton['hover'] = boton['rect'].collidepoint(pos_mouse)
    colision = boton['rect'].collidepoint(pos_mouse)
    return colision

def dibujar_texto(ventana, texto, x, y, paleta, tamano=36, centrado=True):
    fuente = pygame.font.Font(None, tamano)
    superficie = fuente.render(texto, True, paleta['texto'])
    rect = superficie.get_rect()
    
    if centrado:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
        
    ventana.blit(superficie, rect)
    rect_resultado = rect
    return rect_resultado

def crear_botones_menu(opciones, y_inicial=200, espaciado=80):
    botones = []
    for indice, texto in enumerate(opciones):
        boton = {
            'rect': pygame.Rect(440, y_inicial + indice * espaciado, 400, 60),
            'texto': texto,
            'hover': False,
            'fuente': pygame.font.Font(None, 36)
        }
        botones.append(boton)
    return botones

def crear_input_texto(x, y, ancho, alto):
    campo_texto = {
        'rect': pygame.Rect(x, y, ancho, alto),
        'texto': '',
        'activo': False
    }
    return campo_texto

def obtener_lista_preguntas_por_dificultad(dificultad, categoria=None):
    preguntas = leer_archivo_json('configfiles/preguntas.json')
    preguntas_filtradas = filtrar_preguntas(preguntas, dificultad, categoria)
    random.shuffle(preguntas_filtradas)
    return preguntas_filtradas

def filtrar_preguntas(preguntas, dificultad, categoria):
    preguntas_filtradas = []
    
    for pregunta in preguntas:
        if categoria:
            if pregunta['categoria'].lower() == categoria.lower():
                preguntas_filtradas.append(pregunta)
        else:
            if pregunta['dificultad'].lower() == dificultad.lower():
                preguntas_filtradas.append(pregunta)
    
    if not preguntas_filtradas:
        preguntas_filtradas = preguntas[:]
        
    return preguntas_filtradas