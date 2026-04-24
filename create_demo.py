import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime
import random

DB = 'edulingo.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# Create demo user
pw = generate_password_hash('demo123')
c.execute(
    'INSERT INTO users (username, email, password_hash, level, xp, streak, placement_done, dark_mode, last_activity, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
    ('demo', 'demo@edulingo.com', pw, 'B1', 1250, 7, 1, 0, datetime.now().strftime('%Y-%m-%d'), datetime.now().isoformat())
)
user_id = c.lastrowid

# Mark some words as learned
c.execute("SELECT id FROM vocabulary WHERE level IN ('A1','A2') ORDER BY RANDOM() LIMIT 25")
for (vid,) in c.fetchall():
    c.execute(
        'INSERT OR IGNORE INTO user_vocabulary (user_id, vocabulary_id, learned, reviewed_at) VALUES (?,?,1,?)',
        (user_id, vid, datetime.now().isoformat())
    )

# Some quiz results
for i in range(15):
    c.execute(
        'INSERT INTO user_quiz_results (user_id, quiz_id, user_answer, is_correct, answered_at) VALUES (?,?,?,?,?)',
        (user_id, random.randint(1, 20), 'answer', random.choice([0, 1, 1, 1]), datetime.now().isoformat())
    )

# Award badges
for bid in [1, 2, 3, 4]:
    c.execute(
        'INSERT OR IGNORE INTO user_badges (user_id, badge_id, earned_at) VALUES (?,?,?)',
        (user_id, bid, datetime.now().isoformat())
    )

conn.commit()
conn.close()
print('Demo account created: demo / demo123')
