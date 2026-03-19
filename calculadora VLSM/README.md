
```markdown
# Network Asset Discovery Tool

Este proyecto es una herramienta de automatización de red profesional desarrollada en **Python** utilizando la librería **Scapy**. Está diseñada para realizar escaneos de red rápidos y eficientes mediante el protocolo **ARP**, permitiendo identificar dispositivos activos en una red local (LAN) y obtener sus direcciones MAC.

## Características
* **Escaneo de Capa 2:** Utiliza peticiones ARP en lugar de simples pings (ICMP), lo que lo hace más rápido y difícil de bloquear por firewalls locales.
* **Identificación Precisa:** Mapeo automático de direcciones IP a direcciones MAC.
* **Orientado a ASIR:** Herramienta base para auditorías de red y administración de sistemas.

## Requisitos Técnicos
* **Python 3.10+**
* **Scapy:** Librería para manipulación de paquetes de red.
* **Privilegios de Administrador:** Necesarios para enviar paquetes de red crudos (Raw Packets).

## 🔧 Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/wilpinzonc/python-scripting-portfolio.git](https://github.com/wilpinzonc/python-scripting-portfolio.git)
   cd 04-Redes

```

2. **Configurar el entorno virtual:**
```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install scapy

```


3. **Ejecutar el script:**
```powershell
python network_discovery.py

```



## 📊 Habilidades Demostradas

* **Networking:** Dominio de protocolos de red (ARP, Ethernet, TCP/IP).
* **Automatización:** Uso de Python para sustituir herramientas manuales de administración.
* **Ciberseguridad:** Implementación de técnicas de reconocimiento de red.

---

*Desarrollado como parte de mi formación en Administración de Sistemas Informáticos en Red (ASIR).*

```