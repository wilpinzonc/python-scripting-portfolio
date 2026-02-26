import os
from datetime import datetime
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetmikoTimeoutException

# Configuración de dispositivos (Extensible a YAML/JSON)
devices = [
    {
        "device_type": "cisco_ios",
        "host": "192.168.1.1",
        "username": "admin",
        "password": "your_password",
        "secret": "your_enable_secret",
    }
]

def backup_config(device):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"backup_{device['host']}_{now}.txt"
    
    # Crear directorio de backups si no existe
    if not os.path.exists("backups"):
        os.makedirs("backups")

    try:
        print(f"[*] Conectando a {device['host']}...")
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            print(f"[+] Extrayendo running-config de {device['host']}...")
            config_data = net_connect.send_command("show running-config")
            
            with open(f"backups/{filename}", "w") as f:
                f.write(config_data)
            print(f"[OK] Backup guardado: backups/{filename}")

    except NetmikoAuthenticationException:
        print(f"[!] Error de autenticación en {device['host']}")
    except NetmikoTimeoutException:
        print(f"[!] Tiempo de espera agotado para {device['host']}")
    except Exception as e:
        print(f"[!] Error inesperado: {e}")

if __name__ == "__main__":
    for device in devices:
        backup_config(device)