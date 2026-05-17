# Stack Technique

## Langage et environnement d'exécution

| Couche | Technologie | Version |
|--------|-------------|---------|
| Langage | Python | 3.12 |
| Framework web | Django | ~5.2 |

## Base de données

| Environnement | Moteur | Notes |
|---------------|--------|-------|
| Développement | SQLite | `db.sqlite3` à la racine du projet |
| Production | PostgreSQL | Configuré via la variable d'environnement `DATABASE_URL` avec `dj-database-url` + `psycopg2-binary` |

## Applications et paquets Django clés

| Paquet | Rôle |
|--------|------|
| `django.contrib.auth` | Modèle utilisateur intégré, authentification, gestion des sessions |
| `django.contrib.admin` | Interface d'administration (`/django-admin/`) pour le CRUD des modèles |
| `dj-database-url` | Analyse `DATABASE_URL` pour configurer le backend de base de données |
| `psycopg2-binary` | Adaptateur PostgreSQL pour la production |

## Frontend

- Templates HTML rendus côté serveur (Django Template Language).
- JavaScript vanilla pour le flux AJAX de sauvegarde des déjeuners (`/save-lunch/` — POST JSON avec en-tête `X-CSRFToken`).
- Fichier CSS unique : `reservations/static/style.css`.
- Pas d'outillage de build JS ni de framework frontend.

## Déploiement

| Aspect | Approche |
|--------|----------|
| Plateforme | Vercel (serverless, runtime `python3.12`) |
| Point d'entrée | `django_project/wsgi.py` |
| Fichiers statiques | Collectés dans `staticfiles/` via `collectstatic` lors du build |
| Commande de build | `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput` |
| Secrets | `SECRET_KEY`, `DATABASE_URL`, `DEBUG`, identifiants e-mail via variables d'environnement |

## E-mail

Configurable via variables d'environnement. Par défaut, backend `console` (stdout) en développement.

| Variable | Valeur par défaut |
|----------|-------------------|
| `EMAIL_BACKEND` | `django.core.mail.backends.console.EmailBackend` |
| `EMAIL_HOST` | `localhost` |
| `EMAIL_PORT` | `587` |
| `EMAIL_USE_TLS` | `True` |
| `DEFAULT_FROM_EMAIL` | `noreply@example.com` |
| `SUGGESTION_RECIPIENT_EMAIL` | `admin@example.com` |

## Localisation

- `LANGUAGE_CODE = "fr-fr"`, `TIME_ZONE = "Europe/Paris"`
- Tous les textes d'interface et messages flash sont en français.
