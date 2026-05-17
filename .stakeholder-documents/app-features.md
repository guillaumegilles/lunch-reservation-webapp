# Fonctionnalités de l'application

## Authentification

- **Inscription** — Les employés créent un compte avec un identifiant (leurs matricules : une lettre + 6 chiffres), prénom, nom, numéro de badge du CSE Nouvelle-Aquitaine et mot de passe. Le mot de passe est validé selon les règles intégrées de Django.
- **Connexion / Déconnexion** — Authentification par session. Les utilisateurs non connectés sont redirigés vers la page de connexion.

## Tableau de bord

- Accueil personnalisé par nom après connexion.
- L’utilisateur retrouve sur cette page d’acceuil les dernières informations du CSE ou celles du Chef.
- Liens de navigation vers le calendrier et (pour le personnel CSE) le récapitulatif administrateur.
- **Formulaire de suggestion** — Les employés peuvent soumettre des suggestions libres ; le formulaire envoie une notification par e-mail au destinataire configuré.

## Calendrier de réservation

- Vue mensuelle affichant uniquement les jours ouvrés (lundi–vendredi).
- Chaque jour affiche le **menu du jour** (géré par le personnel ou issu du modèle par défaut selon le jour de la semaine).
- Les employés sélectionnent une **option de repas** par jour parmi la liste gérée par le personnel (enregistrements `MealOption` actifs).
- Les sélections sont sauvegardées via une requête AJAX JSON POST (`/save-lunch/`) ; la page ne se recharge pas.
- Les employés ne peuvent pas modifier des dates passées (contrôle côté serveur retournant HTTP 400).
- Navigation mensuelle (précédent / suivant) via paramètres d'URL.
-  

## Récapitulatif administrateur (Personnel CSE uniquement)

- Tableau mensuel affichant les choix de déjeuner de chaque employé par jour ouvré.
- **Formulaire de gestion des menus hebdomadaires** — Le personnel définit le menu pour chaque jour d'une semaine choisie, stocké sous forme d'enregistrements `DailyMenu` qui remplacent les valeurs par défaut.
- Accès restreint aux utilisateurs avec `is_staff=True` ; les autres sont redirigés avec un message d'erreur.

## Système de suggestions

- Les employés soumettent des suggestions depuis le tableau de bord.
- La soumission déclenche un e-mail à l'adresse définie dans `SUGGESTION_RECIPIENT_EMAIL`.
- Des messages flash confirment le succès ou signalent les erreurs d'envoi.

## Administration Django (`/django-admin/`)

- CRUD complet pour les modèles `MealOption`, `DailyMenu`, `Lunch` et `Suggestion`.
- Utilisé par le personnel pour gérer les options de repas et consulter les suggestions.
