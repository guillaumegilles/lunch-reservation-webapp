# Quickstart: Affichage de la date complète dans le calendrier

**Feature**: `003-calendar-full-date-display`  
**Branch**: `003-calendar-full-date-display`

---

## What this feature delivers

- Une étiquette de date complète sur chaque jour ouvrable du calendrier, au format `Lundi 14 juin`
- Des titres de pages et boutons de navigation entièrement en français
- Un rendu stable, généré côté serveur, sans dépendance à la locale du système

Aucune migration de base de données et aucun outil de build n'est nécessaire.

---

## Files changed

| File | Change |
|------|--------|
| `reservations/views.py` | Génère les libellés français pour le calendrier et le récapitulatif admin |
| `reservations/templates/base.html` | Normalise le titre global et les libellés de navigation |
| `reservations/templates/index.html` | Normalise le texte visible en français |
| `reservations/templates/login.html` | Normalise le texte visible en français |
| `reservations/templates/register.html` | Normalise le texte visible en français |
| `reservations/templates/dashboard.html` | Normalise le texte visible en français |
| `reservations/templates/calendar.html` | Affiche les dates complètes et la sélection du jour en français |
| `reservations/templates/admin.html` | Affiche le mois, la navigation et le tableau en français |
| `reservations/static/custom.css` | Ajustements mineurs seulement si le texte plus long le requiert |

---

## Validation steps

```bash
python manage.py test
python manage.py runserver
```

Contrôles manuels à faire ensuite :

- Ouvrir `/calendar/` et vérifier que chaque jour affiche `Jour + numéro + mois`
- Ouvrir `/admin-summary/` et vérifier que les boutons/titres sont en français
- Vérifier les pages d'accueil, connexion, inscription et tableau de bord pour supprimer les derniers termes anglais

