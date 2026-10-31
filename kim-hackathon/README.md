# KIM — Assistant d'orientation du Centre Ivoiro-Coréen

Application web full-stack pour le hackathon **Hack for Humanity**.

## Ce que contient le projet
- Frontend React + TypeScript + Vite + Tailwind CSS, police Geist, icônes Remix Icon.
- Interface visiteur : assistant conversationnel, réponses sourcées, raccourcis vers les services, formulaires guidés pour salles, activités et partenariats.
- Interface administration : tableau de bord, traitement des demandes, conversations à reprendre, gestion du catalogue et des salles.
- Backend FastAPI : API REST, validation des données, orchestration IA, persistance Snowflake et mode local SQLite pour démarrer sans identifiants Snowflake.
- i18n FR / EN / KO avec détection et changement de langue.
- Composant Orb inspiré du composant communautaire 21st.dev (état de l'assistant), adapté à l'identité visuelle KIM.

## Démarrage rapide

### 1. Backend
```bash
cd backend
python -m venv .venv
# Windows PowerShell : .venv\Scripts\Activate.ps1
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```
API : http://localhost:8000 — documentation interactive : http://localhost:8000/docs

Par défaut `STORAGE_MODE=sqlite` pour que la démo soit immédiatement exécutable. Pour Snowflake, renseigner les variables `SNOWFLAKE_*`, exécuter `database/schema.sql`, puis passer `STORAGE_MODE=snowflake`.

### 2. Frontend
Dans un autre terminal :
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```
Ouvrir l'URL affichée par Vite (généralement http://localhost:5173).

## IA et clé fournie
Le fichier de jeton transmis ressemble à un jeton JWT signé émis par Snowflake (`iss: SF:2008`) et non à une clé API LLM générique. Il n'est donc pas injecté aveuglément dans un fournisseur IA. Le backend accepte :
- **Snowflake Cortex** via `AI_PROVIDER=cortex` et une connexion Snowflake configurée ;
- **API compatible OpenAI** via `AI_PROVIDER=openai_compatible`, `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`.

Placez vos secrets dans `backend/.env` uniquement. Ne commitez jamais `.env`, de jeton JWT ou de clé API. Le jeton fourni n'est pas copié dans l'archive.

## Règles métier non négociables
1. KIM informe, prépare et transmet. Il ne confirme jamais une réservation ni une inscription.
2. Toute demande est enregistrée avec le statut `PENDING` et attend une validation humaine.
3. Une disponibilité de salle est indicative tant que l'équipe du Centre ne l'a pas confirmée.
4. Les réponses factuelles doivent citer une source provenant des données du Centre. En l'absence de source, KIM doit le dire clairement et proposer un relais humain.
5. Le catalogue initial contient au moins cinq activités de démonstration clairement marquées comme données de démonstration.

## Comptes de démonstration
Le dashboard admin est ouvert en mode hackathon pour faciliter la démonstration. Ce n'est **pas** une authentification de production. Avant déploiement réel, ajouter une authentification (OAuth/JWT), RBAC, audit des actions, rate limiting et gestion sécurisée des sessions.

## Scripts utiles
- `database/schema.sql` : tables Snowflake et données de départ.
- `backend/app/main.py` : entrée FastAPI.
- `backend/app/services/assistant.py` : orchestration des réponses IA et règles anti-hallucination.
- `docs/ARCHITECTURE.md` : architecture et flux.
- `docs/DEMO.md` : scénario de démonstration jury.
- `docs/DIFFERENTIATION.md` : surplus produit pour se démarquer.

## Limites honnêtes du prototype
Le mode SQLite permet une démo complète locale. Le connecteur Snowflake est implémenté côté backend mais nécessite les identifiants du compte de l'équipe et l'exécution du schéma SQL. L'IA est facultative : sans fournisseur configuré, KIM utilise un moteur de réponses de secours fondé sur le catalogue local et indique les sources disponibles. Les horaires et exemples ne doivent pas être présentés comme des informations officielles tant qu'ils n'ont pas été vérifiés avec le Centre.
