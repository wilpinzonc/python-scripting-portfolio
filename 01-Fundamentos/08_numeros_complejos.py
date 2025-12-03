#Práctica II Python 
#1.Se pide por pantalla al usuario dos números complejos, y se debe mostrar lo siguiente por 
#pantalla: 
#• La suma de los dos números complejos 
#• La resta de los dos números complejos 
#• La multiplicación de los dos números complejos 
#• La división de los dos números complejos 

numcomp1=complex(
    float(input("Introduce la parte real del 1 complejo:")),
    float(input("Introduce la parte imaginaria del 1 complejo:"))
)
numcomp2= complex(
    float(input("Introduce la parte real del 2 complejo:")),
    float(input("Introduce la parte imaginaria del 2 complejo:"))
)   
suma= numcomp1 + numcomp2
resta= numcomp1 - numcomp2
multiplicacion= numcomp1 * numcomp2
division= numcomp1 / numcomp2

#suma de los dos num complejos
print("La suma de los numeros complejos es: ", suma)

#resta de los dos num complejos
print("La resta de los numeros complejos es: ", resta)

#multiplicacion de los dos num complejos
print("La multiplicacion de los numeros complejos es: ", multiplicacion)

#division de los dos num complejos
print("La division de los numeros complejos es: ", division)