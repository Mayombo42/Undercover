from flask import Flask, request, redirect, url_for, render_template_string, session
import random

# =========================================================
# UNDERCOVER WEB - Version site internet avec Flask
# Installation : pip install flask
# Lancement : python undercover.py
# Puis ouvre : http://127.0.0.1:5000
# =========================================================

app = Flask(__name__)
app.secret_key = "undercover_secret_key_change_me"

CATEGORIES = {
    "Bonus": [
        ("Pizza", "Burger"), ("Tacos", "Kebab"), ("Netflix", "YouTube"),
        ("TikTok", "Instagram"), ("PS5", "Xbox"), ("Ferrari", "Lamborghini"),
        ("Tesla", "BMW"), ("Nike", "Adidas"), ("McDonald's", "Burger King"),
        ("Coca-Cola", "Pepsi"), ("Disney", "Pixar"), ("Marvel", "DC"),
        ("Fortnite", "Minecraft"), ("FIFA", "Call of Duty"), ("Spotify", "Deezer"),
        ("Paris", "Lyon"), ("Train", "Avion"), ("Plage", "Piscine"),
        ("Cinéma", "Théâtre"), ("Restaurant", "Fast-food"),
    ],
    "Personnalités": [
        ("Mbappé", "Haaland"), ("Cristiano Ronaldo", "Messi"),
        ("Neymar", "Vinicius"), ("Taylor Swift", "Ariana Grande"),
        ("Beyoncé", "Rihanna"), ("Elon Musk", "Jeff Bezos"),
        ("Squeezie", "Michou"), ("Inoxtag", "Mastu"),
        ("Zendaya", "Jenna Ortega"), ("Drake", "Travis Scott"),
        ("Jul", "Ninho"), ("Gims", "Dadju"), ("Aya Nakamura", "Wejdene"),
        ("Kanye West", "Jay-Z"), ("Kim Kardashian", "Kylie Jenner"),
    ],
    "Animaux": [
        ("Lion", "Tigre"), ("Chien", "Chat"), ("Loup", "Renard"),
        ("Serpent", "Lézard"), ("Dauphin", "Requin"), ("Cheval", "Âne"),
        ("Ours", "Panda"), ("Lapin", "Lièvre"), ("Aigle", "Faucon"),
        ("Vache", "Taureau"), ("Crocodile", "Alligator"),
        ("Mouton", "Chèvre"), ("Poule", "Canard"), ("Pieuvre", "Calamar"),
        ("Tortue", "Escargot"), ("Girafe", "Zèbre"),
        ("Hippopotame", "Rhinocéros"), ("Fourmi", "Abeille"),
        ("Papillon", "Libellule"), ("Singe", "Gorille"),
    ],
    "Objets": [
        ("Stylo", "Crayon"), ("Canapé", "Lit"), ("Lampe", "Bougie"),
        ("Téléphone", "Ordinateur"), ("Télécommande", "Manette"),
        ("Sac", "Valise"), ("Montre", "Bracelet"), ("Clavier", "Souris"),
        ("Chaise", "Tabouret"), ("Lunettes", "Casque"),
        ("Fourchette", "Cuillère"), ("Couteau", "Ciseaux"),
        ("Parapluie", "K-way"), ("Clé", "Cadenas"), ("Livre", "Journal"),
        ("Bouteille", "Gourde"), ("Serviette", "Couverture"),
        ("Brosse à dents", "Peigne"), ("Ventilateur", "Radiateur"),
        ("Réfrigérateur", "Congélateur"),
    ],
    "Pays": [
        ("France", "Belgique"), ("Italie", "Espagne"), ("Brésil", "Argentine"),
        ("Chine", "Japon"), ("Corée du Sud", "Corée du Nord"),
        ("Canada", "États-Unis"), ("Portugal", "Grèce"), ("Suisse", "Autriche"),
        ("Norvège", "Suède"), ("Maroc", "Algérie"), ("Tunisie", "Égypte"),
        ("Inde", "Pakistan"), ("Mexique", "Colombie"),
        ("Australie", "Nouvelle-Zélande"), ("Turquie", "Arabie Saoudite"),
        ("Russie", "Ukraine"), ("Finlande", "Danemark"),
        ("Pays-Bas", "Belgique"), ("Thaïlande", "Vietnam"),
        ("Irlande", "Écosse"),
    ],
}

BASE_HTML = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Undercover</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            font-family: Arial, Helvetica, sans-serif;
            background: radial-gradient(circle at top, #2b1b5f, #090914 55%);
            color: white;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        .app {
            width: 100%;
            max-width: 430px;
        }
        .tag {
            color: #a78bfa;
            font-weight: 800;
            letter-spacing: 1px;
            font-size: 13px;
            margin-bottom: 8px;
        }
        h1 {
            font-size: 38px;
            margin: 0 0 10px;
            line-height: 1;
        }
        h2 { margin-top: 0; }
        p {
            color: #c7c7d8;
            line-height: 1.5;
        }
        .card {
            background: rgba(20, 20, 34, 0.95);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 30px;
            padding: 24px;
            box-shadow: 0 25px 70px rgba(0,0,0,0.35);
            margin-top: 20px;
        }
        .hero {
            text-align: center;
            padding: 42px 24px;
        }
        .emoji { font-size: 70px; margin-bottom: 10px; }
        input, select {
            width: 100%;
            padding: 15px;
            border-radius: 16px;
            border: 1px solid #2f2f46;
            background: #0f1020;
            color: white;
            font-size: 16px;
            margin: 8px 0;
        }
        label {
            font-weight: 700;
            display: block;
            margin-top: 15px;
            margin-bottom: 5px;
        }
        button, .btn {
            width: 100%;
            border: none;
            border-radius: 18px;
            padding: 16px;
            margin-top: 12px;
            background: #7c3aed;
            color: white;
            font-size: 16px;
            font-weight: 800;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            text-align: center;
        }
        .btn-secondary { background: #1f2937; }
        .btn-danger { background: #e11d48; }
        .btn-green { background: #22c55e; }
        .list-item {
            background: #0f1020;
            border-radius: 16px;
            padding: 14px;
            margin: 8px 0;
            font-weight: 700;
        }
        .word {
            font-size: 40px;
            font-weight: 900;
            color: #22c55e;
            text-align: center;
            margin: 30px 0;
            word-break: break-word;
        }
        .white { color: #f43f5e; }
        .center { text-align: center; }
        .small { font-size: 13px; color: #a1a1aa; }
        .score-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #0f1020;
            border-radius: 16px;
            padding: 14px;
            margin: 8px 0;
            font-weight: 800;
        }
    </style>
</head>
<body>
<div class="app">
    {{ content|safe }}
</div>
</body>
</html>
"""

def page(content):
    return render_template_string(BASE_HTML, content=content)


def get_all_words():
    words = []
    for liste in CATEGORIES.values():
        words.extend(liste)
    return words


def init_scores(joueurs):
    scores = session.get("scores", {})
    for joueur in joueurs:
        scores.setdefault(joueur, 0)
    session["scores"] = scores


def current_game():
    return session.get("game", {})


@app.route("/")
def home():
    content = """
    <div class="tag">UNDERCOVER WEB</div>
    <h1>Le jeu des imposteurs</h1>
    <p>Crée une partie, distribue les mots en secret, votez et découvrez qui bluffait.</p>
    <div class="card hero">
        <div class="emoji">🕵️</div>
        <h2>Undercover</h2>
        <p>Version site internet gratuite, avec catégories, Mister White et classement.</p>
        <a class="btn" href="/setup">Créer une partie</a>
        <a class="btn btn-secondary" href="/scores">Voir le classement</a>
    </div>
    """
    return page(content)


@app.route("/setup", methods=["GET", "POST"])
def setup():
    if request.method == "POST":
        nb = int(request.form.get("nb", 5))
        categorie = request.form.get("categorie", "Tous")
        mister_white = request.form.get("mister_white") == "on"
        nb_undercover = request.form.get("nb_undercover", "Auto")

        session["settings"] = {
            "nb": nb,
            "categorie": categorie,
            "mister_white": mister_white,
            "nb_undercover": nb_undercover,
        }
        return redirect(url_for("players"))

    options = "<option>Tous</option>" + "".join([f"<option>{c}</option>" for c in CATEGORIES.keys()])
    content = f"""
    <div class="tag">NOUVELLE PARTIE</div>
    <h1>Paramètres</h1>
    <div class="card">
        <form method="post">
            <label>Nombre de joueurs</label>
            <input type="number" name="nb" value="5" min="3" max="20" required>

            <label>Catégorie</label>
            <select name="categorie">{options}</select>

            <label>Nombre d'Undercover</label>
            <select name="nb_undercover">
                <option>Auto</option>
                <option>1</option>
                <option>2</option>
                <option>3</option>
            </select>

            <label>
                <input style="width:auto;" type="checkbox" name="mister_white" checked>
                Activer Mister White
            </label>

            <button type="submit">Continuer</button>
        </form>
        <a class="btn btn-secondary" href="/">Retour</a>
    </div>
    """
    return page(content)


@app.route("/players", methods=["GET", "POST"])
def players():
    settings = session.get("settings")
    if not settings:
        return redirect(url_for("setup"))

    nb = settings["nb"]

    if request.method == "POST":
        joueurs = []
        for i in range(nb):
            nom = request.form.get(f"joueur_{i}", "").strip()
            joueurs.append(nom if nom else f"Joueur {i + 1}")

        lancer_partie(joueurs, settings)
        return redirect(url_for("pass_phone", index=0))

    inputs = "".join([f'<input name="joueur_{i}" placeholder="Joueur {i + 1}">' for i in range(nb)])
    content = f"""
    <div class="tag">JOUEURS</div>
    <h1>Prénoms</h1>
    <div class="card">
        <form method="post">
            {inputs}
            <button type="submit">Lancer la partie</button>
        </form>
    </div>
    """
    return page(content)


def lancer_partie(joueurs, settings):
    init_scores(joueurs)

    categorie = settings["categorie"]
    if categorie == "Tous":
        mot_civil, mot_undercover = random.choice(get_all_words())
    else:
        mot_civil, mot_undercover = random.choice(CATEGORIES[categorie])

    nb = len(joueurs)
    if settings["nb_undercover"] == "Auto":
        nb_undercover = 1 if nb < 6 else 2
    else:
        nb_undercover = int(settings["nb_undercover"])

    nb_undercover = max(1, min(nb_undercover, nb - 2))
    nb_mister = 1 if settings["mister_white"] and nb >= 4 else 0

    roles = ["Civil"] * nb
    indices = list(range(nb))
    random.shuffle(indices)

    for i in range(nb_undercover):
        roles[indices[i]] = "Undercover"

    if nb_mister and nb_undercover < nb:
        roles[indices[nb_undercover]] = "Mister White"

    mots = []
    for role in roles:
        if role == "Civil":
            mots.append(mot_civil)
        elif role == "Undercover":
            mots.append(mot_undercover)
        else:
            mots.append(None)

    session["game"] = {
        "joueurs": joueurs,
        "roles": roles,
        "mots": mots,
        "vivants": joueurs.copy(),
        "roles_vivants": roles.copy(),
        "mots_vivants": mots.copy(),
        "mot_civil": mot_civil,
        "mot_undercover": mot_undercover,
        "tour": 1,
        "finished": False,
    }


@app.route("/pass/<int:index>")
def pass_phone(index):
    game = current_game()
    joueurs = game.get("joueurs", [])
    if index >= len(joueurs):
        return redirect(url_for("round_page"))

    joueur = joueurs[index]
    content = f"""
    <div class="tag">MOT SECRET</div>
    <h1>Au tour de</h1>
    <div class="card hero">
        <div class="emoji">🔒</div>
        <h2>{joueur}</h2>
        <p>Passe l'écran à ce joueur. Les autres ne doivent pas regarder.</p>
        <a class="btn" href="/word/{index}">Voir mon mot</a>
    </div>
    """
    return page(content)


@app.route("/word/<int:index>")
def word(index):
    game = current_game()
    joueur = game["joueurs"][index]
    role = game["roles"][index]
    mot = game["mots"][index]

    if role == "Mister White":
        shown = "MISTER WHITE"
        classe = "word white"
        desc = "Tu n'as aucun mot. Bluffe et essaie de comprendre le mot des autres."
    else:
        shown = mot
        classe = "word"
        desc = "Voici ton mot secret. Ne le montre à personne."

    content = f"""
    <div class="tag">{joueur}</div>
    <h1>Ton information</h1>
    <div class="card hero">
        <div class="emoji">🎯</div>
        <div class="{classe}">{shown}</div>
        <p>{desc}</p>
        <a class="btn" href="/pass/{index + 1}">Cacher et passer</a>
    </div>
    """
    return page(content)


@app.route("/round")
def round_page():
    game = current_game()
    vivants = game["vivants"]
    joueurs_html = "".join([f'<div class="list-item">● {j}</div>' for j in vivants])

    content = f"""
    <div class="tag">TOUR {game['tour']}</div>
    <h1>Indices</h1>
    <p>Chaque joueur donne un indice à l'oral, puis vous discutez.</p>
    <div class="card">
        <h2>Joueurs en vie</h2>
        {joueurs_html}
        <a class="btn" href="/vote">Passer au vote</a>
    </div>
    """
    return page(content)


@app.route("/vote")
def vote():
    game = current_game()
    buttons = "".join([
        f'<a class="btn btn-danger" href="/eliminate/{i}">Éliminer {joueur}</a>'
        for i, joueur in enumerate(game["vivants"])
    ])
    content = f"""
    <div class="tag">VOTE</div>
    <h1>Qui éliminer ?</h1>
    <div class="card">
        {buttons}
        <a class="btn btn-secondary" href="/round">Retour</a>
    </div>
    """
    return page(content)


@app.route("/eliminate/<int:index>")
def eliminate(index):
    game = current_game()
    joueur = game["vivants"].pop(index)
    role = game["roles_vivants"].pop(index)
    game["mots_vivants"].pop(index)
    session["game"] = game

    if role == "Mister White":
        content = f"""
        <div class="tag">ÉLIMINATION</div>
        <h1>{joueur}</h1>
        <div class="card hero">
            <div class="emoji">👻</div>
            <h2>était Mister White</h2>
            <p>Il peut tenter de deviner le mot des civils.</p>
            <form method="post" action="/white-guess">
                <input name="guess" placeholder="Mot des civils" required>
                <button type="submit">Valider</button>
            </form>
        </div>
        """
        return page(content)

    content = f"""
    <div class="tag">ÉLIMINATION</div>
    <h1>{joueur}</h1>
    <div class="card hero">
        <div class="emoji">🚪</div>
        <h2>était {role}</h2>
        <a class="btn" href="/check-end">Continuer</a>
    </div>
    """
    return page(content)


@app.route("/white-guess", methods=["POST"])
def white_guess():
    game = current_game()
    guess = request.form.get("guess", "").strip().lower()
    if guess == game["mot_civil"].lower():
        attribuer_scores("white")
        return redirect(url_for("end", winner="Mister White gagne !", subtitle="Il a deviné le mot des civils."))
    return redirect(url_for("check_end"))


@app.route("/check-end")
def check_end():
    game = current_game()
    civils = game["roles_vivants"].count("Civil")
    undercover = game["roles_vivants"].count("Undercover")
    white = game["roles_vivants"].count("Mister White")

    if undercover == 0 and white == 0:
        attribuer_scores("civils")
        return redirect(url_for("end", winner="Les civils gagnent !", subtitle="Tous les imposteurs ont été éliminés."))

    if undercover + white >= civils:
        attribuer_scores("undercover")
        return redirect(url_for("end", winner="Les imposteurs gagnent !", subtitle="Ils sont devenus aussi nombreux que les civils."))

    game["tour"] += 1
    session["game"] = game
    return redirect(url_for("round_page"))


def attribuer_scores(gagnant):
    game = current_game()
    scores = session.get("scores", {})

    for joueur, role in zip(game["joueurs"], game["roles"]):
        scores.setdefault(joueur, 0)
        if gagnant == "civils" and role == "Civil":
            scores[joueur] += 1
        elif gagnant == "undercover" and role == "Undercover":
            scores[joueur] += 2
        elif gagnant == "white" and role == "Mister White":
            scores[joueur] += 3

    session["scores"] = scores


@app.route("/end")
def end():
    game = current_game()
    winner = request.args.get("winner", "Fin de partie")
    subtitle = request.args.get("subtitle", "")

    rows = ""
    for joueur, role, mot in zip(game["joueurs"], game["roles"], game["mots"]):
        info = "aucun mot" if role == "Mister White" else mot
        rows += f'<div class="list-item">{joueur} • {role} • {info}</div>'

    content = f"""
    <div class="tag">FIN DE PARTIE</div>
    <h1>{winner}</h1>
    <p>{subtitle}</p>
    <div class="card">
        <h2>Révélation</h2>
        {rows}
        <a class="btn btn-green" href="/setup">Rejouer</a>
        <a class="btn btn-secondary" href="/scores">Classement</a>
    </div>
    """
    return page(content)


@app.route("/scores")
def scores():
    scores = session.get("scores", {})
    classement = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    if not classement:
        rows = '<p>Aucun score pour le moment.</p>'
    else:
        rows = ""
        medals = ["🥇", "🥈", "🥉"]
        for i, (joueur, score) in enumerate(classement):
            medal = medals[i] if i < 3 else "🎖️"
            rows += f'<div class="score-row"><span>{medal} {joueur}</span><span>{score} pts</span></div>'

    content = f"""
    <div class="tag">CLASSEMENT</div>
    <h1>Scores</h1>
    <div class="card">
        {rows}
        <a class="btn" href="/setup">Nouvelle partie</a>
        <a class="btn btn-secondary" href="/">Accueil</a>
    </div>
    """
    return page(content)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
