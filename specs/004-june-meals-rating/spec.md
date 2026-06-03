# Feature Specification : Options de repas de juin & notation des repas passés

**Feature Branch**: `004-june-meals-rating`

**Created**: 2026-06-03

**Status**: Draft

**Input**: Générer des options de repas variées pour chaque jour de juin dans la base de données, avec une option de repas correspondante au menu quotidien pré-sélectionnée par défaut lors du choix du repas ; permettre aux utilisateurs de noter les repas des jours passés avec un système de 5 étoiles.

## Clarifications

### Session 2026-06-03

- Q: La notation des repas passés doit-elle être limitée aux dates passées avec réservation confirmée ? → A: Oui, uniquement pour les dates passées avec réservation confirmée.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Consulter et réserver un repas avec une option pré-sélectionnée (Priority: P1)

En tant qu'employé, lorsque j'ouvre le sélecteur de repas pour un jour de juin, je veux voir une liste de plats variés et attrayants (et non les seuls « steak haché » et « œufs brouillés » fixes) et que l'option de repas correspondante au menu quotidien soit déjà cochée par défaut, afin de réserver en un seul clic sans avoir à faire un choix manuel systématique.

**Why this priority**: C'est le cœur de la demande : enrichir le catalogue de repas et fluidifier la réservation. Sans cette story, les autres n'ont pas de sens.

**Independent Test**: Consulter le calendrier de juin — pour chaque jour ouvrable, le sélecteur de repas doit présenter au moins 3 options variées et l'option de repas correspondant au menu quotidien doit être cochée par défaut.

**Acceptance Scenarios**:

1. **Given** un administrateur a peuplé les menus de juin via la commande de chargement des données, **When** un employé ouvre le calendrier de juin, **Then** chaque jour ouvrable affiche un menu quotidien spécifique à cette date (ex. « Poulet rôti aux herbes ») et non le texte générique « Plat du jour ».
2. **Given** un jour de juin dispose d'un menu défini, **When** l'employé clique sur ce jour pour réserver, **Then** le sélecteur de repas s'ouvre avec l'option de repas correspondante au menu quotidien déjà pré-sélectionnée (premier choix coché).
3. **Given** le sélecteur est ouvert avec l'option pré-sélectionnée, **When** l'employé confirme sans changer la sélection, **Then** la réservation est enregistrée avec l'option de repas correspondant au menu quotidien comme choix de repas.
4. **Given** le sélecteur est ouvert avec l'option pré-sélectionnée, **When** l'employé choisit une option différente puis confirme, **Then** la réservation est enregistrée avec l'option choisie par l'employé (l'option pré-sélectionnée n'est pas imposée).
5. **Given** un jour n'a pas de menu défini en base, **When** l'employé ouvre le sélecteur, **Then** la première option active de la liste globale est pré-sélectionnée par défaut (comportement de repli).

---

### User Story 2 — Charger les données de menus de juin (Priority: P1)

En tant qu'administrateur, je veux disposer d'une commande ou d'un mécanisme qui peuple automatiquement la base de données avec des menus variés et réalistes pour chaque jour ouvrable de juin 2026, afin de ne pas avoir à tout saisir manuellement.

**Why this priority**: Sans données peuplées, l'option pré-sélectionnée (Story 1) n'a rien à afficher. Les deux stories P1 sont indissociables dans l'implémentation.

**Independent Test**: Exécuter la commande de chargement, puis vérifier via l'interface d'administration ou le calendrier que chaque jour ouvrable de juin (du lundi 2 au vendredi 27 juin 2026, hors week-ends) possède un menu défini.

**Acceptance Scenarios**:

1. **Given** la base de données ne contient aucun menu pour juin, **When** l'administrateur exécute la commande de peuplement, **Then** les 22 jours ouvrables de juin 2026 disposent chacun d'un menu distinct et non vide.
2. **Given** des menus de juin existent déjà, **When** l'administrateur exécute à nouveau la commande, **Then** les menus existants ne sont pas dupliqués (opération idempotente).
3. **Given** les menus ont été chargés, **When** on inspecte la liste, **Then** aucun menu ne contient uniquement « Steak haché » ou « Œufs brouillés » — la rotation est variée sur les 4 semaines (au minimum 6 intitulés distincts sur le mois).
4. **Given** les menus ont été chargés, **When** on inspecte les menus du vendredi, **Then** un plat « festif » ou plus élaboré est proposé (ex. dessert spécial, plat régional) pour marquer la fin de semaine.

---

### User Story 3 — Noter un repas passé (Priority: P2)

En tant qu'employé, après avoir déjeuné, je veux pouvoir donner une note de 1 à 5 étoiles au repas que j'ai réservé pour un jour passé, afin d'exprimer ma satisfaction et d'aider la cantine à améliorer ses propositions.

**Why this priority**: Enrichit l'expérience utilisateur mais ne bloque pas les réservations. Peut être livré séparément après les stories P1.

**Independent Test**: Se connecter avec un compte ayant des réservations passées — une interface de notation (1-5 étoiles) doit être accessible pour chaque réservation passée, et la note doit être enregistrée et ré-affichée correctement.

**Acceptance Scenarios**:

1. **Given** l'employé a une réservation pour un jour passé (antérieur à aujourd'hui), **When** il consulte le calendrier ou la vue de ses réservations, **Then** il voit un widget de notation à 5 étoiles associé à ce jour.
2. **Given** l'employé clique sur 4 étoiles pour une date passée, **When** il confirme, **Then** la note « 4/5 » est enregistrée pour ce couple (employé, date) et les 4 étoiles s'affichent en surbrillance lors du prochain chargement.
3. **Given** l'employé a déjà noté un repas (ex. 3 étoiles), **When** il modifie la note à 5 étoiles et confirme, **Then** la nouvelle note (5/5) remplace l'ancienne.
4. **Given** l'employé n'a pas de réservation pour une date passée, **When** il consulte cette date dans le calendrier, **Then** aucun widget de notation n'est affiché pour cette date.
5. **Given** la date est aujourd'hui ou dans le futur, **When** l'employé consulte le calendrier, **Then** aucun widget de notation n'est affiché (la notation est exclusivement rétrospective).

---

### User Story 4 — Consulter les statistiques de notation (admin) (Priority: P3)

En tant qu'administrateur, je veux consulter un résumé des notes reçues par jour, avec les notes individuelles des employés, afin d'orienter les choix de menus futurs.

**Why this priority**: Valeur métier à moyen terme ; ne bloque pas les stories P1 et P2. Peut être reporté si nécessaire.

**Independent Test**: Se connecter en tant qu'admin et accéder à la vue récapitulative — les notes moyennes par jour et les notes individuelles doivent être lisibles.

**Acceptance Scenarios**:

1. **Given** des employés ont noté des repas, **When** l'administrateur consulte la page récapitulative admin, **Then** il voit la note moyenne (ex. « ★ 3,8 / 5 ») pour chaque jour où au moins une note a été soumise.
2. **Given** l'administrateur consulte la récapitulative, **When** il inspecte la colonne d'un employé pour un jour passé, **Then** la note de cet employé est visible (ou un tiret si aucune note).
3. **Given** aucune note n'a été soumise pour un jour donné, **When** l'administrateur consulte ce jour, **Then** la moyenne est affichée comme « Non noté » (et non « 0/5 »).

---

### Edge Cases

- Que se passe-t-il si un jour ouvrable ne correspond pas au calendrier français (jours fériés) ? → Les jours fériés ne sont pas dans le scope de cette version ; le peuplement de juin couvre uniquement les lundis-vendredis.
- Que se passe-t-il si l'employé essaie de noter un repas auquel il n'a pas participé (pas de `Lunch` enregistré) ? → Le widget de notation n'est pas affiché ; la notation sans réservation est refusée côté serveur.
- Que se passe-t-il si l'employé soumet une note hors de la plage 1-5 ? → La soumission est rejetée avec un message d'erreur explicite en français.
- Que se passe-t-il si la commande de peuplement est exécutée pour un mois déjà partiellement peuplé ? → Seuls les jours manquants sont ajoutés ; les jours existants ne sont pas écrasés sauf si l'option `--force` est passée.

---

## Requirements *(mandatory)*

### Functional Requirements

#### Peuplement des menus de juin

- **FR-001**: Le système DOIT fournir un mécanisme permettant de charger des menus pour tous les jours ouvrables de juin 2026 en une seule opération (commande, script ou action admin).
- **FR-002**: Les menus chargés DOIVENT contenir au minimum 6 intitulés de plats distincts répartis sur le mois pour garantir la variété, avec au moins un plat festif ou plus élaboré chaque vendredi.
- **FR-003**: L'opération de chargement DOIT être idempotente : une exécution répétée ne crée pas de doublons.
- **FR-004**: Chaque entrée de menu quotidien DOIT être associée à une date précise et à un intitulé de plat non vide.
- **FR-005**: Les menus chargés DOIVENT être visibles et éditables par un administrateur via l'interface d'administration existante.

#### Option pré-sélectionnée par défaut

- **FR-006**: Lorsqu'un utilisateur ouvre le sélecteur de repas pour un jour ayant un menu quotidien défini, le système DOIT pré-sélectionner automatiquement l'option correspondant à ce menu quotidien.
- **FR-007**: Si le menu quotidien correspond à une option de la liste globale active (`MealOption`), cette option DOIT être visuellement marquée comme sélectionnée (coche, bouton radio, mise en surbrillance) dès l'ouverture du sélecteur.
- **FR-008**: Si aucun menu quotidien n'est défini pour une date, le système DOIT pré-sélectionner la première option active de la liste globale (comportement de repli).
- **FR-009**: La pré-sélection DOIT rester modifiable : l'utilisateur PEUT choisir n'importe quelle autre option active sans restriction.

#### Notation des repas passés

- **FR-010**: Le système DOIT afficher un widget de notation (1 à 5 étoiles) pour chaque date passée où l'utilisateur connecté dispose d'une réservation confirmée.
- **FR-011**: Le widget de notation NE DOIT PAS être affiché pour la date du jour ni pour les dates futures.
- **FR-012**: La notation DOIT être limitée aux utilisateurs disposant d'une réservation pour la date concernée (pas de notation sans réservation).
- **FR-013**: Chaque couple (utilisateur, date) DOIT pouvoir être noté une seule fois, avec possibilité de modifier la note ultérieurement.
- **FR-014**: La note soumise DOIT être un entier compris entre 1 et 5 ; toute valeur hors plage DOIT être rejetée avec un message d'erreur en français.
- **FR-015**: La note soumise DOIT être persistée et ré-affichée correctement lors des consultations ultérieures du calendrier.
- **FR-016**: L'administrateur DOIT pouvoir consulter les notes soumises, avec la note moyenne par jour et les notes individuelles des employés, dans la vue récapitulative mensuelle.

### Key Entities

- **Menu quotidien** (`DailyMenu`, existant) : Associe une date à un intitulé de plat principal affiché dans le calendrier. Un seul menu par date.
- **Option de repas** (`MealOption`, existant) : Option sélectionnable par l'utilisateur lors d'une réservation ; possède un ordre et un statut actif/inactif.
- **Réservation de déjeuner** (`Lunch`, existant) : Enregistre le choix de repas d'un utilisateur pour une date donnée.
- **Notation de repas** (`MealRating`, nouveau) : Enregistre la note (1-5 étoiles) attribuée par un utilisateur à son repas pour une date passée. Relation vers `Lunch` ou couple (utilisateur, date).

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Les 22 jours ouvrables de juin 2026 disposent chacun d'un menu distinct après exécution de la commande de peuplement — vérifiable en moins de 30 secondes.
- **SC-002**: Lorsqu'un menu quotidien est défini pour une date, l'option correspondante est pré-sélectionnée dans 100 % des ouvertures du sélecteur pour cette date.
- **SC-003**: Un employé peut réserver son repas du jour avec l'option par défaut en effectuant au plus 2 actions (clic sur le jour + confirmation) — sans avoir à faire de sélection manuelle.
- **SC-004**: Un employé peut noter un repas passé en moins de 30 secondes à partir de la vue calendrier.
- **SC-005**: La note d'un repas passé est enregistrée et ré-affichée correctement lors de la prochaine consultation du calendrier (persistance vérifiable immédiatement après soumission).
- **SC-006**: Aucune note n'est enregistrée pour une date sans réservation associée (intégrité des données : 0 % de faux positifs).
- **SC-007**: L'administrateur peut consulter les notes moyennes par jour dans la vue récapitulative mensuelle sans quitter cette page.

---

## Assumptions

- **Périmètre temporel** : « Juin » désigne juin 2026, mois en cours au moment de la rédaction de cette spécification. La même approche pourra être étendue à d'autres mois via paramètre, mais cette version couvre uniquement juin 2026.
- **Jours ouvrables** : Les samedis et dimanches sont exclus du peuplement. Les jours fériés français (ex. lundi de Pentecôte, 9 juin 2026) sont inclus dans le scope de cette version faute d'un référentiel officiel intégré — ils seront traités comme des jours ouvrables ordinaires et pourront être supprimés manuellement si besoin.
- **Mécanisme de peuplement** : Les données de menus seront chargées via une commande de gestion Django (extension de la commande `init_db` existante ou nouvelle commande dédiée). Aucune interface graphique d'import n'est requise.
- **Contenu des menus** : Les intitulés de plats de juin sont des données de maquette réalistes (cuisine française de cantine) mais non contractuelles. Un administrateur peut les modifier via l'admin Django après chargement.
- **Correspondance option / menu quotidien** : Si l'intitulé exact du menu quotidien ne correspond à aucune `MealOption` active, le système sélectionne par défaut la première `MealOption` active (ordre `order ASC`). La création automatique de nouvelles `MealOption` à partir des menus quotidiens est hors scope.
- **Notation facultative** : La notation est entièrement optionnelle. L'absence de note pour un repas passé est un état normal et n'affecte pas le flux de réservation.
- **Visibilité des notes** : Les notes individuelles sont visibles uniquement de leur auteur et des administrateurs. Les autres employés ne voient pas les notes des collègues.
- **Pas de commentaire texte** : Cette version ne prévoit pas de champ commentaire libre associé à la note (simplification du scope). Un texte optionnel pourra être ajouté dans une itération ultérieure.
- **Modification de note** : Une note déjà soumise peut être modifiée par l'employé à tout moment (pas de verrouillage dans le temps).
- **Langue** : Tous les libellés, messages de validation et messages d'erreur introduits par cette fonctionnalité sont en français, conformément à la charte de l'application.
- **Compatibilité avec les specs précédentes** : Cette fonctionnalité s'appuie sur le calendrier amélioré livré en spec 003 (affichage date complète). La vue calendrier existante est le point d'entrée principal.
