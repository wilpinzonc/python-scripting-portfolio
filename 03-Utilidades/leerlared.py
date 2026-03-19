import socket
import json
import struct
import time

# Configuración IPC según tu imagen
PT_HOST = '127.0.0.1'
PT_PORT = 39000

def comunicacion_pt_debug(payload):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(5)
            s.connect((PT_HOST, PT_PORT))
            
            # Formatear mensaje: Longitud (4 bytes) + JSON + Byte nulo (vital en algunas versiones)
            mensaje_json = json.dumps(payload)
            mensaje_bytes = mensaje_json.encode('utf-8') + b'\0'
            header = struct.pack('!I', len(mensaje_bytes))
            
            s.sendall(header + mensaje_bytes)
            time.sleep(0.5) # Pequeña pausa para que PT procese
            
            res_header = s.recv(4)
            if not res_header:
                return {"error": "Packet Tracer cerró la conexión. Intenta reiniciar el IPC en PT."}
            
            res_len = struct.unpack('!I', res_header)[0]
            res_data = s.recv(res_len)
            return json.loads(res_data.decode('utf-8').strip('\0'))
    except Exception as e:
        return {"error": str(e)}

def auditoria_asir():
    print("--- ESCANEANDO TOPOLOGÍA ---")
    data = comunicacion_pt_debug({"type": "get_device_list"})
    
    if "error" in data:
        print(f"❌ Error: {data['error']}")
        return

    for dev in data.get("devices", []):
        nombre = dev["name"]
        print(f"Dispositivo encontrado: {nombre} ({dev['type']})")
        # Aquí puedes añadir pings automáticos entre ellos
    
    if not data.get("devices"):
        print("⚠️ Conexión establecida, pero la topología parece vacía.")

if __name__ == "__main__":
    auditoria_asir()