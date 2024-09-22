import sys
import os
from openai import OpenAI


def make_filename_for_text(input_text):
    # Initialiser OpenAI-klienten
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    # Kall OpenAI API for å oppsummere teksten
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": 'Du forteller hvilken informasjon som finnes i teksten, men ikke hva informasjonen er. Unngå ikke-essensielle ord som "informasjon", "hva", "når" og "husk". Resultatet ditt skal brukes i filnavn, så prøv og begrens lengden til 20 tegn og IKKE tegn som komma og punktum. Eksempel 1: "Husk av Eva sin bursdag er 13. april." => "Eva sin fødselsdag". Eksempel 2: "Johann sin favorittfarge re grønn." => "Johann sin favorittfarge".',
            },
            {
                "role": "user",
                "content": f"Oppsummer følgende tekst for bruk i filnavnet til filen som inneholder teksten: {input_text}",
            },
        ],
        max_tokens=150,
        temperature=0.0,
        stop=["\n"],
    )

    result = response.choices[0].message.content
    if result is not None:
        return result.rstrip(".")

    return ""


if __name__ == "__main__":
    make_filename_for_text(sys.stdin.read().strip())
