# Lunch Reservation WebApp (Django)

Application web simple pour réserver les repas du midi.

Ce guide est écrit pour un utilisateur débutant.

## 1) Prérequis

Avant de commencer, installe:

- Python 3.11+
- pip
- git

Vérifie dans un terminal:

```bash
python3 --version
pip3 --version
git --version
```

## 2) Récupérer le projet

```bash
git clone <repo-url>
cd lunch-reservation-webapp
```

## 3) Installer les dépendances

```bash
pip3 install -r requirements.txt
```

Si cette commande échoue, regarde la section "Dépannage" plus bas.

## 4) Initialiser la base de données

Cette étape crée les tables nécessaires dans SQLite.

```bash
python3 manage.py migrate
```

## 5) Créer l'utilisateur admin par défaut

```bash
python3 manage.py init_db
```

## 6) Lancer le serveur

```bash
python3 manage.py runserver 0.0.0.0:8000
```

Puis ouvre ton navigateur sur:

- http://127.0.0.1:8000/

Pour arrêter le serveur dans le terminal: `Ctrl + C`

## 7) Connexion admin

Compte admin créé par `init_db`:

- Username: Z999999
- Password: password

Tu peux aussi créer un compte depuis la page d'inscription.

## Fonctionnement de l'application

Les employés se connectent, choisissent leur repas sur un calendrier mensuel, et peuvent modifier leurs réservations jusqu'au jour même. Les membres du personnel (CSE) ont accès à un récapitulatif mensuel de toutes les réservations.

**Roles utilisateurs**
- Utilisateur standard : consulte et modifie son propre calendrier.
- Staff (`is_staff=True`) : accès supplémentaire au récapitulatif mensuel de tous les employés.

**Flux principal**
1. L'utilisateur se connecte (ou crée un compte).
2. Il arrive sur son calendrier mensuel et clique sur un jour pour choisir son repas parmi les options disponibles.
3. La sélection est sauvegardée en AJAX via `POST /save-lunch/` (JSON + CSRF token).
4. Les dates passées sont verrouillées côté serveur.
5. Le staff peut naviguer sur `/admin-summary/` pour voir le tableau récapitulatif mois par mois.

## Organisation des fichiers

```
lunch-reservation/
├── manage.py                        # Point d'entrée Django
├── requirements.txt                 # Dépendances Python
├── db.sqlite3                       # Base de données SQLite (générée)
│
├── django_project/                  # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py                      # URLs racine (inclut reservations.urls)
│   ├── wsgi.py
│   └── asgi.py
│
└── reservations/                    # Application principale
    ├── models.py                    # Modèle Lunch (user, lunch_date, lunch_choice)
    ├── views.py                     # Toutes les vues + constante LUNCH_OPTIONS
    ├── urls.py                      # Routes de l'app
    ├── forms.py                     # LoginForm, RegisterForm
    ├── admin.py                     # Enregistrement dans l'admin Django
    ├── apps.py
    │
    ├── templates/                   # Templates HTML
    │   ├── base.html                # Layout de base
    │   ├── index.html               # Page d'accueil
    │   ├── login.html
    │   ├── register.html
    │   ├── calendar.html            # Calendrier mensuel (AJAX)
    │   └── admin.html               # Récapitulatif staff
    │
    ├── static/
    │   └── style.css
    │
    ├── management/commands/
    │   └── init_db.py               # Crée l'utilisateur admin par défaut
    │
    ├── migrations/                  # Migrations Django (generees)
    └── tests/
        └── test_views.py
```

## Commandes utiles

Relancer les migrations:

```bash
python3 manage.py migrate
```

Lancer les tests:

```bash
python3 manage.py test
```

## Dépannage (erreurs fréquentes)

### Erreur: "python: can't open file 'manage.py'"

Tu n'es probablement pas dans le bon dossier.

```bash
cd lunch-reservation-webapp
ls
```

Tu dois voir le fichier `manage.py` dans la liste.

### Erreur: "No module named django"

Django n'est pas installé dans l'environnement Python actif.

```bash
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```

### Erreur de conflit entre `python3` et `pip3`

Sur certaines machines, `python3` et `pip3` ne pointent pas vers la même version de Python.

Vérifie:

```bash
python3 -c "import sys; print(sys.executable)"
pip3 --version
```

Si besoin, utilise:

```bash
python3 -m pip install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```
