from grains.parse import parse_board_prices, to_number


def test_to_number():
    assert to_number("545.000") == 545000
    assert to_number("2.505,0") == 2505
    assert to_number("400,00") == 400


def test_soja_2026():
    prices = parse_board_prices("tests/sample_bulletins/2026-11-17.pdf")
    soja = [p for p in prices if p["grain"] == "Soja"][0]
    assert soja["price"] == 545000
    assert soja["type"] == "pizarra"