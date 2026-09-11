# Backlog: ChoreFlow

## Task 1: Set up Housemate and Chore models with database migrations
- Define `Housemate` model with `name` and `email`.
- Define `Chore` model with `title`, `description`, `recurrence`, `assigned_to`, `due_date`, and `status`.
- Generate and run initial Django migrations.

## Task 2: Create Chore listing and detail views
- Implement HTML view displaying active chores grouped by due status.
- Add housemate filter to view chores assigned to a specific person.

## Task 3: Implement Chore Creation and Status Toggle
- Add form to create and assign new chores.
- Add one-click action to mark a chore as completed and log completion timestamp.

## Task 4: Automated Test Suite
- Write unit tests for Housemate and Chore models.
- Write view tests for chore listing, creation, and completion toggle.
- Verify 100% test pass rate via `uv run python manage.py test`.
