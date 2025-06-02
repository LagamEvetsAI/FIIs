from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/dy')
def get_dy():
    ativo = request.args.get("ativo", "").lower()
    if not ativo:
        return jsonify({"erro": "ativo não informado"}), 400

    url = f"https://www.fundsexplorer.com.br/funds/{ativo}"

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url, timeout=60000)

            dy = page.locator(".yieldChart__table__bloco").nth(2).locator(".table__linha").nth(1).inner_text()
            browser.close()

        return jsonify({"ativo": ativo.upper(), "dy_ultimo": dy.strip()})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# 👇 Esta parte garante que o Render saiba que o app está rodando
import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
