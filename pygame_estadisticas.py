import pygame
from pygame_utils import *
from estadisticas_utils import *

def mostrar_estadisticas_pygame(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    if 'scroll_y' not in estado:
        estado['scroll_y'] = 0
    
    dibujar_texto(ventana, "Estadísticas", 640, 50, estado['paleta'])
    
    # Crear una superficie para el contenido scrolleable
    superficie_stats = pygame.Surface((800, 2000))
    superficie_stats.fill(estado['paleta']['fondo'])
    
    archivo_estadisticas = leer_archivo_json("configfiles/estadisticas.json")
    y_pos = 20
    
    for nombre in archivo_estadisticas:
        (partidas_ganadas, aciertos_totales, 
        errores_totales, rondas_totales, 
        tiempo_promedio_por_pregunta) = agarrar_datos_estadisticas_usuario(nombre)
        
        dibujar_texto(superficie_stats, f"———— Estadísticas de {nombre} ————", 
                    400, y_pos, estado['paleta'])
        y_pos += 40
        
        estadisticas = [
            f"Partidas ganadas: {partidas_ganadas}",
            f"Aciertos totales: {aciertos_totales}",
            f"Errores totales: {errores_totales}",
            f"Rondas jugadas: {rondas_totales}",
            f"Tiempo promedio por pregunta: {tiempo_promedio_por_pregunta:.2f}s"
        ]
        
        for stat in estadisticas:
            dibujar_texto(superficie_stats, stat, 400, y_pos, estado['paleta'])
            y_pos += 30
        
        y_pos += 20
    
    # Área visible
    area_visible = pygame.Rect(240, 100, 800, 450)
    ventana.blit(superficie_stats, area_visible, 
                (0, estado['scroll_y'], 800, 450))
    
    # Barra de scroll
    total_altura = y_pos
    if total_altura > 450:
        altura_barra = (450 * 450) / total_altura
        pos_barra = (estado['scroll_y'] * 450) / total_altura
        pygame.draw.rect(ventana, estado['paleta']['boton'], 
                        (1050, 100, 20, 450))
        pygame.draw.rect(ventana, estado['paleta']['resaltado'],
                        (1050, 100 + pos_barra, 20, altura_barra))
    
    boton_volver = crear_boton(440, 600, 400, 60, "Volver", estado['paleta'])
    
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
                if 'scroll_y' in estado:
                    ['scroll_y']