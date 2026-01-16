#Librerías
import re

"""
Expresiones regulares en Python
Problemas Reales
"""
#Codigo
print("Librería cargada correctamente")
#Ejemplo 1
texto="Mi Número es 1118530476" 
resultado=re.search(r"\d+",texto)
print(f"{texto} Resultado: {resultado.group()}")
texto="Mi Número es 1118530-476" 
resultado=re.search(r"\d+",texto)
print(f"{texto} Resultado: {resultado.group()}") 
resultado=re.findall(r"\d+",texto)
print(f"{texto} Resultado: {resultado}")

documento = "cc.111.530.476" 

def clean_id(documento):
    re.sub(r"\D","",documento)
print(clean_id)
