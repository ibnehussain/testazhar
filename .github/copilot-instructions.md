# Project: Mergington High School Activities API
# Copilot Instructions

## Purpose
This file contains the instructions for Copilot to follow when assisting with the development of the Mergington High School Activities API. The goal is to ensure that Copilot's suggestions align with the project's requirements and coding standards.

## NEVER_MODIFY — UAT-locked code
The following have passed User Acceptance Testing and must NOT be
modified by any Copilot suggestion. If Copilot suggests changes to
these, reject the suggestion immediately.

### UAT-locked route functions (src/app.py)
- `signup_for_activity` — Sign up a student for an activity
- `get_activities` — Retrieve the list of available activities
- `remove_signup_for_activity` — Remove a student's signup for an activity

### UAT-locked test file
- `src/tests/test_app.py` — ALL existing test functions are locked.
  Never delete, rename, or modify any existing test function.

## Scope of Copilot assistance
Copilot may help with:
- Adding new features or endpoints to the API without modifying existing UAT-locked code.
- Adding new features or endpoints without modifying existing UAT-locked test functions.
- Documentation for new functions only

## Constraints
- JSON Output must be valid and well-formed
- HTTP Status codes must be appropriate for the operation performed
- Adding new imports is allowed, but never remove existing imports
- Never suggest changes that reduce test coverage
- Never remove or rename any existing public API endpoint