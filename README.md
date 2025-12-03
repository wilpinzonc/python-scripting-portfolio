# 🐍 Python Scripting Portfolio

Este repositorio documenta mi progresión en **Python 3** orientada a la administración de sistemas y automatización.
Aquí demuestro el dominio de la sintaxis, estructuras de control de flujo y la creación de pequeñas herramientas de línea de comandos (CLI).

## 📂 Estructura del Proyecto

### 🔹 1. Fundamentos (`/01-Fundamentos`)
Manejo de tipos de datos básicos, entrada/salida y formateo de cadenas.
* **Conceptos:** `Strings`, `Integers`, `Input`, `Print formatting`.
* **Objetivo:** Entender la interacción básica con la consola del sistema.

### 🔹 2. Lógica y Control de Flujo (`/02-Estructuras-Control`)
El núcleo de la lógica de programación. Scripts que toman decisiones y procesan datos iterativamente.
* **Archivos Clave:**
    * `08_menu_interactivo.py`: Implementación de un menú de opciones persistente con validación de errores (`try-except`) y bucles `while`.
    * `07_ejercicios_variados_bucles.py`: Uso intensivo de `for` y `range` para iteraciones controladas.
* **Habilidades:** Bucles infinitos controlados, condicionales anidados (`if-elif-else`), validación de datos.

### 🔹 3. Utilidades y Herramientas (`/03-Utilidades`)
Scripts funcionales que realizan tareas completas.
* **Destacado:** `calculadora_aritmetica.py`
    * Herramienta que procesa operaciones matemáticas básicas recibiendo parámetros del usuario.

---

## 💻 Ejemplo de Código (Control de Flujo)
*Fragmento de la lógica del menú interactivo (`08_menu_interactivo.py`), demostrando manejo de errores y bucles:*

```python
# El bucle se mantiene vivo hasta que el usuario elige salir (opción 4)
while opcion != 4:
    try:
        opcion = int(input("Tu opción: "))
    except ValueError:
        print("Error: Por favor ingresa un número válido.")
        opcion = 0 # Reinicio seguro del ciclo

    if opcion == 1:
        # Lógica de suma...
    elif opcion == 4:
        print("👋 Saliendo del sistema...")
