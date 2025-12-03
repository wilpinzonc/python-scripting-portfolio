#creamos un numero complejo


num_complejo=complex(float(input("Introduce la parte real del numero complejo:")),
                      float (input ("Introduce la parte imaginaria del numero complejo:")))

print("El numero complejo es: ", num_complejo)
#mostramos la parte real e imaginaria del numero complejo

num_complejo2= complex(float(input("Introduce la parte real del numero complejo:")),
                      float (input ("Introduce la parte imaginaria del numero complejo:")))        

print("La parte real del numero complejo es:" ,num_complejo2)

print("La suma de los numeros completjos es :", num_complejo + num_complejo2)