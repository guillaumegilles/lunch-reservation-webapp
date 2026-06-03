# Data Model: Affichage de la date complète dans le calendrier

**Feature**: `003-calendar-full-date-display`  
**Phase**: 1 — Design

> Cette fonctionnalité ne change pas le schéma de base de données. Les entités ci-dessous décrivent uniquement les modèles de vue et les libellés de présentation.

---

## Entity 1 — `CalendarDayDisplay`

Représente une case de jour ouvrable rendue dans `calendar.html`.

| Field | Type | Description |
|------|------|-------------|
| `day` | integer | Numéro du jour sans zéro initial |
| `weekday_label` | string | Jour de semaine en français, avec majuscule initiale (`Lundi`) |
| `month_label` | string | Mois en français, en minuscules (`juin`) |
| `full_label` | string | Libellé complet affiché dans la case (`Lundi 14 juin`) |
| `lunch_choice` | string | Repas déjà enregistré, sinon chaîne vide |
| `menu_label` | string | Menu quotidien associé à la date |
| `is_locked` | boolean | Indique si le jour reste non modifiable |
| `selectable` | boolean | Vrai si le clic doit rester actif |

### Validation rules

- `full_label` DOIT respecter le format `[Jour] [numéro] [mois]`.
- `weekday_label` DOIT être issu d'un mapping français stable.
- `month_label` DOIT être en minuscules.
- `day` DOIT être affiché sans zéro initial.
- `is_locked` DOIT conserver le comportement actuel des jours passés/trop proches.

### State transitions

- `unselected` → `selected` quand l'utilisateur clique la case.
- `selected` → `saved` quand `/save-lunch/` retourne un succès.
- `saved` → `cleared` quand la réservation est annulée.

---

## Entity 2 — `MonthHeaderContext`

Représente les données de navigation du haut de page pour `calendar.html` et `admin.html`.

| Field | Type | Description |
|------|------|-------------|
| `username` | string | Identifiant affiché dans le titre du calendrier |
| `month_name_fr` | string | Nom du mois en français |
| `year` | integer | Année affichée dans le titre |
| `prev_year` / `prev_month` | integer | Destination du mois précédent |
| `next_year` / `next_month` | integer | Destination du mois suivant |

### Validation rules

- Le titre du calendrier DOIT afficher le mois en français.
- Le titre du récapitulatif admin DOIT utiliser la même règle.

---

## Entity 3 — `UiCopyRegistry`

Représente les libellés visibles qui doivent rester français sur toutes les pages.

| Field | Type | Description |
|------|------|-------------|
| `page_title` | string | Titre HTML ou titre de carte |
| `nav_previous_label` | string | Libellé du bouton précédent |
| `nav_next_label` | string | Libellé du bouton suivant |
| `dashboard_label` | string | Lien vers le tableau de bord |
| `logout_label` | string | Bouton de déconnexion |
| `admin_page_label` | string | Lien admin depuis le calendrier |
| `back_label` | string | Bouton de retour admin |
| `table_user_label` | string | En-tête de colonne utilisateur |

### Validation rules

- Aucun texte anglais ne DOIT rester visible dans les templates concernés.
- Les pages accueil, connexion, inscription, tableau de bord, calendrier et admin DOIVENT suivre la même langue de l'interface.

