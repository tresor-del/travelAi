import os
import re
import certifi
import airportsdata
import pycountry
from dotenv import load_dotenv
import requests

from .utils import CITY_MAIN_AIRPORT, COUNTRY_ALIASES, COUNTRY_MAIN_AIRPORT

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
DEFAULT_ORIGIN_IATA = os.getenv("DEFAULT_ORIGIN_IATA", "LFW")

BASE_URL = "https://api.aviationstack.com/v1/flights"

AIRPORTS = airportsdata.load("IATA")


def clean_text(text: str) -> str:
    """
    Corriger et exclure les mots inutiles dans un texte
    """
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\sàéèêëîïôûùç]", " ", text)
    text = re.sub(r"\s+", " ", text)
    stop_words = {
        "vol", "vols", "billet", "billets", "voyage", "voyages",
        "plan", "complet", "jours", "jour", "incluant", "inclus", "hotel",
        "hotels", "hôtel", "hôtels", "visite", "visites", "sous", "budget",
        "info", "infos", "information", "informations",
        "le", "la", "les", "un", "une", "des", "ce", "cet", "cette", "ces",
        "de", "du", "en", "au", "aux", "pour", "avec", "par", "dans", "sur",
        "et", "ou", "mais", "donc", "pas", "plus", "à", "a"
    }
    words = [w for w in text.split() if w not in stop_words]
    return " ".join(words).strip()


def country_name_to_code(text: str):
    """
    Convertir le nom d'un pays en son code international à 2 lettres
    Exemple: Togo -> TG
    """
    text = clean_text(text)

    if text in COUNTRY_ALIASES:
        return COUNTRY_ALIASES[text]

    try:
        country = pycountry.countries.lookup(text)
        return country.alpha_2
    except LookupError:
        pass

    for country in pycountry.countries:
        country_name = country.name.lower()
        if country_name in text:
            return country.alpha_2

    for alias, code in COUNTRY_ALIASES.items():
        if alias in text:
            return code

    return None


def airport_country_matches(airport: dict, country_code: str) -> bool:
    """
    Vérifie si un aéroport correspond à un pays.
    """
    airport_country = str(airport.get("country", "")).upper().strip()

    if airport_country == country_code:
        return True

    try:
        country = pycountry.countries.get(alpha_2=country_code)
        if country and airport_country.lower() == country.name.lower():
            return True
    except Exception:
        pass

    return False


def get_best_airport_for_country(country_code: str):
    """
    Trouve le meilleur aéroport d'un pays
    """
    preferred = COUNTRY_MAIN_AIRPORT.get(country_code)

    if preferred and preferred in AIRPORTS:
        return preferred

    candidates = []

    for iata, airport in AIRPORTS.items():
        if not iata:
            continue

        if airport_country_matches(airport, country_code):
            name = str(airport.get("name", "")).lower()
            city = str(airport.get("city", "")).lower()

            score = 0
            if "international" in name:
                score += 50
            if "intl" in name:
                score += 40
            if "capital" in name:
                score += 20
            if city:
                score += 5

            candidates.append((score, iata))

    if not candidates:
        return None

    candidates.sort(reverse=True)
    return candidates[0][1]


def resolve_location_to_iata(location: str):
    """
    Trouve le code IATA d'un aéroport à partir d'un texte libre
    (code IATA, ville ou pays).
    """
    if not location:
        return None

    raw_location = location.strip()

    if re.fullmatch(r"[A-Za-z]{3}", raw_location):
        code = raw_location.upper()
        if code in AIRPORTS:
            return code

    location_clean = clean_text(raw_location)

    if not location_clean:
        return None

    if location_clean in CITY_MAIN_AIRPORT:
        return CITY_MAIN_AIRPORT[location_clean]

    country_code = country_name_to_code(location_clean)
    if country_code:
        airport = get_best_airport_for_country(country_code)
        if airport:
            return airport

    city_matches = []

    for iata, airport in AIRPORTS.items():
        city = str(airport.get("city", "")).lower().strip()
        name = str(airport.get("name", "")).lower().strip()

        score = 0
        if city == location_clean:
            score += 100
        elif location_clean in city:
            score += 70

        if location_clean in name:
            score += 50

        if "international" in name:
            score += 10

        if score > 0:
            city_matches.append((score, iata))

    if city_matches:
        city_matches.sort(reverse=True)
        return city_matches[0][1]

    return None


def find_location_mentions(query: str) -> list:
    """
    Recherche et extrait les noms de pays ou de villes cachés
    à l'intérieur d'une requête écrite en langage naturel.
    """
    q = query.lower()
    mentions = []

    for alias in COUNTRY_ALIASES:
        if re.search(rf"\b{re.escape(alias)}\b", q):
            mentions.append(alias)

    for country in pycountry.countries:
        name = country.name.lower()
        if len(name) >= 4 and re.search(rf"\b{re.escape(name)}\b", q):
            mentions.append(name)

    for city in CITY_MAIN_AIRPORT:
        if re.search(rf"\b{re.escape(city)}\b", q):
            mentions.append(city)

    unique_mentions = []
    for item in mentions:
        if item not in unique_mentions:
            unique_mentions.append(item)

    return unique_mentions


# Expressions de durée à retirer avant le parsing de route, pour éviter
# de confondre "7 jours DE voyage" avec un marqueur de provenance "DE Paris".
_DURATION_PATTERN = re.compile(
    r"\b\d+\s*(?:jours?|jour|nuits?|nuit|semaines?|semaine)\b(?:\s+de\s+(?:voyage|séjour)\b)?",
    re.IGNORECASE,
)


def _strip_duration_phrases(text: str) -> str:
    return _DURATION_PATTERN.sub(" ", text)


def parse_route(query: str):
    """
    Analyse une requête textuelle libre pour en extraire la route de vol.
    Ne devrait servir QUE de filet de sécurité pour du texte libre —
    préférer resolve_route() quand départ/arrivée sont connus explicitement.

    Retourne :
    dep_iata, arr_iata

    Cas de retour possibles :
    - None, None -> Recherche globale
    - DAC, NRT   -> Route précise
    - DAC, None  -> Tous les vols au départ de DAC
    - None, NRT  -> Tous les vols à l'arrivée de NRT
    """
    q = query.strip()
    q_lower = _strip_duration_phrases(q.lower())

    global_keywords = [
        "all country", "all countries", "global flight", "global flights",
        "all flight", "all flights", "worldwide flight", "worldwide flights",
        "tous les pays", "tout pays", "vol mondial", "vols mondiaux",
        "tous les vols", "vol global", "vols globaux", "monde entier"
    ]

    if any(keyword in q_lower for keyword in global_keywords):
        return None, None

    codes = re.findall(r"\b[A-Z]{3}\b", q)
    if len(codes) >= 2:
        return codes[0].upper(), codes[1].upper()

    match = re.search(
        r"\b(?:from|de|depuis)\s+(.+?)\s+\b(?:to|à|a|vers|pour)\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at|par|pour|avec|dans|incluant)\b|[.!?]|$)",
        q_lower,
    )
    if match:
        return resolve_location_to_iata(match.group(1)), resolve_location_to_iata(match.group(2))

    match = re.search(
        r"\b(?:to|à|a|vers|pour)\s+(.+?)\s+\b(?:from|de|depuis)\s+(.+?)(?:\s+(?:on|for|under|including|with|in|at|par|pour|avec|dans|incluant)\b|[.!?]|$)",
        q_lower,
    )
    if match:
        dest_text, origin_text = match.group(1), match.group(2)
        return resolve_location_to_iata(origin_text), resolve_location_to_iata(dest_text)

    match = re.search(r"\b(?:from|de|depuis)\s+(.+?)(?:[.!?]|$)", q_lower)
    if match:
        return resolve_location_to_iata(match.group(1)), None

    match = re.search(r"\b(?:to|à|a|vers|pour)\s+(.+?)(?:[.!?]|$)", q_lower)
    if match:
        return None, resolve_location_to_iata(match.group(1))

    mentions = find_location_mentions(q_lower)
    if len(mentions) >= 2:
        return resolve_location_to_iata(mentions[0]), resolve_location_to_iata(mentions[1])

    if len(mentions) == 1:
        return DEFAULT_ORIGIN_IATA, resolve_location_to_iata(mentions[0])

    return None, None


def resolve_route(departure: str = None, arrival: str = None, query: str = ""):
    """
    Point d'entrée unique pour déterminer dep_iata / arr_iata.

    Priorité :
    1. departure / arrival fournis explicitement (depuis le formulaire) ->
       résolution directe, sans passer par le parsing NLP fragile.
    2. Sinon, retombe sur le parsing de texte libre (parse_route).
    """
    if departure or arrival:
        dep_iata = resolve_location_to_iata(departure) if departure else None
        arr_iata = resolve_location_to_iata(arrival) if arrival else None
        return dep_iata, arr_iata

    return parse_route(query)


def format_flight(flight: dict):
    airline = flight.get("airline", {}).get("name") or "compagnie aérienne inconnu"
    flight_number = flight.get("flight", {}).get("iata") or "Numéro de vol inconnu"
    status = flight.get("flight_status") or "inconnu"

    dep = flight.get("departure", {}) or {}
    arr = flight.get("arrival", {}) or {}

    dep_airport = dep.get("airport") or "aéroport de départ inconnu"
    dep_iata = dep.get("iata") or "inconnu"
    dep_terminal = dep.get("terminal") or "N/A"
    dep_gate = dep.get("gate") or "N/A"
    dep_scheduled = dep.get("scheduled") or "inconnu"
    dep_delay = dep.get("delay")
    dep_delay_text = f"{dep_delay} minutes" if dep_delay is not None else "N/A"

    arr_airport = arr.get("airport") or "aéroport d'arrivé inconnu"
    arr_iata = arr.get("iata") or "inconnu"
    arr_terminal = arr.get("terminal") or "N/A"
    arr_gate = arr.get("gate") or "N/A"
    arr_scheduled = arr.get("scheduled") or "inconnu"
    arr_delay = arr.get("delay")
    arr_delay_text = f"{arr_delay} minutes" if arr_delay is not None else "N/A"

    return f"""
Compagnie aérienne : {airline}
Vol : {flight_number}
Statut : {status}

Départ :
- Aéroport : {dep_airport}
- IATA : {dep_iata}
- Terminal : {dep_terminal}
- Porte : {dep_gate}
- Prévu : {dep_scheduled}
- Retard : {dep_delay_text}

Arrivée :
- Aéroport : {arr_airport}
- IATA : {arr_iata}
- Terminal : {arr_terminal}
- Porte : {arr_gate}
- Prévu : {arr_scheduled}
- Retard : {arr_delay_text}
""".strip()


def _build_route_info(dep_iata, arr_iata):
    if dep_iata and arr_iata:
        return f"Vol en direct de {dep_iata} à {arr_iata}"
    if dep_iata:
        return f"Vol en direct de {dep_iata}"
    if arr_iata:
        return f"Vol en direct à {arr_iata}"
    return "Vols en direct globals"


def search_flights(query: str = "", departure: str = None, arrival: str = None, limit: int = 10):
    """
    Fonction principale pour rechercher les informations de vol.

    - Si `departure` / `arrival` sont fournis (ex: formulaire structuré),
      ils sont utilisés directement, sans parsing NLP.
    - Sinon, `query` est analysée en texte libre via parse_route.
    """
    if not API_KEY:
        return (
            "Flight API error: AVIATIONSTACK_API_KEY is missing.\n"
            "Please add this in your .env file:\n"
            "AVIATIONSTACK_API_KEY=your_api_key_here"
        )

    dep_iata, arr_iata = resolve_route(departure, arrival, query)

    params = {
        "access_key": API_KEY,
        "limit": min(limit, 100),
    }

    if dep_iata:
        params["dep_iata"] = dep_iata

    if arr_iata:
        params["arr_iata"] = arr_iata

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return f"Flight API request failed: {e}"
    except ValueError:
        return "Flight API returned invalid JSON."

    if "error" in data:
        error = data["error"]
        return (
            "Flight API error:\n"
            f"Code: {error.get('code', 'Unknown')}\n"
            f"Message: {error.get('message', 'Unknown error')}"
        )

    flight_data = data.get("data", [])
    route_info = _build_route_info(dep_iata, arr_iata)

    if not flight_data:
        return f"{route_info}\n\nAucun vol trouvé pour cette recherche."

    formatted_flights = [format_flight(flight) for flight in flight_data[:limit]]

    return f"{route_info}\n\n" + "\n\n---\n\n".join(formatted_flights)


if __name__ == "__main__":
    # Test avec champs structurés (comme depuis le formulaire)
    print(search_flights(departure="Lomé", arrival="Paris"))
    print("\n" + "=" * 80 + "\n")
    # Test avec texte libre (fallback)
    print(search_flights(query="Donne moi les informations de vol de tous les pays"))