# Hybrid Network Automation: Cisco PT + Python

## Descripción
Este proyecto implementa un entorno de automatización híbrido conectando una instancia virtual de **Cisco Packet Tracer 9.0** con un entorno de ejecución **Python 3.10** externo. Utiliza un adaptador de bucle invertido (Loopback) para simular la gestión de red en un entorno real de Data Center.

## Stack Tecnológico
| Componente | Tecnología |
| :--- | :--- |
| Simulación | Cisco Packet Tracer 9.0 |
| Lenguaje | Python 3.10+ |
| Librería de Automatización | Netmiko (SSH) |
| Conectividad | Microsoft Loopback Adapter |

## Arquitectura de Red
- **Host OS:** Windows 10/11 con IP `192.168.100.1/24` (Loopback).
- **Guest Router (PT):** Cisco 2911 con IP `192.168.100.2/24` en G0/0.
- **Protocolo:** SSHv2 habilitado con privilegios de nivel 15.

## Scripts Incluidos
- `backup_manager.py`: Automatiza la extracción del `running-config` y lo versiona con timestamps.
- `bridge_test.py`: Valida la adyacencia SSH entre el host físico y el entorno virtual.