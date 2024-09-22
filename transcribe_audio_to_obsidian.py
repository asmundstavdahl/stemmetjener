import os
import sys
from openai import OpenAI
from openai.types.audio.transcription import Transcription

# Konfigurasjonsinnstillinger
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OBSIDIAN_VAULT_PATH = "/home/stavdahl/Åsmunds Obsidian-velv/Åsmunds Obsidian-velv"

client = OpenAI(api_key=OPENAI_API_KEY)
from datetime import datetime

# Sett OpenAI API-nøkkelen


def transcribe_audio(file_path):
    # Åpne lydfilen
    with open(file_path, "rb") as audio_file:
        # Kall Whisper API for å transkribere lydfilen
        response = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-1",
            response_format="text",
        )

    return response


def save_transcription_to_obsidian(transcription, note_title):
    # Beregn filbane til Obsidian-vault
    note_path = os.path.join(OBSIDIAN_VAULT_PATH, f"{note_title}.md")

    # Lag metadata for notatet
    date = datetime.now().strftime("%Y-%m-%d")
    metadata = f'---\ntitle: "{note_title}"\ndate: {date}\ntags: #transcription #speech\n---\n\n'

    # Lag notatet i Markdown-format
    note_content = f"{metadata}Her er innholdet fra lydklippet:\n{transcription}"

    # Skriv notatet til fil
    with open(note_path, "w") as file:
        file.write(note_content)


def main(file_path):
    # Sjekk om filen eksisterer
    if not os.path.isfile(file_path):
        print("Feil: Filen eksisterer ikke.")
        return

    # Transkribere lydfilen
    transcription = transcribe_audio(file_path)

    # Lag et tittel for notatet (f.eks. basert på filnavnet)
    note_title = os.path.splitext(os.path.basename(file_path))[0]

    # Lagre transkripsjonen i Obsidian Vault
    save_transcription_to_obsidian(transcription, note_title)

    print(
        f"Transkripsjonen har blitt lagret i {OBSIDIAN_VAULT_PATH} som {note_title}.md"
    )


if __name__ == "__main__":
    main(sys.argv[1])
