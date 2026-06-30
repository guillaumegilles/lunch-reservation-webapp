# Quickstart: Option salade avec fenêtre de 48 heures

**Feature**: `005-salad-meal-window`  
**Branch**: `005-salad-meal-window`

---

## What this feature delivers

- Des options salade gérées dans le catalogue de repas existant
- Une disponibilité des salades limitée aux dates à au moins 48 heures (2 jours) d'avance
- Une explication claire en français quand la salade n'est plus disponible
- La conservation visuelle d'une salade déjà réservée, même quand la date passe sous le seuil

---

## Files changed

| File | Change |
|------|--------|
| `reservations/admin.py` | Exposer le délai d'avance dans le catalogue admin existant |
| `reservations/management/commands/init_db.py` | Garantir les options salade bootstrap avec `advance_days = 2` |
| `reservations/views.py` | Centraliser la règle d'éligibilité, alimenter le calendrier et valider `/save-lunch/` |
| `reservations/templates/calendar.html` | Filtrer les options salade inéligibles et afficher l'explication utilisateur |
| `reservations/tests/test_views.py` | Couvrir les réservations salade éligibles, bloquées et persistées sous le seuil |

---

## Run it locally

```bash
python3 manage.py migrate
python3 manage.py init_db
python3 manage.py runserver
```

---

## Manual validation

1. Ouvrir le calendrier sur une date située à au moins 2 jours et vérifier qu'une salade peut être sélectionnée puis enregistrée.
2. Ouvrir une date encore réservable mais à moins de 2 jours et vérifier qu'aucune salade n'est proposée comme nouveau choix.
3. Vérifier qu'un message en français explique que la salade doit être commandée au moins 48 heures à l'avance.
4. Enregistrer une salade pour une date éligible, puis vérifier qu'elle reste visible si la date passe ensuite sous le seuil.
5. Sur cette même date devenue proche, vérifier qu'une annulation ou un remplacement par un autre repas autorisé fonctionne, mais qu'une resélection salade est refusée.

---

## Sample shell check

Vérifier les délais configurés pour les options de repas :

```bash
python3 manage.py shell -c "from reservations.models import MealOption; print(list(MealOption.objects.values_list('name', 'advance_days')))"
```
