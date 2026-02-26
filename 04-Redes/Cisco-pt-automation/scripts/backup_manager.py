import os
import logging
from datetime import datetime
from netmiko import ConnectHandler

# Configuración de Logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_backup():
    # En un entorno real, usarías variables de entorno (os.getenv)
    device = {
        "device_type": "cisco_ios",
        "host": "192.168.100.2",
        "username": "wil",
        "password": "your_password",
        "secret": "your_enable_password",
    }

    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    backup_path = "backups/"
    
    if not os.path.exists(backup_path):
        os.makedirs(backup_path)

    try:
        logging.info(f"Iniciando conexión con {device['host']}...")
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            hostname = ssh.find_prompt()[:-1] # Limpia el prompt para obtener el nombre
            config = ssh.send_command("show running-config")
            
            filename = f"{backup_path}{hostname}_{date_str}.cfg"
            with open(filename, "w") as f:
                f.write(config)
            
            logging.info(f"Backup completado con éxito: {filename}")
            
    except Exception as e:
        logging.error(f"Fallo en la automatización: {e}")

if __name__ == "__main__":
    run_backup()