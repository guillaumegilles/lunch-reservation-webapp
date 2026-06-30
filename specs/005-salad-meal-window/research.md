# Research: Option salade avec fenêtre de 48 heures

**Feature**: `005-salad-meal-window`  
**Phase**: 0 — Research

---

## 1. Modélisation de la règle de disponibilité

### Context

La fonctionnalité doit ajouter une ou plusieurs options salade sans créer un parcours métier séparé du catalogue de repas existant.

### Decision

Réutiliser `MealOption.advance_days` comme source de vérité pour la disponibilité, avec une valeur de `2` pour les options salade et les valeurs existantes conservées pour les autres repas.

### Rationale

Le dépôt possède déjà un catalogue d'options de repas administrable et une validation serveur basée sur les options actives. Réutiliser le délai d'avance par option permet d'appliquer la règle salade sans durcir des noms en code ni introduire un nouveau modèle.

### Alternatives considered

- Coder en dur une liste de noms de salade dans `views.py` : rejeté, car fragile et contraire au catalogue administrable.
- Ajouter un modèle séparé de configuration salade : rejeté, car complexité inutile pour une seule règle de disponibilité.

---

## 2. Interprétation de la fenêtre de 48 heures

### Context

La spécification parle de "48 heures", alors que l'application manipule des dates de déjeuner et non des horaires de service.

### Decision

Interpréter la règle comme un délai minimum inclusif de 2 jours calendaires basé sur `localdate()`, c'est-à-dire qu'une nouvelle réservation salade est autorisée lorsque `lunch_date >= today + 2 jours`.

### Rationale

Cette interprétation correspond aux scénarios d'acceptation donnés (lundi -> mercredi autorisé, vendredi -> lundi autorisé) et reste cohérente avec un domaine métier centré sur des dates entières. Elle évite d'introduire une heure de déjeuner artificielle qui n'existe pas aujourd'hui dans le modèle.

### Alternatives considered

- Comparer des `datetime` précis à l'heure courante : rejeté, car le système ne stocke aucun horaire de repas.
- Utiliser les seuls jours ouvrés dans le calcul : rejeté, car la spécification inclut explicitement le cas vendredi -> lundi.

---

## 3. Comportement UI sous le seuil

### Context

Le calendrier doit empêcher de nouvelles sélections salade pour les dates trop proches tout en gardant lisible une salade déjà enregistrée avant la limite.

### Decision

Filtrer les salades inéligibles de la liste des nouveaux choix, afficher un message explicatif en français quand la date est trop proche, et conserver l'affichage d'une réservation salade existante tant qu'elle n'est pas annulée ou remplacée.

### Rationale

Cette approche couvre simultanément FR-004, FR-005, FR-008, FR-009 et FR-010. Elle évite la confusion d'une option visible mais interdite, tout en préservant la confiance de l'utilisateur dans une réservation déjà validée.

### Alternatives considered

- Afficher la salade désactivée dans le `<select>` : rejeté, car moins clair sur mobile et plus ambigu pour l'utilisateur.
- Bloquer toute modification d'une réservation salade passée sous le seuil : rejeté, car contraire à la possibilité d'annuler ou remplacer la réservation existante.

---

## 4. Administration du catalogue salade

### Context

La fonctionnalité doit continuer à être administrable dans le catalogue existant sans créer un écran dédié.

### Decision

Conserver `MealOption` comme point d'administration unique et exposer le délai d'avance (`advance_days`) dans l'admin existant afin que le personnel puisse activer, désactiver ou ajuster les options salade.

### Rationale

Cela respecte FR-013 et reste aligné avec la convention du projet de préférer les mécanismes Django existants aux solutions personnalisées. Le personnel conserve un seul point de gestion pour le catalogue.

### Alternatives considered

- Ajouter une page d'administration séparée pour les salades : rejeté, car redondant avec `MealOptionAdmin`.
- Déplacer le délai vers une constante de configuration : rejeté, car cela retirerait la souplesse d'administration prévue par le catalogue.
