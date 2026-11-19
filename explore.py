import pdfplumber

path = "tests/sample_bulletins/2026-11-17.pdf"

with pdfplumber.open(path) as pdf:
    page = pdf.pages[0]
    words = page.extract_words()

    # Agrupar palabras por fila
    rows = {}
    for word in words:
        top = round(word["top"])
        if top not in rows:
            rows[top] = []
        rows[top].append(word)

    # Ubicar columnas
    board_x = None
    estimate_x = None
    header_top = None
    for word in words:
        if word["text"] == "Pizarra":
            board_x = word["x0"]
            header_top = word["top"]
        if word["text"] == "Estimativo":
            estimate_x = word["x0"]

    print("Pizarra:", board_x, "Estimativo:", estimate_x)

    # Leer la tabla
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
            elif text[0].isdigit() and abs(word["x0"] - board_x) < 10:  # pizarra
                print(" ".join(name_parts), "-> pizarra:", text)
            elif text[0].isdigit() and abs(word["x0"] - estimate_x) < 10:  # estimativo
                print(" ".join(name_parts), "-> estimativo:", text)