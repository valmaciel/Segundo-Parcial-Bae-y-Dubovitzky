def inicializar_mensajes_menu_principal(usuario:str) -> tuple:
    mensaje_bienvenido = f"¡Hola {usuario}!"
    mensaje_opciones = """Elija su opción:
    1. Jugar juego ARCADE
    2. Jugar juego VERSUS
    3. Ver estadísticas
    4. Opciones
    5. Cerrar sesión\n"""
    mensaje_salida = "Cerrando sesión..."

    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_pre_menu() -> tuple:
    mensaje_bienvenido = "¡Bienvenido a PyQUIZ!"
    mensaje_opciones = """Elija su opción:
    1. Iniciar sesión
    2. Registrarse
    3. Opciones
    4. Salir del juego\n"""
    mensaje_salida = "¡Gracias por jugar PyQUIZ!\nSaliendo..."

    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_ajustes() -> tuple:
    mensaje_bienvenido = "Ajustes:"
    mensaje_opciones = """Elija su opción:
    1. Sonido
    2. Accesibilidad
    3. Volver\n"""
    mensaje_salida = "Volviendo..."

    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_sonido() -> tuple:
    mensaje_bienvenido = "Sonido:"
    mensaje_opciones = """Elija su opción:
    1. Volumen general
    2. Música
    3. Efectos
    4. Volver\n"""
    mensaje_salida = "Volviendo..."
    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_accesibilidad() -> tuple:
    mensaje_bienvenido = "Accesibilidad:"
    mensaje_opciones = """Elija su opción:
    1. TDAH
    2. Daltonismo
    3. TEA
    4. Volver\n"""
    mensaje_salida = "Volviendo..."
    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_accesibilidad_toggle(subconfig:str, estado:bool) -> tuple:
    diccionario = {True: "ON", False: "OFF"}
    estado_subconfig = diccionario[estado]

    mensaje_bienvenido = f"Configuración de {subconfig.upper()}\n\nOpción está {estado_subconfig}"
    mensaje_opciones = """Elija su opción:
    1. ON
    2. OFF
    3. Volver\n"""
    mensaje_salida = "Volviendo..."
    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_accesibilidad_daltonismo(estado_subconfig:str) -> tuple:
    mensaje_bienvenido = f"Opciones de DALTONISMO\n\nTipo de daltonismo activado: {estado_subconfig.capitalize()}"
    mensaje_opciones = """Elija su opción:
    1. Protanopía
    2. Deuteranopía
    3. Tritanopía
    4. Ninguno
    5. Volver\n"""
    mensaje_salida = "Volviendo..."
    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

def inicializar_mensajes_estadisticas_usuario(partidas_ganadas:int, aciertos_totales:int, errores_totales:int, rondas_totales:int, tiempo_promedio_por_pregunta:float) -> tuple:
    mensaje_partidas_ganadas = f"Partidas ganadas: {partidas_ganadas:.0f}"
    mensaje_aciertos_totales = f"Aciertos totales: {aciertos_totales:.0f}"
    mensaje_errores_totales = f"Errores totales: {errores_totales:.0f}"
    mensaje_rondas_totales = f"Rondas jugadas: {rondas_totales:.0f}"
    mensaje_tiempo_promedio_por_pregunta = f"Tiempo promedio por pregunta (s): {tiempo_promedio_por_pregunta:.2f}"
    return mensaje_partidas_ganadas, mensaje_aciertos_totales, mensaje_errores_totales, mensaje_rondas_totales, mensaje_tiempo_promedio_por_pregunta

def inicializar_mensajes_menu_arcade(usuario:str):
    mensaje_bienvenido = f"¡Bienvenido {usuario}!"
    mensaje_opciones = """Elige tu dificultad:
    1. Fácil
    2. Normal
    3. Difícil
    4. Volver al menú principal\n"""
    mensaje_salida = "Volviendo..."
    return mensaje_bienvenido, mensaje_opciones, mensaje_salida

