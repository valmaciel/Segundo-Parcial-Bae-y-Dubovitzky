import time
import sys
import random

# def coin_flip_animation():
#     spinner = ['/', '—', '\\', '|']
#     total_spins = 30  # cantidad de pasos de animación
#     base_delay = 0.1  # velocidad inicial

#     print("Flipping the coin...   ", end='', flush=True)

#     for i in range(total_spins):
#         # Easing out: va aumentando el delay en cada giro
#         delay = base_delay + (i / total_spins) ** 2 * 0.1  # curva cuadrática
#         sys.stdout.write('\b' + spinner[i % len(spinner)])
#         sys.stdout.flush()
#         time.sleep(delay)

#     # Termina en posición "—" (plana)
#     sys.stdout.write('\b—')
#     sys.stdout.flush()
#     time.sleep(0.6)

#     # Resultado
#     result = random.choice(['Heads', 'Tails'])
#     print(f"\nThe result is: {result}!")

# coin_flip_animation()




def funcion(nombre_de_un_usuario):
    print(nombre_de_un_usuario)

funcion('juan')
funcion('peralta')

