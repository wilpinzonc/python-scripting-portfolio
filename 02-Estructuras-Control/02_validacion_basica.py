#se pide por pantalla un dato numerico entero y comprobamos si es par o impar


#ejercicio 1
num1=int(input("Introduce un numero entero:"))

#utilice la 
if num1 % 2 == 0:
    print("El numero es par")
else:
    print("El numero es impar")


#ejercicio 2
#se piden dos valores de tipo texto por pantalla, y se guardan en una tercera variable 
#y se imprimen con print todos los valores con comillas

#el string esta por defecto en python
val1=input("Introduce el primer valor:")
val2=input("Introduce el segundo valor:")
val3= val1 + val2

print("El primer valor es:\"", val1 ,"\" El segundo valor es:\"", val2, "\" La suma de los dos valores es:\"", val3, "\"")


#ejercicio 3
#se pide una nota, si es >5 aprueba, si no, suspenso

notaPhyton= int(input("Introduce la nota de python:"))
if notaPhyton >= 5:
    print("Has aprobado")
else:
    print("Has suspendido")