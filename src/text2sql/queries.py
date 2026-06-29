SQL_QUERIES = {
    "q1": {
        "sql": """-- How many students have signed up for Chess Club?
SELECT COUNT(*)
FROM signups s
JOIN activities a ON s.activity_id = a.id
WHERE a.name = %s;""",
        "params": ("Chess Club",),
    },
    "q2": {
        "sql": """-- List all activities that still have spots available.
SELECT a.id, a.name, a.description, a.max_participants, a.schedule
FROM activities a
LEFT JOIN signups s ON s.activity_id = a.id
GROUP BY a.id, a.name, a.description, a.max_participants, a.schedule
HAVING COUNT(s.id) < a.max_participants;""",
        "params": (),
    },
    "q3": {
        "sql": """-- Which activities is student Alice Johnson signed up for?
SELECT a.name
FROM activities a
JOIN signups s ON s.activity_id = a.id
WHERE s.student_name = %s
ORDER BY a.name;""",
        "params": ("Alice Johnson",),
    },
    "q4": {
        "sql": """-- Show activities with more than 10 max participants.
SELECT id, name, description, max_participants, schedule
FROM activities
WHERE max_participants > %s
ORDER BY max_participants DESC, name;""",
        "params": (10,),
    },
    "q5": {
        "sql": """-- Remove Alice Johnson from Basketball Team.
DELETE FROM signups
WHERE student_name = %s
  AND activity_id = (
      SELECT id
      FROM activities
      WHERE name = %s
  );""",
        "params": ("Alice Johnson", "Basketball Team"),
    },
}