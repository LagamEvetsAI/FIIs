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

        if preco_atual is None or ultimo_dividendo is None:
            return jsonify({
                "ativo": ativo,
                "dy_mensal": "Não disponível",
                "dy_anualizado": info.get("dividendYield")
            })

        dy_mensal = (ultimo_dividendo / preco_atual) * 100
        dy_anualizado = info.get("dividendYield")

        return jsonify({
            "ativo": ativo,
            "dy_mensal": f"{dy_mensal:.2f}%",
            "dy_anualizado": f"{dy_anualizado * 100:.2f}%" if dy_anualizado else "Não disponível",
            "ultimo_dividendo": f"R$ {ultimo_dividendo:.2f}",
            "preco_atual": f"R$ {preco_atual:.2f}"
        })

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
