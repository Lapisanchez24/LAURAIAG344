from chatbot.data import training_data
from chatbot.model import build_and_train_model, predict_answer,load_model
# Programa principal
def main():
    # Intentar cargar el modelo existente
    model, vectorizer, unique_answers = load_model()
    # Si no existe un modelo entrenado, entrenarlo
    if model is None:
        model, vectorizer, unique_answers = build_and_train_model(training_data)
    #Mostrar un mensaje inicial al usuario
    print("\n 🤖 Chatbot supervisado listo, Escribe 'Salir' para terminar.\n")
    while True:
        #Pedimos una frase al usuario
        user =input("Tú: ").strip()
        if user.lower() in {"salir","exit","quit"}:
            print("Bot: ¡Hasta pronto!")
            break
        response=predict_answer(model,vectorizer,unique_answers,user)
        print("Bot: ",response)
if __name__ == "__main__":
    main()