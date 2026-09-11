# SplitFair — Product Specification

## 1. Executive Summary
**SplitFair** is an intuitive, multi-party expense splitter application designed for roommates, group trips, and shared household finances. It enables groups to track shared expenses, calculate exact net balances, and minimize settlement transactions without financial confusion.

---

## 2. Target Audience & User Personas
* **Roommates**: Splitting rent, utilities, groceries, and cleaning supplies.
* **Travel Groups**: Tracking shared dinners, Airbnb bookings, and car rentals during trips.
* **Event Planners**: Tracking shared party or conference costs across multiple contributors.

---

## 3. Core User Stories & Features

### Feature 1: Group & Member Management
* **Story**: As a user, I want to create an expense group (e.g., "Summer Trip 2026") and add members by name and email.
* **Acceptance Criteria**:
  * Users can create a group with a title, description, and currency (default: USD).
  * Multiple members can be added to the group with unique identifiers.
  * Group summary lists all active members.

### Feature 2: Expense Creation & Equal/Custom Splits
* **Story**: As a user, I want to record an expense paid by one member and split among specific or all group members.
* **Acceptance Criteria**:
  * User enters amount, description, date, category, payer ID, and participant IDs.
  * System validates that total split matches the recorded amount.
  * Expenses are timestamped and preserved in the group history.

### Feature 3: Net Balance & Debt Minimization
* **Story**: As a user, I want to see who owes whom in real-time so we can settle debts easily.
* **Acceptance Criteria**:
  * System calculates each member's net balance: `Total Paid - Total Share`.
  * Generates simplified settlement suggestions (e.g., "Bob owes Alice $25.00").
  * Total group balance must always sum to $0.00.

### Feature 4: Settlement Recording
* **Story**: As a user, I want to record when a debt has been settled between two members.
* **Acceptance Criteria**:
  * User can record a settlement payment (from payer to receiver).
  * Balances update immediately to reflect the settlement.

---

## 4. API & Data Contract (Overview)
* `GET /api/groups` — List groups
* `POST /api/groups` — Create new group
* `GET /api/groups/{id}` — Get group details with members
* `POST /api/groups/{id}/members` — Add member to group
* `GET /api/groups/{id}/expenses` — List group expenses
* `POST /api/groups/{id}/expenses` — Record new expense
* `GET /api/groups/{id}/balances` — Compute net balances & settlement plan
* `POST /api/groups/{id}/settle` — Record settlement transaction

---

## 5. Non-Goals (Out of Scope for v1)
* Live banking or payment gateway integration (Stripe/PayPal direct debits).
* Multi-currency conversion via real-time forex APIs.
* Recurring scheduled expenses (deferred to v2).
