# Architecture technique

## Vue d'ensemble

```text
Navigateur (React / TypeScript / Tailwind)
  ├── Espace visiteur : chat, activités, salles, formulaires
  ├── Espace administration : indicateurs, demandes, conversations, catalogue
  └── i18next : français / anglais / coréen
          │ REST / JSON
          ▼
FastAPI
  ├── /api/chat             orchestration IA + règles métier
  ├── /api/activities       catalogue du Centre
  ├── /api/rooms            espaces et équipements
  ├── /api/requests         création d'une demande
  └── /api/admin/*          pilotage administratif
          │
          ├── SQLite (développement et démo locale)
          └── Snowflake (stockage cible du hackathon)
                  └── Cortex (option IA)
```

## Découpage des responsabilités
- `frontend/src/App.tsx` : shell responsive, vues publiques/admin et flux de formulaires.
- `frontend/src/i18n.ts` : dictionnaires FR/EN/KO et langue active.
- `frontend/src/components/Orb.tsx` : état visuel de Kim (disponible, réflexion, parole).
- `backend/app/main.py` : routes HTTP et validation Pydantic.
- `backend/app/services/assistant.py` : prompt système, contexte factuel, connecteur LLM compatible et réponse de secours.
- `backend/app/db.py` : initialisation SQLite et catalogue local de démonstration.
- `backend/app/services/snowflake_store.py` : connexion Snowflake par variables d'environnement.
- `database/schema.sql` : tables Snowflake et données de démonstration.

## Modèle de données
- `ACTIVITIES` : catalogue, catégorie, critères d'éligibilité, description, places indicatives, activation.
- `ROOMS` : espaces, capacité, équipements, activation.
- `REQUESTS` : identifiant, type (`room`, `activity`, `partnership`, `contact`), payload semi-structuré VARIANT, statut, note administrative, dates.
- `MESSAGES` : session, rôle, contenu, date pour audit et reprise ultérieure.

## Statuts d'une demande
`PENDING` → `IN_REVIEW` → `APPROVED` ou `REJECTED`. `CONTACTED` peut être utilisé lorsque l'équipe a recontacté le demandeur. Aucun statut n'est communiqué comme une confirmation automatique de réservation : la validation reste humaine.

## Sécurité à compléter avant production
- Authentification admin réelle, mots de passe hashés, sessions sécurisées et RBAC.
- Validation stricte des champs par type de demande et contrôle anti-spam / rate limit.
- Journal d'audit des décisions, suppression/export des données personnelles et politique de conservation.
- TLS, secrets dans un coffre, CORS restreint aux domaines de production.
- Filtrage des prompts et minimisation des données personnelles envoyées au fournisseur IA.
