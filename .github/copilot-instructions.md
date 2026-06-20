# Project: Mergington High School Activities API
# Copilot Instructions

## Purpose
This project provides a REST API for viewing and managing extracurricular activities at Mergington High School.

## NEVER_MODIFY — UAT-locked code
The following have passed User Acceptance Testing and must NOT be modified by any Copilot suggestion. If Copilot suggests changes to these, reject the suggestion immediately.

### UAT-locked route functions (src/app.py)
- `get_activities()` — GET /activities
- `signup_for_activity()` — POST /activities/{activity_name}/signup

### UAT-locked test file
- `src/tests/test_app.py` — ALL existing test functions are locked.
  Never delete, rename, or modify any existing test function.

## Scope of Copilot assistance
Copilot may help with:
- Adding the new GET /activities/{activity_name} endpoint
- Updating documentation for the new endpoint only
- Suggesting safe, isolated code changes that do not touch locked routes

## Constraints
- Keep all existing public endpoints unchanged
- Preserve the current response behavior for locked routes
- Return JSON with a 404 error message when an activity name is invalid
- Do not add new imports unless they are clearly needed
- Never suggest changes that reduce test coverage
- Never remove or rename any existing public API endpoint