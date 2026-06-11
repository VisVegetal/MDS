import sys
from openai import OpenAI

# Inițializăm clientul API.
# - Dacă folosești Ollama local, păstrează `base_url` așa cum e mai jos.
# - Dacă folosești OpenAI oficial, elimină `base_url` și setează `api_key` la cheia ta reală.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Pentru Ollama local nu contează textul exact al cheii
)


def chat_interactiv():
    # Interfață simplă de chat în terminal.
    print("====================================================")
    print(" Mini-Ollama personalizat în Python ")
    print(" Scrie 'exit' sau 'quit' ca să închizi chat-ul. ")
    print("====================================================\n")

    # Istoricul conversației — păstrăm contextul între mesaje.
    # Fiecare element din listă este un dict cu `role` și `content`.
    history = [
        {"role": "system", "content": "Ești un asistent util, politicos și glumeț."}
    ]

    while True:
        try:
            # Citim ce scrie utilizatorul
            user_input = input(">>> ")

            # Ieșire curată la comanda user-ului
            if user_input.strip().lower() in ['exit', 'quit']:
                print("La revedere!")
                break

            # Dacă utilizatorul a apăsat Enter fără text, ignorăm
            if not user_input.strip():
                continue

            # 1) Adăugăm mesajul utilizatorului în istoric
            #    Așa modelul vede toată conversația, nu doar ultimul mesaj.
            history.append({"role": "user", "content": user_input})

            # 2) Trimitem întreg istoricul către model.
            #    Schimbă `model` cu numele modelului tău local (ex: 'llama3').
            response = client.chat.completions.create(
                model="llama3",
                messages=history,
            )

            # 3) Extragem textul răspunsului din structura returnată
            #    (majoritatea SDK-urilor pun textul în choices[0].message.content)
            ai_response = response.choices[0].message.content

            # 4) Afișăm răspunsul la ecran pentru utilizator
            print(ai_response)
            print()

            # 5) Salvăm răspunsul AI în istoric, ca să păstrăm contextul
            history.append({"role": "assistant", "content": ai_response})

        except KeyboardInterrupt:
            # Încheiere frumoasă la Ctrl+C
            print("\nLa revedere!")
            break
        except Exception as e:
            # Mesaj prietenos de eroare și sugestie de verificare
            print(f"\nA apărut o eroare: {e}")
            print("Verifică că serverul Ollama e pornit (într-un terminal rulează: ollama serve)\n")
            break


if __name__ == "__main__":
    chat_interactiv()
