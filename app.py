from scripts import julia_set
from flask import Flask, render_template, request, jsonify
import numpy as np
import matplotlib

matplotlib.use("Agg")  # modo no interactivo para servidores
import matplotlib.pyplot as plt
import io
import base64
import time

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/calc")
def calc():
    start_time = time.time()

    # obtener parámetros enviados por el JS desde la URL
    c_real = float(request.args.get("c_real", -0.62772))
    c_imag = float(request.args.get("c_imag", -0.42193))
    res = int(request.args.get("res", 500))
    iters = int(request.args.get("iters", 300))

    julia_data = julia_set.calculate_julia(res, res, iters, c_real, c_imag)

    # rendering
    fig, ax = plt.subplots(figsize=(6, 6), dpi=100)
    ax.imshow(julia_data, extent=[-1.8, 1.8, -1.8, 1.8], cmap="magma")
    plt.axis("off")
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    plt.close(fig)

    end_time = time.time()

    return jsonify(
        {
            "image": f"data:image/png;base64,{img_base64}",
            "time": f"{end_time - start_time:.4f}",
        }
    )


if __name__ == "__main__":
    app.run(debug=True)
