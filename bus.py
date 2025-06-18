from flask import Flask, render_template, request
from PIL import Image
import io, base64, requests
from mimetypes import guess_type

app = Flask(__name__)
GEMINI_API_KEY = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    fruit_name = None

    if request.method == 'POST':
        image_file = request.files['image']

        if image_file:
            try:
                # Get MIME type dynamically
                mime_type = guess_type(image_file.filename)[0] or "image/jpeg"

                # Read and encode the image
                image_bytes = image_file.read()
                base64_image = base64.b64encode(image_bytes).decode('utf-8')

                # Prepare payload
                payload = {
                    "contents": [
                        {
                            "parts": [
                                {"text": "What fruit is this?"},
                                {
                                    "inlineData": {
                                        "mimeType": mime_type,
                                        "data": base64_image
                                    }
                                }
                            ]
                        }
                    ]
                }

                # Make the API call
                response = requests.post(
                    "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent",
                    params={"key": GEMINI_API_KEY},
                    json=payload
                )

                # Debug log
                print("Status Code:", response.status_code)
                print("Response JSON:", response.json())

                # Parse the response safely
                data = response.json()
                candidates = data.get('candidates', [])
                if candidates and 'content' in candidates[0]:
                    parts = candidates[0]['content'].get('parts', [])
                    if parts and 'text' in parts[0]:
                        fruit_name = parts[0]['text']
                    else:
                        fruit_name = "⚠️ No text in response parts"
                else:
                    fruit_name = "⚠️ No candidates/content in response"

            except Exception as e:
                fruit_name = f"⚠️ Error: {str(e)}"

    return render_template("index.html", fruit_name=fruit_name)

if __name__ == '__main__':
    app.run(debug=True)