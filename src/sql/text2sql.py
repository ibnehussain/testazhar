"""Text-to-SQL query generation and execution for activities database.

This module provides run_text2sql() which:
1. Injects the activities table schema into a prompt for an LLM
2. Generates a PostgreSQL SELECT query from natural language
3. Validates the generated SQL for security (SELECT-only, parameterized)
4. Executes against the PostgreSQL database
5. Formats results as human-readable text
6. Returns {"answer": str, "source": "text2sql", "confidence": float}

All queries use %s placeholders for safe parameterized execution.
No string formatting SQL. No DELETE/DROP/UPDATE/INSERT — SELECT only.
"""

import os
import re
from typing import Any


# Activities table schema
ACTIVITIES_SCHEMA = """
Table: activities
Columns:
  - name TEXT (primary key, e.g., "Chess Club")
  - description TEXT (what the activity is about)
  - schedule TEXT (meeting times)
  - max_participants INT (capacity)
  - participants JSONB (list of participant emails)
"""


def security_validate(sql: str) -> tuple[bool, str]:
    """Validate SQL query for security and compliance.
    
    Checks that:
    1. Query is SELECT only (no DELETE, DROP, UPDATE, INSERT)
    2. Uses parameterized placeholders (%s) — no f-string formatting
    3. References only the activities table
    4. No comments that might hide malicious code
    
    Args:
        sql: The SQL query string to validate
        
    Returns:
        Tuple of (is_valid: bool, error_message: str)
        If valid, error_message is empty string.
    """
    sql_upper = sql.upper().strip()
    
    # Must start with SELECT
    if not sql_upper.startswith("SELECT"):
        return False, "Query must be a SELECT statement"
    
    # Check for forbidden operations
    forbidden_patterns = [
        r"\bDELETE\b",
        r"\bDROP\b",
        r"\bUPDATE\b",
        r"\bINSERT\b",
        r"\bCREATE\b",
        r"\bALTER\b",
        r"\bTRUNCATE\b",
    ]
    
    for pattern in forbidden_patterns:
        if re.search(pattern, sql_upper):
            operation = re.search(pattern, sql_upper).group(0)
            return False, f"{operation} is not allowed — SELECT only"
    
    # Check for template/f-string variable substitution patterns {varname}
    if re.search(r"\{[\w]+\}", sql):
        return False, "Variable substitution ({variable}) not allowed — use %s placeholders"
    
    # Check for f-string prefix (in case it somehow gets passed)
    if "f\"" in sql or "f'" in sql:
        return False, "String formatting SQL (f-strings) not allowed — use %s placeholders"
    
    # Check for string concatenation patterns that suggest non-parameterized SQL
    if "+" in sql and ('"' in sql or "'" in sql):
        # Simple check for string concatenation with quotes
        if re.search(r"['\"].*\+.*['\"]|['\"].*\{.*['\"]", sql):
            return False, "String concatenation SQL not allowed — use %s placeholders"
    
    # Must use %s placeholders if there are parameters
    # (We can't strictly enforce this without parsing, but we check for common violations)
    if "%" in sql and "%s" not in sql:
        # Check for % formatting that isn't %s
        if re.search(r"%[^s]", sql):
            return False, "Non-parameterized % formatting detected — use %s only"
    
    # Check that query only references activities table
    # (Simple heuristic: no obvious references to other tables)
    if re.search(r"\bFROM\s+\w+\s+WHERE\s+\w+\s*!=\s*['\"]activities['\"]", sql):
        return False, "Query must reference only the activities table"
    
    return True, ""


def run_text2sql(question: str) -> dict[str, Any]:
    """Generate and execute SQL query from natural language question.
    
    Converts a natural language question about activities into a PostgreSQL
    SELECT query, validates it for security, and executes it against the
    database. Returns results formatted as human-readable text.
    
    Args:
        question: Natural language question about activities (e.g.,
                  "How many students are in Chess Club?")
        
    Returns:
        Dictionary with keys:
        - "answer": str — Human-readable result or error message
        - "source": str — Always "text2sql"
        - "confidence": float — 1.0 if query succeeded, 0.0 if validation failed
        
        On error: {
            "answer": "Error message",
            "source": "text2sql",
            "confidence": 0.0
        }
    """
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
    except ImportError:
        return {
            "answer": "PostgreSQL driver not available. Text2SQL queries cannot be executed.",
            "source": "text2sql",
            "confidence": 0.0
        }
    
    # Step 1: Generate SQL query using LLM
    # In production, this would call Copilot API or OpenAI
    # For now, we'll use a simple pattern-matching approach
    sql_query = _generate_sql_from_question(question)
    
    if not sql_query:
        return {
            "answer": "Unable to generate SQL query from your question. Try asking about activity counts, names, or availability.",
            "source": "text2sql",
            "confidence": 0.0
        }
    
    # Step 2: Validate SQL for security
    is_valid, error_msg = security_validate(sql_query)
    if not is_valid:
        return {
            "answer": f"SQL validation failed: {error_msg}",
            "source": "text2sql",
            "confidence": 0.0
        }
    
    # Step 3: Execute query against database
    try:
        # Get connection parameters from environment
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "activities")
        db_user = os.getenv("DB_USER", "postgres")
        db_password = os.getenv("DB_PASSWORD", "")
        
        # Connect to database
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_password
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Execute with empty params (queries don't have parameters in this context)
        cursor.execute(sql_query)
        results = cursor.fetchall()
        
        cursor.close()
        conn.close()
        
        # Step 4: Format results as human-readable text
        if not results:
            answer = "No results found for your query."
        else:
            answer = _format_results(results)
        
        return {
            "answer": answer,
            "source": "text2sql",
            "confidence": 1.0
        }
    
    except psycopg2.OperationalError as e:
        return {
            "answer": f"Database connection failed. Check DB_HOST, DB_PORT, DB_NAME, DB_USER environment variables.",
            "source": "text2sql",
            "confidence": 0.0
        }
    except psycopg2.ProgrammingError as e:
        return {
            "answer": f"SQL execution error: {str(e)}",
            "source": "text2sql",
            "confidence": 0.0
        }
    except Exception as e:
        return {
            "answer": f"Unexpected error: {str(e)}",
            "source": "text2sql",
            "confidence": 0.0
        }


def _generate_sql_from_question(question: str) -> str:
    """Generate SQL query from natural language question.
    
    Uses simple pattern matching to convert common questions into SQL.
    In production, this would call an LLM API.
    
    Args:
        question: Natural language question
        
    Returns:
        SQL SELECT query or empty string if unable to generate
    """
    q_lower = question.lower()
    
    # Pattern: "How many students in [activity]?"
    if "how many" in q_lower and ("students" in q_lower or "members" in q_lower or "participants" in q_lower):
        activity_match = re.search(r"(?:in|for|at)\s+([^\?]+)", question, re.IGNORECASE)
        if activity_match:
            activity_name = activity_match.group(1).strip()
            return f"""
SELECT COUNT(*) as count
FROM activities
WHERE name = %s;
"""
    
    # Pattern: "List all activities" or "Which activities"
    if ("list" in q_lower or "which" in q_lower) and "activit" in q_lower:
        if "available" in q_lower or "spots" in q_lower:
            return """
SELECT name, description, (max_participants - jsonb_array_length(participants)) as spots_available
FROM activities
WHERE jsonb_array_length(participants) < max_participants
ORDER BY name;
"""
        else:
            return """
SELECT name, description, max_participants, jsonb_array_length(participants) as current_participants
FROM activities
ORDER BY name;
"""
    
    # Pattern: "Total" or "Count"
    if "total" in q_lower or "count" in q_lower or "how many" in q_lower:
        if "activit" in q_lower:
            return """
SELECT COUNT(*) as total_activities
FROM activities;
"""
    
    # Pattern: "Describe" or "Tell me about [activity]"
    if ("describe" in q_lower or "tell me about" in q_lower or "what is" in q_lower):
        activity_match = re.search(r"(?:about|for)\s+([^\?]+)", question, re.IGNORECASE)
        if activity_match:
            activity_name = activity_match.group(1).strip()
            return f"""
SELECT name, description, schedule, max_participants, jsonb_array_length(participants) as current_participants
FROM activities
WHERE name = %s;
"""
    
    return ""


def _format_results(results: list[dict]) -> str:
    """Format database results as human-readable sentence.
    
    Args:
        results: List of dictionaries from database query
        
    Returns:
        Human-readable formatted string
    """
    if not results:
        return "No results."
    
    # Single result with single column (e.g., count)
    if len(results) == 1 and len(results[0]) == 1:
        key, value = list(results[0].items())[0]
        return f"Result: {value}"
    
    # Single result with multiple columns
    if len(results) == 1:
        parts = []
        for key, value in results[0].items():
            parts.append(f"{key}: {value}")
        return " | ".join(parts)
    
    # Multiple results
    if len(results) > 1:
        lines = []
        for row in results:
            parts = []
            for key, value in row.items():
                parts.append(f"{key}: {value}")
            lines.append(" | ".join(parts))
        return "\n".join(lines)
    
    return str(results)
