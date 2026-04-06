from flask import Flask, request, render_template
import enchant

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""
    result = None
    language = request.form.get("language", "en") if request.method == "POST" else "en"
    
    # Map language codes to enchant language codes
    lang_map = {"en": "en_US", "sv": "sv_SE"}
    enchant_lang = lang_map.get(language, "en_US")
    
    # Initialize spell checker with selected language
    try:
        checker = enchant.Dict(enchant_lang)
    except enchant.DictNotFoundError:
        checker = enchant.Dict("en_US")
        language = "en"

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            words = text.split()
            result = {}
            for word in sorted(set(words)):
                # Check if word is misspelled
                if not checker.check(word):
                    suggestions = checker.suggest(word)[:5]
                    result[word] = suggestions
            

    return render_template('index.html', text=text, result=result, language=language)

if __name__ == "__main__":
    app.run(debug=True)