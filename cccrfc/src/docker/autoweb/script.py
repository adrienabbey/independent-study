from flask import Flask, jsonify, send_from_directory
import os



app = Flask(__name__)
IMAGE_FOLDER = "static/images"  # Folder where images are stored

@app.route("/images")
def get_images():
    images = [f for f in os.listdir(IMAGE_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]
    images = images[:10]  # Get up to 10 images
    return jsonify(images)

@app.route("/static/images/<filename>")
def serve_image(filename):
    return send_from_directory(IMAGE_FOLDER, filename)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Dynamic Image Gallery</title>
        <script>
            function loadImages() {
                fetch('/images')
                    .then(response => response.json())
                    .then(images => {
                        let container = document.getElementById('gallery');
                        container.innerHTML = '';
                        images.forEach(img => {
                            let imgElement = document.createElement('img');
                            imgElement.src = '/static/images/' + img;
                            imgElement.style.width = '48%';
                            imgElement.style.margin = '5px';
                            container.appendChild(imgElement);
                        });
                    });
            }
            setInterval(loadImages, 5000); // Refresh every 5 seconds
            window.onload = loadImages;
        </script>
    </head>
    <body>
        <div id="gallery"></div>
    </body>
    </html>
    """


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
