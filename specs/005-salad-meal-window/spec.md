# Feature Specification: Option salade avec fenêtre de 48 heures

**Feature Branch**: `005-salad-meal-window`

**Created**: 2026-06-28

**Status**: Draft

**Input**: User description: "I try to implement a new feature, where there is a 2nd meal option, which is salad. These meal options are only avalaible under 48h window, meaning on monday, you can only select a salad for wednesday and forward."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Réserver une salade pour une date éligible (Priority: P1)

En tant qu'employé, je veux pouvoir choisir une salade comme alternative au repas standard lorsque ma date de déjeuner est suffisamment éloignée, afin d'avoir une option plus légère sans changer mes habitudes de réservation sur le calendrier.

**Why this priority**: C'est la valeur principale de la demande : ajouter une véritable nouvelle option de repas utilisable dans le flux existant.

**Independent Test**: Depuis le calendrier, sélectionner une date ouvrée située au moins 48 heures à l'avance, choisir "Salade", enregistrer la réservation et vérifier que le choix reste visible lors du retour sur la même date.

**Acceptance Scenarios**:

1. **Given** nous sommes lundi et mercredi est encore réservable, **When** l'employé ouvre mercredi dans le calendrier, choisit "Salade" et enregistre, **Then** la réservation est acceptée et le repas enregistré affiché est "Salade".
2. **Given** nous sommes vendredi et le lundi suivant est réservable, **When** l'employé sélectionne "Salade" pour lundi, **Then** la réservation est acceptée car la fenêtre minimale de 48 heures est respectée.
3. **Given** une réservation salade a été enregistrée pour une date éligible, **When** l'employé revient sur cette date plus tard, **Then** le calendrier affiche toujours "Salade" comme repas enregistré.

---

### User Story 2 - Comprendre quand la salade n'est plus disponible (Priority: P1)

En tant qu'employé, je veux comprendre immédiatement quand l'option salade n'est plus proposée pour une date trop proche, afin d'éviter les erreurs et de pouvoir réserver un autre repas sans ambiguïté.

**Why this priority**: La règle de 48 heures est aussi importante que l'ajout de la salade elle-même ; sans explication claire, l'expérience utilisateur serait confuse.

**Independent Test**: Depuis le calendrier, sélectionner une date située à moins de 48 heures, vérifier que la salade n'est pas disponible pour une nouvelle réservation et qu'un message explicatif en français est affiché.

**Acceptance Scenarios**:

1. **Given** nous sommes lundi et mardi est encore réservable selon les règles existantes, **When** l'employé ouvre mardi dans le calendrier, **Then** l'option "Salade" n'est pas proposée comme nouveau choix et une explication en français indique qu'elle doit être commandée au moins 48 heures à l'avance.
2. **Given** une date est située à moins de 48 heures, **When** l'employé tente malgré tout de valider une nouvelle réservation salade, **Then** la réservation est refusée et un message d'erreur explicite en français est affiché.
3. **Given** la salade n'est plus disponible pour une date proche, **When** l'employé réserve un autre repas encore autorisé pour cette date, **Then** la réservation alternative reste possible dans le flux normal.

---

### User Story 3 - Conserver la lisibilité d'une réservation salade déjà prise (Priority: P2)

En tant qu'employé, je veux continuer à voir ma réservation salade si je l'ai enregistrée avant la limite, afin de garder confiance dans mon choix même lorsque la date passe ensuite sous le seuil des 48 heures.

**Why this priority**: Cette story protège la compréhension et la confiance dans le système, mais elle vient après la possibilité de réserver et la clarté de la règle.

**Independent Test**: Enregistrer une salade pour une date éligible, attendre que cette date passe sous le seuil des 48 heures dans les données de test, puis vérifier que la réservation reste visible et qu'une nouvelle sélection salade n'est plus possible si le choix est retiré.

**Acceptance Scenarios**:

1. **Given** une salade a été réservée avant la limite, **When** la date concernée devient inférieure à 48 heures dans le calendrier, **Then** le repas enregistré reste affiché comme "Salade".
2. **Given** une réservation salade existante est visible pour une date désormais proche, **When** l'employé annule sa réservation ou bascule vers un autre repas autorisé, **Then** le changement est pris en compte normalement.
3. **Given** l'employé a retiré sa réservation salade alors que la date est désormais à moins de 48 heures, **When** il tente de rechoisir "Salade" pour cette même date, **Then** le système refuse ce nouveau choix.

---

### Edge Cases

- Le seuil exact de 48 heures est inclusif : une salade reste autorisée dès que la date du déjeuner est à 48 heures ou plus du moment de réservation.
- Une réservation salade déjà enregistrée avant la limite reste visible même lorsque la date passe ensuite sous le seuil.
- Si la salade est temporairement désactivée dans le catalogue des repas, elle ne doit plus être proposée pour de nouvelles réservations, quelle que soit la date.
- Les dates passées restent non réservable comme aujourd'hui ; cette fonctionnalité n'ajoute aucune exception pour la salade.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Le système DOIT proposer "Salade" comme option de repas identifiable aux côtés du repas standard pour les dates éligibles.
- **FR-002**: Le système DOIT autoriser la sélection d'une salade uniquement pour les dates de déjeuner situées à au moins 48 heures du moment de réservation.
- **FR-003**: Le seuil de 48 heures DOIT être interprété de manière inclusive : une réservation effectuée exactement 48 heures avant le déjeuner reste autorisée.
- **FR-004**: Pour toute date située à moins de 48 heures, le système NE DOIT PAS permettre une nouvelle sélection de la salade.
- **FR-005**: Lorsque la salade n'est pas disponible à cause de la règle des 48 heures, le système DOIT l'indiquer clairement à l'utilisateur avec un libellé ou message en français compréhensible.
- **FR-006**: Si un utilisateur tente de soumettre une nouvelle réservation salade pour une date non éligible, le système DOIT refuser l'enregistrement et afficher un message d'erreur en français.
- **FR-007**: Une réservation salade enregistrée pour une date éligible DOIT être sauvegardée et réaffichée dans le calendrier comme n'importe quel autre repas réservé.
- **FR-008**: Lorsqu'une réservation salade existante passe ensuite sous le seuil des 48 heures, le système DOIT continuer à afficher ce choix comme réservation active.
- **FR-009**: L'utilisateur DOIT pouvoir annuler une réservation existante ou la remplacer par un autre repas encore autorisé via le flux habituel.
- **FR-010**: Si une réservation salade a été retirée alors que la date concernée est déjà à moins de 48 heures, le système NE DOIT PAS permettre de sélectionner à nouveau la salade pour cette date.
- **FR-011**: La règle de disponibilité de la salade DOIT être appliquée de façon cohérente sur tout parcours de création ou de modification de réservation afin qu'elle ne puisse pas être contournée.
- **FR-012**: Les règles existantes empêchant les réservations sur des dates passées DOIVENT rester inchangées.
- **FR-013**: Le système DOIT continuer à permettre l'administration de l'option salade dans le catalogue existant des repas, sans créer un parcours de gestion séparé.

### Key Entities *(include if feature involves data)*

- **Option de repas**: Choix proposé à l'employé lors d'une réservation, incluant au minimum le repas standard et la salade, avec ses propres règles de disponibilité.
- **Date de déjeuner**: Jour ouvré affiché dans le calendrier sur lequel porte la réservation et à partir duquel la fenêtre des 48 heures est calculée.
- **Réservation de déjeuner**: Association entre un employé, une date de déjeuner et l'option de repas choisie.
- **Fenêtre de disponibilité**: Règle métier qui détermine si la salade peut encore être choisie comme nouvelle réservation pour une date donnée.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Dans 100 % des tests de référence à 48 heures ou plus (par exemple lundi→mercredi, mardi→jeudi, vendredi→lundi), la salade peut être réservée avec succès.
- **SC-002**: Dans 100 % des tests de référence à moins de 48 heures, une nouvelle réservation salade est bloquée et accompagnée d'une explication en français dès la première tentative.
- **SC-003**: Un employé peut finaliser une réservation salade éligible en moins d'une minute et en 3 interactions maximum depuis la carte de sélection du calendrier.
- **SC-004**: Une réservation salade déjà enregistrée reste visible dans 100 % des consultations ultérieures du calendrier pour la même date.
- **SC-005**: Pour 100 % des dates proches encore ouvertes selon les règles actuelles, l'utilisateur peut toujours réserver un repas autorisé même lorsque la salade n'est plus disponible.

## Assumptions

- La règle des 48 heures s'applique uniquement à l'option "Salade" dans cette version ; les autres options de repas conservent leurs règles actuelles.
- Le calendrier mensuel existant reste le point d'entrée principal pour consulter, créer, modifier et annuler une réservation.
- La logique porte uniquement sur les jours ouvrés déjà affichés dans l'application ; aucun nouveau comportement n'est attendu pour les week-ends.
- Lorsqu'une date est trop proche pour la salade, l'utilisateur peut toujours choisir un autre repas si cette date reste réservable selon les règles existantes.
- Les textes, libellés d'interface et messages d'erreur ajoutés par cette fonctionnalité sont en français.
- La fonctionnalité ne change ni la gestion des menus du jour, ni la notation des repas passés, ni le périmètre des rôles utilisateurs existants.
