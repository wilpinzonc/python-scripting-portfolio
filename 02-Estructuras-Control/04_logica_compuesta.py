#usar el operador not, pedir num por pantalla, probar que es distinto de cero y mayor que cero
#si se cumple la condicion se calcula si el numero es par o impar
#si no se cumple la condicion, se muestra un mensaje de error

numero1= int(input("Ingrese el supermeganúmero: "))

if numero1 != 0 and not (numero1 < 0):
    print("El número es válido.")
    if numero1 % 2 == 0:
        print("El numero es par")
    else:
        print("El numero es impar")
else :
    print("Error: El número debe ser distinto de cero y mayor que cero.")



##parte dos del ejercicio
#se pide por pantalla un numero entero
#a. se comprueba que es positivo y distinto de cero
#i. si es de dos cifras se muestra si es par o impar
#ii. si es de tres cifras se muestra el resto de dividir este numero entre 2
#b. si no se cumple la condicion se muestra un mensaje de error

valor1= float(input("Ingrese un número entero: "))

if numero1 == int(numero1) and numero1 > 0:
    print("El número es válido.")
    if 10 <= numero1 < 100:
        if numero1 % 2 == 0:
            print("El número es de dos cifras y es par.")
        else:
            print("El número es de dos cifras y es impar.")
    elif 100 <= numero1 < 1000:
        resto = numero1 % 2
        print("El número es de tres cifras. El resto de dividirlo entre 2 es:", resto)
    else:
        print("El número no tiene dos o tres cifras.")
else:
    print ("El numero no es valido.")