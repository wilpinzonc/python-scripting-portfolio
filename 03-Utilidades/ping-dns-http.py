import socket
import json
import struct

PT_HOST = '127.0.0.1'
PT_PORT = 39000

def pt_cli(dispositivo, comando):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(4)
            s.connect((PT_HOST, PT_PORT))
            payload = {"type": "cli_command", "device": dispositivo, "command": comando}
            msg = json.dumps(payload).encode('utf-8')
            s.sendall(struct.pack('!I', len(msg)) + msg)
            res_len = struct.unpack('!I', s.recv(4))[0]
            return json.loads(s.recv(res_len).decode('utf-8')).get("output", "")
    except: return ""

def auditar_red_completa():
    # CONFIGURACIÓN DE TU TOPOLOGÍA
    ORIGEN = "PC0"
    SRV_PLANETA = "192.168.10.2"
    DOM_PLANETA = "www.planeta.es"
    IPV6_PLANETA = "2000:A:A:A::10" # Ajusta según tu etiqueta
    ROUTER = "Router0"

    print(f"--- INICIANDO AUDITORÍA ASIR EN {ORIGEN} ---")
    
    # 1. Prueba IPv4
    p4 = pt_cli(ORIGEN, f"ping {SRV_PLANETA}")
    print(f"IPv4 Connectivity: {'✅' if 'Reply' in p4 else '❌'}")

    # 2. Prueba IPv6
    p6 = pt_cli(ORIGEN, f"ping {IPV6_PLANETA}")
    print(f"IPv6 Connectivity: {'✅' if 'Reply' in p6 or 'Success' in p6 else '❌'}")

    # 3. Prueba DNS
    dns = pt_cli(ORIGEN, f"nslookup {DOM_PLANETA}")
    print(f"Servicio DNS:      {'✅' if 'Address' in dns else '❌'}")

    # 4. Prueba HTTP (Puerto 80)
    web = pt_cli(ORIGEN, f"telnet {SRV_PLANETA} 80")
    print(f"Servicio Web:     {'✅' if 'Connected' in web or 'Open' in web else '❌'}")

    # 5. Estado del Túnel en el Router
    tunnel = pt_cli(ROUTER, "show interfaces tunnel 0")
    print(f"Estado Túnel:     {'✅ UP' if 'up, line protocol is up' in tunnel.lower() else '❌ DOWN'}")

    print("\n--- AUDITORÍA FINALIZADA ---")

if __name__ == "__main__":
    auditar_red_completa()