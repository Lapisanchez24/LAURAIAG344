from groq import Groq

# API Key directamente en el código
API_KEY = "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"

# Crear cliente
client = Groq(api_key=API_KEY)

# Solicitud al modelo
chat_completion = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": (
                "Eres un experto en Microsoft Excel y análisis de datos. "
                "Tu tarea es interpretar instrucciones en lenguaje natural "
                "y extraer la instrucción del usuario.\n\n"
                "Debes identificar:\n"
                "- la acción principal (sumar, filtrar, ordenar, agrupar, etc.)\n"
                "- las columnas involucradas\n"
                "- las condiciones si existen\n\n"
                "Devuelve SIEMPRE la respuesta en formato JSON con esta estructura:\n"
                "{\n"
                '  "accion": "",\n'
                '  "columnas": [],\n'
                '  "condiciones": [],\n'
                '  "resultado": ""\n'
                "}"
            )
        },
        {
            "role": "user",
            "content": "Quiero sumar las ventas por vendedor solo del año 2024"
        }
    ]
)

# Mostrar la respuesta
print(chat_completion.choices[0].message.content)
