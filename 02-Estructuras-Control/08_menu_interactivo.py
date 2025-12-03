"""
Ejercicios de bucles While y Menús Interactivos.
Author: Wilson Pinzon
"""

# ---------------------------------------------------------
# EJERCICIO 1: Contar del 1 al 100 (For vs While)
# ---------------------------------------------------------
print("--- EJERCICIO 1: CONTADORES ---")

# Versión Bucle FOR
print("Bucle For:")
for i in range(1, 101):
    print(i, end=" ") # end=" " imprime en horizontal para ahorrar espacio
print("\nFin del ejercicio 1 con for\n")

# Versión Bucle WHILE
print("Bucle While:")
i = 1
while i <= 100:
    print(i, end=" ")
    i += 1
print("\nFin del ejercicio 1 con while\n")


# ---------------------------------------------------------
# EJERCICIO 2: Acumulador de positivos
# ---------------------------------------------------------
# Solicita números positivos y los suma. Se detiene con un negativo.
print("--- EJERCICIO 2: ACUMULADOR ---")

suma = 0
# Inicializamos b para entrar al bucle
b = int(input("Dame un numero positivo para sumar (o negativo para salir): "))

while b >= 0:
    suma = suma + b
    print(f"Llevas acumulado: {suma}")
    b = int(input("Dame otro numero positivo (o negativo para salir): "))

print(f"Has salido. La suma total final es: {suma}\n")


# ---------------------------------------------------------
# EJERCICIO 3: Menú Interactivo (Calculadora)
# ---------------------------------------------------------
# El programa vuelve a mostrar el menú después de cada operación
print("--- EJERCICIO 3: MENU INTERACTIVO ---")

opcion = 0

# El bucle se repite MIENTRAS la opción NO sea 4 (Salir)
while opcion != 4:
    print("""
    Selecciona una opcion:
    1. Sumar
    2. Restar
    3. Multiplicar
    4. Salir
    """)
    
    try:
        opcion = int(input("Tu opción: "))
    except ValueError:
        print("Error: Por favor ingresa un número válido.")
        opcion = 0 # Reinicia el bucle

    if opcion == 1:
        a = int(input("Primer numero: "))
        b = int(input("Segundo numero: "))
        print(f" Resultado Suma: {a + b}")
        
    elif opcion == 2:
        a = int(input("Primer numero: "))
        b = int(input("Segundo numero: "))
        print(f" Resultado Resta: {a - b}")
        
    elif opcion == 3:
        a = int(input("Primer numero: "))
        b = int(input("Segundo numero: "))
        print(f" Resultado Multiplicación: {a * b}")
        
    elif opcion == 4:
        print(" ¡Hasta luego! Saliendo del programa...")
        
    else:
        print("Opción incorrecta, intenta de nuevo.")

print("Fin del programa")