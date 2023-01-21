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
        f'<form action="/static/Instrukcja.pdf"><input type="submit" value="Instrukcja"></form><br>'
        f'<form action="/static/UNI{typ_pv}{uklad_pv}.pdf"><input type="submit" value="Rysunek"></form>'
        f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
        f"<table>"
        f"<tr><th>Poz.<th>Nazwa<th>Liczba<th>Opis<th>Długość"
        f"<tr><th>[nr]<th>-<th>[szt.]<th>-<th>[mm]"
        f"<tr><td>1<td>SŁUP DOLNY<td>{4 * ilosc_kons}<td>C75x45x15x3.0<td>2000"
        f"<tr><td>2<td>SŁUP GÓRNY TYLNI<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>2165"
        f"<tr><td>3<td>SŁUP GÓRNY PRZEDNI<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>1000"
        f"<tr><td>4<td>WSPORNIK BOCZNY<td>{2 * ilosc_kons}<td>LZR60x60x2<td>2750"
        f"<tr><td>5<td>WSPORNIK TYLNI<td>{1 * ilosc_kons}<td>LZR70x70x2<td>3100"
    )
    if typ_pv == 1 and uklad_pv == 1:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{8 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{12 * ilosc_kons}<td>C109x49x15x1.5<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {188.3 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{62 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{62 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{124 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 2:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C109x49x15x1.5<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {171.3 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{56 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{56 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{112 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv in [3, 4, 5, 6] or (typ_pv == 7 and uklad_pv == 2):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C109x49x15x1.5<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {174.4 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{56 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{56 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{112 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif (
        (typ_pv == 7 and uklad_pv == 1)
        or (typ_pv == 8 and uklad_pv == 2)
        or (typ_pv == 9 and uklad_pv == 2)
    ):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>73<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2680"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C109x49x15x1.5<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {178.3 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{56 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{56 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{112 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 8:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C109x49x15x1.5<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {180.1 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{56 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{56 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{112 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 9:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C109x49x15x1.5<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {183.2 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{56 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{56 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{112 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M16<td>{4 * ilosc_kons}<td>DIN-933-TZN-8.8<td>40"
            f"<tr><td>S.5<td>NAKRĘTKA M16<td>{4 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D17<td>{8 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    result += (
        f"<tr><th colspan=6>Ilość konstrukcji (stołów) = {ilosc_kons:.0f} szt."
        f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
        f"</table>"
    )
    if typ_pv == 1 and uklad_pv == 2:
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
