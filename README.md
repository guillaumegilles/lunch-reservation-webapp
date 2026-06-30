# Lunch Reservation

Application Django de réservation de repas en entreprise.

## Ce que fait l'application

- création de compte avec identifiant au format `1 lettre + 6 chiffres`
- connexion par session Django
- calendrier mensuel utilisateur sur jours ouvrés
- réservation et annulation de repas
- délai minimal configurable par option de repas
- notation des repas passés sur 5 étoiles
- récapitulatif mensuel staff avec moyennes de notes
- saisie hebdomadaire des menus
- suggestions utilisateur stockées en base et envoyées par e-mail si le SMTP est configuré

## Démarrage rapide

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py init_db
python manage.py runserver
```

Application : `http://127.0.0.1:8000/`

Admin Django : `http://127.0.0.1:8000/django-admin/`

Compte initial créé par `init_db` :

- identifiant : `Z999999`
- mot de passe : `password`

## Commandes utiles

```bash
python manage.py check
python manage.py test
python manage.py seed_june_menus
python manage.py collectstatic --no-input
```

## Stack

- Python 3.11+
- Django 5.2
- SQLite en local
- PostgreSQL si `DATABASE_URL` est défini
- Bootstrap 5 + JavaScript vanilla

## Documentation

La documentation complète se trouve dans [`wiki/`](wiki/).

### Démarrage

- [Accueil wiki](wiki/Home.md)
- [Introduction](wiki/01-Introduction.md)
- [Getting Started](wiki/Getting-Started.md)
- [Référence rapide](wiki/06-Quick-Reference.md)

### Utilisation

- [Guide utilisateur](wiki/User-Guide.md)
- [Guide staff](wiki/Staff-Guide.md)

### Développement et exploitation

- [Guide du développeur](wiki/02-Developer-Guide.md)
- [API Reference](wiki/03-API-Reference.md)
- [Configuration](wiki/Configuration.md)
- [Deployment](wiki/04-Deployment-Complete.md)
- [Troubleshooting](wiki/Troubleshooting.md)

## Arborescence principale

```text
django_project/   configuration Django
reservations/     application métier unique
wiki/             documentation
specs/            specs et plans de fonctionnalités
```

## Tests

```bash
python manage.py test
```
