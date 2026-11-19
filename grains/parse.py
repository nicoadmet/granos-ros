import pdfplumber

def to_number(text):
    text = text.replace(".", "")   
    text = text.replace(",", ".")  
    return float(text)

def parse_board_prices(path):
    #Devuelve los precios de la columna CAC Rosario del boletín.
    with pdfplumber.open(path) as pdf:
        words = pdf.pages[0].extract_words()

    # Agrupar palabras por fila
    rows = {}
    for word in words:
        top = round(word["top"])
        rows.setdefault(top, []).append(word)

    # Ubicar columnas
    board_x = estimate_x = header_top = None
    for word in words:
        if word["text"] == "Pizarra":
            board_x = word["x0"]
            header_top = word["top"]
        if word["text"] == "Estimativo":
            estimate_x = word["x0"]

    # Leer la tabla
    prices = []
    for top, row_words in rows.items():
        if top <= header_top:  # arriba del cuadro
            continue
        if row_words[0]["text"] == "Cuando":  # fin del cuadro
            break
        name_parts = []
        for word in row_words:
            text = word["text"]
            if word["x0"] < board_x - 10:  # nombre del grano
                name_parts.append(text)
            elif text[0].isdigit() and abs(word["x0"] - board_x) < 10:
                prices.append({"grain": " ".join(name_parts), "price": to_number(text), "type": "pizarra"})
            elif text[0].isdigit() and abs(word["x0"] - estimate_x) < 10:
                prices.append({"grain": " ".join(name_parts), "price": to_number(text), "type": "estimativo"})

    return prices