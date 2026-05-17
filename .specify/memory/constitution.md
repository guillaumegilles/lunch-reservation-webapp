<!--
Sync Impact Report
==================
Version change: 1.0.0 → 1.0.1
Modified principles: Traduction intégrale en français — aucun changement sémantique
Added sections: Aucune
Removed sections: Aucune
Templates requiring updates:
  - .specify/templates/plan-template.md ✅ Aucune mise à jour requise
  - .specify/templates/spec-template.md ✅ Aucune mise à jour requise
  - .specify/templates/tasks-template.md ✅ Aucune mise à jour requise
Follow-up TODOs: Aucun
-->

# Constitution — Réservation de déjeuner

## Principes fondamentaux

### I. Sécurité par défaut

- Les jetons CSRF DOIVENT être envoyés sur tous les appels AJAX non-GET via l'en-tête
  `X-CSRFToken`.
- Tous les secrets (`SECRET_KEY`, `DATABASE_URL`, identifiants e-mail) DOIVENT être
  fournis via des variables d'environnement ; aucun secret NE DOIT apparaître dans le
  code source ou le contrôle de version.
- Chaque vue nécessitant une authentification DOIT être décorée avec `@login_required` ;
  chaque vue réservée au personnel DOIT vérifier `request.user.is_staff` et rediriger
  avec un message d'erreur si la vérification échoue.
- `DEBUG` DOIT être `False` en production ; cela DOIT être appliqué via la variable
  d'environnement `DEBUG`.
- La validation côté serveur DOIT rejeter les entrées invalides ou non autorisées avec
  des codes de statut HTTP explicites (400 pour les requêtes incorrectes, 403 pour les
  accès non autorisés).

**Justification** : L'application gère les données de planning des employés et les
récapitulatifs réservés au personnel. Une authentification faible ou des secrets
exposés compromettraient la vie privée des employés et les données opérationnelles
internes.

### II. Intégrité des données au niveau de la base de données

- Toutes les règles métier DOIVENT être appliquées côté serveur ; les contrôles côté
  client sont complémentaires uniquement et NE DOIVENT PAS constituer le seul garde-fou.
- Le rejet des réservations pour des dates passées DOIT être appliqué dans la vue
  `save_lunch` et retourner HTTP 400 avec un corps d'erreur JSON.
- Les upserts de déjeuner DOIVENT utiliser `Lunch.objects.update_or_create(user=...,
  lunch_date=..., defaults={...})` pour éviter les doublons de réservation pour le même
  utilisateur et la même date.
- La contrainte d'unicité `(user, lunch_date)` DOIT être maintenue au niveau du modèle
  Django ORM et répercutée dans les migrations.
- Toutes les valeurs de choix fournies par l'utilisateur (ex. : options de repas) DOIVENT
  être validées par rapport à la liste canonique `LUNCH_OPTIONS` avant persistance ;
  les valeurs inconnues DOIVENT être rejetées.

**Justification** : Les données de réservation alimentent les prévisions de restauration ;
les doublons ou les choix invalides entraîneraient des erreurs d'approvisionnement réelles
pour la cuisine ou le traiteur.

### III. Interface minimale et explicite

- Tout le HTML DOIT être rendu côté serveur en utilisant le Django Template Language ;
  aucun framework frontend (React, Vue, etc.) n'est autorisé.
- JavaScript DOIT rester vanilla ; aucun pipeline de build npm, bundler ou transpileur
  n'est autorisé.
- Les appels AJAX DOIVENT utiliser un POST JSON vers `/save-lunch/` avec un en-tête
  `X-CSRFToken` ; les réponses du serveur DOIVENT être en JSON.
- Une seule feuille de styles (`reservations/static/style.css`) DOIT contenir tous les
  styles ; les attributs `style` en ligne dans les templates NE DOIVENT PAS être utilisés.
- Tous les textes d'interface et messages flash DOIVENT être rédigés en français en
  utilisant le framework `messages` de Django (`messages.success` / `messages.error`).

**Justification** : L'application cible un environnement de bureau interne unique. Maintenir
le frontend minimal réduit la charge de maintenance, élimine les outils de build et assure
un déploiement serverless Vercel simple.

### IV. Conventions Django plutôt que solutions personnalisées

- Le modèle `User` intégré de Django (`django.contrib.auth`) DOIT être utilisé pour toute
  authentification et gestion des utilisateurs ; les modèles utilisateur personnalisés sont
  interdits.
- `is_staff=True` DOIT être le seul mécanisme accordant l'accès administrateur/personnel
  CSE ; aucun système de rôles ou de permissions parallèle NE DOIT être introduit.
- Tout accès à la base de données DOIT passer par l'ORM Django ; le SQL brut est interdit
  sauf si strictement nécessaire et explicitement documenté avec un commentaire de
  justification.
- Les patterns d'URL au niveau de l'application DOIVENT résider dans `reservations/urls.py` ;
  le fichier `django_project/urls.py` au niveau projet DOIT uniquement inclure/déléguer
  vers les URLs de l'application.
- Toute initialisation et alimentation de la base de données DOIT être implémentée comme
  des commandes de gestion Django (ex. : `python manage.py init_db`) ; les scripts ad hoc
  à la racine du projet sont interdits.

**Justification** : Suivre les conventions Django maintient la base de code accessible à
tout développeur familier avec Django, réduit le temps d'intégration et exploite la
sécurité intégrée éprouvée.

### V. Configuration pilotée par l'environnement

- `SECRET_KEY`, `DEBUG`, `DATABASE_URL` et tous les paramètres liés à l'e-mail DOIVENT
  être fournis via des variables d'environnement ; les valeurs par défaut dans `settings.py`
  DOIVENT être sûres pour le développement uniquement (ex. : backend e-mail `console`,
  chemin SQLite).
- Le développement local DOIT fonctionner immédiatement avec SQLite (`db.sqlite3` à la
  racine du projet) ; la production DOIT utiliser PostgreSQL configuré via la variable
  d'environnement `DATABASE_URL` analysée par `dj-database-url`.
- Les déploiements Vercel DOIVENT utiliser le runtime `python3.12` ; la commande de build
  DOIT être : `pip install -r requirements.txt && python manage.py migrate &&
  python manage.py collectstatic --noinput`.
- Aucun feature flag ou basculement d'environnement NE DOIT être implémenté au-delà de
  `DEBUG` et des paramètres Django standard pilotés par des variables d'environnement.

**Justification** : La séparation nette entre configuration et code prévient l'exposition
accidentelle de secrets, permet des builds reproductibles et supporte la stratégie duale
SQLite/PostgreSQL sans modification du code.

## Standards de déploiement et d'environnement

- Les fichiers statiques DOIVENT être collectés dans `staticfiles/` via `collectstatic`
  lors de l'étape de build Vercel ; `reservations/static/` NE DOIT PAS être servi
  directement en production.
- Les migrations DOIVENT être appliquées lors de l'étape de build du déploiement
  (`manage.py migrate`), et non manuellement après le déploiement.
- Le point d'entrée WSGI DOIT rester `django_project/wsgi.py` ; il NE DOIT PAS être
  renommé ou déplacé.
- `SUGGESTION_RECIPIENT_EMAIL` DOIT être configuré via une variable d'environnement ;
  aucune adresse de repli codée en dur NE DOIT apparaître dans le code source.
- `EMAIL_BACKEND` DOIT utiliser par défaut `django.core.mail.backends.console.EmailBackend`
  en développement et DOIT être remplacé via une variable d'environnement en production.

## Critères de qualité du code

- Chaque vue DOIT gérer explicitement tous les cas d'erreur documentés et retourner le
  code de statut HTTP approprié ; les échecs silencieux sont interdits.
- Les vérifications d'authentification et de permissions DOIVENT apparaître en début de
  chaque fonction de vue, avant toute logique métier ou accès à la base de données.
- Les nouvelles dépendances Python DOIVENT être ajoutées à `requirements.txt` avec une
  version fixée ou contrainte ; les dépendances avec version générique non contrainte
  sont interdites.
- Les pull requests DOIVENT être revues pour la conformité aux cinq principes fondamentaux
  avant fusion ; toute violation DOIT être résolue, non différée.
- Les ajouts de complexité (nouveaux packages tiers, applications Django ou patterns
  architecturaux) DOIVENT être justifiés par rapport à la stack existante dans la
  description de la PR.
- Les constantes d'options de repas DOIVENT être gérées exclusivement via la liste
  `LUNCH_OPTIONS` dans `reservations/views.py` ; les chaînes d'options codées en dur
  dispersées dans les vues ou les templates sont interdites.

## Gouvernance

Cette constitution prime sur toutes les autres pratiques implicites du projet Réservation
de déjeuner. Toute modification requiert :

1. Une justification documentée expliquant pourquoi le principe actuel est insuffisant.
2. Un plan de migration pour tout code existant qui violerait le nouveau principe.
3. Un incrément de version suivant le versionnage sémantique :
   - **MAJEURE** : Suppression ou redéfinition d'un principe de manière incompatible.
   - **MINEURE** : Ajout d'un nouveau principe ou extension significative d'un principe
     existant.
   - **CORRECTIVE** : Clarifications, corrections de formulation ou ajustements non
     sémantiques.
4. Mise à jour de `LAST_AMENDED_DATE` à la date de modification.

Toutes les revues de code DOIVENT vérifier la conformité à ces principes. La complexité
DOIT être justifiée ; en cas de doute, préférer la solution la plus simple qui respecte
les conventions Django existantes.

Se référer au `README.md` du projet et à `COPILOT-INSTRUCTIONS.md` pour les conseils de
développement au quotidien.

**Version** : 1.0.1 | **Ratifiée** : 2026-05-17 | **Dernière modification** : 2026-05-17
