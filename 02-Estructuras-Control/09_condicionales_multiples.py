#ejercicio 1
#se pide por pantalla dos numeros
# print cual es el mayor

num1=float(input("Escribe tu primer numero: "))
num2=float(input("Escribe tu segundo numero: "))

if num1 > num2:
    print ("El numero mayor es: ", num1)
if num1 == num2:
    print ("Los numeros son iguales!")
if  num1 < num2:
    print ("El numero mayor es: ", num2)

print ("Fin del ejercicio 1")

#ejercicio 2
print ("Inicio ejercicio 2-1")
val1=float(input("Escribe tu primer numero: "))
val2=float(input("Escribe tu segundo numero: "))

if val1 > val2:
    print ("El numero mayor es: ", val1)
    val3= float(input("Dame otro numero para sumar al mayor"))
    print("la suma del mayor al valor 3 es  ", val1+val3)
if val1 == val2:
    print ("Los numeros son iguales!")
    val3= float(input("Dame otro numero para sumar al mayor"))
    print ("La suma del valor 3 es: ", val1+val3)
if  val1 < val2:
    print ("El numero mayor es: ", val2)
    val3= float(input("Dame otro numero para sumar al mayor"))
    print ("La suma de valor 3 y el mayor es: ", val2+val3)

print ("Final ejercicio 2-1")
#suma el mayor , en caso de iguales suma el primero, multiplicar para el menor
print ("Ejercicio 2-2")

if val1> val2:
    print ("el numero menor es:" , val2)
    val4=(int(input("Dame otro valor pa multiplicar con el menor: ")))
    print ("La multiplicacion x el menor es: ", val4 * val2)
    
if val1==val2:
    print ("Los numeros son iguales!:")
    val4= int(input("Dame otro numero para multiplicar: "))
    print ("El valor de la multiplicacion es:" , val1 * val4)

if val1<val2:  
    print ("El numero menor es:" ,val1)
    val4 = int(input("Dame un numero para multiplicar por el menor:"))
    print ("La multiplicacion por el menor es: ", val4 * val1)

print ("Fin del ejercicio!!")
