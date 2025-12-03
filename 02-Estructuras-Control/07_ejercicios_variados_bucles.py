#1. programa que piad al usuario una palabra y la muestre en pantalla 40veces

palabra= input("Ingrese una palabra: ")

for dato in range (40):
    print(palabra)

print("Fin ejercicio 1")
#2. pedir por pantalla numeros, mientras que no se teclea el 100, y mostrar si el numero es par o impar
#normalemnete usaria el while pero como es un for usare esta funcion para crear el bucle, mas adelante
#uso una condicional para poner el break en caso de que se ponga el numero 100

for i in iter(int, 1):  # bucle infinito
    numero = int(input("Ingrese un número: "))

    if numero == 100:
        print("Ha ingresado 100, el programa finaliza.")
        break
    elif numero % 2 == 0:
        print("El número es par.")
    else:
        print("El número es impar.")
print("Fin ejercicio 2")

#3. disena un programa que pida al usuario un numero entero mayor que cero y muestre por pantalla la cuenta
#atras desde ese numero hasta cero separado por comas
#se puede escoger el inicio, el final y el paso en la clausula range (inicio, valor final, paso)
#en este caso puse el numero2 como inicio, el -1 como final porque el anterior es cero y el paso -1 para que se
#vaya restando

numero2= int(input("Ingrese un numero entero mayor al cero: "))

for numero2 in range (numero2, -1, -1):
        if numero2 > 0:
            print(numero2, end=", ")
        else:
            print(numero2)
print("Fin ejercicio 3")

#4. disena un programa que pida al user un num entero y muestre por pantalla un 
#triangulo rectangulo como el de mas abajo, de altura el numero introducido

numero3= int(input("Ingrese un numero para la altura de la piramide: "))

for i in range (1, numero3 + 1):
    print("*" * i)
print("Fin ejercicio 4")

#5. disena un programa que pida al usuario un numero entero y muestre por pantalla si es num primo o no
# Funcion que verifica si un numero es divisible por cualquier numero anterior a el.
# Si encuentra algun divisor (modulo 0), retorna False.

def es_primo(n):
    if n < 2:
        return False
    for i in range(2, n):
        if n % i == 0:
            return False
    return True

numero5 = int(input("Ingresa un número para ver si es primo: "))
if es_primo(numero5):
    print("El número es primo.")
else:
    print("el número no es primo.")

print("Fin ejercicio 5")
####################################################

#6, disena un programa que muestre eco de todo lo que el usuario escriba , hasta que se escriba "salir"

for i in iter(int, 1):  # bucle infinito
    palabra2 = input("Escribe algo (escribe 'salir' para terminar): ")
    if palabra2 == "salir":
        print("Ha escrito salir, hasta luego!.")
        break
    else:
        print(palabra2)

print("Fin ejercicio 6")