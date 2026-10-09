from flask import Flask, render_template, request
from google import genai

app = Flask(__name__)

client = genai.Client()


@app.route("/", methods=["GET", "POST"])
def home():
    translation = ""
    error = ""

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        target_language = request.form.get("target_language", "Telugu")

        if not text:
            error = "Please enter some text."

        else:
            try:
                prompt = f"""
Translate the following text into {target_language}.

Rules:
- Return only the translated text.
- Do not explain anything.
- Preserve the original meaning.
- Preserve names, numbers and punctuation.
- Do not add extra information.
- Translate the complete text, including sentences.

Text:
{text}
"""

                response = client.models.generate_content(
                    model="gemini-3.5-flash-lite",
                    contents=prompt
                )

                translation = response.text.strip()

            except Exception as e:
                error = f"Translation error: {e}"

    return render_template(
        "index.html",
        translation=translation,
        error=error
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)