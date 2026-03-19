import socket

def test_conexion():
    host = '127.0.0.1' # Tu propia PC
    port = 39000       # El puerto que aparece en tu imagen

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        print("¡Conexión exitosa! Python puede ver a Packet Tracer.")
        s.close()
    except Exception as e:
        print(f"Error al conectar: {e}")

test_conexion()