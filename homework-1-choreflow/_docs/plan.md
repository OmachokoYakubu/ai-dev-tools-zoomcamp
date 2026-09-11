# Product Specification: ChoreFlow (Shared Household Chores Manager)

## 1. Problem Statement
Living with roommates or family members often leads to friction over who cleans what, missed chores, and lack of transparency. Existing task managers are either overly generic or too complex for simple household coordination.

## 2. Core Features (Scope)
The spec settles on 3 core features:
1. **Housemate & Chore Assignment**: Register household members and assign specific chores with rotation capabilities.
2. **Recurring Schedule & Status Tracking**: Chores with customizable recurrence (daily, weekly) and clear status tags (Pending, Completed, Overdue).
3. **Completion Verification & Activity History**: A shared completion log where housemates mark chores done with optional notes and timestamps.

## 3. Data Entities
- **Housemate**: Name, email, active status.
- **Chore**: Title, description, recurrence (Daily/Weekly/Monthly), assigned_to (Housemate foreign key), due_date, status (Pending, Done).
- **ChoreLog**: Chore, completed_by, completed_at, notes.

## 4. Non-Goals (Out of Scope for v1)
- Complex financial penalty systems.
- Push notifications via third-party SMS/WhatsApp APIs.
- Multi-household tenancy.
