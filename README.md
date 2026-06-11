# 🍽️ Lunch Reservation WebApp (Django)

Application web pour gérer les réservations de repas du midi en entreprise. Les employés réservent leur repas, le personnel CSE visualise les demandes et ajuste les quantités.

**Documentation complète** : 📖 Voir [`wiki/`](wiki/) (en français)

## 🚀 Démarrage rapide

### 1️⃣ Prérequis
- Python 3.11+
- pip / git

### 2️⃣ Installation locale (5 minutes)

```bash
# Cloner le repository
git clone <repo-url>
cd lunch-reservation

# Créer un environnement virtuel
python3 -m venv .venv
source .venv/bin/activate          # Sur Windows: .venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Initialiser la base de données
python manage.py migrate
python manage.py init_db

# Lancer le serveur
python manage.py runserver
```

Ouvrir : http://127.0.0.1:8000/

### 3️⃣ Comptes de test

| Identifiant | Mot de passe | Rôle |
|------------|-------------|------|
| `Z999999` | `password` | Admin |
| _À créer_ | - | Utilisateur standard |

### 4️⃣ Lancer les tests

```bash
python manage.py test
```

## 📚 Documentation

### Pour les utilisateurs finaux
- 👤 **[Guide utilisateur](wiki/User-Guide.md)** — Comment réserver un repas
- 👔 **[Guide staff](wiki/Staff-Guide.md)** — Récapitulatif et gestion des menus

### Pour les administrateurs
- ⚙️ **[Guide d'administration](wiki/05-Administration.md)** — Gestion complète
- 🚀 **[Déploiement](wiki/04-Deployment-Complete.md)** — Production & Vercel
- 🐧 **[Configuration](wiki/Configuration.md)** — Variables d'environnement

### Pour les développeurs
- 💻 **[Guide du développeur](wiki/02-Developer-Guide.md)** — Architecture & code
- 🔌 **[API Reference](wiki/03-API-Reference.md)** — Endpoints JSON
- 🏗️ **[Architecture](wiki/Architecture.md)** — Diagrammes & flux
- 🐛 **[Troubleshooting](wiki/Troubleshooting.md)** — Dépannage

### Démarrage
- 📖 **[Introduction](wiki/01-Introduction.md)** — Vue d'ensemble
- ⚡ **[Getting Started](wiki/Getting-Started.md)** — Détails installation

👉 **Accès complet** : [Wiki complet](wiki/Home.md)

## 🎯 Fonctionnalités principales

### Pour les employés ✅
- ✏️ Se connecter avec identifiant badge (1 lettre + 6 chiffres)
- 📅 Consulter le calendrier mensuel
- 🍽️ Choisir un repas pour chaque jour ouvrable
- 🔒 Modification jusqu'au jour même (dates passées verrouillées)
- ⭐ Noter les repas après consommation
- 💡 Suggérer des améliorations

### Pour le staff (CSE) ✅
- 📊 Voir le récapitulatif mensuel des réservations
- 📝 Définir le menu de la semaine
- 👥 Consulter les suggestions des employés
- 📈 Analyser les tendances de demande
- 👨‍💼 Accès complet à l'administration Django

## 🗂️ Structure du projet

```
lunch-reservation/
├── django_project/                    # Configuration Django
│   ├── settings.py                    # Settings
│   ├── urls.py                        # URLs racine
│   └── wsgi.py
│
├── reservations/                      # Application métier
│   ├── models.py                      # Modèles : Lunch, MealOption, MealRating, etc.
│   ├── views.py                       # Vues : login, calendar, save_lunch, admin, etc.
│   ├── urls.py                        # Routes de l'app
│   ├── forms.py                       # Formulaires : LoginForm, RegisterForm, WeeklyMenuForm
│   ├── admin.py                       # Configuration admin Django
│   ├── templates/                     # Pages HTML (en français)
│   │   ├── base.html                  # Layout de base
│   │   ├── calendar.html              # Calendrier interactif (AJAX)
│   │   ├── admin.html                 # Récapitulatif staff
│   │   └── ...
│   ├── static/
│   │   └── style.css                  # Feuille de styles responsive
│   ├── management/commands/
│   │   └── init_db.py                 # Initialise admin + options
│   └── tests/
│       └── test_views.py              # Tests des vues
│
├── wiki/                              # Documentation (LIRE D'ABORD!)
├── specs/                             # Spécifications des features
├── manage.py                          # Exécutable Django
├── requirements.txt                   # Dépendances
├── db.sqlite3                         # BD locale (générée)
├── vercel.json                        # Config Vercel
└── README.md                          # Ce fichier
```

## 🔐 Modèles de données

### Lunch
Réservation d'un utilisateur pour un jour
```python
user         # FK vers User Django
lunch_date   # DateField
lunch_choice # CharField
# unique_together: (user, lunch_date)
```

### MealOption
Options de repas disponibles
```python
name        # "Poisson", "Végétarien", etc.
is_active   # True/False
order       # Ordre d'affichage
```

### MealRating
Notation d'un repas (1-5 étoiles)
```python
lunch       # OneToOne vers Lunch
rating      # int 1-5
created_at  # Timestamp
```

### DailyMenu
Menu du jour défini par le staff
```python
date        # DateField (unique)
menu        # CharField
```

### Suggestion
Suggestions d'amélioration des utilisateurs
```python
user        # FK vers User
text        # TextField (max 500)
created_at  # Timestamp
is_read     # Boolean
```

Voir [`reservations/models.py`](reservations/models.py) pour le détail complet.

## ⚙️ Configuration

### Variables d'environnement clés

| Variable | Défaut | Production |
|----------|--------|-----------|
| `DEBUG` | `True` | `False` ❌ |
| `SECRET_KEY` | Généré | À définir 🔑 |
| `ALLOWED_HOSTS` | `localhost` | Domaines réels |
| `DATABASE_URL` | SQLite local | PostgreSQL URL |
| `SECURE_SSL_REDIRECT` | `False` | `True` 🔒 |

Voir [Configuration.md](wiki/Configuration.md) pour tous les détails.

## 🚀 Déploiement

### Option 1 : Vercel (recommandé - gratuit)

```bash
# Créer un compte Vercel
# Connecter le GitHub repo
# Vercel crée automatiquement PostgreSQL
# Variables d'environnement via Vercel Dashboard
```

👉 Guide : [Vercel Deployment](wiki/Vercel-Deployment.md)

### Option 2 : Serveur Linux + Gunicorn + Nginx

```bash
pip install gunicorn
gunicorn django_project.wsgi --bind 0.0.0.0:8000 --workers 4
```

👉 Guide : [Deployment](wiki/04-Deployment-Complete.md)

## 🔍 Commandes utiles

```bash
# Appliquer les migrations
python manage.py migrate

# Initialiser la BD (admin + options)
python manage.py init_db

# Lancer le serveur local
python manage.py runserver

# Lancer les tests
python manage.py test

# Accéder au shell Django
python manage.py shell

# Créer un superuser supplémentaire
python manage.py createsuperuser

# Vérifier la config production
python manage.py check --deploy

# Collecter les fichiers statiques
python manage.py collectstatic --no-input
```

## 📋 Routes principales

| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET | Accueil |
| `/login/` | GET/POST | Connexion |
| `/register/` | GET/POST | Inscription |
| `/dashboard/` | GET | Tableau de bord |
| `/calendar/` | GET | Calendrier mensuel |
| `/save-lunch/` | POST | Enregistrer réservation (AJAX) |
| `/admin-summary/` | GET | Récapitulatif (staff) |
| `/weekly-menu/` | GET/POST | Gestion menu (staff) |
| `/suggestions/` | GET | Voir suggestions (staff) |
| `/django-admin/` | GET | Admin Django (superuser) |

Voir [API Reference](wiki/03-API-Reference.md) pour le détail complet.

## 🧪 Tests

```bash
# Lancer tous les tests
python manage.py test

# Test verbose
python manage.py test -v 2

# Un fichier spécifique
python manage.py test reservations.tests.test_views

# Une classe spécifique
python manage.py test reservations.tests.test_views.LoginViewTests
```

## 🐛 Troubleshooting

### Erreur : "No module named django"
```bash
pip install -r requirements.txt
```

### Erreur : "Allowed host not valid"
Ajouter le domaine à `ALLOWED_HOSTS` dans `.env.production`

### BD inaccessible
Vérifier `DATABASE_URL` et permissions PostgreSQL

👉 Voir [Troubleshooting.md](wiki/Troubleshooting.md) pour plus.

## 🔒 Sécurité

✅ **Implémenté :**
- CSRF protection (tokens sur tous les POST)
- Password hashing (bcrypt via Django)
- Session-based authentication
- Dates passées verrouillées côté serveur

⚠️ **À faire en production :**
- `DEBUG=False`
- HTTPS forcé (`SECURE_SSL_REDIRECT=True`)
- Cookies sécurisés (`SESSION_COOKIE_SECURE=True`)
- Clé secrète forte et unique

## 📊 Performance

- **Calendrier** : Une requête BD par mois
- **Save lunch** : Une requête BD + upsert
- **Admin summary** : Une requête BD avec agrégation

Optimisations :
- Pas de N+1 queries (select_related/prefetch_related)
- Indexation BD sur (user, lunch_date)
- Caching optionnel en session

## 📝 Convention de nommage

- Format identifiants : **1 lettre + 6 chiffres** (ex: `K589479`)
- Dates : **ISO 8601** (YYYY-MM-DD)
- Langue interface : **Français** 🇫🇷
- Langue code : **Anglais** 🇬🇧
- Langue commentaires : **Anglais** ou **Français**

## 📞 Support & Documentation

- **Wiki complet** : [wiki/Home.md](wiki/Home.md)
- **Installation** : [wiki/Getting-Started.md](wiki/Getting-Started.md)
- **Déploiement** : [wiki/04-Deployment-Complete.md](wiki/04-Deployment-Complete.md)
- **Dépannage** : [wiki/Troubleshooting.md](wiki/Troubleshooting.md)
- **GitHub** : [Repository](https://github.com/skekcoon/lunch-reservation)

## 👥 Contribution

Les contributions sont les bienvenues ! Pour contribuer :
1. Fork le repository
2. Créer une branche `feature/ma-feature`
3. Commit les changements
4. Push et ouvrir une Pull Request

## 📄 License

[À définir - voir LICENSE.md]

---

**Version** : 1.0  
**Dernière mise à jour** : Juin 2026  
**Statut** : Production-ready ✅

Pour une première utilisation, lire [wiki/Getting-Started.md](wiki/Getting-Started.md) ou [wiki/Introduction](wiki/01-Introduction.md).
