# Feature Specification: Modern Website Styling

**Feature Branch**: `002-modern-website-styling`

**Created**: 2025-06-03

**Status**: Draft

**Input**: User description: "Create a modern styling for the website"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Visually Refreshed Experience Across All Pages (Priority: P1)

Any visitor — whether logging in, navigating the dashboard, or managing reservations — encounters a cohesive, polished, and visually appealing design that feels up-to-date and professional. Every page shares the same visual language: consistent typography, colour palette, spacing, and component styles.

**Why this priority**: This is the core deliverable. A consistent design system applied globally ensures every page benefits from the styling overhaul.

**Independent Test**: Can be fully tested by visiting each page (home, login, register, dashboard, calendar, admin summary) and verifying the visual consistency — same fonts, colours, and component styles throughout — delivering an immediately noticeable improvement.

**Acceptance Scenarios**:

1. **Given** a user opens the home/login page, **When** the page loads, **Then** they see a modern, visually polished layout with a clear typographic hierarchy, readable colours, and no unstyled elements.
2. **Given** a user navigates from the login page to the dashboard, **When** the page transitions, **Then** the visual language (colours, fonts, button styles, card shapes) remains identical, reinforcing a single coherent product.
3. **Given** a staff user visits the admin summary page, **When** the page loads, **Then** the table and heading elements use the same design system as the rest of the site.

---

### User Story 2 - Readable and Accessible Colour Scheme (Priority: P2)

All text, buttons, and interactive elements meet minimum contrast requirements so the site is usable by users with visual impairments or in low-light conditions. The colour palette feels intentional and modern (no harsh defaults or clashing tones).

**Why this priority**: Accessibility and legibility are non-negotiable for a daily-use internal tool. Styling improvements that reduce readability would be counterproductive.

**Independent Test**: Can be fully tested by running a contrast-ratio audit on the most common text/background pairings (body text, button labels, heading/background) and confirming all pairs meet WCAG AA standards, delivering measurable accessibility compliance.

**Acceptance Scenarios**:

1. **Given** any text element on any page, **When** its foreground and background colours are checked, **Then** the contrast ratio is at minimum 4.5:1 for normal text and 3:1 for large text (WCAG AA).
2. **Given** a button (primary, secondary, outline variants), **When** inspected, **Then** the label colour against the button background meets contrast requirements.
3. **Given** the site is viewed on a mobile device in bright ambient light, **When** the user reads body text, **Then** the text remains legible without zooming.

---

### User Story 3 - Responsive Layout on Mobile and Tablet (Priority: P3)

Users accessing the reservation system from a phone or tablet experience a layout that adapts gracefully: readable text, tap-friendly buttons, and no horizontal overflow or clipped content.

**Why this priority**: A significant share of the users may check or change their reservations on mobile. The redesign must not introduce regressions on small screens.

**Independent Test**: Can be fully tested by resizing the browser to 375 px (mobile) and 768 px (tablet) widths and verifying that all content is accessible, buttons are comfortably tappable, and no content overflows, delivering a fully functional mobile experience.

**Acceptance Scenarios**:

1. **Given** a user opens the calendar page on a 375 px wide screen, **When** the page renders, **Then** all day cells are visible and the action buttons are large enough to tap without zooming.
2. **Given** a user fills in the login form on a tablet, **When** they interact with the input fields, **Then** field labels, inputs, and the submit button are clearly distinguishable and not clipped.
3. **Given** the dashboard is viewed on a phone, **When** the user scrolls, **Then** no element extends beyond the viewport width.

---

### Edge Cases

- What happens when the user has cookies or local storage from the old design? — No data migration needed; purely CSS/template changes.
- How does the design handle very long user-submitted text (e.g., a long suggestion message)? — Text should wrap gracefully without breaking the card layout.
- What if an alert message is triggered (e.g., login error)? — Alert components must use the new colour scheme and remain clearly distinguishable from non-alert content.
- How does the design degrade when Google Fonts are unavailable? — A defined system-font fallback stack must be specified so the layout does not collapse.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The visual design MUST be applied consistently across all existing pages: home/index, login, registration, user dashboard, reservation calendar, and admin monthly summary.
- **FR-002**: The design system MUST define a unified colour palette with named roles (background, surface, primary action, secondary action, text, muted text, error/warning, success), built by **retaining and refining the existing warm palette** — berry and plum tones for primary actions, apricot and sun tones for accents; all palette values MUST be re-evaluated and adjusted as needed to achieve sufficient contrast on flat minimal (opaque) surfaces.
- **FR-003**: All heading and body text MUST use a defined typeface pairing with a clear typographic scale (size and weight hierarchy from page title down to captions).
- **FR-004**: Interactive elements (buttons, links, form fields) MUST have visually distinct hover, focus, and active states so users can tell what is interactive.
- **FR-005**: Button styles MUST clearly differentiate primary actions (e.g., "Se connecter", "Envoyer") from secondary/destructive actions (e.g., "Se déconnecter") through colour and visual weight.
- **FR-006**: Form fields (text inputs, selects) MUST have clear focus indicators that are visible to keyboard-only users.
- **FR-007**: Card and container components MUST use a **flat minimal treatment**: a solid (opaque) surface colour, a subtle 1 px border, and a soft drop shadow — applied consistently throughout all pages. Glassmorphism (backdrop-filter / translucent fills) is explicitly out of scope.
- **FR-008**: The layout MUST be fully responsive with defined breakpoints for mobile (≤ 576 px), tablet (577–991 px), and desktop (≥ 992 px).
- **FR-009**: The redesign MUST NOT remove or hide any existing functionality; it is purely a visual layer applied on top of the current HTML structure.
- **FR-010**: All text/background colour combinations MUST meet WCAG AA contrast ratio requirements (4.5:1 for body text, 3:1 for large text and UI components).
- **FR-011**: A font fallback stack MUST be defined for each typeface so the layout remains functional when web fonts fail to load.
- **FR-012**: All custom styles MUST be delivered in a **single `custom.css` file** that uses CSS custom properties (e.g., `--color-primary`) for all design tokens and overrides Bootstrap component classes directly — no CSS preprocessor (Sass/Less), PostCSS pipeline, or build step is required or permitted.
- **FR-013**: The navbar/header MUST use a **coloured brand treatment**: a solid berry/plum fill, light (near-white) text and icon colours, and `position: sticky` so it remains visible at the top of the viewport during vertical scroll. A transparent or white navbar is explicitly out of scope.

### Key Entities

- **Design Token**: A named CSS custom property representing a colour, spacing value, typography size, or shadow depth — defined in `:root` within `custom.css` and referenced throughout all component overrides (e.g., `--color-primary`, `--radius-card`). No preprocessor variables or build-time tokens are used.
- **Component Style**: A reusable visual treatment applied to a specific HTML/Bootstrap element class (button, card, alert, table, form control) that references design tokens rather than hardcoded values.
- **Page Layout**: The overall structural composition of a single page, defined by container width, vertical rhythm, and how components are arranged at each breakpoint.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Every page shares at least 95% of its visual style through the common design system (tokens + component overrides), with no page having unique ad-hoc colour or font values outside the token set.
- **SC-002**: 100% of body-text / background pairs and button-label / button-background pairs pass WCAG AA contrast ratio check (≥ 4.5:1 for normal text, ≥ 3:1 for large text / UI components).
- **SC-003**: On a 375 px wide mobile viewport, all pages load with zero horizontal scrollbar and all buttons have a minimum tap-target height of 44 px.
- **SC-004**: First visual feedback (hover/focus state change) on any interactive element occurs in under 200 ms after user interaction, ensuring the UI feels snappy and responsive.
- **SC-005**: Users asked to perform a common task (e.g., log in, navigate to the calendar) report finding the primary action button immediately visible without scrolling on all screen sizes.

## Clarifications

### Session 2026-06-02

- Q: Card/container visual treatment → A: Flat minimal — solid surface colour, subtle 1px border, soft drop shadow (glassmorphism explicitly excluded).
- Q: Colour palette direction → A: Retain & refine existing warm palette — berry/plum/apricot/sun — adapt tones to flat minimal surfaces.
- Q: CSS architecture → A: Single `custom.css` file — CSS custom properties (`--token` notation) for all design tokens, Bootstrap component class overrides, no build step or preprocessor.
- Q: Navbar/header treatment → A: Coloured brand navbar — solid berry/plum fill, light text, `position: sticky`; transparent or white navbar explicitly excluded.

## Assumptions

- The website currently uses Bootstrap 5.3.2 as its CSS framework; the new styling will layer on top of Bootstrap through custom CSS overrides and design-token variables rather than replacing Bootstrap.
- The existing warm colour palette (berry/plum for primary actions, apricot/sun for accents) is retained and refined rather than replaced; individual hex values may be adjusted to satisfy WCAG AA contrast requirements on flat minimal surfaces.
- The existing Google Fonts (Archivo Black for headings, DM Sans for body text) are retained unless the redesign explicitly proposes an alternative — the spec focuses on the design system, not on mandating a specific typeface.
- The redesign applies only to the front-end visual layer (CSS and template markup tweaks); no changes to back-end logic, URL structure, or database schema are required.
- All custom styling is delivered via a single `custom.css` file using native CSS custom properties; no Sass, Less, PostCSS, or any build tooling is introduced — the file is loaded directly alongside Bootstrap's CDN stylesheet.
- Dark mode support is out of scope for this iteration; a single light-mode theme is targeted.
- The French-language content of all templates is preserved as-is; the spec covers visual design only, not copy changes.
- Performance impact of additional web font weights or CSS is assumed acceptable given the existing use of Google Fonts and Bootstrap CDN.
- The navbar uses a solid berry/plum fill with light (near-white) text and `position: sticky`; no transparent, scroll-triggered, or white navbar variants are in scope for this iteration.
- The admin Django back-office (`/admin/`) is out of scope; only the custom application templates are being restyled.
