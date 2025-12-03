print ("Hello world")
print ("Texto dentro de la funcion print")

#no es necesario especificar el tipo de dato para asignar variables, py lo hace implicitamente
edad = 31

numero1 = 5 #entero
numero2 = 3.2 #float
nombre = "Juan" #string
es_programador = True #booleano

print ("la varidable edad contiene:", edad)
print ("la variable numero1 contiene:" ,numero1) 
print ("la variable numero2:" ,numero2)
print ("la variable nombre contiene",nombre)
print ("La variable es programador contiene:" ,es_programador)

#probamos los paramtros de print
print(1, 2, 3, 4, 5, 6, 7, 8, 9, sep="      ", end="***\n")
print(1, 2, 3, 4, 5, 6, 7, 8, 9, sep="      ", end="***\t")

#\n salto de linea
#\t tabulador
#\\ barra invertida
#\" comillas dobles
#\' comillas simples
#r"" cadena raw (raw string) no interpreta caracteres especiales

print("primera linea:\"texto entre comillas\"\nSegunda linea:\'\x24\'")