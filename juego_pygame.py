import pygame
import random
import time
import pygame.mixer as mixer
import json
import os
from parser import *
from usuarios import *
from especificas_complejas import *

pygame.init()
mixer.init()

# Música
mixer.music.load("sonido/musica.mp3")
mixer.music.play(-1)

# Pantalla
display = pygame.display.set_mode((1000, 750))
pygame.display.set_caption("PyQuiz")

# Icono
icono = pygame.image.load("imagenes/corazoncito.png")
pygame.display.set_icon(icono)

# Colores

modo_daltonico = False



# Fuente
fuente_grande = pygame.font.SysFont("Segoe UI", 50, bold=True)
fuente_texto_bold = pygame.font.SysFont("Segoe UI", 36, bold=True)
fuente_texto_chica = pygame.font.SysFont("Segoe UI", 24, bold=True)

# Función para dibujar caja redondeada
def rectangulo_redondeado(surface, color, rect, radius=10, width=0):
    pygame.draw.rect(surface, color, rect, width=width, border_radius=radius)

# Botón volver
def dibujar_boton_volver():
    boton_volver = pygame.Rect(20, display.get_height() - 70, 100, 40)
    sombra_rect = boton_volver.copy()
    sombra_rect.x += 4
    sombra_rect.y += 4
    rectangulo_redondeado(display, sombra, sombra_rect, radius=12)

    mouse_pos = pygame.mouse.get_pos()
    color = lila_suave if boton_volver.collidepoint(mouse_pos) else blanco
    rectangulo_redondeado(display, color, boton_volver, radius=12)

    texto = fuente_texto_chica.render("Volver", True, violeta_profundo)
    texto_rect = texto.get_rect(center=boton_volver.center)
    display.blit(texto, texto_rect)

    return boton_volver

# Personajes
jaden = pygame.image.load("imagenes/jaden.png")
bauti = pygame.image.load("imagenes/bauti.png")
hina = pygame.image.load("imagenes/hina.png")
jess = pygame.image.load("imagenes/jess.png")
julie = pygame.image.load("imagenes/julie.png")

personajes = [jaden, bauti, hina, jess, julie]

def aplicar_modo_daltonico():
    global rosita, blanco, lila_suave, violeta_profundo, sombra

    if modo_daltonico:
        # Colores amigables para daltónicos (alto contraste)
        rosita = (216, 227, 254)
        blanco = (255, 255, 255)
        lila_suave = (147, 168, 215)  # Azul intenso
        violeta_profundo = (0, 68, 129)
        sombra = (178, 197, 240)
    else:
        # Restaurar los colores originales
        rosita = (250, 223, 255)
        blanco = (255, 255, 255)
        lila_suave = (236, 155, 215)
        violeta_profundo = (115, 55, 130)
        sombra = (230, 190, 240)

aplicar_modo_daltonico()


#1
def pantalla_de_carga():
    
    display.fill(rosita)
    duracion = 4
    tiempo_inicial = time.time()

    while time.time() - tiempo_inicial < duracion:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pass

        display.fill(rosita)

        # Animación de puntos
        puntos = int((time.time() - tiempo_inicial) * 2) % 4
        texto_carga = "Cargando" + "." * puntos
        texto_render = fuente_grande.render(texto_carga, True, violeta_profundo)
        display.blit(texto_render, (400, 350))

        pygame.display.update()
        pygame.time.delay(400) 

#2
def pre_menu(personajes):
    boton_iniciar_sesion = pygame.Rect(300, 200, 400, 60)
    boton_registrarse = pygame.Rect(300, 300, 400, 60)
    boton_ajustes = pygame.Rect(300, 400, 400, 60)
    boton_salir = pygame.Rect(300, 500, 400, 60)  # Nuevo botón

    pygame.display.update()

    running = True
    while running:
        display.fill(rosita)

        titulo = fuente_grande.render("PyQuiz", True, violeta_profundo)
        display.blit(titulo, (425, 50))

        botones = [
            (boton_iniciar_sesion, "Iniciar Sesión"),
            (boton_registrarse, "Registrarse"),
            (boton_ajustes, "Ajustes"),
            (boton_salir, "Salir del juego")  # Nuevo texto
        ]

        mouse_pos = pygame.mouse.get_pos()

        for rect, texto in botones:
            # Sombra
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, radius=12)

            # Hover
            color = lila_suave if rect.collidepoint(mouse_pos) else blanco

            rectangulo_redondeado(display, color, rect, radius=12)
            texto_render = fuente_texto_bold.render(texto, True, violeta_profundo)
            text_rect = texto_render.get_rect(center=rect.center)
            display.blit(texto_render, text_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_iniciar_sesion.collidepoint(evento.pos):
                    inicio_sesion(personajes)

                elif boton_registrarse.collidepoint(evento.pos):
                    registro()

                elif boton_ajustes.collidepoint(evento.pos):
                    ajustes()

                elif boton_salir.collidepoint(evento.pos):  # 🚪 salir
                    pygame.quit()
                    exit()

        pygame.display.update()

#4
def registro():
    nombre = ""
    contraseña = ""
    activo_nombre = True
    activo_contraseña = False
    mostrar_contraseña = False
    guardado = False
    mensaje = ""
    tiempo_mensaje = 0

    input_box_nombre = pygame.Rect(290, 200, 450, 60)
    input_box_contraseña = pygame.Rect(290, input_box_nombre.bottom + 40, 450, 60)
    mensaje_y = input_box_contraseña.bottom + 5
    boton_crear = pygame.Rect(390, mensaje_y + 70, 220, 50)

    ojo = pygame.image.load("imagenes/ojo.png")
    cerrado = pygame.image.load("imagenes/cerrado.png")
    ojo = pygame.transform.scale(ojo, (30, 30))
    cerrado = pygame.transform.scale(cerrado, (30, 30))

    if guardado:
        contra_guardada = fuente_texto_chica.render("¡La contraseña ha sido guardada!", True, blanco)
        display.blit(contra_guardada, (300, input_box_contraseña.y + 50))

    running = True
    while running:
        
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Registrar usuario", True, violeta_profundo)
        display.blit(titulo, (335, 50))

        # Etiquetas
        texto_usuario = fuente_texto_bold.render("Ingresar nombre de usuario:", True, blanco)
        display.blit(texto_usuario, (300, 150))

        texto_contra = fuente_texto_bold.render("Contraseña:", True, blanco)
        display.blit(texto_contra, (300, 300))

        # Caja usuario
        sombra_rect = input_box_nombre.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, radius=12)
        rectangulo_redondeado(display, blanco, input_box_nombre, radius=12)
        color_borde = lila_suave if activo_nombre else (180, 180, 180)
        pygame.draw.rect(display, lila_suave, input_box_nombre, width=3, border_radius=12)

        texto_nombre = fuente_texto_chica.render(nombre, True, violeta_profundo)
        display.blit(texto_nombre, (input_box_nombre.x + 15, input_box_nombre.y + 10))
        color_borde = lila_suave if activo_nombre else (180, 180, 180)
        pygame.draw.rect(display, color_borde, input_box_nombre, width=3, border_radius=12)

        # Caja contraseña
        sombra_contraseña = input_box_contraseña.copy()
        sombra_contraseña.x += 4
        sombra_contraseña.y += 4
        rectangulo_redondeado(display, sombra, sombra_contraseña, radius=12)
        rectangulo_redondeado(display, blanco, input_box_contraseña, radius=12)
        color_borde = lila_suave if activo_contraseña else (180, 180, 180)
        pygame.draw.rect(display, color_borde, input_box_contraseña, width=3, border_radius=12)

        # Mostrar contraseña (censurada o no)
        texto_mostrado = contraseña if mostrar_contraseña else "•" * len(contraseña)
        texto_contra = fuente_texto_chica.render(texto_mostrado, True, violeta_profundo)
        display.blit(texto_contra, (input_box_contraseña.x + 15, input_box_contraseña.y + 10))

        # Censura
        boton_ver = pygame.Rect(750, input_box_contraseña.y + 15, 30, 30)
        if mostrar_contraseña:
            display.blit(ojo, (boton_ver.x, boton_ver.y))
        else:
            display.blit(cerrado, (boton_ver.x, boton_ver.y))

        for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    running = False

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_volver.collidepoint(evento.pos):
                        return
                    
                    if input_box_nombre.collidepoint(evento.pos):
                        activo_nombre = True
                        activo_contraseña = False

                    elif input_box_contraseña.collidepoint(evento.pos):
                        activo_nombre = False
                        activo_contraseña = True

                    else:
                        activo_nombre = False
                        activo_contraseña = False

                    if boton_ver.collidepoint(evento.pos):
                        mostrar_contraseña = not mostrar_contraseña

                    if boton_crear.collidepoint(evento.pos):
                        tiempo_mensaje = time.time()
                        if nombre.strip() != "" and contraseña.strip() != "":
                            archivo = parser_json()
                            usuarios_guardados = archivo['jugadores']
                            if verificar_repeticion_usuarios(usuarios_guardados, nombre):
                                guardado = False
                                mensaje = "El usuario ya existe"
                            else:
                                nuevo_usuario = crear_usuario(nombre, contraseña)
                                agregar_usuario(usuarios_guardados, nuevo_usuario)
                                cargar_datos_json(archivo)
                                guardado = True
                                mensaje = "¡Usuario creado con éxito!"
                        else:
                            guardado = False
                            mensaje = "Faltan completar campos"

                if evento.type == pygame.KEYDOWN:
                    if activo_nombre:
                        if evento.key == pygame.K_RETURN:
                            activo_nombre = False
                        elif evento.key == pygame.K_BACKSPACE:
                            nombre = nombre[:-1]
                        else:
                            nombre += evento.unicode

                    elif activo_contraseña:
                        if evento.key == pygame.K_RETURN:
                            activo_contraseña = False
                        elif evento.key == pygame.K_BACKSPACE:
                            contraseña = contraseña[:-1]
                        else:
                            contraseña += evento.unicode

        # Mensaje bajo contraseña
        if mensaje != "":
            if time.time() - tiempo_mensaje < 3:
                texto_mensaje = fuente_texto_chica.render(mensaje, True, blanco)
                display.blit(texto_mensaje, (input_box_contraseña.x, mensaje_y))
            else:
                mensaje = ""

        # Botón "Crear usuario"
        mouse_pos = pygame.mouse.get_pos()
        sombra_rect = boton_crear.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, radius=12)

        # Hover
        if boton_crear.collidepoint(mouse_pos):
            color_boton = lila_suave
        else:
            color_boton = blanco

        rectangulo_redondeado(display, color_boton, boton_crear, radius=12)
        texto_boton = fuente_texto_bold.render("Crear usuario", True, violeta_profundo)
        text_rect = texto_boton.get_rect(center=boton_crear.center)
        display.blit(texto_boton, text_rect)

        boton_volver = dibujar_boton_volver()

        pygame.display.update()

#3
def inicio_sesion(personajes, generico = False, mensaje_inicio = "Iniciar Sesión"):
    nombre = ""
    contraseña = ""
    activo_nombre = True
    activo_contraseña = False
    mostrar_contraseña = False
    mensaje = ""
    tiempo_mensaje = 0

    archivo = parser_json()
    usuarios_guardados = archivo['jugadores']

    input_box_nombre = pygame.Rect(290, 200, 450, 60)
    input_box_contraseña = pygame.Rect(290, input_box_nombre.bottom + 40, 450, 60)
    mensaje_y = input_box_contraseña.bottom + 5
    boton_iniciar = pygame.Rect(390, mensaje_y + 70, 220, 50)

    # Texto clickeable
    texto_link = fuente_texto_chica.render("¿No creaste una cuenta aún?", True, blanco)
    rect_link = texto_link.get_rect(center=(500, boton_iniciar.bottom + 30))

    ojo = pygame.transform.scale(pygame.image.load("imagenes/ojo.png"), (30, 30))
    cerrado = pygame.transform.scale(pygame.image.load("imagenes/cerrado.png"), (30, 30))

    running = True
    while running:
        display.fill(rosita)

        # Titulo
        titulo = fuente_grande.render(mensaje_inicio, True, violeta_profundo)
        titulo_rect = titulo.get_rect(centerx=display.get_width() // 2)
        titulo_rect.top = 50
        display.blit(titulo, titulo_rect)

        # Etiquetas
        display.blit(fuente_texto_bold.render("Ingresar nombre de usuario:", True, blanco), (300, 150))
        display.blit(fuente_texto_bold.render("Contraseña:", True, blanco), (300, 300))

        # Input nombre
        sombra_rect = input_box_nombre.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        rectangulo_redondeado(display, blanco, input_box_nombre, 12)
        pygame.draw.rect(display, lila_suave if activo_nombre else (180,180,180), input_box_nombre, 3, 12)
        display.blit(fuente_texto_chica.render(nombre, True, violeta_profundo), (input_box_nombre.x+15, input_box_nombre.y+10))

        # Input contraseña
        sombra_rect = input_box_contraseña.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        rectangulo_redondeado(display, blanco, input_box_contraseña, 12)
        pygame.draw.rect(display, lila_suave if activo_contraseña else (180,180,180), input_box_contraseña, 3, 12)
        censura = contraseña if mostrar_contraseña else "•" * len(contraseña)
        display.blit(fuente_texto_chica.render(censura, True, violeta_profundo), (input_box_contraseña.x+15, input_box_contraseña.y+10))

        # Boton ver
        boton_ver = pygame.Rect(750, input_box_contraseña.y + 15, 30, 30)
        display.blit(ojo if mostrar_contraseña else cerrado, (boton_ver.x, boton_ver.y))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return
                if input_box_nombre.collidepoint(evento.pos):
                    activo_nombre, activo_contraseña = True, False
                elif input_box_contraseña.collidepoint(evento.pos):
                    activo_contraseña, activo_nombre = True, False
                else:
                    activo_nombre = activo_contraseña = False
                if boton_ver.collidepoint(evento.pos):
                    mostrar_contraseña = not mostrar_contraseña
                if boton_iniciar.collidepoint(evento.pos):
                    tiempo_mensaje = time.time()
                    if nombre.strip() != "" and contraseña.strip() != "":
                        for i in range(len(usuarios_guardados)):
                            if (usuarios_guardados[i]["nombre"] == nombre) and (usuarios_guardados[i]["contra"] == contraseña):
                                if generico:
                                    return nombre, contraseña
                                else:
                                    menu_principal(nombre, contraseña, personajes)
                            else:
                                mensaje = "Error, usuario o contraseña incorrecta."
                    else:
                        mensaje = "Faltan completar campos."
                if rect_link.collidepoint(evento.pos):
                    registro()

            elif evento.type == pygame.KEYDOWN:
                if activo_nombre:
                    if evento.key == pygame.K_RETURN:
                        activo_nombre = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nombre = nombre[:-1]
                    else:
                        nombre += evento.unicode
                elif activo_contraseña:
                    if evento.key == pygame.K_RETURN:
                        activo_contraseña = False
                    elif evento.key == pygame.K_BACKSPACE:
                        contraseña = contraseña[:-1]
                    else:
                        contraseña += evento.unicode

        # Mensaje
        if mensaje != "" and time.time() - tiempo_mensaje < 3:
            display.blit(fuente_texto_chica.render(mensaje, True, blanco), (input_box_contraseña.x, mensaje_y))

        # Botón iniciar sesión
        mouse_pos = pygame.mouse.get_pos()
        sombra_rect = boton_iniciar.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        color = lila_suave if boton_iniciar.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color, boton_iniciar, 12)
        texto_boton = fuente_texto_bold.render("Iniciar sesi\u00f3n", True, violeta_profundo)
        display.blit(texto_boton, texto_boton.get_rect(center=boton_iniciar.center))

        # Texto clickeable debajo
        display.blit(texto_link, rect_link)

        if not generico:
            boton_volver = dibujar_boton_volver()

        pygame.display.update()

#5
def ajustes():
    volumen_musica = 100
    volumen_efectos = 100

    opciones_volumen = [0, 25, 50, 75, 100]
    seleccion_musica = 4
    seleccion_efectos = 4

    barra_musica = pygame.Rect(290, 200, 450, 60)
    barra_efectos = pygame.Rect(290, barra_musica.bottom + 60, 450, 60)

    running = True
    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Ajustes", True, violeta_profundo)
        display.blit(titulo, (400, 50))

        # Etiquetas
        texto_musica = fuente_texto_bold.render("Volumen música:", True, blanco)
        texto_efectos = fuente_texto_bold.render("Volumen efectos:", True, blanco)
        display.blit(texto_musica, (300, 150))
        display.blit(texto_efectos, (300, barra_musica.bottom + 10))
        boton_daltonico = pygame.Rect(290, barra_efectos.bottom + 80, 450, 60)


        # Dibujar barra de música
        sombra_musica = barra_musica.copy()
        sombra_musica.x += 4; sombra_musica.y += 4
        rectangulo_redondeado(display, sombra, sombra_musica, 12)
        rectangulo_redondeado(display, blanco, barra_musica, 12)
        pygame.draw.rect(display, lila_suave, barra_musica, 3, 12)

        # Dibujar barra de efectos
        sombra_efectos = barra_efectos.copy()
        sombra_efectos.x += 4; sombra_efectos.y += 4
        rectangulo_redondeado(display, sombra, sombra_efectos, 12)
        rectangulo_redondeado(display, blanco, barra_efectos, 12)
        pygame.draw.rect(display, lila_suave, barra_efectos, 3, 12)

        # Dibujar opciones (5 divisiones)
        ancho_opcion = barra_musica.width // 5
        for i, valor in enumerate(opciones_volumen):
            # Música
            rect_op = pygame.Rect(barra_musica.x + i * ancho_opcion, barra_musica.y, ancho_opcion, barra_musica.height)
            color = lila_suave if i == seleccion_musica else blanco
            rectangulo_redondeado(display, color, rect_op, 12)
            texto = fuente_texto_chica.render(f"{valor}", True, violeta_profundo)
            texto_rect = texto.get_rect(center=rect_op.center)
            display.blit(texto, texto_rect)

            # Efectos
            rect_op2 = pygame.Rect(barra_efectos.x + i * ancho_opcion, barra_efectos.y, ancho_opcion, barra_efectos.height)
            color2 = lila_suave if i == seleccion_efectos else blanco
            rectangulo_redondeado(display, color2, rect_op2, 12)
            texto2 = fuente_texto_chica.render(f"{valor}", True, violeta_profundo)
            texto2_rect = texto2.get_rect(center=rect_op2.center)
            display.blit(texto2, texto2_rect)

            # Botón modo daltónico
        sombra_dalt = boton_daltonico.copy()
        sombra_dalt.x += 4; sombra_dalt.y += 4
        rectangulo_redondeado(display, sombra, sombra_dalt, 12)
        color_dalt = lila_suave if boton_daltonico.collidepoint(pygame.mouse.get_pos()) else blanco
        rectangulo_redondeado(display, color_dalt, boton_daltonico, 12)

        texto_dalt = fuente_texto_chica.render("Modo daltónico", True, violeta_profundo)
        display.blit(texto_dalt, texto_dalt.get_rect(center=boton_daltonico.center))


        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                
                if boton_volver.collidepoint(evento.pos):
                    return
                
                # Boton daltonico
                if boton_daltonico.collidepoint(evento.pos):
                    global modo_daltonico
                    modo_daltonico = not modo_daltonico
                    aplicar_modo_daltonico()

                # Check en barra de música
                for i in range(5):
                    rect_op = pygame.Rect(barra_musica.x + i * ancho_opcion, barra_musica.y, ancho_opcion, barra_musica.height)
                    if rect_op.collidepoint(evento.pos):
                        seleccion_musica = i
                        volumen_musica = opciones_volumen[i]
                        pygame.mixer.music.set_volume(volumen_musica / 100)

                # Check en barra de efectos
                for i in range(5):
                    rect_op2 = pygame.Rect(barra_efectos.x + i * ancho_opcion, barra_efectos.y, ancho_opcion, barra_efectos.height)
                    if rect_op2.collidepoint(evento.pos):
                        seleccion_efectos = i
                        volumen_efectos = opciones_volumen[i]
                


        boton_volver = dibujar_boton_volver()

        pygame.display.update()

#6
def menu_principal(nombre, contraseña, personajes):
    running = True

    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    id_usuario = obtener_id_usuario(nombre, contraseña)
    indice = lista_usuarios[id_usuario]['aspecto']

    # Cargar imágenes
    icono_personaje = pygame.image.load("imagenes/icono_personaje.png")
    icono_estadisticas = pygame.image.load("imagenes/icono_estadisticas.png")
    icono_ajustes = pygame.image.load("imagenes/icono_ajustes.png")
    icono_tienda = pygame.image.load("imagenes/icono_tienda.png")

    icono_personaje = pygame.transform.scale(icono_personaje, (150, 150))
    icono_estadisticas = pygame.transform.scale(icono_estadisticas, (100, 100))
    icono_ajustes = pygame.transform.scale(icono_ajustes, (100, 100))
    icono_tienda = pygame.transform.scale(icono_tienda, (100, 100))

    # Posiciones
    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2

    boton_personajes = pygame.Rect(centro_x - 350, centro_y - 100, 150, 150)
    boton_estadisticas = pygame.Rect(centro_x + 200, centro_y - 100, 150, 150)
    boton_ajustes = pygame.Rect(centro_x - 350, centro_y + 100, 150, 150)
    boton_tienda = pygame.Rect(centro_x + 200, centro_y + 100, 150, 150)
    boton_jugar = pygame.Rect(centro_x - 125, centro_y + 250, 250, 70)

    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("PyQuiz", True, violeta_profundo)
        titulo_rect = titulo.get_rect(center=(centro_x, 80))
        display.blit(titulo, titulo_rect)

        # Nombre usuario
        titulo = fuente_texto_bold.render(nombre, True, blanco)
        titulo_rect = titulo.get_rect(center=(centro_x, 150))
        display.blit(titulo, titulo_rect)

        # Imagen del personaje
        archivo = parser_json()
        lista_usuarios = archivo['jugadores']
        id_usuario = obtener_id_usuario(nombre, contraseña)
        indice = lista_usuarios[id_usuario]['aspecto']
        personaje = personajes[indice]
        display.blit(personaje, (centro_x - personaje.get_width() // 2, centro_y - 200))

        # Botones con sombra y hover
        mouse_pos = pygame.mouse.get_pos()

        def dibujar_boton(rect, imagen):
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, 12)
            color = lila_suave if rect.collidepoint(mouse_pos) else blanco
            rectangulo_redondeado(display, color, rect, 12)
            display.blit(imagen, imagen.get_rect(center=rect.center))

        dibujar_boton(boton_personajes, icono_personaje)
        dibujar_boton(boton_estadisticas, icono_estadisticas)
        dibujar_boton(boton_ajustes, icono_ajustes)
        dibujar_boton(boton_tienda, icono_tienda)

        # Botón JUGAR
        sombra_jugar = boton_jugar.copy()
        sombra_jugar.x += 4
        sombra_jugar.y += 4
        rectangulo_redondeado(display, sombra, sombra_jugar, 20)
        color_jugar = lila_suave if boton_jugar.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color_jugar, boton_jugar, 20)
        texto_jugar = fuente_texto_bold.render("JUGAR", True, violeta_profundo)
        display.blit(texto_jugar, texto_jugar.get_rect(center=boton_jugar.center))

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return
                if boton_jugar.collidepoint(evento.pos):
                    seleccion_modo(nombre, contraseña)
                elif boton_personajes.collidepoint(evento.pos):
                    seleccionar_personaje(nombre, contraseña, personajes)
                elif boton_estadisticas.collidepoint(evento.pos):
                    estadisticas()
                elif boton_ajustes.collidepoint(evento.pos):
                    ajustes()
                elif boton_tienda.collidepoint(evento.pos):
                    tienda(nombre)

        boton_volver = dibujar_boton_volver()
        
        pygame.display.update()

#7
def seleccion_modo(nombre, contraseña):
    running = True

    # Posiciones
    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2

    boton_arcade = pygame.Rect(centro_x - 200, centro_y - 100, 400, 80)
    boton_vs = pygame.Rect(centro_x - 200, centro_y + 20, 400, 80)

    # Imagen del botón ajustes
    icono_ajustes = pygame.image.load("imagenes/icono_ajustes.png")
    icono_ajustes = pygame.transform.scale(icono_ajustes, (60, 60))
    rect_ajustes = pygame.Rect(display.get_width() - 80, display.get_height() - 80, 60, 60)

    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Seleccionar modo", True, violeta_profundo)
        display.blit(titulo, (centro_x - titulo.get_width() // 2, 100))

        # Mouse
        mouse_pos = pygame.mouse.get_pos()

        # Función botón con sombra
        def dibujar_boton(rect, texto):
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, radius=12)
            color = lila_suave if rect.collidepoint(mouse_pos) else blanco
            rectangulo_redondeado(display, color, rect, radius=12)
            texto_render = fuente_texto_bold.render(texto, True, violeta_profundo)
            display.blit(texto_render, texto_render.get_rect(center=rect.center))

        # Dibujar botones
        dibujar_boton(boton_arcade, "Modo Arcade")
        dibujar_boton(boton_vs, "Modo VS")

        # Botón volver (esquina inferior izquierda)
        boton_volver = dibujar_boton_volver()

        # Botón ajustes (esquina inferior derecha)
        display.blit(icono_ajustes, rect_ajustes)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_arcade.collidepoint(evento.pos):
                    print("Modo Arcade seleccionado")
                    # Acá podés poner: juego_arcade(nombre)
                elif boton_vs.collidepoint(evento.pos):
                    segundo_jugador_nombre, segundo_jugador_contraseña = inicio_sesion(personajes, generico = True, mensaje_inicio = "Inicie sesión del segundo jugador")
                    jugar_pygame(nombre, contraseña, segundo_jugador_nombre, segundo_jugador_contraseña, personajes)
                elif boton_volver.collidepoint(evento.pos):
                    return
                elif rect_ajustes.collidepoint(evento.pos):
                    ajustes()

        pygame.display.update()

#8
def seleccionar_personaje(nombre, contraseña, personajes):
    running = True

    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    id_usuario = obtener_id_usuario(nombre, contraseña)
    indice_actual = lista_usuarios[id_usuario]['aspecto']

    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2

    # Cargar flechas
    flecha_izq = pygame.image.load("imagenes/flecha_izquierda.png")
    flecha_der = pygame.image.load("imagenes/flecha_derecha.png")
    flecha_izq = pygame.transform.scale(flecha_izq, (100, 100))
    flecha_der = pygame.transform.scale(flecha_der, (100, 100))

    rect_izq = pygame.Rect(centro_x - 350, centro_y, 60, 60)
    rect_der = pygame.Rect(centro_x + 250, centro_y, 60, 60)

    # Botón seleccionar
    boton_seleccionar = pygame.Rect(centro_x - 250, centro_y + 250, 500, 70)

    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Seleccionar personaje", True, violeta_profundo)
        display.blit(titulo, (centro_x - titulo.get_width() // 2, 80))

        # Nombre del usuario
        nombre_render = fuente_texto_bold.render(nombre, True, blanco)
        display.blit(nombre_render, (centro_x - nombre_render.get_width() // 2, 150))

        # Personaje actual
        personaje = personajes[indice_actual]
        display.blit(personaje, (centro_x - personaje.get_width() // 2, centro_y - 200))

        # Flechas
        display.blit(flecha_izq, rect_izq)
        display.blit(flecha_der, rect_der)

        # Botón seleccionar
        sombra_rect = boton_seleccionar.copy()
        sombra_rect.x += 4
        sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 20)
        mouse_pos = pygame.mouse.get_pos()
        color = lila_suave if boton_seleccionar.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color, boton_seleccionar, 20)
        texto = fuente_texto_bold.render("SELECCIONAR", True, violeta_profundo)
        display.blit(texto, texto.get_rect(center=boton_seleccionar.center))

        # Botón volver
        boton_volver = dibujar_boton_volver()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if rect_izq.collidepoint(evento.pos):
                    indice_actual = (indice_actual - 1) % len(personajes)
                elif rect_der.collidepoint(evento.pos):
                    indice_actual = (indice_actual + 1) % len(personajes)
                elif boton_seleccionar.collidepoint(evento.pos):
                    lista_usuarios[id_usuario]['aspecto'] = indice_actual
                    cargar_datos_json(archivo)
                    return
                elif boton_volver.collidepoint(evento.pos):
                    return

        pygame.display.update()

#9
def estadisticas():
    archivo = parser_json()
    jugadores = archivo.get("jugadores", [])

    running = True
    scroll_offset = 0
    max_scroll = max(0, len(jugadores) * 60 - 450)

    columna_x = [90, 240, 380, 510, 640, 770]
    columnas = ["Nombre", "TPP (s)", "Rondas", "Aciertos", "Errores", "Ganadas"]

    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Estadísticas Globales", True, violeta_profundo)
        display.blit(titulo, titulo.get_rect(center=(500, 50)))

        # Dibujar encabezados
        for i, texto in enumerate(columnas):
            encabezado = fuente_texto_bold.render(texto, True, blanco)
            display.blit(encabezado, (columna_x[i], 120))

        # Dibujar filas de jugadores
        for idx, jugador in enumerate(jugadores):
            y = 170 + idx * 50 - scroll_offset
            if 130 < y < 700:
                datos = [
                    jugador['nombre'],
                    f"{jugador['promedio_tiempo_por_ronda']:.2f}",
                    str(jugador['rondas_jugadas']),
                    str(jugador['aciertos_totales']),
                    str(jugador['errores_totales']),
                    str(jugador['wins'])
                ]
                for i, dato in enumerate(datos):
                    celda = pygame.Rect(columna_x[i] - 10, y - 5, 120, 40)
                    rectangulo_redondeado(display, blanco, celda, 8)
                    texto = fuente_texto_chica.render(dato, True, violeta_profundo)
                    display.blit(texto, (celda.x + 10, celda.y + 8))

        # Scroll con flechas
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            scroll_offset = max(scroll_offset - 10, 0)
        elif keys[pygame.K_DOWN]:
            scroll_offset = min(scroll_offset + 10, max_scroll)

        volver_rect = dibujar_boton_volver()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if volver_rect.collidepoint(evento.pos):
                    return

        pygame.display.update()

def dibujar_boton_item(rect, imagen):
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, 16)
            color = lila_suave if rect.collidepoint(mouse_pos) else blanco
            rectangulo_redondeado(display, color, rect, 16)
            display.blit(imagen, imagen.get_rect(center=rect.center))

            # Precio debajo
            texto_precio = fuente_texto_chica.render("1000 puntos", True, blanco)
            precio_rect = texto_precio.get_rect(center=(rect.centerx, rect.bottom + 25))
            display.blit(texto_precio, precio_rect)

#10
def tienda(nombre):
    if os.path.exists("estadisticas.json"):
        with open("estadisticas.json", "r") as f:
            todas_estadisticas = json.load(f)
    else:
        todas_estadisticas = {}

    if nombre not in todas_estadisticas:
        todas_estadisticas[nombre] = {
            "puntaje_total": 0,
            "modo_arcade": {"total": 0, "mejor": 0},
            "modo_vs": {"total": 0, "mejor": 0}
        }

    puntos = todas_estadisticas[nombre]["puntaje_total"]
    mensaje = ""
    tiempo_mensaje = 0

    # Cargar imágenes de ítems
    miau = pygame.image.load("imagenes/miau.png")
    pizza = pygame.image.load("imagenes/pizza.png")
    miau = pygame.transform.scale(miau, (150, 150))
    pizza = pygame.transform.scale(pizza, (150, 150))

    # Botones
    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2
    boton_miau = pygame.Rect(centro_x - 250, centro_y - 100, 200, 200)
    boton_pizza = pygame.Rect(centro_x + 50, centro_y - 100, 200, 200)

    running = True
    while running:
        display.fill(rosita)

        # Título
        titulo = fuente_grande.render("Tienda", True, violeta_profundo)
        titulo_rect = titulo.get_rect(center=(centro_x, 80))
        display.blit(titulo, titulo_rect)

        # Puntos del usuario
        texto_puntos = fuente_texto_bold.render(f"Puntos: {puntos}", True, blanco)
        texto_puntos_rect = texto_puntos.get_rect(center=(centro_x, 150))
        display.blit(texto_puntos, texto_puntos_rect)

        # Mouse
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar botones con imágenes y precios
        

        dibujar_boton_item(boton_miau, miau)
        dibujar_boton_item(boton_pizza, pizza)

        # Mostrar mensaje de compra si corresponde
        if mensaje != "" and time.time() - tiempo_mensaje < 3:
            texto_mensaje = fuente_texto_bold.render(mensaje, True, blanco)
            texto_mensaje_rect = texto_mensaje.get_rect(center=(centro_x, boton_pizza.bottom + 100))
            display.blit(texto_mensaje, texto_mensaje_rect)

        # Botón volver
        boton_volver = dibujar_boton_volver()

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_volver.collidepoint(evento.pos):
                    return

                elif boton_miau.collidepoint(evento.pos) or boton_pizza.collidepoint(evento.pos):
                    if puntos >= 1000:
                        puntos -= 1000
                        todas_estadisticas[nombre]["puntaje_total"] = puntos
                        with open("estadisticas.json", "w") as f:
                            json.dump(todas_estadisticas, f)
                        mensaje = "¡Item comprado con éxito!"
                    else:
                        mensaje = "No tiene suficientes puntos"
                    tiempo_mensaje = time.time()

        pygame.display.update()

def mostrar_pausa():
    boton_continuar = pygame.Rect(375, 300, 250, 60)
    boton_menu = pygame.Rect(375, 400, 250, 60)
    boton_salir = pygame.Rect(375, 500, 250, 60)


    en_pausa = True
    while en_pausa:
        display.fill(rosita)

        titulo = fuente_grande.render("Pausa", True, violeta_profundo)
        display.blit(titulo, titulo.get_rect(center=(500, 200)))

        mouse_pos = pygame.mouse.get_pos()

        # Botón continuar
        sombra_rect = boton_continuar.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        color = lila_suave if boton_continuar.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color, boton_continuar, 12)
        texto = fuente_texto_bold.render("Continuar", True, violeta_profundo)
        display.blit(texto, texto.get_rect(center=boton_continuar.center))

        # Botón volver a menú
        sombra_rect = boton_menu.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        color = lila_suave if boton_menu.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color, boton_menu, 12)
        texto = fuente_texto_bold.render("Volver al menú", True, violeta_profundo)
        display.blit(texto, texto.get_rect(center=boton_menu.center))

        # Botón salir al escritorio
        sombra_rect = boton_salir.copy()
        sombra_rect.x += 4; sombra_rect.y += 4
        rectangulo_redondeado(display, sombra, sombra_rect, 12)
        color = lila_suave if boton_salir.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color, boton_salir, 12)
        texto = fuente_texto_bold.render("Salir al escritorio", True, violeta_profundo)
        display.blit(texto, texto.get_rect(center=boton_salir.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_continuar.collidepoint(evento.pos):
                    en_pausa = False
                elif boton_menu.collidepoint(evento.pos):
                    pre_menu(personajes)
                    return  # sale de pausa completamente
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    exit()

        pygame.display.update()


def pantalla_de_pregunta_6_opciones(nombre, contraseña):
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    usuario_id = obtener_id_usuario(nombre, contraseña)
    jugador = lista_usuarios[usuario_id]
    indice_aspecto = lista_usuarios[usuario_id]['aspecto']
    texto_pregunta = f"Categorías restantes: {jugador['categorias_restantes']}"

    #posiciones
    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2

    #cajas
    boton_opcion_1 = pygame.Rect(centro_x - 450, centro_y - 50, 400, 100)
    boton_opcion_2 = pygame.Rect(centro_x + 50, centro_y - 50, 400, 100)
    boton_opcion_3 = pygame.Rect(centro_x - 450, centro_y + 75, 400, 100)
    boton_opcion_4 = pygame.Rect(centro_x + 50, centro_y + 75, 400, 100)
    boton_opcion_5 = pygame.Rect(centro_x - 450, centro_y + 200, 400, 100)
    boton_opcion_6 = pygame.Rect(centro_x + 50, centro_y + 200, 400, 100)
    boton_pausa = pygame.Rect(850, 50, 100, 50)
    caja_pregunta = pygame.Rect(centro_x - 220, centro_y - 225, 550, 150)

    # Imagen
    imagen = personajes[indice_aspecto]    #cambiar por personaje q este usando el usuario
    imagen = pygame.transform.scale(imagen, (270, 320))

    running = True
    while running:
        display.fill(rosita)
        mouse_pos = pygame.mouse.get_pos()

        # Botón de pausa
        sombra_pausa = boton_pausa.copy()
        sombra_pausa.x += 4; sombra_pausa.y += 4
        rectangulo_redondeado(display, sombra, sombra_pausa, 12)
        color_pausa = lila_suave if boton_pausa.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color_pausa, boton_pausa, 12)
        texto_pausa = fuente_texto_chica.render("Pausa", True, violeta_profundo)
        display.blit(texto_pausa, texto_pausa.get_rect(center=boton_pausa.center))

        #caja pregunta
        sombra_caja_pregunta = caja_pregunta.copy()
        sombra_caja_pregunta.x += 4; sombra_caja_pregunta.y += 4
        rectangulo_redondeado(display, sombra, sombra_caja_pregunta, 12)
        color_caja_pregunta = blanco
        rectangulo_redondeado(display, color_caja_pregunta, caja_pregunta, 12)
        texto_caja_pregunta = fuente_texto_chica.render(texto_pregunta, True, violeta_profundo)
        display.blit(texto_caja_pregunta, texto_caja_pregunta.get_rect(center=caja_pregunta.center))

        pregunta = fuente_texto_bold.render(texto_pregunta, True, violeta_profundo)
        display.blit(pregunta, (350, 30))
        categoría = fuente_texto_bold.render("Elija una categoría", True, violeta_profundo)
        display.blit(categoría, (350, 80))
        display.blit(imagen, (20, 20))

        sombra_pausa = boton_pausa.copy()
        sombra_pausa.x += 4; sombra_pausa.y += 4
        rectangulo_redondeado(display, sombra, sombra_pausa, 12)
        color_pausa = lila_suave if boton_pausa.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color_pausa, boton_pausa, 12)
        texto_pausa = fuente_texto_chica.render("Pausa", True, violeta_profundo)
        display.blit(texto_pausa, texto_pausa.get_rect(center=boton_pausa.center))

        opciones = [
            (boton_opcion_1, "Historia"),
            (boton_opcion_2, "Ciencia"),
            (boton_opcion_3, "Geografía"),
            (boton_opcion_4, "Arte"),
            (boton_opcion_5, "Deportes"),
            (boton_opcion_6, "Entretenimiento")
        ]

        for rect, texto in opciones:
            # Sombra
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, radius=12)

            # Detectar si el mouse está encima
            if rect.collidepoint(mouse_pos):
                color = lila_suave
            else:
                color = blanco

            # Botones
            rectangulo_redondeado(display, color, rect, radius=12)
            texto_render = fuente_texto_chica.render(texto, True, violeta_profundo)
            text_rect = texto_render.get_rect(center=rect.center)
            display.blit(texto_render, text_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_opcion_1.collidepoint(evento.pos):
                    categoria_electa = "Historia"
                    return categoria_electa

                elif boton_opcion_2.collidepoint(evento.pos):
                    categoria_electa = "Ciencia"
                    return categoria_electa

                elif boton_opcion_3.collidepoint(evento.pos):
                    categoria_electa = "Geografía"
                    return categoria_electa

                elif boton_opcion_4.collidepoint(evento.pos):
                    categoria_electa = "Arte"
                    return categoria_electa

                elif boton_opcion_5.collidepoint(evento.pos):
                    categoria_electa = "Deportes"
                    return categoria_electa
                    
                elif boton_opcion_6.collidepoint(evento.pos):
                    categoria_electa = "Entretenimiento"
                    return categoria_electa

                elif boton_pausa.collidepoint(evento.pos):
                    mostrar_pausa()

        pygame.display.update()

def pantalla_de_pregunta_4_opciones(nombre, contraseña, personajes, categoria_electa, texto_pregunta, lista_respuestas):
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    usuario_id = obtener_id_usuario(nombre, contraseña)
    jugador = lista_usuarios[usuario_id]
    indice_aspecto = lista_usuarios[usuario_id]['aspecto']
    respuesta_a = lista_respuestas[0]
    respuesta_b = lista_respuestas[1]
    respuesta_c = lista_respuestas[2]
    respuesta_d = lista_respuestas[3]

    #posiciones
    centro_x = display.get_width() // 2
    centro_y = display.get_height() // 2

    #Botones
    boton_opcion_1 = pygame.Rect(centro_x - 450, centro_y, 400, 100)
    boton_opcion_2 = pygame.Rect(centro_x + 50, centro_y, 400, 100)
    boton_opcion_3 = pygame.Rect(centro_x - 450, centro_y + 150, 400, 100)
    boton_opcion_4 = pygame.Rect(centro_x + 50, centro_y + 150, 400, 100)
    boton_pausa = pygame.Rect(850, 50, 100, 50)
    caja_pregunta = pygame.Rect(centro_x - 220, centro_y - 225, 550, 150) 
    

    # Imagen decorativa (más grande que el botón de pausa)
    imagen = personajes[indice_aspecto]    #cambiar por personaje q este usando el usuario
    imagen = pygame.transform.scale(imagen, (270, 320))

    running = True
    while running:
        display.fill(rosita)
        mouse_pos = pygame.mouse.get_pos()

        # Botón de pausa
        sombra_pausa = boton_pausa.copy()
        sombra_pausa.x += 4; sombra_pausa.y += 4
        rectangulo_redondeado(display, sombra, sombra_pausa, 12)
        color_pausa = lila_suave if boton_pausa.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color_pausa, boton_pausa, 12)
        texto_pausa = fuente_texto_chica.render("Pausa", True, violeta_profundo)
        display.blit(texto_pausa, texto_pausa.get_rect(center=boton_pausa.center))

        #caja pregunta
        
        sombra_caja_pregunta = caja_pregunta.copy()
        sombra_caja_pregunta.x += 4; sombra_caja_pregunta.y += 4
        rectangulo_redondeado(display, sombra, sombra_caja_pregunta, 12)
        color_caja_pregunta = blanco
        rectangulo_redondeado(display, color_caja_pregunta, caja_pregunta, 12)
        texto_caja_pregunta = fuente_texto_chica.render(texto_pregunta, True, violeta_profundo)
        display.blit(texto_caja_pregunta, texto_caja_pregunta.get_rect(center=caja_pregunta.center))

        pregunta = fuente_texto_bold.render(texto_pregunta, True, violeta_profundo)
        display.blit(pregunta, (350, 30))
        categoria = fuente_texto_bold.render(f"Categoría: {categoria_electa}", True, violeta_profundo)
        display.blit(categoria, (350, 80))
        display.blit(imagen, (20, 20))
        texto_corona = fuente_texto_bold.render(f"Puntos corona: {jugador['puntos_corona']}", True, violeta_profundo)
        display.blit(texto_corona, (350, 110))
        texto_puntos = fuente_texto_bold.render(f"Puntos: {jugador['puntos']}", True, violeta_profundo)
        display.blit(texto_puntos, (350, 140))


        sombra_pausa = boton_pausa.copy()
        sombra_pausa.x += 4; sombra_pausa.y += 4
        rectangulo_redondeado(display, sombra, sombra_pausa, 12)
        color_pausa = lila_suave if boton_pausa.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color_pausa, boton_pausa, 12)
        texto_pausa = fuente_texto_chica.render("Pausa", True, violeta_profundo)
        display.blit(texto_pausa, texto_pausa.get_rect(center=boton_pausa.center))

        opciones = [
            (boton_opcion_1, respuesta_a),
            (boton_opcion_2, respuesta_b),
            (boton_opcion_3, respuesta_c),
            (boton_opcion_4, respuesta_d)
        ]

        for rect, texto in opciones:
            # Sombra
            sombra_rect = rect.copy()
            sombra_rect.x += 4
            sombra_rect.y += 4
            rectangulo_redondeado(display, sombra, sombra_rect, radius=12)

            # Detectar si el mouse está encima
            if rect.collidepoint(mouse_pos):
                color = lila_suave
            else:
                color = blanco

            # Botones
            rectangulo_redondeado(display, color, rect, radius=12)
            texto_render = fuente_texto_chica.render(texto, True, violeta_profundo)
            text_rect = texto_render.get_rect(center=rect.center)
            display.blit(texto_render, text_rect)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_opcion_1.collidepoint(evento.pos):
                    respuesta = 'a'
                    return respuesta

                elif boton_opcion_2.collidepoint(evento.pos):
                    respuesta = 'b'
                    return respuesta

                elif boton_opcion_3.collidepoint(evento.pos):
                    respuesta = 'c'
                    return respuesta

                elif boton_opcion_4.collidepoint(evento.pos):
                    respuesta = 'd'
                    return respuesta

                elif boton_pausa.collidepoint(evento.pos):
                    mostrar_pausa()

        pygame.display.update()

def jugar_ronda_normal(nombre, contraseña, categoria_para_ronda, personajes):
    terminado = False
    archivo = parser_json()
    preguntas_dict = parser_csv()
    lista_usuarios = archivo['jugadores']
    jugador_id = obtener_id_usuario(nombre, contraseña)
    jugador = lista_usuarios[jugador_id]

    while not terminado:
        archivo = parser_json()
        lista_usuarios = archivo['jugadores']
        jugador_id = obtener_id_usuario(nombre, contraseña)
        jugador = lista_usuarios[jugador_id]
        pregunta_numero = elegir_numero_de_pregunta_aleatorio(preguntas_dict, categoria_para_ronda)
        pregunta_de_ronda = preguntas_dict[categoria_para_ronda][pregunta_numero]
        respuesta = pantalla_de_pregunta_4_opciones(nombre, contraseña, personajes, categoria_para_ronda, pregunta_de_ronda['pregunta'], pregunta_de_ronda['opciones'])
        if respuesta == pregunta_de_ronda['respuesta']:
            jugador['puntos_corona'] += 1
            jugador['aciertos_totales'] += 1
            cargar_datos_json(archivo)
            print('Correcto')
            break
        else:
            jugador['puntos_corona'] = 0
            jugador['errores_totales'] += 1
            terminado = True
            cargar_datos_json(archivo)
            print('Incorrecto')
            break
    return terminado

def jugar_ronda_corona(nombre, contraseña, personajes):    
    terminado = False
    archivo = parser_json()
    preguntas_dict = parser_csv()
    lista_usuarios = archivo['jugadores']
    jugador_id = obtener_id_usuario(nombre, contraseña)
    jugador = lista_usuarios[jugador_id]

    while not terminado:
        categoria_para_ronda = pantalla_de_pregunta_6_opciones(nombre, contraseña)
        while categoria_para_ronda not in jugador['categorias_restantes']:
            categoria_para_ronda = pantalla_de_pregunta_6_opciones(nombre, contraseña)
        pregunta_numero = elegir_numero_de_pregunta_aleatorio(preguntas_dict, categoria_para_ronda)
        pregunta_de_ronda = preguntas_dict[categoria_para_ronda][pregunta_numero]
        respuesta = pantalla_de_pregunta_4_opciones(nombre, contraseña, personajes, categoria_para_ronda, pregunta_de_ronda['pregunta'], pregunta_de_ronda['opciones'])
        if respuesta == pregunta_de_ronda['respuesta']:
            jugador['puntos'] += 1
            if categoria_para_ronda in jugador['categorias_restantes']:
                jugador['categorias_restantes'].remove(categoria_para_ronda) 
            jugador['puntos_corona'] = 0
            jugador['aciertos_totales'] += 1
            cargar_datos_json(archivo)
            print('Correcto')
            break
        else:
            jugador['puntos_corona'] = 0
            jugador['errores_totales'] += 1
            terminado = True
            cargar_datos_json(archivo)
            print('Incorrecto')
            break
    return terminado
    
def jugar_turno_pygame(nombre, contraseña, personajes):
    jugador_id = obtener_id_usuario(nombre, contraseña)
    archivo = parser_json()
    lista_usuarios = archivo['jugadores']
    jugador = lista_usuarios[jugador_id]

    categorias = ['Historia', 'Ciencia', 'Geografía', 'Arte', 'Deportes', 'Entretenimiento', 'Corona']

    terminado = False

    while not terminado:
        categoria_para_ronda = obtener_categoria_aleatoria(categorias)
        archivo = parser_json()
        lista_usuarios = archivo['jugadores']
        jugador = lista_usuarios[jugador_id]
        if jugador['puntos'] >= 6:
            terminado = True
            return terminado
        elif calcular_puntos_coronas(categoria_para_ronda, jugador['puntos_corona']):
            terminado = jugar_ronda_corona(nombre, contraseña, personajes)
            if terminado:
                break
        else:
            terminado = jugar_ronda_normal(nombre, contraseña, categoria_para_ronda, personajes)
            if terminado:
                break

    return terminado

def pantalla_ganador(nombre_ganador, avatar_ganador, puntaje_ganador,
    nombre_perdedor, avatar_perdedor, puntaje_perdedor, nombre, contraseña):

    # 🛡️ Verificación de imágenes válidas
    if avatar_ganador is None or avatar_perdedor is None:
        print("❌ Error: avatar no cargado correctamente")
        pygame.time.wait(2000)
        return

    # 📸 Redimensionar sin modificar la imagen original
    avatar_ganador = pygame.transform.scale(avatar_ganador.copy(), (450, 520))
    avatar_perdedor = pygame.transform.scale(avatar_perdedor.copy(), (350, 400))

    # 🎮 Botones
    boton_jugar_otra_vez = pygame.Rect(350, 600, 300, 60)
    boton_menu = pygame.Rect(400, 670, 200, 40)

    running = True
    while running:
        display.fill(rosita)
        mouse_pos = pygame.mouse.get_pos()

        # 🏆 Títulos
        texto_ganador = fuente_grande.render("GANADOR", True, violeta_profundo)
        display.blit(texto_ganador, texto_ganador.get_rect(center=(500, 50)))

        texto_nombre = fuente_texto_bold.render(nombre_ganador, True, violeta_profundo)
        display.blit(texto_nombre, texto_nombre.get_rect(center=(500, 110)))

        # 👑 Avatar ganador
        display.blit(avatar_ganador, avatar_ganador.get_rect(center=(500, 425)))
        texto_puntaje_g = fuente_texto_chica.render(f"Puntaje: {puntaje_ganador}", True, blanco)
        display.blit(texto_puntaje_g, texto_puntaje_g.get_rect(center=(500, 575)))

        # 😢 Avatar perdedor
        texto_nombre_p = fuente_texto_chica.render(nombre_perdedor, True, violeta_profundo)
        display.blit(texto_nombre_p, texto_nombre_p.get_rect(center=(825, 180)))
        display.blit(avatar_perdedor, avatar_perdedor.get_rect(center=(825, 425)))
        texto_puntaje_p = fuente_texto_chica.render(f"Puntaje: {puntaje_perdedor}", True, blanco)
        display.blit(texto_puntaje_p, texto_puntaje_p.get_rect(center=(825, 550)))

        # 🔁 Botón jugar otra vez
        sombra1 = boton_jugar_otra_vez.copy(); sombra1.x += 4; sombra1.y += 4
        rectangulo_redondeado(display, sombra, sombra1, 12)
        color1 = lila_suave if boton_jugar_otra_vez.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color1, boton_jugar_otra_vez, 12)
        texto_jugar = fuente_texto_bold.render("Jugar otra vez", True, violeta_profundo)
        display.blit(texto_jugar, texto_jugar.get_rect(center=boton_jugar_otra_vez.center))

        # ⏪ Botón menú
        sombra2 = boton_menu.copy(); sombra2.x += 4; sombra2.y += 4
        rectangulo_redondeado(display, sombra, sombra2, 12)
        color2 = lila_suave if boton_menu.collidepoint(mouse_pos) else blanco
        rectangulo_redondeado(display, color2, boton_menu, 12)
        texto_menu = fuente_texto_chica.render("Menú", True, violeta_profundo)
        display.blit(texto_menu, texto_menu.get_rect(center=boton_menu.center))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_jugar_otra_vez.collidepoint(evento.pos):
                    print("Jugar otra vez")
                    running = False  # volvés al flujo anterior
                elif boton_menu.collidepoint(evento.pos):
                    menu_principal(nombre, contraseña, personajes)

        pygame.display.update()


def jugar_pygame(jugador1_nombre, jugador1_contraseña, jugador2_nombre, jugador2_contraseña, personajes):
    archivo = parser_json()
    lista_usuario = archivo['jugadores']
    
    jugador1_id = obtener_id_usuario(jugador1_nombre, jugador1_contraseña)
    jugador2_id = obtener_id_usuario(jugador2_nombre, jugador2_contraseña)
    jugador1 = lista_usuario[jugador1_id]
    jugador2 = lista_usuario[jugador2_id]
    avatar1 = personajes[(jugador1['aspecto'])]
    avatar2 = personajes[(jugador2['aspecto'])]

    turno_jugador = True
    en_juego = True
    puntos_necesarios = 6

    while en_juego:
        if jugador1['puntos'] >= puntos_necesarios or jugador2['puntos'] >= puntos_necesarios:
            print("Puntos jugador 1:", jugador1['puntos'])
            print("Puntos jugador 2:", jugador2['puntos'])
            en_juego = False
            break
        if turno_jugador:
            perdió_turno = jugar_turno_pygame(jugador1_nombre, jugador1_contraseña, personajes)
            archivo = parser_json()
            jugador1 = archivo['jugadores'][jugador1_id]
            if jugador1['puntos'] >= puntos_necesarios:
                en_juego = False
                break
            if perdió_turno:
                turno_jugador = False
        else:
            perdió_turno = jugar_turno_pygame(jugador2_nombre, jugador2_contraseña, personajes)
            archivo = parser_json()
            jugador2 = archivo['jugadores'][jugador2_id]
            if jugador2['puntos'] >= puntos_necesarios:
                en_juego = False
                break
            if perdió_turno:
                turno_jugador = True

    archivo = parser_json()
    lista_usuario = archivo['jugadores']
    jugador1 = lista_usuario[jugador1_id]
    jugador2 = lista_usuario[jugador2_id]

    # 🏁 Lógica de victoria
    if jugador1['puntos'] > jugador2['puntos']:
        jugador1['wins'] += 1
        jugador_ganador = jugador1
        aspecto_ganador = avatar1

        jugador_perdedor = jugador2
        aspecto_perdedor = avatar2

    elif jugador2['puntos'] > jugador1['puntos']:
        jugador2['wins'] += 1
        jugador_ganador = jugador2
        aspecto_ganador = avatar2

        jugador_perdedor = jugador1
        aspecto_perdedor = avatar1
    else:
        print('Empate!')
        jugador1['puntos'] = 0
        jugador2['puntos'] = 0
        cargar_datos_json(archivo)
        return

    jugador1['puntos'] = 0
    jugador2['puntos'] = 0
    agregar_todas_las_categorias()
    cargar_datos_json(archivo)
    pantalla_ganador(jugador_ganador['nombre'], aspecto_ganador, jugador_ganador['wins'],
                    jugador_perdedor['nombre'], aspecto_perdedor, jugador_perdedor['wins'],
                    jugador1_nombre, jugador1_contraseña)

pre_menu(personajes)




