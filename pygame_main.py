import pygame
import sys
from pygame_utils import *
from pygame_menu import *
from pygame_ajustes import *
from pygame_estadisticas import *
from pygame_juego import *
from pygame_juego_versus import *
from parser import *
from paletas_colores import PALETAS_DALTONISMO

def inicializar_pygame():
    pygame.init()
    pygame.mixer.init()
    ANCHO = 1280
    ALTO = 720
    ventana = pygame.display.set_mode((ANCHO, ALTO))
    icono = pygame.image.load("imagenes/icono.png")
    pygame.display.set_icon(icono)
    pygame.display.set_caption("PyCRONOS Quiz")
    clock = pygame.time.Clock()
    return ventana, clock

def cargar_sonidos(estado):
    sonidos = {
        'click': None,
        'correcto': None,
        'incorrecto': None,
        'musica': None
    }
    
    archivos_sonido = {
        'click': 'sonidos/click.wav',
        'correcto': 'sonidos/correcto.wav',
        'incorrecto': 'sonidos/error.wav',
        'musica': 'sonidos/musica.wav'
    }

    
    for nombre, archivo in archivos_sonido.items():
        sonido = pygame.mixer.Sound(archivo)
        if nombre == 'musica':
            sonido.set_volume(estado['config']['volumen']['musica'] / 100)
            sonido.play(-1)  # Loop infinito
        else:
            sonido.set_volume(estado['config']['volumen']['efectos'] / 100)
        sonidos[nombre] = sonido # Sobreescribe el diccionario de sonidos con todos los path o "pygame.mixer.Sound(archivo)" de sonido donde (archivo) se cambia por el path del archivo
    
    pygame.mixer.music.set_volume(estado['config']['volumen']['general'] / 100)
    return sonidos

def main():
    ventana, clock = inicializar_pygame()
    
    estado = {
        'pantalla_actual': 'pre_menu',
        'usuario': '',
        'password': '',
        'config': leer_archivo_json('configfiles/config.json'),
        'paleta': PALETAS_DALTONISMO['ninguno'],
    }
    
    estado['sonidos'] = cargar_sonidos(estado)
    
    while True:
        eventos = pygame.event.get()
        for evento in eventos:
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    if estado['pantalla_actual'] not in ['pre_menu', 'menu_principal']:
                        if estado['usuario']:
                            estado['pantalla_actual'] = 'menu_principal'
                        else: 
                            estado['pantalla_actual'] = 'pre_menu'

        tipo_daltonismo = estado['config']['accesibilidad']['daltonismo']
        estado['paleta'] = PALETAS_DALTONISMO[tipo_daltonismo]
                
        match estado['pantalla_actual']:
            case 'pre_menu':
                mostrar_pre_menu(ventana, estado, eventos)
            case 'login':
                mostrar_login(ventana, estado, eventos)
            case 'registro':
                mostrar_registro(ventana, estado, eventos)
            case 'menu_principal':
                mostrar_menu_principal(ventana, estado, eventos)
            case 'menu_arcade':
                mostrar_menu_arcade(ventana, estado, eventos)
            case 'menu_versus':
                mostrar_menu_versus(ventana, estado, eventos)
            case 'ajustes':
                mostrar_ajustes(ventana, estado, eventos)
            case 'ajustes_sonido':
                mostrar_ajustes_sonido(ventana, estado, eventos)
            case 'ajustes_accesibilidad':
                mostrar_ajustes_accesibilidad(ventana, estado, eventos)
            case 'ajustes_daltonismo':
                mostrar_ajustes_daltonismo(ventana, estado, eventos)
            case 'ajustes_tdah':
                mostrar_ajustes_tdah(ventana, estado, eventos)
            case 'ajustes_tea':
                mostrar_ajustes_tea(ventana, estado, eventos)
            case 'estadisticas':
                mostrar_estadisticas_pygame(ventana, estado, eventos)
            case 'juego_arcade':
                mostrar_juego_arcade(ventana, estado, eventos)
            case 'resultado_arcade':
                mostrar_resultado_arcade(ventana, estado, eventos)
            case 'juego_versus':
                mostrar_juego_versus(ventana, estado, eventos)
            case 'resultado_versus':
                mostrar_resultado_versus(ventana, estado, eventos)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()