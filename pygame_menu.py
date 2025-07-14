import pygame
import sys
from pygame_utils import *
from usuarios import *
import pygame
import sys
from pygame_utils import *
from usuarios import *

def mostrar_pre_menu(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "¡Bienvenido a PyCRONOS Quiz!", 640, 100, estado['paleta'])
    
    botones = crear_botones_menu([
        "Iniciar sesión",
        "Registrarse", 
        "Opciones",
        "Salir del juego"
    ])
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, pos_mouse):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    match indice:
                        case 0:
                            estado['pantalla_actual'] = 'login'
                        case 1:
                            estado['pantalla_actual'] = 'registro'
                        case 2:
                            estado['pantalla_actual'] = 'ajustes'
                        case 3:
                            pygame.quit()
                            sys.exit()
                indice += 1

def mostrar_menu_principal(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, f"¡Hola {estado['usuario']}!", 640, 100, estado['paleta'])
    
    botones = crear_botones_menu([
        "Jugar juego ARCADE",
        "Jugar juego VERSUS",
        "Ver estadísticas",
        "Opciones",
        "Cerrar sesión"
    ])
    
    pos_mouse = pygame.mouse.get_pos()
    
    for boton in botones:
        actualizar_boton(boton, pos_mouse)
        dibujar_boton(ventana, boton, estado['paleta'])
        
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            indice = 0
            for boton in botones:
                if actualizar_boton(boton, pos_mouse):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    if indice == 0:
                        estado['pantalla_actual'] = 'menu_arcade'
                    elif indice == 1:
                        estado['pantalla_actual'] = 'menu_versus'
                        estado['versus_estado'] = None
                    elif indice == 2:
                        estado['pantalla_actual'] = 'estadisticas'
                    elif indice == 3:
                        estado['pantalla_actual'] = 'ajustes'
                    elif indice == 4:
                        estado['usuario'] = ''
                        estado['password'] = ''
                        estado['pantalla_actual'] = 'pre_menu'
                indice += 1

def mostrar_menu_versus(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    dibujar_texto(ventana, "Modo VERSUS", 640, 100, estado['paleta'])

    # Si no hay segundo jugador, mostrar pantalla de login
    if not estado.get('versus_estado') or not estado['versus_estado'].get('usuario2'):
        # Inicializar campos_login si no existen o si están en None
        if not estado.get('campos_login'):
            estado['campos_login'] = {
                'usuario': crear_input_texto(440, 200, 400, 50),
                'password': crear_input_texto(440, 300, 400, 50)
            }

        dibujar_texto(ventana, "Inicio de sesión del segundo jugador", 640, 150, estado['paleta'])
        dibujar_texto(ventana, "Usuario:", 440, 180, estado['paleta'], centrado=False)
        dibujar_texto(ventana, "Contraseña:", 440, 280, estado['paleta'], centrado=False)

        pos_mouse = pygame.mouse.get_pos()

        # Dibujar campos de texto
        for nombre, campo in estado['campos_login'].items():
            pygame.draw.rect(ventana, estado['paleta']['texto'], campo['rect'], 2)
            if campo['activo']:
                pygame.draw.rect(ventana, estado['paleta']['resaltado'], campo['rect'], 4)

            texto_surface = pygame.font.Font(None, 36).render(
                '*' * len(campo['texto']) if nombre == 'password' else campo['texto'],
                True, estado['paleta']['texto']
            )
            ventana.blit(texto_surface, (campo['rect'].x + 5, campo['rect'].y + 5))

        boton_ingresar = crear_boton(440, 400, 400, 50, "Ingresar", estado['paleta'])
        boton_volver = crear_boton(440, 470, 400, 50, "Volver", estado['paleta'])

        actualizar_boton(boton_ingresar, pos_mouse)
        actualizar_boton(boton_volver, pos_mouse)

        dibujar_boton(ventana, boton_ingresar, estado['paleta'])
        dibujar_boton(ventana, boton_volver, estado['paleta'])

        if estado.get('mensaje_error'):
            dibujar_texto(ventana, estado['mensaje_error'], 640, 360, estado['paleta'])

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Activar/desactivar campos de texto según dónde se hace click
                for campo in estado['campos_login'].values():
                    campo['activo'] = campo['rect'].collidepoint(evento.pos)

                # Botón ingresar
                if actualizar_boton(boton_ingresar, pos_mouse):
                    usuario = estado['campos_login']['usuario']['texto']
                    password = estado['campos_login']['password']['texto']

                    if usuario == estado['usuario']:
                        estado['mensaje_error'] = "No puedes jugar contra ti mismo"
                    elif iniciar_sesion(usuario, password):
                        estado['versus_estado'] = {
                            'usuario2': usuario,
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
                        estado['campos_login'] = None
                        estado['mensaje_error'] = None
                    else:
                        estado['mensaje_error'] = "Usuario o contraseña incorrectos"

                # Botón volver
                elif actualizar_boton(boton_volver, pos_mouse):
                    estado['pantalla_actual'] = 'menu_principal'
                    estado['campos_login'] = None
                    estado['mensaje_error'] = None

            elif evento.type == pygame.KEYDOWN:
                campos = estado.get('campos_login')
                if campos:
                    for campo in campos.values():
                        if campo['activo']:
                            if evento.key == pygame.K_RETURN:
                                campo['activo'] = False
                            elif evento.key == pygame.K_BACKSPACE:
                                campo['texto'] = campo['texto'][:-1]
                            elif evento.unicode.isprintable():
                                campo['texto'] += evento.unicode

    else:
        # Pantalla de confirmación
        dibujar_texto(ventana, f"Jugador 1: {estado['usuario']}", 640, 200, estado['paleta'])
        dibujar_texto(ventana, f"Jugador 2: {estado['versus_estado']['usuario2']}", 640, 250, estado['paleta'])

        boton_comenzar = crear_boton(440, 350, 400, 60, "Comenzar partida", estado['paleta'])
        boton_volver = crear_boton(440, 450, 400, 60, "Volver", estado['paleta'])

        pos_mouse = pygame.mouse.get_pos()

        actualizar_boton(boton_comenzar, pos_mouse)
        actualizar_boton(boton_volver, pos_mouse)

        dibujar_boton(ventana, boton_comenzar, estado['paleta'])
        dibujar_boton(ventana, boton_volver, estado['paleta'])

        for evento in eventos:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if actualizar_boton(boton_comenzar, pos_mouse):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    estado['pantalla_actual'] = 'juego_versus'
                elif actualizar_boton(boton_volver, pos_mouse):
                    if estado['sonidos']['click']:
                        estado['sonidos']['click'].play()
                    estado['pantalla_actual'] = 'menu_principal'
                    estado['versus_estado'] = None

def mostrar_menu_arcade(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, f"¡Bienvenido {estado['usuario']}!", 640, 100, estado['paleta'])
    
    botones = crear_botones_menu([
        "Fácil",
        "Normal", 
        "Difícil",
        "Volver al menú principal"
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
                            estado['dificultad'] = "Fácil"
                            estado['vidas'] = 3
                            estado['puntaje'] = 0
                            estado['pantalla_actual'] = 'juego_arcade'
                        case 1:
                            estado['dificultad'] = "Normal"
                            estado['vidas'] = 3
                            estado['puntaje'] = 0
                            estado['pantalla_actual'] = 'juego_arcade'
                        case 2:
                            estado['dificultad'] = "Difícil"
                            estado['vidas'] = 3
                            estado['puntaje'] = 0
                            estado['pantalla_actual'] = 'juego_arcade'
                        case 3:
                            estado['pantalla_actual'] = 'menu_principal'
                indice += 1

def mostrar_login(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Iniciar Sesión", 640, 100, estado['paleta'])
    
    if 'campos_login' not in estado or estado['campos_login'] is None:
        estado['campos_login'] = {
            'usuario': crear_input_texto(440, 200, 400, 50),
            'password': crear_input_texto(440, 300, 400, 50)
        }
    
    pos_mouse = pygame.mouse.get_pos()
    
    dibujar_texto(ventana, "Usuario:", 440, 180, estado['paleta'], centrado=False)
    dibujar_texto(ventana, "Contraseña:", 440, 280, estado['paleta'], centrado=False)
    
    # Solo iterar si 'campos_login' no es None
    if estado['campos_login'] is not None:
        for campo in estado['campos_login'].values():
            pygame.draw.rect(ventana, estado['paleta']['texto'], campo['rect'], 2)
            if campo['activo']:
                pygame.draw.rect(ventana, estado['paleta']['resaltado'], campo['rect'], 4)
            
            texto_surface = pygame.font.Font(None, 36).render(
                '*' * len(campo['texto']) if campo == estado['campos_login']['password'] 
                else campo['texto'], True, estado['paleta']['texto']
            )
            ventana.blit(texto_surface, (campo['rect'].x + 5, campo['rect'].y + 5))
    
    boton_ingresar = crear_boton(440, 400, 400, 50, "Ingresar", estado['paleta'])
    boton_volver = crear_boton(440, 470, 400, 50, "Volver", estado['paleta'])
    
    actualizar_boton(boton_ingresar, pos_mouse)
    actualizar_boton(boton_volver, pos_mouse)
    
    dibujar_boton(ventana, boton_ingresar, estado['paleta'])
    dibujar_boton(ventana, boton_volver, estado['paleta'])
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Manejo de campos de texto
            if estado['campos_login'] is not None:
                for campo in estado['campos_login'].values():
                    campo['activo'] = campo['rect'].collidepoint(evento.pos)
            
            # Manejo de botones
            if actualizar_boton(boton_ingresar, evento.pos):
                if estado['campos_login'] is not None:
                    usuario = estado['campos_login']['usuario']['texto']
                    password = estado['campos_login']['password']['texto']
                    
                    if iniciar_sesion(usuario, password):
                        estado['usuario'] = usuario
                        estado['password'] = password
                        estado['pantalla_actual'] = 'menu_principal'
                        estado['campos_login'] = None
            
            elif actualizar_boton(boton_volver, evento.pos):
                estado['pantalla_actual'] = 'pre_menu'
                estado['campos_login'] = None
        
        elif evento.type == pygame.KEYDOWN:
            if estado['campos_login'] is not None:
                for campo in estado['campos_login'].values():
                    if campo['activo']:
                        if evento.key == pygame.K_RETURN:
                            campo['activo'] = False
                        elif evento.key == pygame.K_BACKSPACE:
                            campo['texto'] = campo['texto'][:-1]
                        elif evento.unicode.isprintable():
                            campo['texto'] += evento.unicode

def mostrar_registro(ventana, estado, eventos):
    ventana.fill(estado['paleta']['fondo'])
    
    dibujar_texto(ventana, "Registro de Usuario", 640, 100, estado['paleta'])
    
    if 'campos_registro' not in estado:
        estado['campos_registro'] = {
            'usuario': crear_input_texto(440, 200, 400, 50),
            'password1': crear_input_texto(440, 300, 400, 50),
            'password2': crear_input_texto(440, 400, 400, 50)
        }
    
    pos_mouse = pygame.mouse.get_pos()
    
    dibujar_texto(ventana, "Usuario:", 440, 180, estado['paleta'], centrado=False)
    dibujar_texto(ventana, "Contraseña:", 440, 280, estado['paleta'], centrado=False)
    dibujar_texto(ventana, "Confirmar contraseña:", 440, 380, estado['paleta'], centrado=False)
    
    for campo in estado['campos_registro'].values():
        pygame.draw.rect(ventana, estado['paleta']['texto'], campo['rect'], 2)
        if campo['activo']:
            pygame.draw.rect(ventana, estado['paleta']['resaltado'], campo['rect'], 4)
        
        texto_surface = pygame.font.Font(None, 36).render(
            '*' * len(campo['texto']) if campo in [estado['campos_registro']['password1'], 
                                                estado['campos_registro']['password2']] 
            else campo['texto'], True, estado['paleta']['texto']
        )
        ventana.blit(texto_surface, (campo['rect'].x + 5, campo['rect'].y + 5))
    
    boton_registrar = crear_boton(440, 500, 400, 50, "Registrarse", estado['paleta'])
    boton_volver = crear_boton(440, 570, 400, 50, "Volver", estado['paleta'])
    
    actualizar_boton(boton_registrar, pos_mouse)
    actualizar_boton(boton_volver, pos_mouse)
    
    dibujar_boton(ventana, boton_registrar, estado['paleta'])
    dibujar_boton(ventana, boton_volver, estado['paleta'])
    
    for evento in eventos:
        if evento.type == pygame.MOUSEBUTTONDOWN:
            # Manejo de campos de texto
            for campo in estado['campos_registro'].values():
                campo['activo'] = campo['rect'].collidepoint(evento.pos)
            
            # Manejo de botones
            if actualizar_boton(boton_registrar, evento.pos):
                usuario = estado['campos_registro']['usuario']['texto']
                password1 = estado['campos_registro']['password1']['texto']
                password2 = estado['campos_registro']['password2']['texto']
                
                if usuario and password1 and password2:
                    if not verificar_existencia_usuario(usuario):
                        if password1 == password2:
                            registrar_usuario(usuario, password1)
                            estado['pantalla_actual'] = 'pre_menu'
                            if 'campos_registro' in estado:
                                estado['campos_registro'] = None
            
            elif actualizar_boton(boton_volver, evento.pos):
                estado['pantalla_actual'] = 'pre_menu'
                if 'campos_registro' in estado:
                    estado['campos_registro'] = None
        
        elif evento.type == pygame.KEYDOWN:
            for campo in estado['campos_registro'].values():
                if campo['activo']:
                    if evento.key == pygame.K_RETURN:
                        campo['activo'] = False
                    elif evento.key == pygame.K_BACKSPACE:
                        campo['texto'] = campo['texto'][:-1]
                    elif evento.unicode.isprintable():
                        campo['texto'] += evento.unicode