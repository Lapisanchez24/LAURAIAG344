# Programa principal
if __name__ == "__main__":
    training_data =[
    ("hola", "¡Hola! ¿En qué podemos ayudarte hoy?"),
    ("buenos días", "Buenos días, gracias por contactarnos. ¿Cómo podemos asistirte?"),
    ("buenas tardes", "Buenas tardes, es un gusto atenderte. ¿Qué consulta tienes?"),
    ("buenas noches", "Buenas noches, estamos a tu disposición. ¿En qué podemos ayudarte?"),
    ("información", "Con gusto te brindamos la información que necesitas. ¿Sobre qué tema?"),
    ("soporte", "Nuestro equipo de soporte está listo para ayudarte. Cuéntanos tu inconveniente."),
    ("precio", "Con gusto te compartimos nuestros precios. ¿Qué servicio te interesa?"),
    ("gracias", "Gracias a ti por comunicarte con nosotros. ¡Que tengas un excelente día!")

    ]
    #Entrenar el modelo con la lista
    model,vectorizer,unique_answers=build_and_train_model(training_data)
    #Mostrar un mensaje inicial al usuario
    print("Chatbot supervisado listo,Escribe Salir para terminar.\n")
    while True:
        #Pedimos una frase al usuario
        user =input("Tú: ").strip()
        if user.lower() in {"salir","exit","quit"}:
            print("Bot: !Hasta pronto¡")
            break
        response=predict_answer(model,vectorizer,unique_answers,user)
        print("Bot: ",response)