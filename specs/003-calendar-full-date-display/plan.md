# Implementation Plan: Affichage de la date complète dans le calendrier

**Branch**: `003-calendar-full-date-display` | **Date**: 2026-06-03 | **Spec**: `specs/003-calendar-full-date-display/spec.md`

**Input**: Feature specification from `/specs/003-calendar-full-date-display/spec.md`

## Summary

Afficher dans le calendrier une date complète en français pour chaque jour ouvrable, puis normaliser tous les textes visibles de l'application en français. Les libellés de jour et de mois seront générés côté serveur avec des tables explicites plutôt qu'avec la locale système, afin d'obtenir un rendu stable quel que soit l'environnement de déploiement.

## Technical Context

**Language/Version**: Python 3.12  
**Primary Dependencies**: Django 5.2.13, standard library (`datetime`, `calendar`), vanilla JavaScript, Bootstrap 5.3.2 via CDN  
**Storage**: SQLite en local (`db.sqlite3`), PostgreSQL en production via `DATABASE_URL`  
**Testing**: `python manage.py test`  
**Target Platform**: Application web Django sur Linux/Vercel  
**Project Type**: Web app  
**Performance Goals**: Conserver les temps de rendu actuels; aucun aller-retour supplémentaire côté client pour les libellés de date  
**Constraints**: Aucun changement de schéma BDD; aucun build frontend; tout texte visible doit rester en français; conserver CSRF/auth/contrôle staff  
**Scale/Scope**: Petit périmètre fonctionnel centré sur les vues `index`, `login`, `register`, `dashboard`, `calendar` et `admin_summary`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Sécurité par défaut**: conforme — pas de nouveaux flux d'authentification, CSRF inchangé, pas de secret ajouté.
- **Intégrité des données**: conforme — aucun changement de modèle; la logique serveur de réservation reste inchangée.
- **Interface minimale et explicite**: conforme — templates Django + JS vanilla, aucun outil de build.
- **Conventions Django**: conforme — changements limités aux vues, templates et constantes d'affichage.
- **Configuration pilotée par l'environnement**: conforme — aucun paramètre d'environnement ajouté.

## Project Structure

### Documentation (this feature)

```text
specs/003-calendar-full-date-display/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/
    └── ui-and-endpoint.md
```

### Source Code (repository root)

```text
django_project/
└── urls.py

reservations/
├── views.py
├── urls.py
├── models.py
├── forms.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── calendar.html
│   └── admin.html
└── static/
    └── custom.css
```

**Structure Decision**: La fonctionnalité reste dans l'application Django existante; la logique de formatage des dates vit dans `reservations/views.py`, les textes statiques sont normalisés dans les templates, et `custom.css` n'est modifié que si le texte complet nécessite un ajustement de hauteur ou d'espacement.

## Phase 0 — Research

- Confirmer la stratégie de formatage française indépendante de la locale système.
- Garder la logique côté serveur pour tous les mois et jours affichés.
- Vérifier qu'aucune clarification supplémentaire n'est nécessaire.

## Phase 1 — Design & Contracts

- Définir les modèles de vue pour les jours du calendrier et le récapitulatif mensuel.
- Documenter le contrat de l'interface UI et du endpoint JSON `/save-lunch/`.
- Mettre à jour `.github/copilot-instructions.md` pour pointer vers ce plan.

## Phase 2 — Implementation Outline

1. Ajouter des libellés français explicites pour les jours et les mois dans `reservations/views.py`.
2. Transmettre au template calendrier la date complète formatée (`Lundi 14 juin`) et `month_name_fr` pour le titre visible du calendrier.
3. Utiliser `month_name_fr` aussi pour le titre visible de `admin.html` afin que le récapitulatif mensuel affiche le mois en français dans le `<h3>` et le `<title>`.
4. Remplacer les chaînes anglaises restantes dans `base.html`, `calendar.html`, `admin.html`, `index.html`, `login.html`, `register.html`, `dashboard.html`.
5. Ajuster le JS du calendrier pour afficher la date complète au lieu du seul numéro.
6. Vérifier visuellement qu'aucune chaîne anglaise n'apparaît sur les pages concernées.

## Complexity Tracking

Aucune violation de constitution. Aucune complexité supplémentaire à justifier.
