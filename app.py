from flask import Flask, request, render_template
import subprocess
import re

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("chat.html")


@app.route("/get", methods=["POST"])
def chat():
    user_message = request.form["msg"]
    try:
        result = subprocess.run(
            ["ollama", "run", "llama3.2:1b", user_message],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
        )

        # Decode output, replacing invalid characters with placeholders
        response_message = (
            result.stdout.decode("utf-8", errors="replace").strip()
            if result.stdout
            else "No response from model."
        )
    except subprocess.CalledProcessError as e:
        # Handle errors similarly, making sure to decode stderr properly
        response_message = f"Error communicating with the model: {e.stderr.decode('utf-8', errors='replace').strip() if e.stderr else 'Unknown error.'}"

    # Strip out unwanted console messages
    response_message = re.sub(
        r"failed to get console mode for stdout:.*|failed to get console mode for stderr:.*",
        "",
        response_message,
    ).strip()

    return response_message


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
