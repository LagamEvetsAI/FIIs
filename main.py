from flask import Flask, request, jsonify
import yfinance as yf
import os

# 1️⃣ Cria a aplicação Flask
app = Flask(__name__)

# 2️⃣ Define a rota DEPOIS de criar o app
@app.route('/dy')
def get_dy():
    ativo = request.args.get("ativo", "").upper()
    if not ativo.endswith(".SA"):
        ativo += ".SA"
    
    try:
        ticker = yf.Ticker(ativo)
        info = ticker.info

        preco_atual = info.get("regularMarketPrice")
        ultimo_dividendo = info.get("lastDividendValue")
        dy_anualizado = info.get("dividendYield")

        if preco_atual is None or ultimo_dividendo is None:
            return jsonify({
                "ativo": ativo,
                "dy_mensal": "Não disponível",
                "dy_anualizado": f"{dy_anualizado * 100:.2f}%" if dy_anualizado else "Não disponível"
            })

        dy_mensal = (ultimo_dividendo / preco_atual) * 100

        return jsonify({
            "ativo": ativo,
            "dy_mensal": f"{dy_mensal:.2f}%",
            "dy_anualizado": f"{dy_anualizado * 100:.2f}%" if dy_anualizado else "Não disponível",
            "ultimo_dividendo": f"R$ {ultimo_dividendo:.2f}",
            "preco_atual": f"R$ {preco_atual:.2f}"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

# 3️⃣ Inicializa o servidor corretamente para o Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
