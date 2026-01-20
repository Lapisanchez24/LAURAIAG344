# controller.py
# Coordina la interfaz, la IA y la lógica de Excel

from ia_interpreter import interpretar_texto
from proccessor import ejecutar_accion


def procesar_instruccion(texto, ruta_excel):
    try:
        instruccion = interpretar_texto(texto)
        ejecutar_accion(instruccion, ruta_excel)
        return True, "Instrucción ejecutada correctamente"
    except Exception as e:
        return False, str(e)
