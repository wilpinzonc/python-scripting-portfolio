print("--- BIENVENIDO A LA CALCULADORA ---")

while True:
    # 1. Mostramos el menú DENTRO del bucle para que se repita siempre
    print("\nSelecciona una opción:")
    print("1. Suma")
    print("2. Resta")
    print("3. Multiplicación")
    print("4. Salir")
    
    # 2. Pedimos la opción UNA sola vez
    try:
        opcion = int(input("Introduce el número de tu opción: "))
    except ValueError:
        print("Error: Debes introducir un número.")
        continue # Vuelve al inicio del while

    # 3. Evaluamos la opción
    if opcion == 4:
        print("¡Hasta luego! Saliendo del programa...")
        break  # <--- ESTO ROMPE EL BUCLE Y TERMINA EL PROGRAMA

    # Verificamos si es una opción válida antes de pedir los números
    if opcion >= 1 and opcion <= 3:
        # Pedimos los números aquí para no repetir código en cada if
        a = int(input("Selecciona el primer número: "))
        b = int(input("Selecciona el segundo número: "))

        if opcion == 1:
            print(f"--> El resultado de la SUMA es: {a + b}")
        
        elif opcion == 2:
            print(f"--> El resultado de la RESTA es: {a - b}")
            
        elif opcion == 3:
            print(f"--> El resultado de la MULTIPLICACIÓN es: {a * b}")
    
    else:
        # Si puso 5, 8, -1, etc.
        print("Opción incorrecta. Por favor elige entre 1 y 4.")