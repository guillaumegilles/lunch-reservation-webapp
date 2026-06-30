# Data Model: Option salade avec fenêtre de 48 heures

**Feature**: `005-salad-meal-window`  
**Phase**: 1 — Design

---

## Entity 1 — `MealOption` (existing)

Représente une option de repas sélectionnable dans le calendrier.

| Field | Type | Description |
|------|------|-------------|
| `name` | String | Libellé affiché à l'utilisateur |
| `is_active` | Boolean | Indique si l'option peut être proposée pour de nouvelles réservations |
| `order` | Integer | Ordre d'affichage et priorité de fallback |
| `advance_days` | Integer | Délai minimum de réservation, en jours calendaires, pour cette option |

### Rules

- Les options actives alimentent le sélecteur de repas.
- Les options salade implémentées par cette feature portent `advance_days = 2`.
- Les autres repas conservent leur valeur actuelle de `advance_days`.
- Une option inactive n'est jamais proposée pour une nouvelle réservation, même si elle existait auparavant dans le catalogue.

### Relationships

- Utilisée à la fois par le rendu du calendrier et par la validation serveur de `/save-lunch/`.
- Administrée via le catalogue Django existant (`MealOptionAdmin`) et initialisée par `init_db`.

---

## Entity 2 — `Lunch` (existing)

Représente la réservation d'un utilisateur pour une date donnée.

| Field | Type | Description |
|------|------|-------------|
| `user` | User | Propriétaire de la réservation |
| `lunch_date` | Date | Date de déjeuner réservée |
| `lunch_choice` | String | Nom de l'option de repas choisie |

### Rules

- Un utilisateur ne peut avoir qu'une réservation par date (`unique_together`).
- Une réservation existante reste visible dans le calendrier même si son option n'est plus éligible pour une nouvelle sélection à la date courante.
- Une réservation existante peut être annulée ou remplacée via le flux habituel tant que la nouvelle option choisie respecte sa propre règle de délai.

---

## Derived Rule — `MealAvailability`

Règle calculée au runtime pour décider si une option donnée peut encore être choisie pour une date de déjeuner.

| Field | Type | Description |
|------|------|-------------|
| `option_name` | String | Option évaluée |
| `lunch_date` | Date | Date ciblée par la réservation |
| `today` | Date | Date locale renvoyée par `localdate()` |
| `advance_days` | Integer | Délai minimum requis pour l'option |
| `is_selectable` | Boolean | Résultat d'éligibilité pour une nouvelle sélection |
| `message` | String or null | Message de refus ou d'aide en français si l'option n'est pas disponible |

### Rules

- `is_selectable` vaut `True` si `lunch_date >= today + timedelta(days=advance_days)`.
- L'égalité au seuil est autorisée.
- Une salade supprimée alors que la date est déjà sous le seuil redevient un nouveau choix inéligible pour cette date.
- Le message utilisateur reste en français et doit être cohérent entre l'UI et l'endpoint JSON.

---

## Derived View Model — `CalendarDaySelectionState`

État calculé pour alimenter la carte de sélection du calendrier.

| Field | Type | Description |
|------|------|-------------|
| `day` | Integer | Jour du mois affiché |
| `full_label` | String | Date complète affichée en français |
| `existing_lunch` | String | Choix déjà enregistré pour cette date, s'il existe |
| `available_options` | Collection | Options actives encore autorisées pour une nouvelle réservation |
| `default_option` | String | Option présélectionnée si aucune réservation n'existe |
| `unavailable_notice` | String or null | Explication affichée quand une salade active est filtrée par la règle des 48 heures |

### Rules

- `available_options` n'inclut que les options actives et éligibles pour une nouvelle réservation à cette date.
- `existing_lunch` peut référencer une salade absente de `available_options` si elle a été réservée avant la limite.
- `default_option` ne doit jamais présélectionner une salade devenue inéligible.
- `unavailable_notice` n'apparaît que lorsque la date est encore réservable pour au moins un repas, mais plus pour la salade.
