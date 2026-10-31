# Activer Snowflake et Cortex

1. Créer/activer le compte Snowflake du programme partenaire du hackathon.
2. Exécuter `database/schema.sql` dans un worksheet Snowflake.
3. Copier `backend/.env.example` vers `backend/.env` et renseigner le compte, utilisateur, mot de passe, entrepôt, base et schéma.
4. Passer `STORAGE_MODE=snowflake`.
5. Pour l'IA Cortex, passer `AI_PROVIDER=cortex`, choisir un modèle autorisé dans `CORTEX_MODEL` (ex. `mistral-large2`) et vérifier que le rôle possède les privilèges Cortex requis.
6. Relancer FastAPI.

Le backend interroge le catalogue et les salles dans Snowflake, écrit les demandes dans `REQUESTS` et utilise `SNOWFLAKE.CORTEX.COMPLETE` si Cortex est activé.

## À propos du jeton transmis
Le fichier fourni contient un JWT dont les claims visibles indiquent un émetteur `SF:2008`. Cela ne correspond pas au format d'une clé API LLM générique. Il n'est donc pas traité comme une clé OpenAI ou envoyé à un endpoint tiers. Configurez l'authentification Snowflake standard du compte (ou un mécanisme de clé privée pris en charge) via les variables d'environnement. Ne partagez pas le jeton dans le dépôt Git.
