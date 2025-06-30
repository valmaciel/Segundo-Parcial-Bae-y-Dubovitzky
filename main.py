import random
from especificas import *
from input import *

# def hacer_pregunta(pregunta):
#     print(f"\n📚 Categoría: {pregunta['categoria']}")
#     print(pregunta['pregunta'])
#     for i, opcion in enumerate(pregunta['opciones']):
#         print(f"{chr(97 + i)}) {opcion}")
#     while True:
#         respuesta = input("Tu respuesta (a, b, c, d): ").lower()
#         if respuesta in ['a', 'b', 'c', 'd']:
#             return respuesta == pregunta['respuesta']
#         else:
#             print("")


def main():
    preguntas_por_categoria = {
        "Historia": [
            {"pregunta": "¿Quién fue el primer presidente de Argentina?", "opciones": ["Rivadavia", "San Martín", "Belgrano", "Sarmiento"], "respuesta": "a", "categoria": "Historia"},
        ],
        "Ciencia": [
            {"pregunta": "¿Cuál es la fórmula del agua?", "opciones": ["H2O", "CO2", "NaCl", "O2"], "respuesta": "a", "categoria": "Ciencia"},
        ],
        "Geografía": [
            {"pregunta": "¿Cuál es la capital de Japón?", "opciones": ["Kioto", "Osaka", "Tokio", "Hiroshima"], "respuesta": "c", "categoria": "Geografía"},
        ],
        "Arte": [
            {"pregunta": "¿Quién pintó la Mona Lisa?", "opciones": ["Picasso", "Van Gogh", "Da Vinci", "Dalí"], "respuesta": "c", "categoria": "Arte"},
        ],
        "Deportes": [
            {"pregunta": "¿En qué deporte se usa una raqueta?", "opciones": ["Fútbol", "Tenis", "Boxeo", "Hockey"], "respuesta": "b", "categoria": "Deportes"},
        ],
        "Entretenimiento": [
            {"pregunta": "¿Quién protagoniza 'Iron Man'?", "opciones": ["Chris Evans", "Robert Downey Jr.", "Mark Ruffalo", "Tom Holland"], "respuesta": "b", "categoria": "Entretenimiento"},
        ]
    }

    categorias = ['Deportes', 'Geografía', 'Ciencia', 'Arte', 'Entretenimiento', 'Historia', 'Corona']

    puntos_jugador1 = 0

    # # Mezclamos las preguntas
    # for categoria in preguntas_por_categoria:
    #     random.shuffle(preguntas_por_categoria[categoria])

    # jugadores = input("👥 Ingresá los nombres separados por coma: ").split(",")
    # jugadores = [j.strip() for j in jugadores if j.strip()]
    # progreso = {j: set() for j in jugadores}

    # terminado = False
    # while not terminado:
    #     for jugador in jugadores:
    #         if jugar_turno(jugador, preguntas_por_categoria, progreso):
    #             terminado = True
    #             break
    jugar_turno('Denis', categorias, preguntas_por_categoria, puntos_jugador1)

    print("\n🎉 Fin del juego. Gracias por jugar Preguntados!")

if __name__ == "__main__":
    main()
