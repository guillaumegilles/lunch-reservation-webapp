# Feature Specification: Affichage de la date complète dans le calendrier

**Feature Branch**: `003-calendar-full-date-display`

**Created**: 2026-06-03

**Status**: Draft

**Input**: User description: "Add a feature to display the actual date on every day rather day 14, but Lundi 14 juin, for example"

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Lire la date complète sur chaque jour du calendrier (Priority: P1)

En tant qu'employé, je consulte le calendrier mensuel pour réserver mon déjeuner. Actuellement, chaque case affiche uniquement le numéro du jour (ex. « 14 »). Je veux voir la date complète au format « Lundi 14 juin » afin d'identifier le bon jour sans avoir à compter les cases ou croiser avec un autre calendrier.

**Why this priority**: C'est le besoin principal de la fonctionnalité. Sans cela, le reste n'a pas de valeur.

**Independent Test**: Naviguer vers la vue calendrier — chaque case doit afficher le jour de la semaine en français, le numéro du jour et le nom du mois en français.

**Acceptance Scenarios**:

1. **Given** l'utilisateur est connecté et consulte le calendrier de juin 2026, **When** la page se charge, **Then** chaque case de jour ouvrable affiche une étiquette de la forme « Lundi 2 juin », « Mardi 3 juin », etc.
2. **Given** l'utilisateur navigue vers un mois différent (ex. juillet), **When** la page se charge, **Then** les étiquettes reflètent le bon mois (ex. « Mercredi 1 juillet »).
3. **Given** un jour est verrouillé (passé ou trop proche), **When** la page se charge, **Then** l'étiquette complète est toujours affichée (avec l'opacité réduite habituelle).
4. **Given** l'utilisateur clique sur un jour (ex. le 14 juin), **When** le panneau de sélection s'affiche, **Then** il indique « Lundi 14 juin » (et non « 14 »).

---

### User Story 2 — Cohérence de la langue française sur toute l'interface (Priority: P2)

En tant qu'utilisateur francophone, je veux que l'intégralité des textes visibles sur **toutes les pages de l'application** (noms de jours, noms de mois, titres de pages, boutons de navigation, étiquettes d'action) soient en français, cohérents avec le reste de l'interface.

**Why this priority**: L'interface est intégralement en français (principe gouvernant de l'application). Tout terme anglais visible sur n'importe quelle page briserait la cohérence et nuirait à l'expérience utilisateur.

**Independent Test**: Inspecter chaque texte visible sur toutes les pages de l'application (accueil, connexion, inscription, tableau de bord, calendrier, récapitulatif admin) — aucun terme anglais ne doit apparaître.

**Acceptance Scenarios — Page Calendrier**:

1. **Given** la page calendrier est affichée, **When** on lit les étiquettes de dates, **Then** les jours s'affichent comme « Lundi », « Mardi » … « Vendredi » (jamais « Monday », « Tuesday », etc.).
2. **Given** la page calendrier est affichée, **When** on lit les étiquettes de dates, **Then** les mois s'affichent comme « janvier », « février » … « décembre » (jamais « January », « February », etc.).
3. **Given** la page calendrier est affichée, **When** on inspecte les boutons de navigation, **Then** ils affichent « ← Précédent » et « Suivant → » (et non « ← Previous » / « Next → »).
4. **Given** la page calendrier est affichée pour un utilisateur staff, **When** on lit le bouton de lien admin, **Then** il affiche « Page Admin » en français (et non « Admin Page »).
5. **Given** la page calendrier est affichée, **When** on inspecte tous les boutons d'action, **Then** aucun texte en anglais n'est visible (« Dashboard » → « Tableau de bord », « Logout » → « Déconnexion »).

**Acceptance Scenarios — Page Récapitulatif Admin**:

6. **Given** la page récapitulatif admin est affichée, **When** on lit le titre de la page, **Then** il affiche « Récapitulatif mensuel - [mois] [année] » (et non « Admin Summary - ... »).
7. **Given** la page récapitulatif admin est affichée, **When** on inspecte les boutons de navigation entre les mois, **Then** ils affichent « ← Précédent » et « Suivant → » (et non « ← Previous » / « Next → »).
8. **Given** la page récapitulatif admin est affichée, **When** on inspecte le bouton de retour, **Then** il affiche « Retour » (et non « Back »).
9. **Given** la page récapitulatif admin est affichée, **When** on lit l'en-tête de la colonne utilisateurs dans le tableau, **Then** il affiche « Employé » (et non « User »).

---

### Edge Cases

- Que se passe-t-il pour les mois qui commencent un mercredi ou finissent un lundi ?
  → Les étiquettes doivent être correctes pour tous les jours ouvrables, quelle que soit la position dans la semaine.
- Les week-ends ne sont pas affichés dans le calendrier — ce comportement reste inchangé.
- Le format ne doit pas être tronqué pour les noms longs comme « mercredi » ou « septembre ».

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT afficher une étiquette de date complète sur chaque case de jour ouvrable du calendrier, au format « [Jour] [numéro] [mois] » (ex. « Lundi 14 juin »).
- **FR-002**: Le nom du jour de la semaine DOIT être en français et commencer par une majuscule (ex. « Lundi », « Mardi »).
- **FR-003**: Le nom du mois DOIT être en français et en minuscules (ex. « juin », « octobre »), conformément à la typographie française.
- **FR-004**: Le numéro du jour DOIT être affiché sans zéro initial (ex. « 4 » et non « 04 »).
- **FR-005**: L'étiquette de date complète DOIT remplacer l'actuel affichage du seul numéro de jour dans chaque case du calendrier.
- **FR-006**: Le comportement existant des jours verrouillés (opacité réduite, non cliquables) DOIT être préservé sans modification.
- **FR-007**: L'étiquette de date complète DOIT rester lisible lorsqu'un choix de repas est déjà enregistré pour ce jour.
- **FR-008**: Le titre de la page calendrier (ex. « Alice - June 2026 ») DOIT afficher le nom du mois en français (ex. « Alice - juin 2026 »), en minuscules conformément à la typographie française.
- **FR-009**: Le titre de la page de récapitulatif admin DOIT également afficher le nom du mois en français (même règle que FR-008), assurant une cohérence de langue sur toutes les pages de l'application.
- **FR-010**: Lorsque l'utilisateur clique sur un jour du calendrier, le panneau de sélection DOIT afficher la date complète en français (ex. « Lundi 14 juin ») et non uniquement le numéro du jour.
- **FR-011**: Tous les libellés de l'interface utilisateur visibles par l'employé et le personnel admin DOIVENT être rédigés en français, sans aucun terme anglais — y compris les boutons de navigation (ex. « ← Précédent », « Suivant → »), les libellés d'action (ex. « Page Admin », « Tableau de bord », « Déconnexion ») et tous les textes statiques des templates.

### Key Entities

- **Jour du calendrier** : représente un jour ouvrable du mois. Attributs : numéro du jour, nom du jour de la semaine (français), nom du mois (français), repas choisi (optionnel), statut verrouillé/déverrouillé.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100 % des cases de jours ouvrables affichent une étiquette au format « [Jour] [numéro] [mois] » pour n'importe quel mois de l'année.
- **SC-002**: 100 % des textes visibles de l'interface (libellés de dates, noms de mois, titres de pages, boutons de navigation et d'action) sont en français — aucun terme anglais ne subsiste.
- **SC-003**: L'affichage ne dépasse pas la hauteur actuelle des cases du calendrier sur desktop et mobile (pas de rupture de mise en page).
- **SC-004**: Tous les tests existants (26/26) continuent de passer après la modification.

## Assumptions

- Le calendrier n'affiche que les jours ouvrables (lundi–vendredi) — comportement inchangé.
- Le format retenu est « Lundi 14 juin » (jour + numéro + mois) sans l'année, car l'année est déjà affichée dans le titre de la page.
- Les noms de jours et de mois sont fournis par le back-end (vue Django) afin d'éviter toute dépendance à la locale du navigateur client.
- Aucune modification de la base de données n'est nécessaire : seul l'affichage est concerné.
- La mise en page des cases du calendrier peut nécessiter un léger ajustement CSS pour accommoder le texte plus long, mais sans refonte visuelle.

## Clarifications

### Session 2026-06-03

- Q: Le titre de la page admin affiche-t-il aussi le mois en français ? → A: Oui — même règle que la page calendrier (FR-009 ajouté).
- Q: Le panneau de sélection du jour affiche-t-il la date complète en français ? → A: Oui — « Lundi 14 juin » (FR-010 ajouté).
- Q: FR-011 s'applique-t-il uniquement aux pages calendrier et admin, ou à toutes les pages de l'application ? → A: À toutes les pages de l'application (accueil, connexion, inscription, tableau de bord, calendrier, récapitulatif admin). Note : les pages accueil, connexion, inscription et tableau de bord sont déjà entièrement en français — les seuls termes anglais résiduels se trouvent dans `calendar.html` et `admin.html`.
