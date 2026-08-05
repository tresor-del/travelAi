# TravalAI

TravalAI est un assistant de planification de voyage basé sur l'IA. Il utilise FastAPI pour l'interface web, LangGraph pour orchestrer des agents de voyage, Groq pour le modèle LLM, Tavily pour la recherche d'hôtels et AviationStack pour trouver des vols.

## Fonctionnalités

- Interface web de planification de voyage avec FastAPI
- Recherche de vols via un outil dédié
- Recherche d'hôtels via Tavily
- Génération d'un itinéraire de voyage complet
- Téléchargement PDF du plan de voyage
- Gestion de sessions avec `thread_id`

## Structure du projet

- `app.py` : point d'entrée FastAPI, routes web et API
- `backend.py` : logique des agents de voyage, orchestration LangGraph
- `tools/flight_tool.py` : résolution de lieux et recherche de vols
- `tools/tavily_tool.py` : intégration Tavily pour la recherche d'hôtels
- `tools/utils.py` : utilitaires pour la conversion de pays / villes et IATA
- `templates/index.html` : interface utilisateur principale
- `static/` : CSS et JavaScript front-end
- `tests/` : tests unitaires

## Prérequis

- Python 3.11+
- Virtualenv ou environnement Python isolé
- Clés API pour :
  - `GROQ_API_KEY`
  - `AVIATIONSTACK_API_KEY`
- Base de données PostgreSQL

## Installation

1. Copier le projet localement
2. Créer et activer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Installer les dépendances

```bash
pip install -r requirements.txt
```

4. Créer un fichier `.env` à la racine du projet avec les variables suivantes :

```env
GROQ_API_KEY=your_groq_api_key
AVIATIONSTACK_API_KEY=your_aviationstack_api_key
DATABASE_URL=postgresql://user:password@host:port/dbname
DEFAULT_ORIGIN_IATA=LFW
```

> `DEFAULT_ORIGIN_IATA` est optionnel. Il est utilisé comme aéroport d'origine par défaut.

## Lancement

Lancer l'application avec Uvicorn :

```bash
uvicorn app:app --reload
```

Puis ouvrir `http://127.0.0.1:8000` dans votre navigateur.

## API

### POST `/api/travel`

Envoie une requête de voyage structurée.

Exemple de payload :

```json
{
  "departure": "Lomé",
  "arrival": "Paris",
  "days": 7,
  "details": "Voyage économique avec visites culturelles",
  "thread_id": null
}
```

Réponse attendue :

- `success`: booléen
- `thread_id`: identifiant de conversation
- `answer`: réponse générée par l'IA
- `flight_results`: informations de vol
- `hotel_results`: résultats d'hôtels
- `itinerary`: itinéraire de voyage
- `llm_calls`: nombre d'appels LLM réalisés

### GET `/health`

Point de santé de l'API retournant l'état du service.

## Tests

Exécuter les tests avec `pytest` :

```bash
pytest
```

## Développement

- Modifier `templates/index.html` pour changer l'interface utilisateur
- Mettre à jour `static/script.js` pour le comportement front-end
- Étendre `backend.py` pour ajouter de nouveaux agents de planification

## Notes techniques

- `backend.py` utilise `langgraph.graph.StateGraph` pour orchestrer les étapes : `flight_agent`, `hotel_agent`, `itinerary_agent`, `final_agent`
- `flight_tool.py` résout les textes de localisation en codes IATA et interroge AviationStack
- `tavily_tool.py` effectue une recherche de résultats sur Tavily et retourne un résumé formaté

