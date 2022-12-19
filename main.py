from math import ceil
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/_zestawienie")
def _zestawienie():
    typ_pv = int(request.args.get("typ_pv"))
    uklad_pv = int(request.args.get("uklad_pv"))
    moc_pv = int(request.args.get("moc_pv"))
    ilosc_pv = int(request.args.get("ilosc_pv"))
    ilosc_kons = ceil(ilosc_pv / 12) if typ_pv == 1 else ceil(ilosc_pv / 8)
    result = (
        f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
        f"<table>"
        f"<tr><th>Poz.<th>Liczba<th>Przekrój<th>Długość<th>Ciężar"
        f"<tr><th>[nr]<th>[szt.]<th>[opis]<th>[cm]<th>[kg/szt.]"
        f"<tr><td>1<td>{4 * ilosc_kons}<td>C75x45x15x3.0<td>200<td>7,9"
        f"<tr><td>2<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>216,5<td>6,8"
        f"<tr><td>3<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>100<td>3,1"
        f"<tr><td>4<td>{2 * ilosc_kons}<td>LZR60x60x2<td>275<td>5,0"
        f"<tr><td>5<td>{1 * ilosc_kons}<td>LZR70x70x2<td>310<td>6,6"
    )
    if typ_pv == 1 and uklad_pv == 1:
        result += (
            f"<tr><td>6<td>{8 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>72<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>240<td>8,3"
            f"<tr><td>81<td>{12 * ilosc_kons}<td>C110x50x15x1.5<td>230<td>6,1"
            f"<tr><th colspan=5>Ciężar konstrukcji = {186.5 * ilosc_kons:.0f} kg</td>"
        )
    elif typ_pv == 2:
        result += (
            f"<tr><td>6<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>71<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>218<td>7,6"
            f"<tr><td>81<td>{10 * ilosc_kons}<td>C110x50x15x1.5<td>230<td>6,1"
            f"<tr><th colspan=5>Ciężar konstrukcji = {169.7 * ilosc_kons:.0f} kg</td>"
        )
    elif typ_pv in [3, 4, 5, 6] or (typ_pv == 7 and uklad_pv == 2):
        result += (
            f"<tr><td>6<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>72<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>240<td>8,3"
            f"<tr><td>81<td>{10 * ilosc_kons}<td>C110x50x15x1.5<td>230<td>6,1"
            f"<tr><th colspan=5>Ciężar konstrukcji = {172.8 * ilosc_kons:.0f} kg</td>"
        )
    elif (
        (typ_pv == 7 and uklad_pv == 1)
        or (typ_pv == 8 and uklad_pv == 2)
        or (typ_pv == 9 and uklad_pv == 2)
    ):
        result += (
            f"<tr><td>6<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>73<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>268<td>9,3"
            f"<tr><td>81<td>{10 * ilosc_kons}<td>C110x50x15x1.5<td>230<td>6,1"
            f"<tr><th colspan=5>Ciężar konstrukcji = {176.7 * ilosc_kons:.0f} kg</td>"
        )
    elif typ_pv == 8:
        result += (
            f"<tr><td>6<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>71<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>218<td>7,6"
            f"<tr><td>82<td>{10 * ilosc_kons}<td>C110x50x15x1.5<td>264<td>7,0"
            f"<tr><th colspan=5>Ciężar konstrukcji = {178.9 * ilosc_kons:.0f} kg</td>"
        )
    elif typ_pv == 9:
        result += (
            f"<tr><td>6<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>42<td>1,3"
            f"<tr><td>72<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>240<td>8,3"
            f"<tr><td>82<td>{10 * ilosc_kons}<td>C110x50x15x1.5<td>264<td>7,0"
            f"<tr><th colspan=5>Ciężar konstrukcji = {182.0 * ilosc_kons:.0f} kg</td>"
        )
    result += (
        f"<tr><th colspan=5>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW</td>"
        f"</table>"
    )
    if typ_pv == 1 and uklad_pv == 2:
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
