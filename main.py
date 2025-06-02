from flask import Flask, request, jsonify
import yfinance as yf

app = Flask(__name__)

@app.route('/dy')
def get_dy():
    ativo = request.args.get("ativo", "").upper()
    if not ativo.endswith(".SA"):
        ativo += ".SA"
    
    try:
        ticker = yf.Ticker(ativo)
        info = ticker.info
        dy = info.get("dividendYield")

        if dy is None:
            return jsonify({"ativo": ativo, "dy_ultimo": "Não disponível"})

        return jsonify({"ativo": ativo, "dy_ultimo": f"{dy * 100:.2f}%"})
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

import os
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
