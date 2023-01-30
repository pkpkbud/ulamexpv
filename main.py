from math import ceil

from flask import Flask, jsonify, render_template, request
from flask_autoindex import AutoIndex

app = Flask(__name__)
idx = AutoIndex(app, "./pliki", add_url_rules=False)


@app.route("/pliki/")
@app.route("/pliki/<path:path>")
def autoindex(path="."):
    return idx.render_autoindex(path)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/dwupodporowa")
def dwupodporowa():
    return render_template("dwupodporowa.html")


@app.route("/_dwupodporowa")
def _dwupodporowa():
    typ_pv = int(request.args.get("typ_pv"))
    uklad_pv = int(request.args.get("uklad_pv"))
    moc_pv = int(request.args.get("moc_pv"))
    ilosc_pv = int(request.args.get("ilosc_pv"))
    ilosc_kons = ceil(ilosc_pv / 12) if typ_pv == 1 else ceil(ilosc_pv / 8)
    result = (
        f'<p><form action="/pliki/Dwupodporowa/Dwupodporowa_Instrukcja.pdf"><input type="submit" value="Instrukcja"></form></p>'
        f'<p><form action="/pliki/Dwupodporowa/Dwupodporowa_U{typ_pv}{uklad_pv}.pdf"><input type="submit" value="Rysunek"></form></p>'
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
            f"<tr><td>81<td>PŁATEW (81-82)<td>{12 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {213.1 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{66 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{66 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{132 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 2:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {192 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{60 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{60 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{120 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv in [3, 4, 5, 6] or (typ_pv == 7 and uklad_pv == 2):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {195.1 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{60 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{60 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{120 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif (
        (typ_pv == 7 and uklad_pv == 1)
        or (typ_pv == 8 and uklad_pv == 2)
        or (typ_pv == 9 and uklad_pv == 2)
    ):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>73<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2680"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {199 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{60 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{60 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{120 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 8:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {203.9 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{60 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{60 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{120 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 9:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {207 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{60 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{60 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{120 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    result += (
        f"<tr><th colspan=6>Ilość konstrukcji (stołów) = {ilosc_kons:.0f} szt."
        f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
        f"</table>"
    )
    if typ_pv == 1 and uklad_pv == 2:
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


@app.route("/jednopodporowa")
def jednopodporowa():
    return render_template("jednopodporowa.html")


@app.route("/_jednopodporowa")
def _jednopodporowa():
    szer_pv = int(request.args.get("szer_pv"))
    wys_pv = int(request.args.get("wys_pv"))
    moc_pv = int(request.args.get("moc_pv"))
    ilosc_pv = int(request.args.get("ilosc_pv"))
    dlugosc = ceil(ilosc_pv / 2) * (szer_pv + 20) + 60
    ilosc_ram = max(2, ceil((dlugosc - 1000) / 2000) + 1)
    if wys_pv == 1:
        result = (
            f'<p><form action="/pliki/Jednopodporowa/Jednopodporowa_Instrukcja.pdf"><input type="submit" value="Instrukcja"></form></p>'
            f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
            f"<table>"
            f"<tr><th>Poz.<th>Nazwa<th>Liczba<th>Opis<th>Długość"
            f"<tr><th>[nr]<th>-<th>[szt.]<th>-<th>[mm]"
            f"<tr><td>1<td>SŁUP<td>{1 * ilosc_ram}<td>C120x40x15x3.0<td>2800"
            f"<tr><td>2<td>RYGIEL<td>{1 * ilosc_ram}<td>L100x70x25x2.5<td>2800"
            f"<tr><td>3<td>STĘŻENIE DŁUGIE<td>{1 * ilosc_ram}<td>LZR70x70x2<td>1700"
            f"<tr><td>4<td>STĘŻENIE KRÓTKIE<td>{1 * ilosc_ram}<td>LZR70x70x2<td>1100"
            f"<tr><td>5<td>PŁATEW<td>{4 * ceil(dlugosc / 6210)}<td>PV40x40<td>6210"
            f"<tr><th colspan=6>Masa konstrukcji = {30 * ilosc_ram + 0.8e-3 * 4 * dlugosc:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{5 * ilosc_ram}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{5 * ilosc_ram}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{10 * ilosc_ram}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><th colspan=6>Ilość konstrukcji (długość do 20 m) = {ceil(dlugosc / 20000):.0f} szt."
            f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
            f"</table>"
        )
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
