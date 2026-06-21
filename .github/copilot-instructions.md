# Copilot Instructions - Merington High School Activities API

## Project context
This file contains instructions for GitHub Copilot to assist in developing the Merington High School.

## NEVER_MODIFY - UAT-LOCKED Code
These following have passed UAT  and must not modified by any Copilot suggestion.

### Routes(src.app.py)
 - 'get_activities' - the GET /activities route
 - 'sign_in' - the POST /activities/{activity_name}/signup
 - 'remove_signup_for_activity' - the POST /activities/{activity_name}/signup route

### Tests(src/tests/test_app.py)
 - ALL existing testsfunctions - never delete,modify or,rename.
 - Never reduce assertion count in any existing test function.
 -

## What Copilot MAY help with
- New routes, functions, and tests that are not part of the UAT-LOCKED code.
- README and documentation updates.
- requirements.txt updates.

## Constraints
- Always use Falsks jsonify for returning JSON responses.
- Alweays return appropriate HTTP status codes for success and error scenarios.
- New routes and functions should be well-documented with docstrings and must have a corresponding test function in src/tests/test_app.py.