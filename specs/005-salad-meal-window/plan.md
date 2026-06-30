# Implementation Plan: Option salade avec fenêtre de 48 heures

**Branch**: `005-salad-meal-window` | **Date**: 2026-06-30 | **Spec**: `specs/005-salad-meal-window/spec.md`

**Input**: Feature specification from `/specs/005-salad-meal-window/spec.md`

## Summary

Ajouter des options salade administrables dans le catalogue de repas existant, les rendre réservables uniquement à partir de 2 jours d'avance, afficher clairement en français quand elles ne sont plus disponibles, et continuer à montrer une salade déjà réservée même lorsque la date passe sous le seuil.

## Technical Context

**Language/Version**: Python 3.11 en CI, runtime Python 3.12 sur Vercel  
**Primary Dependencies**: Django 5.2.13, vanilla JavaScript, Bootstrap 5.3.2 via CDN, Python stdlib (`datetime`, `json`, `calendar`)  
**Storage**: SQLite en local (`db.sqlite3`), PostgreSQL en production via `DATABASE_URL`; réutilisation de `MealOption` et `Lunch` sans nouveau schéma requis pour cette fonctionnalité  
**Testing**: `python manage.py check`, `python manage.py test`  
**Target Platform**: Application web Django sur Linux/Vercel  
**Project Type**: Web app  
**Performance Goals**: Conserver un flux calendrier en une page avec le seul POST JSON existant pour l'enregistrement, et garder le calcul de disponibilité borné au petit catalogue d'options actives  
**Constraints**: UI et messages en français, validation serveur obligatoire dans `save_lunch`, aucun build frontend, conservation du garde-fou sur les dates passées, et maintien du flux normal d'annulation/remplacement des réservations existantes  
**Scale/Scope**: Une seule application Django, un calendrier mensuel par utilisateur, un catalogue réduit d'options de repas administrables, et une suite de tests ciblée dans `reservations/tests/test_views.py`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- **Sécurité par défaut**: pass — le flux reste derrière `@login_required`, utilise le POST JSON existant avec CSRF, et ne requiert aucun nouveau secret.
- **Intégrité des données**: pass — la règle des 48 heures reste appliquée côté serveur dans `save_lunch`, les options sont validées via `MealOption` actifs, et l'unicité de `Lunch` ne change pas.
- **Interface minimale et explicite**: pass — la fonctionnalité reste dans des templates Django avec JS vanilla et messages français.
- **Conventions Django**: pass — l'ORM, l'admin Django existant et la commande de gestion `init_db` suffisent; aucun nouveau service ou framework n'est nécessaire.
- **Configuration pilotée par l'environnement**: pass — aucun nouveau paramètre d'environnement ni feature flag n'est introduit.

## Project Structure

### Documentation (this feature)

```text
specs/005-salad-meal-window/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── ui-and-api.md
└── tasks.md
```

### Source Code (repository root)

```text
django_project/
└── urls.py

reservations/
├── admin.py
├── models.py
├── views.py
├── urls.py
├── templates/
│   └── calendar.html
├── management/
│   └── commands/
│       └── init_db.py
└── tests/
    └── test_views.py
```

**Structure Decision**: Garder tout le travail dans l'application Django existante et réutiliser `MealOption.advance_days` comme configuration canonique de disponibilité. Le calendrier et `/save-lunch/` partagent la même règle métier, tandis que l'administration reste portée par `MealOptionAdmin` et la commande `init_db`.

## Phase 0 — Research

- Confirmer que `MealOption.advance_days` est la meilleure source de vérité pour la règle salade.
- Fixer l'interprétation inclusive du seuil comme "2 jours calendaires d'avance" basée sur `localdate()`.
- Définir le comportement UX sous le seuil pour distinguer "plus sélectionnable" de "déjà réservé et encore visible".
- Vérifier que la gestion du catalogue salade peut rester dans l'admin existant sans nouveau parcours.

## Phase 1 — Design & Contracts

- Documenter le rôle de `MealOption.advance_days`, `Lunch` et des états dérivés de disponibilité/calendrier.
- Décrire le contrat UI et endpoint de `/save-lunch/`, y compris l'explication française et la logique d'annulation/remplacement.
- Mettre à jour `.github/copilot-instructions.md` pour pointer vers ce plan.

## Phase 2 — Implementation Outline

1. Garantir la présence des options salade bootstrap avec `advance_days = 2` et exposer le délai d'avance dans l'admin de `MealOption`.
2. Centraliser le calcul d'éligibilité d'une option à partir de `localdate()` et de `advance_days` pour qu'il soit identique dans le rendu calendrier et dans `save_lunch`.
3. Étendre le contexte de `calendar_view` afin de séparer les options disponibles pour une nouvelle sélection, le choix existant à afficher, et le message d'indisponibilité salade.
4. Mettre à jour `calendar.html` pour masquer les salades inéligibles des nouveaux choix, garder visibles les réservations salade existantes, et permettre l'annulation ou le basculement vers un autre repas autorisé.
5. Ajouter des tests de régression couvrant la réservation salade à J+2, le rejet à moins de 2 jours, la visibilité d'une salade déjà réservée, et l'interdiction de re-sélection après annulation sous le seuil.

## Complexity Tracking

Aucune violation de constitution. Aucune complexité supplémentaire à justifier.
