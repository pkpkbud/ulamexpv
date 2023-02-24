from contextlib import suppress
from math import ceil, floor

from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_autoindex import AutoIndex
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = "ULAMEX_SECRET_KEY"

idx = AutoIndex(app, "./pliki", add_url_rules=False)

login_manager = LoginManager()
login_manager.init_app(app)

users = {
    "monika": {"password": "cichowska"},
    "jakub": {"password": "zientek"},
}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in users:
        return

    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    username = request.form.get("username")
    if username not in users:
        return

    user = User()
    user.id = username
    user.is_authenticated = request.form["password"] == users[username]["password"]
    return user


@app.route("/pliki/")
@app.route("/pliki/<path:path>")
@login_required
def autoindex(path="."):
    return idx.render_autoindex(path)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        with suppress(KeyError):
            username = request.form.get("username")
            if request.form.get("password") == users[username]["password"]:
                user = User()
                user.id = username
                login_user(user)
                return redirect(url_for("autoindex"))
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
    mono = [1, 11, 12, 14, 16]
    ilosc_kons = ceil(ilosc_pv / 12) if typ_pv in mono else ceil(ilosc_pv / 8)
    result = (
        f'<p><form action="/static/Dwupodporowa_Instrukcja.pdf"><input type="submit" value="Instrukcja"></form></p>'
        f'<p><form action="/static/Dwupodporowa_U{typ_pv}{uklad_pv}.pdf"><input type="submit" value="Rysunek"></form></p>'
        f'<h2><img src="/static/Dwupodporowa_{1 if typ_pv in mono else 2}{uklad_pv}.png"> x {ilosc_kons}</h2>'
        f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
        f"<table>"
        f"<tr><th>Poz.<th>Nazwa<th>Liczba<th>Opis<th>Długość"
        f"<tr><th>[nr]<th>-<th>[szt.]<th>-<th>[mm]"
        f"<tr><td>1<td>SŁUP DOLNY<td>{4 * ilosc_kons}<td>C75x45x15x3.0<td>2000"
        f"<tr><td>2<td>SŁUP GÓRNY TYLNY<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>2165"
        f"<tr><td>3<td>SŁUP GÓRNY PRZEDNI<td>{2 * ilosc_kons}<td>C82x50x18x2.0<td>1000"
        f"<tr><td>4<td>WSPORNIK BOCZNY<td>{2 * ilosc_kons}<td>LZR60x60x2<td>2750"
        f"<tr><td>5<td>WSPORNIK TYLNY<td>{1 * ilosc_kons}<td>LZR70x70x2<td>3100"
    )
    if typ_pv in mono and uklad_pv == 1:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{8 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{12 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {213.1 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{54 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{54 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{108 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{12 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{12 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{24 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv in [2, 10, 13] or (typ_pv == 15 and uklad_pv == 1):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {192 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{50 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{50 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{100 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{10 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{10 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{20 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv in [3, 4, 5, 6] or (typ_pv in [7, 15] and uklad_pv == 2):
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>81<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2300"
            f"<tr><th colspan=6>Masa konstrukcji = {195.1 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{50 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{50 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{100 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{10 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{10 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{20 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
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
            f"<tr><td>S.1<td>ŚRUBA M12<td>{50 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{50 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{100 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{10 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{10 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{20 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 8:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>71<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2180"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {203.9 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{50 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{50 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{100 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{10 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{10 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{20 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    elif typ_pv == 9:
        result += (
            f"<tr><td>6<td>ŁĄCZNIK RYGLI, PŁATWI<td>{7 * ilosc_kons}<td>C104x45x12x2.0<td>600"
            f"<tr><td>72<td>RYGIEL (71-73)<td>{4 * ilosc_kons}<td>C110x50x15x2.0<td>2400"
            f"<tr><td>82<td>PŁATEW (81-82)<td>{10 * ilosc_kons}<td>C110x50x15x2.0<td>2640"
            f"<tr><th colspan=6>Masa konstrukcji = {207 * ilosc_kons:.0f} kg"
            f"<tr><td>S.1<td>ŚRUBA M12<td>{50 * ilosc_kons}<td>DIN-933-TZN-8.8<td>35"
            f"<tr><td>S.2<td>NAKRĘTKA M12<td>{50 * ilosc_kons}<td>DIN-6923-TZN-8<td>-"
            f"<tr><td>S.3<td>PODKŁADKA D13<td>{100 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
            f"<tr><td>S.4<td>ŚRUBA M8<td>{10 * ilosc_kons}<td>DIN-933-TZN-8.8<td>30"
            f"<tr><td>S.5<td>NAKRĘTKA M8<td>{10 * ilosc_kons}<td>DIN-895-TZN-8<td>-"
            f"<tr><td>S.6<td>PODKŁADKA D9<td>{20 * ilosc_kons}<td>DIN-9021-TZN-200HV<td>-"
        )
    result += (
        f"<tr><th colspan=6>Ilość konstrukcji (stołów) = {ilosc_kons:.0f} szt."
        f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
        f"</table>"
    )
    if typ_pv in mono and uklad_pv == 2:
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


@app.route("/jednopodporowa")
def jednopodporowa():
    return render_template("jednopodporowa.html")


@app.route("/_jednopodporowa")
def _jednopodporowa():
    wym_pv_1 = int(request.args.get("wym_pv_1"))
    wym_pv_2 = int(request.args.get("wym_pv_2"))
    uklad_pv = int(request.args.get("uklad_pv"))
    moc_pv = int(request.args.get("moc_pv"))
    ilosc_pv = int(request.args.get("ilosc_pv"))
    szer_pv, dlug_pv = sorted([wym_pv_1, wym_pv_2])
    L = 20000  # mm - długość konstrukcji do 20 m
    if uklad_pv == 1:
        l = ceil(ilosc_pv / 2) * (szer_pv + 20)
        n = min(ceil(ilosc_pv / 2), floor((L - 60) / (szer_pv + 20)))
    elif uklad_pv == 2:
        l = ceil(ilosc_pv / 3) * (dlug_pv + 10)
        n = min(ceil(ilosc_pv / 3), floor((L - 60) / (dlug_pv + 10)))
    l += ceil(l / L) * 60
    ilosc_kons = l / L
    ilosc_ram = ceil(ilosc_kons * ceil((L - 1000) / 1700))
    ilosc_stezen = 2 * ceil(ilosc_kons)
    dlug_platwi = (4 if uklad_pv == 1 else 6) * l
    ilosc_platwi = ceil(dlug_platwi / 6210)
    masa = 35.3 * ilosc_ram + 4.0 * ilosc_stezen + 0.86e-3 * dlug_platwi
    result = (
        f'<p><form action="/static/Jednopodporowa_Instrukcja.pdf"><input type="submit" value="Instrukcja"></form></p>'
        f'<p><form action="/static/Jednopodporowa_U{uklad_pv}.pdf"><input type="submit" value="Rysunek"></form></p>'
        + n * f'<h2><img src="/static/Jednopodporowa_{uklad_pv}.png"></h2>'
        + f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
        f"<table>"
        f"<tr><th>Poz.<th>Nazwa<th>Liczba<th>Opis<th>Długość"
        f"<tr><th>[nr]<th>-<th>[szt.]<th>-<th>[mm]"
        f"<tr><td>1<td>SŁUP<td>{1 * ilosc_ram}<td>C130x50x15x3.0<td>2800"
        f"<tr><td>2<td>RYGIEL<td>{1 * ilosc_ram}<td>L100x70x25x2.5<td>3100"
        f"<tr><td>31<td>STĘŻENIE DŁUGIE<td>{1 * ilosc_ram}<td>CZ60x40x3<td>1700"
        f"<tr><td>32<td>STĘŻENIE KRÓTKIE<td>{1 * ilosc_ram}<td>CZ60x40x3<td>1100"
        f"<tr><td>4<td>STĘŻENIE PODŁUŻNE<td>{ilosc_stezen}<td>LZR60x60x2<td>2220"
        f"<tr><td>5<td>PŁATEW<br>* długość łączna<td>{ilosc_platwi}<td>"
        f"<a href='https://ulamex.com.pl/profil-aluminiowy-pv-40x40-do-fotowoltaiki'>PV 40x40 6-kątny</a><td>6210<br>{dlug_platwi:,}*"
        f"<tr><td>6<td>ŁĄCZNIK PŁATWI<td>{ilosc_platwi}<td>"
        f"<a href='https://ulamex.com.pl/lacznik-ceownik-aluminium'>C45x25</a><td>100"
        f"<tr><th colspan=6>Masa konstrukcji = {masa:.0f} kg"
        f"<tr><td>S.1<td>ŚRUBA M12<td>{5 * ilosc_ram + 2 * ilosc_stezen}<td>DIN-933-TZN-8.8<td>35"
        f"<tr><td>S.2<td>NAKRĘTKA M12<td>{5 * ilosc_ram + 2 * ilosc_stezen}<td>DIN-6923-TZN-8<td>-"
        f"<tr><td>S.3<td>PODKŁADKA D13<td>{10 * ilosc_ram + 4 * ilosc_stezen}<td>DIN-9021-TZN-200HV<td>-"
        f"<tr><td>S.4<td>ŚRUBA M10<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-933-TZN-8.8<td>30"
        f"<tr><td>S.5<td>NAKRĘTKA M10<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-6923-TZN-8<td>-"
        f"<tr><td>S.6<td>PODKŁADKA D11<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-9021-TZN-200HV<td>-"
        f"<tr><th colspan=6>Ilość niezależnych konstrukcji (do 20 m) = {ceil(ilosc_kons):.0f} szt."
        f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
        f"</table>"
    )
    if (
        uklad_pv == 1
        and (dlug_pv > 1800 or dlug_pv < 1600)
        or uklad_pv == 2
        and (szer_pv > 1150 or szer_pv < 800)
    ):
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


@app.route("/dwupodporowa_m")
def dwupodporowa_m():
    return render_template("dwupodporowa_m.html")


@app.route("/_dwupodporowa_m")
def _dwupodporowa_m():
    wym_pv_1 = int(request.args.get("wym_pv_1"))
    wym_pv_2 = int(request.args.get("wym_pv_2"))
    uklad_pv = int(request.args.get("uklad_pv"))
    moc_pv = int(request.args.get("moc_pv"))
    ilosc_pv = int(request.args.get("ilosc_pv"))
    szer_pv, dlug_pv = sorted([wym_pv_1, wym_pv_2])
    L = 20000  # mm - długość konstrukcji do 20 m
    if uklad_pv == 1:
        l = ceil(ilosc_pv / 2) * (szer_pv + 20)
        n = min(ceil(ilosc_pv / 2), floor((L - 60) / (szer_pv + 20)))
    elif uklad_pv == 2:
        l = ceil(ilosc_pv / 3) * (dlug_pv + 10)
        n = min(ceil(ilosc_pv / 3), floor((L - 60) / (dlug_pv + 10)))
    l += ceil(l / L) * 60
    ilosc_kons = l / L
    ilosc_ram = ceil(ilosc_kons * ceil((L - 1000) / 1700))
    ilosc_stezen = 2 * ceil(ilosc_kons)
    dlug_platwi = (4 if uklad_pv == 1 else 6) * l
    ilosc_platwi = ceil(dlug_platwi / 6210)
    masa = 35.0 * ilosc_ram + 4.0 * ilosc_stezen + 0.86e-3 * dlug_platwi
    result = (
        f'<p><form action="/static/Dwupodporowa_M_Instrukcja.pdf"><input type="submit" value="Instrukcja"></form></p>'
        f'<p><form action="/static/Dwupodporowa_M_U{uklad_pv}.pdf"><input type="submit" value="Rysunek"></form></p>'
        + n * f'<h2><img src="/static/Jednopodporowa_{uklad_pv}.png"></h2>'
        + f"<p><h2>ZESTAWIENIE ELEMENTÓW</h2></p>"
        f"<table>"
        f"<tr><th>Poz.<th>Nazwa<th>Liczba<th>Opis<th>Długość"
        f"<tr><th>[nr]<th>-<th>[szt.]<th>-<th>[mm]"
        f"<tr><td>11<td>SŁUP TYLNY<td>{1 * ilosc_ram}<td>C75x45x15x2.5<td>3320"
        f"<tr><td>12<td>SŁUP PRZEDNI<td>{1 * ilosc_ram}<td>C75x45x15x2.5<td>2280"
        f"<tr><td>2<td>RYGIEL<td>{1 * ilosc_ram}<td>L100x70x25x2.5<td>3100"
        f"<tr><td>33<td>STĘŻENIE POPRZECZNE<td>{1 * ilosc_ram}<td>CZ60x40x3<td>1480"
        f"<tr><td>4<td>STĘŻENIE PODŁUŻNE<td>{ilosc_stezen}<td>LZR60x60x2<td>2220"
        f"<tr><td>5<td>PŁATEW<br>* długość łączna<td>{ilosc_platwi}<td>"
        f"<a href='https://ulamex.com.pl/profil-aluminiowy-pv-40x40-do-fotowoltaiki'>PV 40x40 6-kątny</a><td>6210<br>{dlug_platwi:,}*"
        f"<tr><td>6<td>ŁĄCZNIK PŁATWI<td>{ilosc_platwi}<td>"
        f"<a href='https://ulamex.com.pl/lacznik-ceownik-aluminium'>C45x25</a><td>100"
        f"<tr><th colspan=6>Masa konstrukcji = {masa:.0f} kg"
        f"<tr><td>S.1<td>ŚRUBA M12<td>{4 * ilosc_ram + 2 * ilosc_stezen}<td>DIN-933-TZN-8.8<td>35"
        f"<tr><td>S.2<td>NAKRĘTKA M12<td>{4 * ilosc_ram + 2 * ilosc_stezen}<td>DIN-6923-TZN-8<td>-"
        f"<tr><td>S.3<td>PODKŁADKA D13<td>{8 * ilosc_ram + 4 * ilosc_stezen}<td>DIN-9021-TZN-200HV<td>-"
        f"<tr><td>S.4<td>ŚRUBA M10<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-933-TZN-8.8<td>30"
        f"<tr><td>S.5<td>NAKRĘTKA M10<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-6923-TZN-8<td>-"
        f"<tr><td>S.6<td>PODKŁADKA D11<td>{(4 if uklad_pv == 1 else 6) * ilosc_ram + 2 * ilosc_platwi}<td>DIN-9021-TZN-200HV<td>-"
        f"<tr><th colspan=6>Ilość niezależnych konstrukcji (do 20 m) = {ceil(ilosc_kons):.0f} szt."
        f"<tr><th colspan=6>Moc instalacji = {(ilosc_pv * moc_pv) / 1000:.1f} kW"
        f"</table>"
    )
    if (
        uklad_pv == 1
        and (dlug_pv > 1800 or dlug_pv < 1600)
        or uklad_pv == 2
        and (szer_pv > 1150 or szer_pv < 800)
    ):
        result = "<h2>BRAK</h2>"
    return jsonify(result=result)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
