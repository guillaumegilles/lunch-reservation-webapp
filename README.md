# Lunch Reservation WebApp (Django)

Application web simple pour reserver les repas du midi.

Ce guide est ecrit pour un utilisateur debutant.

## 1) Prerequis

Avant de commencer, installe:

- Python 3.11+
- pip
- git

Verifie dans un terminal:

```bash
python3 --version
pip3 --version
git --version
```

## 2) Recuperer le projet

```bash
git clone <repo-url>
cd lunch-reservation-webapp
```

## 3) Installer les dependances

```bash
pip3 install -r requirements.txt
```

Si cette commande echoue, regarde la section "Depannage" plus bas.

## 4) Initialiser la base de donnees

Cette etape cree les tables necessaires dans SQLite.

```bash
python3 manage.py migrate
```

## 5) Creer l'utilisateur admin par defaut

```bash
python3 manage.py init_db
```

## 6) Lancer le serveur

```bash
python3 manage.py runserver 0.0.0.0:8000
```

Puis ouvre ton navigateur sur:

- http://127.0.0.1:8000/

Pour arreter le serveur dans le terminal: `Ctrl + C`

## 7) Connexion admin

Compte admin cree par `init_db`:

- Username: admin
- Password: password

Tu peux aussi creer un compte depuis la page d'inscription.

## Fonctionnement de l'application

Les employes se connectent, choisissent leur repas sur un calendrier mensuel, et peuvent modifier leurs reservations jusqu'au jour meme. Les membres du personnel (CSE) ont acces a un recapitulatif mensuel de toutes les reservations.

**Roles utilisateurs**
- Utilisateur standard : consulte et modifie son propre calendrier.
- Staff (`is_staff=True`) : acces supplementaire au recapitulatif mensuel de tous les employes.

**Flux principal**
1. L'utilisateur se connecte (ou cree un compte).
2. Il arrive sur son calendrier mensuel et clique sur un jour pour choisir son repas parmi les options disponibles.
3. La selection est sauvegardee en AJAX via `POST /save_lunch/` (JSON + CSRF token).
4. Les dates passees sont verrouillees cote serveur.
5. Le staff peut naviguer sur `/admin-summary/` pour voir le tableau recapitulatif mois par mois.

## Organisation des fichiers

```
lunch-reservation/
├── manage.py                        # Point d'entree Django
├── requirements.txt                 # Dependances Python
├── instance/
│   └── lunch.db                     # Base de donnees SQLite (generee)
│
├── lunch_project/                   # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py                      # URLs racine (inclut reservations.urls)
│   ├── wsgi.py
│   └── asgi.py
│
└── reservations/                    # Application principale
    ├── models.py                    # Modele Lunch (user, lunch_date, lunch_choice)
    ├── views.py                     # Toutes les vues + constante LUNCH_OPTIONS
    ├── urls.py                      # Routes de l'app
    ├── forms.py                     # LoginForm, RegisterForm
    ├── admin.py                     # Enregistrement dans l'admin Django
    ├── apps.py
    │
    ├── templates/reservations/      # Templates HTML
    │   ├── base.html                # Layout de base
    │   ├── index.html               # Page d'accueil
    │   ├── login.html
    │   ├── register.html
    │   ├── calendar.html            # Calendrier mensuel (AJAX)
    │   └── admin_summary.html       # Recapitulatif staff
    │
    ├── static/reservations/
    │   └── style.css
    │
    ├── management/commands/
    │   └── init_db.py               # Cree l'utilisateur admin par defaut
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

## Depannage (erreurs frequentes)

### Erreur: "python: can't open file 'manage.py'"

Tu n'es probablement pas dans le bon dossier.

```bash
cd lunch-reservation-webapp
ls
```

Tu dois voir le fichier `manage.py` dans la liste.

### Erreur: "No module named django"

Django n'est pas installe dans l'environnement Python actif.

```bash
pip3 install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```

### Erreur de conflit entre `python3` et `pip3`

Sur certaines machines, `python3` et `pip3` ne pointent pas vers la meme version de Python.

Verifie:

```bash
python3 -c "import sys; print(sys.executable)"
pip3 --version
```

Si besoin, utilise:

```bash
python3 -m pip install -r requirements.txt
python3 manage.py runserver 0.0.0.0:8000
```
