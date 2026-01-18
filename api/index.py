import tempfile
from flask import Flask, render_template, request
from serpapi import GoogleSearch

app = Flask(__name__, template_folder="../templates")

API_KEY = "68271b35ee6940978e0f3b068c09ae9dda0f49d3c5df538ad1efa78d031ca54c"

@app.route("/", methods=["GET", "POST"])
def index():
    results = []

    if request.method == "POST":
        image = request.files.get("image")
        if image:
            with tempfile.NamedTemporaryFile(delete=True) as temp:
                image.save(temp.name)

                params = {
                    "engine": "google_lens",
                    "api_key": API_KEY,
                    "source": "upload",
                    "file": open(temp.name, "rb")
                }

                search = GoogleSearch(params)
                data = search.get_dict()

                for item in data.get("visual_matches", []):
                    results.append({
                        "title": item.get("title"),
                        "source": item.get("source"),
                        "link": item.get("link")
                    })

    return render_template("index.html", results=results)

# WAJIB untuk Vercel
def handler(request, context):
    return app(request.environ, lambda status, headers: None)
