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
