import streamlit as st
import time as t
import requests
from prompts import dev_prompt_agent


# Initialise l'historique de chat dans la session Streamlit si non existant
if "history" not in st.session_state:
    st.session_state.history = []


def update_chat() -> None:
    """
    Affiche les messages de l'historique dans l'interface Streamlit.
    Chaque message est affiché dans une "bubble" style chat.
    """
    with st.container():
        for message in st.session_state.history:
            with st.chat_message(message["role"]):
                st.write(message["content"])


def http_request(data_: list[dict[str, str]]) -> dict[str, str]:
    """
    Envoie une requête HTTP POST au backend local pour obtenir une réponse du chatbot.

    Args:
        data_ (list[dict[str, str]]): L'historique complet des messages, incluant le prompt dev initial.

    Returns:
        dict[str, str]: La réponse JSON du backend sous forme de dictionnaire, ou une erreur.
    """

    url = "http://127.0.0.1:8000/chat"
    try:
        response = requests.post(url, json=data_)
        response.raise_for_status()  # Lève une erreur si la requête échoue
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def streamlit_content() -> None:
    """
    Gère l'interaction principale avec l'utilisateur via Streamlit :
    - Récupère l'input utilisateur
    - Met à jour l'historique
    - Appelle l'api'
    - Affiche la réponse
    """

    dev_data = [{"role": "developer", "content": dev_prompt_agent}]
    prompt: str | None = st.chat_input("Say something")
    
    if prompt:
        st.session_state.history.append({"role": "user", "content": prompt})
        full_prompt_history = dev_data + st.session_state.history
        response_agent = http_request(data_=full_prompt_history)
        if response_agent and "error" not in response_agent:
            st.session_state.history.append(response_agent)
            update_chat()


def main() -> None:
    """
    Fonction principale de l'app. Lance le contenu Streamlit.
    """
    streamlit_content()


if __name__ == "__main__":
    main()