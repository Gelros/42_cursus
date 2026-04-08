import re

# 2. ANATOMIE DE LA REGEX (LE PATTERN) :
# --------------------------------------
# pattern = r"hub:\s+(\w+)\s+(-?\d+)\s+(-?\d+)\s+\[(.*)\]"
#
# r"..."    -> 'Raw string' : traite les backslashes (\) comme du texte normal.
# hub:      -> Cherche exactement la chaîne "hub:".
# \s+       -> Un ou plusieurs espaces (flexible si le fichier est mal aligné).
# (\w+)     -> GROUPE 1 : Capture des lettres/chiffres (le NOM du hub).
# (-?\d+)   -> GROUPE 2 : Capture un nombre (le -? permet de gérer les négatifs).
# (-?\d+)   -> GROUPE 3 : Idem pour la deuxième coordonnée.
# \[        -> Cherche le crochet ouvrant '[' (on l'échappe avec \ car [ est spécial).
# (.*)      -> GROUPE 4 : Capture TOUT ce qu'il y a à l'intérieur.
# \]        -> Cherche le crochet fermant ']'.

DEFAULT_ZONE_TYPE: str = "normal"
DEFAULT_MAX_DRONES: int = 1
DEFAULT_MAX_LINK_CAPACITY: int = 1
VALID_ZONE_TYPES: set[str] = {"normal", "blocked", "restricted", "priority"}


def parse_metadata(raw: str, line_num: int) -> dict[str, str | int]:
    """
    Parse le contenu brut des métadonnées d'une zone ou connexion.

    Args:
        raw: la chaîne brute à l'intérieur des crochets,
             ex: "zone=normal color=blue max_drones=2"
        line_num: numéro de ligne (pour les messages d'erreur)

    Returns:
        Un dictionnaire avec les clés/valeurs parsées et typées.
        ex: {"zone": "normal", "color": "blue", "max_drones": 2}
    """
    ...


def parse_line(line: str) -> dict | None:
    """
    Dispatch : identifie le type de ligne et appelle le bon parser.

    Args:
        line: la ligne (déjà stripped)
        line_num: numéro de ligne pour les erreurs

    Returns:
        Un dictionnaire parsé, ou None si la ligne est vide/commentaire.

    Raises:
        ValueError: si la ligne est invalide ou malformée.
    """
    pattern = r"\s+(\w+)\s+(\d+)\s+(\d+)\s+\[(.*)\]"
    match = re.search(pattern, line)
    try:
        type = line.split(':', 1)[0]
        key = type
    except ValueError as e:
        print(e.errors())
    return {key: 'inc'}


def main():
    res = list()
    with open("./exs/map.txt", 'r', encoding='utf8') as e:
        for line in e:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            res.append(parse_line(line))
    print(res)


if __name__ == "__main__":
    main()
