# Contracts: UI et endpoint calendrier

**Feature**: `003-calendar-full-date-display`

---

## 1. Calendar UI contract

### Required visible text

- Chaque case de jour ouvrable DOIT afficher `Jour + numéro + mois` en français.
- Le panneau de sélection DOIT afficher la même date complète après clic.
- Le titre de page DOIT afficher le mois en français.

### Navigation labels

- `← Précédent`
- `Suivant →`
- `Page Admin`
- `Tableau de bord`
- `Déconnexion`

---

## 2. Admin summary UI contract

### Required visible text

- Le titre de page DOIT suivre le format `Récapitulatif mensuel - [mois] [année]`.
- Le bouton de retour DOIT afficher `Retour`.
- L'en-tête de colonne utilisateur DOIT afficher `Employé`.

---

## 3. `/save-lunch/` JSON contract

### Request

`POST /save-lunch/`

```json
{
  "day": 14,
  "month": 6,
  "year": 2026,
  "lunch": "Plat du jour"
}
```

### Success response

```json
{
  "status": "success",
  "message": "Déjeuner enregistré."
}
```

### Error response

```json
{
  "status": "error",
  "message": "Option de repas invalide."
}
```

### Error conditions

- Date passée ou trop proche
- Option de repas inactive ou inconnue
- Payload JSON invalide

