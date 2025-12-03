#pedir 4 numeros y devovler el mayor

valor1=int(input("Teclea el primer valor:"))
valor2=int(input("Teclea el segundo valor:"))
valor3=int(input("Teclea el tercer valor:"))
valor4=int(input("Teclea el cuarto valor:"))

if valor1 > valor2 and valor1 > valor3 and valor1 > valor4:
    print("El valor mayor es:", valor1)
elif valor2 > valor1 and valor2 > valor3 and valor2 > valor4:
    print("El valor mayor es:", valor2)
elif valor3 > valor1 and valor3 > valor2 and valor3 > valor4:
    print("El valor mayor es:", valor3)
elif valor4 > valor1 and valor4 > valor2 and valor4 > valor3:
    print("El valor mayor es:", valor4)

else:
    print("Hay valores iguales")

