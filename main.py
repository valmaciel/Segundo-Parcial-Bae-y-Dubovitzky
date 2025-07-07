import random
from especificas_simples import *
from especificas_complejas import *
from input import *
from parser import *
from usuarios import *
import os

def main():
    while True:
        os.system('cls')
        print("¡Bienvenido a Preguntados!\n")
        print("""Menú principal:

1. Ingresar usuario
2. Registrar usuario
3. Configuración y ajustes de accesibilidad
4. Salir
""")

        ingreso_usuario = manejar_menu("1234")

        match ingreso_usuario:
            case 1:
                os.system("cls")
                archivo = parser_json()
                lista_usuarios = archivo['jugadores']
                usuario_ingresado, password_ingresado = loguear_usuario(lista_usuarios)
                ingreso_a_menu_principal(usuario_ingresado, password_ingresado)
            case 2:
                os.system("cls")
                registrar_usuario()
            case 3:
                pass
            case 4:
                os.system("cls")
                print("¡Gracias por jugar preguntados! \nSaliendo...")
                time.delay(3)
                break
            case x:
                print("ERROR")


if __name__ == "__main__":
    main()