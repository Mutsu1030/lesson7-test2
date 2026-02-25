import os
import io
import base64
from flask import Flask, request, render_template
import qrcode
from qrcode.constants import ERROR_CORRECT_L

app = Flask(__name__)
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"


@app.route("/", methods=["GET", "POST"])
def index():
    qr_data = None
    error_msg = None
    text = ""
    size = 300
    border = 4
    error_level = "L"

    if request.method == "POST":
        text = request.form.get("text", "").strip()
        try:
            size = int(request.form.get("size", 300))
            border = int(request.form.get("border", 4))
            error_level = request.form.get("error", "L").upper()
        except ValueError:
            error_msg = "数値入力に誤りがあります。"
            size, border, error_level = 300, 4, "L"

        if not text:
            error_msg = "テキストを入力してください。"
        elif len(text) > 500:
            error_msg = "テキストが長すぎます（最大500文字）。"
        elif size > 1024 or size < 100:
            error_msg = "サイズは100〜1024の範囲で指定してください。"
        else:
            try:
                correction = {
                    "L": qrcode.constants.ERROR_CORRECT_L,
                    "M": qrcode.constants.ERROR_CORRECT_M,
                    "Q": qrcode.constants.ERROR_CORRECT_Q,
                    "H": qrcode.constants.ERROR_CORRECT_H,
                }.get(error_level, ERROR_CORRECT_L)

                qr = qrcode.QRCode(
                    version=1,
                    error_correction=correction,
                    box_size=10,
                    border=border,
                )
                qr.add_data(text)
                qr.make(fit=True)
                img = qr.make_image(
                    fill_color="black",
                    back_color="white"
                ).resize((size, size))

                buf = io.BytesIO()
                img.save(buf, format="PNG")
                qr_data = base64.b64encode(buf.getvalue()).decode("utf-8")

            except Exception as e:
                error_msg = f"QR生成エラー: {e}"

    return render_template(
        "index.html",
        qr_data=qr_data,
        text=text,
        size=size,
        border=border,
        error=error_level,
        error_msg=error_msg,
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    app.run(host=host, port=port, debug=DEBUG)