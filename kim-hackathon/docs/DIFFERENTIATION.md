# Le surplus KIM — ce qui le distingue des chatbots génériques

Le hackathon attend un chatbot trilingue, les demandes de salles, les pré-inscriptions, les partenariats et un dashboard. Ces éléments constituent le socle, pas la différenciation. KIM ajoute une logique de service fiable et une expérience plus proche d'un véritable guichet numérique.

## 1. Le « zéro fausse confirmation »
Un assistant classique peut donner l'impression qu'une réservation est faite. KIM sépare clairement trois étapes :
1. **Préparer** : l'assistant collecte les informations utiles dans le langage naturel.
2. **Transmettre** : le backend enregistre un dossier structuré et retourne une référence traçable.
3. **Décider** : un agent du Centre valide, refuse ou reprend contact depuis le dashboard.

L'interface rappelle cette règle au moment où elle compte : avant l'envoi, après l'envoi et dans le panneau de traitement.

## 2. Réponses avec provenance et abstention utile
- Les réponses factuelles sont accompagnées d'une source issue du catalogue ou de la base du Centre.
- Les horaires, coordonnées ou disponibilités non vérifiés ne sont pas inventés.
- Quand la donnée manque, KIM le dit et propose un chemin humain plutôt qu'une réponse plausible mais fausse.
- Le catalogue porte un indicateur « données de démonstration » tant que le Centre ne l'a pas validé.

## 3. Un guichet multilingue cohérent, pas seulement une traduction du chatbot
Le français, l'anglais et le coréen couvrent aussi les libellés, formulaires, statuts, actions et navigation. La langue sélectionnée est transmise au backend afin que l'assistant réponde dans la même langue.

## 4. Une demande structurée depuis la conversation
La conversation n'est pas une impasse : les raccourcis ouvrent un formulaire pré-structuré. Les champs sont validés, la demande est enregistrée, un identifiant est renvoyé et le dossier apparaît dans le tableau de bord.

## 5. Expérience soignée et accessible
- Interface responsive pensée pour mobile et desktop.
- Typographie Geist, icônes Remix Icon et composants simples, cohérents et réutilisables.
- Orb d'état de l'assistant inspiré de la communauté 21st.dev, sans animation décorative agressive.
- États vides, états de chargement, erreurs de connexion et confirmation d'envoi.

## 6. Une démo transparente
Le prototype fonctionne localement avec SQLite pour éviter qu'un souci de configuration Snowflake bloque la présentation. Le mode Snowflake est disponible et le script SQL est livré. Le README indique explicitement ce qui est connecté et ce qui reste à configurer : cette transparence est préférable à une intégration Snowflake fictive.

## Pitch différenciant
« KIM ne se contente pas de répondre. Il transforme une question en démarche structurée, traçable et transmise au bon service — sans jamais prendre une décision à la place du Centre. »

## Suite produit crédible
- Reprise de conversation par un agent humain avec transfert de contexte.
- Disponibilité des salles calculée sur un planning réel, avec conflits de créneaux.
- Notifications email/SMS à chaque changement de statut.
- Gestion de contenu admin complète pour activités, salles et horaires.
- Recherche sémantique Cortex sur les documents institutionnels validés.
- Authentification et permissions par rôle, journal d'audit et consentement RGPD / loi locale applicable.
