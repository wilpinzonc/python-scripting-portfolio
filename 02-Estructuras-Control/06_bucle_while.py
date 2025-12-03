#1.diseniar un codigo con dos bucles anidados, para imprimir por pantalla la tabla de multiplicar del 2.
#debe aparecer por pantalla: 2x1=2 2X2=4 etc hasta el 2x10=20

#necesitamos un bucle que realizara la multiplicacion del numero 2
#necesitamos otro bucle que realizara las veces que se multiplica el numero 2 del 1 al 10

print("Tabla de multiplicar del 2:")
for i in range (2,3):  # bucle para el 2
    for j in range(1, 11):  # bucle para multiplicar del 1 al 10
        resultado = i * j
        print(f"{i} x {j} = {resultado}")

print("Fin ejercicio 1")
print()
#2. Calcular los n, los primeros 10 numeros de la serie de fibonacci
#eso es sumando 0,1, y luego es la suma de los dos numeros anteriores
#necesito un bucle que haga el limitador de 10 num
#necesito un segundo bucle que sume los dos numeros anteriores para sacar el siguiente valor
print("Los primeros 10 números de la serie de Fibonacci son:")
for n in range(0,11): #bucle pa los primeros 10#
    a=0
    b=1
    for m in range(n):
        a, b = b, a + b #aqui declaro que a tomara el valor de b, y que b, tomcara el valor de a+b
    print(a)        

print("Fin ejercicio 2")
print()
#3#calcular el factorial del numero 15

##aqui necesitamos hacer 15*14*13*12*11*10*9*8*7*6*5*4*3*2*1
##un bucle que haga la multiplicacion desde el 15 hasta el 1

integral = 1
for k in range(1,16): #bucle para multiplicar del 1 al 15
    integral = integral * k
print("La integral de 15 es", integral)

print("Fin ejercicio 3")
print()
#4 pedir un numero entre 0 y 999, nos aparece un mensaje con el numero de digitos que tiene el numero
#si escriben 0 se acaba el programa

while True:
    numero = int(input("Ingrese un número entre 0 y 999: "))
    if numero == 0:
        print("Se acabo el juego.")
        break
    elif numero < 10 :
        print("El número tiene 1 dígito.")
    elif numero >9 and numero <100:
        print("El número tiene 2 dígitos.")
    elif numero >= 100 and numero <= 999:
        print("El número tiene 3 dígitos.")
    else:
        print("Numero invalido, pon algo entre 0 y 999.")


