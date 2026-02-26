La forma profesional de hacerlo es mediante un **Microsoft Loopback Adapter**. Esto crea una tarjeta de red virtual en tu Windows que sirve de "puente" físico entre tu Python (VS Code) y el entorno simulado de Packet Tracer.

### 1. Configuración en Windows (El Puente)

1. Pulsa `Win + R`, escribe `hdwwiz.exe` y pulsa Enter.
2. Selecciona **Instalar el hardware seleccionándolo manualmente de una lista**.
3. Elige **Adaptadores de red** -> **Microsoft** -> **Microsoft Loopback Adapter**.
4. Una vez instalado, ve a "Conexiones de red", busca el nuevo adaptador y asígnale una IP fija (ej: `192.168.100.1 / 24`).

### 2. Configuración en Packet Tracer

1. Arrastra una **Cloud-PT** al entorno.
2. Haz clic en la Cloud -> pestaña **Config** -> **Ethernet**.
3. En el desplegable "Network Adapter", selecciona tu **Microsoft Loopback Adapter**.
4. Conecta un cable directo (Copper Straight-Through) desde un **Router** (G0/0) a la Cloud (Ethernet).

### 3. Configuración del Router Cisco (CLI)

Copia y pega esto en la consola del router para permitir que tu script de Python entre por SSH:

```bash
en
conf t
hostname R1
ip domain-name asir.local

# Configurar IP en la interfaz conectada a la Cloud
int g0/0
 ip address 192.168.100.2 255.255.255.0
 no shut
exit

# Configurar SSH y Usuario
crypto key generate rsa  # Elige 1024
username wil privilege 15 secret cisco123
ip ssh version 2

# Habilitar líneas VTY
line vty 0 4
 login local
 transport input ssh
exit
enable secret cisco_enable

```

### 4. Test de Conectividad (Python)

Usa este script rápido para verificar que el puente funciona. Si responde el `prompt`, tienes vía libre para usar todos tus scripts de automatización.

```python
from netmiko import ConnectHandler

device = {
    "device_type": "cisco_ios",
    "host": "192.168.100.2",  # IP del Router en PT
    "username": "wil",
    "password": "cisco123",
    "secret": "cisco_enable",
}

try:
    with ConnectHandler(**device) as net_connect:
        net_connect.enable()
        output = net_connect.find_prompt()
        print(f"Conexión exitosa. Prompt del router: {output}")
except Exception as e:
    print(f"Error de conexión: {e}")

```

**¿Prefieres que probemos esto primero o quieres que te explique cómo usar el "Network Controller" de PT 9 que funciona por API REST?** (Esto último es muy valorado en Cloud Engineering).