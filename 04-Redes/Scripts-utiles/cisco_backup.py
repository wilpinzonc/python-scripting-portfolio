from netmiko import ConnectHandler
from datetime import datetime
import getpass
import os

def backup_config(device_params):
    # Generar nombre de archivo con fecha: config_R1_20260226.txt
    hostname = device_params['host']
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"backup_{hostname}_{date_str}.txt"
    
    # Asegurar que existe carpeta de backups
    if not os.path.exists('backups'):
        os.makedirs('backups')

    try:
        print(f"[*] Conectando a {hostname}...")
        with ConnectHandler(**device_params) as net_connect:
            net_connect.enable()
            # Comando clave de CCNA
            config_data = net_connect.send_command("show running-config")
            
            with open(f"backups/{filename}", "w") as f:
                f.write(config_data)
            
            print(f"[+] Backup guardado en: backups/{filename}")
            
    except Exception as e:
        print(f"[!] Error en {hostname}: {e}")

if __name__ == "__main__":
    # Datos de tu laboratorio (Packet Tracer o GNS3)
    cisco_device = {
        'device_type': 'cisco_ios',
        'host': '192.168.1.1',  # Cambia por la IP de tu router
        'username': 'admin',
        'password': 'Password123',
        'secret': 'class',      # Contraseña de enable
    }
    
    backup_config(cisco_device)