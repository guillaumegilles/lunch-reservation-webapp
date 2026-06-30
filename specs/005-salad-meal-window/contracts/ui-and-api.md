# Contracts: Option salade avec fenêtre de 48 heures

**Feature**: `005-salad-meal-window`

---

## 1. Contrat du catalogue d'options de repas

### Règles de gestion

- Le personnel continue de gérer les options salade dans le catalogue `MealOption` existant.
- Une salade soumise à cette fonctionnalité doit porter `advance_days = 2`.
- La désactivation d'une salade (`is_active = false`) la retire des nouvelles sélections sans supprimer les réservations déjà enregistrées.

---

## 2. Contrat de sélection dans le calendrier

### Availability rules

- Pour une nouvelle réservation, le sélecteur n'affiche que les options actives dont le délai `advance_days` est respecté pour la date choisie.
- Pour une date à moins de 48 heures (2 jours calendaires), une nouvelle salade n'est pas proposée.
- Si une salade a déjà été réservée avant la limite, son libellé reste visible sur la journée concernée.
- L'annulation de la réservation et le basculement vers un autre repas encore autorisé restent possibles dans le flux normal.

### User guidance

- Quand une salade est filtrée uniquement par la règle de délai, l'interface affiche une explication en français indiquant qu'elle doit être commandée au moins 48 heures à l'avance.
- La zone de statut existante continue d'afficher les messages de succès ou d'erreur des appels AJAX.

---

## 3. Contrat du endpoint de réservation

### Request

`POST /save-lunch/`

```json
{
  "day": 16,
  "month": 7,
  "year": 2026,
  "lunch": "🥗 Salade César"
}
```

### Success response

```json
{
  "status": "success",
  "message": "Déjeuner enregistré."
}
```

### Cancellation request

`lunch: ""` continue d'annuler la réservation existante pour la date donnée.

### Validation rules

- Le serveur valide que `lunch` correspond à une option active.
- Le serveur applique la règle `lunch_date >= localdate() + timedelta(days=advance_days)` pour toute nouvelle sélection non vide.
- Le serveur continue de rejeter les dates passées.
- Le serveur ne permet pas de rechoisir une salade sous le seuil après annulation.

### Error response example

```json
{
  "status": "error",
  "message": "Cette option doit être réservée au moins 2 jours à l'avance."
}
```

### Error cases

- Option de repas inconnue ou inactive
- Date passée
- Date encore réservable globalement mais trop proche pour l'option salade
- Utilisateur non authentifié

---

## 4. Contrat de persistance d'une salade existante

### Display and replacement rules

- Une réservation salade existante reste affichée après le passage sous le seuil.
- Un remplacement vers un autre repas reste autorisé uniquement si ce nouveau repas respecte sa propre règle `advance_days`.
- Une fois la salade retirée pour une date déjà sous le seuil, elle n'apparaît plus comme nouvelle option disponible pour cette même date.
