# Research: Affichage de la date complète dans le calendrier

**Feature**: `003-calendar-full-date-display`  
**Phase**: 0 — Research

---

## 1. Formatage français indépendant de la locale système

### Context

Le code actuel s'appuie sur `calendar.month_name[month]` et `date.strftime("%a")` pour les libellés de date. Ces valeurs dépendent de la locale du processus et peuvent rester en anglais sur Vercel, en local ou en CI.

### Decision

Utiliser des tables explicites de correspondance pour les jours de semaine et les mois dans `reservations/views.py`, puis construire côté serveur les libellés complets comme `Lundi 14 juin`.

### Rationale

Cette approche est déterministe, ne dépend pas de la locale de l'hôte et n'ajoute aucune dépendance.

### Alternatives considered

- `locale.setlocale(...)` + `strftime(...)` : rejeté, car la locale est globale au processus et fragile en déploiement.
- Une couche de traduction Django complète : rejetée, car le périmètre est limité et n'a pas besoin d'un système i18n plus large.

---

## 2. Portée de la normalisation linguistique

### Context

La spec impose désormais que tous les textes visibles soient en français sur toutes les pages, pas seulement sur le calendrier et le récapitulatif admin. Les chaînes anglaises restantes sont localisées dans les templates serveur.

### Decision

Modifier directement les templates Django existants pour normaliser le texte visible, au lieu d'ajouter une couche de traduction dynamique côté client.

### Rationale

Le site rend déjà toute l'interface côté serveur; la surface à corriger est finie et facile à auditer.

### Alternatives considered

- Traduction côté navigateur : rejetée, car inutile pour une interface serveur statique.
- Fichiers de traduction Django (`.po`/`.mo`) : rejetés pour ce cas précis, car ils introduisent plus de structure que nécessaire.

---

## 3. Stabilité du contrat du endpoint `/save-lunch/`

### Context

Le calendrier dépend déjà d'un POST JSON vers `/save-lunch/`. La fonctionnalité ne change pas la réservation elle-même, seulement les libellés affichés.

### Decision

Conserver la forme du payload et des réponses JSON existantes pour éviter tout effet de bord sur le JavaScript du calendrier.

### Rationale

Le contrat actuel fonctionne déjà et les tests existants le couvrent; il n'y a aucune raison de le casser pour un changement purement visuel.

### Alternatives considered

- Introduire un nouveau format JSON localisé : rejeté, car cela compliquerait inutilement le front.
