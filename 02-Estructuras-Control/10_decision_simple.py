##solicitar al ususario, edad,altura en cm
#determinar que tipo de atracciones puede acceder
#us debe teclear edad , guardar como entero, altura en cm como entero


edad= int(input("Ingrese su edad en años: "))
altura= int(input("Ingrese su altura en cm: "))

if altura < 140: 
    if edad < 12:
        print("Puede acceder a las atracciones infantiles.")
    elif edad >= 12:
        print("no puede acceder a ninguna atraccion debido a la restriccion de altura")
elif altura >= 140 and altura < 170:
    if edad < 12:
        print("Puede acceder a las atracciones familaires")
    elif edad >= 12:
        print("Puede acceder a las atracciones familiares y a las montanas rusas de intensidad media")
elif altura >= 170:
    if edad < 12:
        print("Puede acceder a las atracciones familiares y a las montanas rusas de intensidad media")
    elif edad >= 12:
        print("Puede acceder a todas las atracciones del parque incluidas las de alta intensidad")
else:
    print("Datos invalidos, por favor ingrese valores correctos de edad y altura.")