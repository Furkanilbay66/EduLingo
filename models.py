import sqlite3
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'edulingo.db')


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            level TEXT DEFAULT 'A1',
            xp INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_activity DATE,
            placement_done INTEGER DEFAULT 0,
            dark_mode INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            meaning TEXT NOT NULL,
            translation TEXT,
            example_sentence TEXT,
            example_translation TEXT,
            level TEXT NOT NULL,
            category TEXT,
            image_url TEXT
        );

        CREATE TABLE IF NOT EXISTS user_vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            vocabulary_id INTEGER NOT NULL,
            learned INTEGER DEFAULT 0,
            favorite INTEGER DEFAULT 0,
            reviewed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (vocabulary_id) REFERENCES vocabulary(id),
            UNIQUE(user_id, vocabulary_id)
        );

        CREATE TABLE IF NOT EXISTS grammar_lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            level TEXT NOT NULL,
            explanation TEXT NOT NULL,
            examples TEXT NOT NULL,
            order_num INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS user_grammar_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            lesson_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            score INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (lesson_id) REFERENCES grammar_lessons(id),
            UNIQUE(user_id, lesson_id)
        );

        CREATE TABLE IF NOT EXISTS quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            quiz_type TEXT NOT NULL,
            options TEXT,
            correct_answer TEXT NOT NULL,
            level TEXT NOT NULL,
            category TEXT,
            lesson_id INTEGER,
            FOREIGN KEY (lesson_id) REFERENCES grammar_lessons(id)
        );

        CREATE TABLE IF NOT EXISTS user_quiz_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            user_answer TEXT,
            is_correct INTEGER,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
        );

        CREATE TABLE IF NOT EXISTS writing_submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            prompt TEXT NOT NULL,
            content TEXT NOT NULL,
            feedback TEXT,
            score INTEGER,
            submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS speaking_scenarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            level TEXT NOT NULL,
            dialogue TEXT NOT NULL,
            category TEXT
        );

        CREATE TABLE IF NOT EXISTS user_speaking_progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            scenario_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (scenario_id) REFERENCES speaking_scenarios(id),
            UNIQUE(user_id, scenario_id)
        );

        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            requirement_type TEXT NOT NULL,
            requirement_value INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS user_badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            badge_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (badge_id) REFERENCES badges(id),
            UNIQUE(user_id, badge_id)
        );

        CREATE TABLE IF NOT EXISTS placement_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            options TEXT NOT NULL,
            correct_answer TEXT NOT NULL,
            difficulty TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            challenge_date DATE NOT NULL,
            challenge_type TEXT NOT NULL,
            content TEXT NOT NULL,
            level TEXT NOT NULL,
            xp_reward INTEGER DEFAULT 20
        );

        CREATE TABLE IF NOT EXISTS user_daily_challenges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            challenge_id INTEGER NOT NULL,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (challenge_id) REFERENCES daily_challenges(id),
            UNIQUE(user_id, challenge_id)
        );

        CREATE TABLE IF NOT EXISTS writing_prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT NOT NULL,
            level TEXT NOT NULL,
            hint TEXT,
            category TEXT
        );
    ''')

    conn.commit()
    conn.close()


# ─── User Functions ───

def create_user(username, email, password):
    conn = get_db()
    try:
        conn.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username, email, generate_password_hash(password))
        )
        conn.commit()
        user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        return dict(user)
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()


def authenticate_user(username, password):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()
    if user and check_password_hash(user['password_hash'], password):
        return dict(user)
    return None


def get_user(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return dict(user) if user else None


def update_user_xp(user_id, xp_amount):
    conn = get_db()
    conn.execute('UPDATE users SET xp = xp + ? WHERE id = ?', (xp_amount, user_id))
    conn.commit()
    user = get_user(user_id)
    conn.close()
    check_and_award_badges(user_id)
    return user


def update_user_level(user_id, level):
    conn = get_db()
    conn.execute('UPDATE users SET level = ? WHERE id = ?', (level, user_id))
    conn.commit()
    conn.close()


def update_streak(user_id):
    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    today = datetime.now().date().isoformat()

    if user['last_activity']:
        last = datetime.fromisoformat(user['last_activity']).date() if isinstance(user['last_activity'], str) else user['last_activity']
        today_date = datetime.now().date()
        if isinstance(last, str):
            last = datetime.fromisoformat(last).date()
        diff = (today_date - last).days
        if diff == 1:
            conn.execute('UPDATE users SET streak = streak + 1, last_activity = ? WHERE id = ?', (today, user_id))
        elif diff > 1:
            conn.execute('UPDATE users SET streak = 1, last_activity = ? WHERE id = ?', (today, user_id))
        # same day: no change to streak
        else:
            conn.execute('UPDATE users SET last_activity = ? WHERE id = ?', (today, user_id))
    else:
        conn.execute('UPDATE users SET streak = 1, last_activity = ? WHERE id = ?', (today, user_id))

    conn.commit()
    conn.close()
    check_and_award_badges(user_id)


def set_placement_done(user_id):
    conn = get_db()
    conn.execute('UPDATE users SET placement_done = 1 WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()


def toggle_dark_mode(user_id):
    conn = get_db()
    user = get_user(user_id)
    new_mode = 0 if user['dark_mode'] else 1
    conn.execute('UPDATE users SET dark_mode = ? WHERE id = ?', (new_mode, user_id))
    conn.commit()
    conn.close()
    return new_mode


# ─── Vocabulary Functions ───

def get_daily_vocabulary(user_id, level, limit=10):
    conn = get_db()
    words = conn.execute('''
        SELECT v.* FROM vocabulary v
        LEFT JOIN user_vocabulary uv ON v.id = uv.vocabulary_id AND uv.user_id = ?
        WHERE v.level = ? AND (uv.learned IS NULL OR uv.learned = 0)
        ORDER BY RANDOM()
        LIMIT ?
    ''', (user_id, level, limit)).fetchall()
    conn.close()
    return [dict(w) for w in words]


def get_all_vocabulary(level):
    conn = get_db()
    words = conn.execute('SELECT * FROM vocabulary WHERE level = ? ORDER BY category, word', (level,)).fetchall()
    conn.close()
    return [dict(w) for w in words]


def mark_word_learned(user_id, vocab_id):
    conn = get_db()
    conn.execute('''
        INSERT INTO user_vocabulary (user_id, vocabulary_id, learned, reviewed_at)
        VALUES (?, ?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, vocabulary_id) DO UPDATE SET learned = 1, reviewed_at = CURRENT_TIMESTAMP
    ''', (user_id, vocab_id))
    conn.commit()
    conn.close()


def toggle_favorite_word(user_id, vocab_id):
    conn = get_db()
    existing = conn.execute(
        'SELECT * FROM user_vocabulary WHERE user_id = ? AND vocabulary_id = ?',
        (user_id, vocab_id)
    ).fetchone()

    if existing:
        new_fav = 0 if existing['favorite'] else 1
        conn.execute(
            'UPDATE user_vocabulary SET favorite = ? WHERE user_id = ? AND vocabulary_id = ?',
            (new_fav, user_id, vocab_id)
        )
    else:
        conn.execute(
            'INSERT INTO user_vocabulary (user_id, vocabulary_id, favorite) VALUES (?, ?, 1)',
            (user_id, vocab_id)
        )
    conn.commit()
    conn.close()


def get_favorite_words(user_id):
    conn = get_db()
    words = conn.execute('''
        SELECT v.* FROM vocabulary v
        JOIN user_vocabulary uv ON v.id = uv.vocabulary_id
        WHERE uv.user_id = ? AND uv.favorite = 1
    ''', (user_id,)).fetchall()
    conn.close()
    return [dict(w) for w in words]


def get_learned_word_count(user_id):
    conn = get_db()
    count = conn.execute(
        'SELECT COUNT(*) as cnt FROM user_vocabulary WHERE user_id = ? AND learned = 1',
        (user_id,)
    ).fetchone()['cnt']
    conn.close()
    return count


# ─── Grammar Functions ───

def get_grammar_lessons(level):
    conn = get_db()
    lessons = conn.execute(
        'SELECT * FROM grammar_lessons WHERE level = ? ORDER BY order_num',
        (level,)
    ).fetchall()
    conn.close()
    return [dict(l) for l in lessons]


def get_grammar_lesson(lesson_id):
    conn = get_db()
    lesson = conn.execute('SELECT * FROM grammar_lessons WHERE id = ?', (lesson_id,)).fetchone()
    conn.close()
    return dict(lesson) if lesson else None


def complete_grammar_lesson(user_id, lesson_id, score):
    conn = get_db()
    conn.execute('''
        INSERT INTO user_grammar_progress (user_id, lesson_id, completed, score, completed_at)
        VALUES (?, ?, 1, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, lesson_id) DO UPDATE SET completed = 1, score = MAX(score, ?), completed_at = CURRENT_TIMESTAMP
    ''', (user_id, lesson_id, score, score))
    conn.commit()
    conn.close()


def get_user_grammar_progress(user_id):
    conn = get_db()
    progress = conn.execute(
        'SELECT lesson_id, completed, score FROM user_grammar_progress WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    conn.close()
    return {p['lesson_id']: dict(p) for p in progress}


# ─── Quiz Functions ───

def get_quizzes_by_level(level, limit=10):
    conn = get_db()
    quizzes = conn.execute(
        'SELECT * FROM quizzes WHERE level = ? ORDER BY RANDOM() LIMIT ?',
        (level, limit)
    ).fetchall()
    conn.close()
    parsed = []
    for quiz in quizzes:
        q = dict(quiz)
        if q.get('options'):
            try:
                q['options'] = json.loads(q['options'])
            except (json.JSONDecodeError, TypeError):
                q['options'] = []
        parsed.append(q)
    return parsed


def get_quizzes_by_lesson(lesson_id):
    conn = get_db()
    quizzes = conn.execute(
        'SELECT * FROM quizzes WHERE lesson_id = ? ORDER BY id',
        (lesson_id,)
    ).fetchall()
    conn.close()
    parsed = []
    for quiz in quizzes:
        q = dict(quiz)
        if q.get('options'):
            try:
                q['options'] = json.loads(q['options'])
            except (json.JSONDecodeError, TypeError):
                q['options'] = []
        parsed.append(q)
    return parsed


def save_quiz_result(user_id, quiz_id, user_answer, is_correct):
    conn = get_db()
    conn.execute(
        'INSERT INTO user_quiz_results (user_id, quiz_id, user_answer, is_correct) VALUES (?, ?, ?, ?)',
        (user_id, quiz_id, user_answer, is_correct)
    )
    conn.commit()
    conn.close()


def get_user_quiz_stats(user_id):
    conn = get_db()
    stats = conn.execute('''
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN is_correct = 1 THEN 1 ELSE 0 END) as correct
        FROM user_quiz_results WHERE user_id = ?
    ''', (user_id,)).fetchone()
    conn.close()
    return dict(stats)


# ─── Writing Functions ───

def get_writing_prompts(level):
    conn = get_db()
    prompts = conn.execute(
        'SELECT * FROM writing_prompts WHERE level = ? ORDER BY RANDOM()',
        (level,)
    ).fetchall()
    conn.close()
    return [dict(p) for p in prompts]


def save_writing_submission(user_id, prompt, content, feedback, score):
    conn = get_db()
    conn.execute(
        'INSERT INTO writing_submissions (user_id, prompt, content, feedback, score) VALUES (?, ?, ?, ?, ?)',
        (user_id, prompt, content, feedback, score)
    )
    conn.commit()
    conn.close()


def get_user_writings(user_id):
    conn = get_db()
    writings = conn.execute(
        'SELECT * FROM writing_submissions WHERE user_id = ? ORDER BY submitted_at DESC',
        (user_id,)
    ).fetchall()
    conn.close()
    return [dict(w) for w in writings]


# ─── Speaking Functions ───

def get_speaking_scenarios(level):
    conn = get_db()
    scenarios = conn.execute(
        'SELECT * FROM speaking_scenarios WHERE level = ? ORDER BY id',
        (level,)
    ).fetchall()
    conn.close()
    return [dict(s) for s in scenarios]


def get_speaking_scenario(scenario_id):
    conn = get_db()
    scenario = conn.execute('SELECT * FROM speaking_scenarios WHERE id = ?', (scenario_id,)).fetchone()
    conn.close()
    return dict(scenario) if scenario else None


def complete_speaking_scenario(user_id, scenario_id):
    conn = get_db()
    conn.execute('''
        INSERT INTO user_speaking_progress (user_id, scenario_id, completed, completed_at)
        VALUES (?, ?, 1, CURRENT_TIMESTAMP)
        ON CONFLICT(user_id, scenario_id) DO UPDATE SET completed = 1, completed_at = CURRENT_TIMESTAMP
    ''', (user_id, scenario_id))
    conn.commit()
    conn.close()


def get_user_speaking_progress(user_id):
    conn = get_db()
    progress = conn.execute(
        'SELECT scenario_id, completed FROM user_speaking_progress WHERE user_id = ?',
        (user_id,)
    ).fetchall()
    conn.close()
    return {p['scenario_id']: dict(p) for p in progress}


# ─── Badge Functions ───

def get_all_badges():
    conn = get_db()
    badges = conn.execute('SELECT * FROM badges ORDER BY id').fetchall()
    conn.close()
    return [dict(b) for b in badges]


def get_user_badges(user_id):
    conn = get_db()
    badges = conn.execute('''
        SELECT b.*, ub.earned_at FROM badges b
        JOIN user_badges ub ON b.id = ub.badge_id
        WHERE ub.user_id = ?
        ORDER BY ub.earned_at DESC
    ''', (user_id,)).fetchall()
    conn.close()
    return [dict(b) for b in badges]


def check_and_award_badges(user_id):
    conn = get_db()
    user = get_user(user_id)
    all_badges = get_all_badges()
    user_badge_ids = {b['id'] for b in get_user_badges(user_id)}

    for badge in all_badges:
        if badge['id'] in user_badge_ids:
            continue

        awarded = False
        if badge['requirement_type'] == 'streak' and user['streak'] >= badge['requirement_value']:
            awarded = True
        elif badge['requirement_type'] == 'xp' and user['xp'] >= badge['requirement_value']:
            awarded = True
        elif badge['requirement_type'] == 'vocab':
            count = get_learned_word_count(user_id)
            if count >= badge['requirement_value']:
                awarded = True
        elif badge['requirement_type'] == 'quiz':
            stats = get_user_quiz_stats(user_id)
            if stats['total'] and stats['total'] >= badge['requirement_value']:
                awarded = True
        elif badge['requirement_type'] == 'grammar':
            progress = get_user_grammar_progress(user_id)
            completed = sum(1 for p in progress.values() if p['completed'])
            if completed >= badge['requirement_value']:
                awarded = True

        if awarded:
            try:
                conn.execute(
                    'INSERT INTO user_badges (user_id, badge_id) VALUES (?, ?)',
                    (user_id, badge['id'])
                )
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()


# ─── Placement Test Functions ───

def get_placement_questions():
    conn = get_db()
    questions = conn.execute('SELECT * FROM placement_questions ORDER BY difficulty, id').fetchall()
    conn.close()
    parsed = []
    for question in questions:
        q = dict(question)
        if q.get('options'):
            try:
                q['options'] = json.loads(q['options'])
            except (json.JSONDecodeError, TypeError):
                q['options'] = []
        parsed.append(q)
    return parsed


def calculate_level(score, total):
    pct = (score / total) * 100 if total > 0 else 0
    if pct >= 80:
        return 'B2'
    elif pct >= 60:
        return 'B1'
    elif pct >= 40:
        return 'A2'
    else:
        return 'A1'


# ─── Leaderboard ───

def get_leaderboard(limit=20):
    conn = get_db()
    users = conn.execute(
        'SELECT id, username, level, xp, streak FROM users ORDER BY xp DESC LIMIT ?',
        (limit,)
    ).fetchall()
    conn.close()
    return [dict(u) for u in users]


# ─── Dashboard Stats ───

def get_dashboard_stats(user_id):
    user = get_user(user_id)
    quiz_stats = get_user_quiz_stats(user_id)
    vocab_learned = get_learned_word_count(user_id)
    grammar_progress = get_user_grammar_progress(user_id)
    grammar_completed = sum(1 for p in grammar_progress.values() if p['completed'])
    badges = get_user_badges(user_id)

    return {
        'user': user,
        'quiz_total': quiz_stats['total'] or 0,
        'quiz_correct': quiz_stats['correct'] or 0,
        'vocab_learned': vocab_learned,
        'grammar_completed': grammar_completed,
        'badge_count': len(badges),
        'recent_badges': badges[:3]
    }
