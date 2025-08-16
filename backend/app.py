from flask import Flask, render_template, request, jsonify
import subprocess, sys

app = Flask(__name__)  # looks for templates/ and static/ next to this file

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/run", methods=["POST"])
def run_code():
    data = request.get_json(force=True)
    code = (data.get("code") or "")
    language = (data.get("language") or "python").lower()

    try:
        if language == "python":
            # use the same interpreter running Flask (works reliably on Windows)
            result = subprocess.run(
                [sys.executable, "-c", code],
                capture_output=True, text=True, timeout=5
            )
        elif language == "javascript":
            # requires Node.js installed and on PATH
            result = subprocess.run(
                ["node", "-e", code],
                capture_output=True, text=True, timeout=5
            )
        else:
            return jsonify({"output": "❌ Unsupported language"}), 400

        output = (result.stdout or "") + (result.stderr or "")
        return jsonify({"output": (output.strip() or "(no output)")})
    except subprocess.TimeoutExpired:
        return jsonify({"output": "⏳ Execution timed out (5s)"})
    except FileNotFoundError as e:
        # e.g. node not installed
        return jsonify({"output": f"⚠️ Runtime missing: {e}"})
    except Exception as e:
        return jsonify({"output": f"⚠️ Error: {e}"})

if __name__ == "__main__":
    app.run(debug=True)
