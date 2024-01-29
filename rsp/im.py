import subprocess

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    # Generate the slideshow video
    generate_slideshow()

    # Render the HTML template
    return render_template("index.html")


def generate_slideshow():
    image_folder = "images"
    output_video = "static/slideshow.mp4"

    common_width = 1200
    common_height = 1600

    # Use ffmpeg to create a slideshow video
    subprocess.run(
        [
            "ffmpeg",
            "-framerate",
            "1/6",
            "-pattern_type",
            "glob",
            "-i",
            f"{image_folder}/*.jpeg",  # Change the extension if your images have a different format
            "-vf",
            f"scale={common_width}:{common_height}",  # Resize images to a common size
            "-c:v",
            "libx264",
            "-r",
            "30",
            "-pix_fmt",
            "yuv420p",
            "-y",
            output_video,
        ]
    )


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5500)
