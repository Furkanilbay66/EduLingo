import os
import json
import re
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from models import (
    init_db, create_user, authenticate_user, get_user, update_user_xp,
    update_user_level, update_streak, set_placement_done, toggle_dark_mode,
    get_daily_vocabulary, get_all_vocabulary, mark_word_learned, toggle_favorite_word,
    get_favorite_words, get_learned_word_count,
    get_grammar_lessons, get_grammar_lesson, complete_grammar_lesson, get_user_grammar_progress,
    get_quizzes_by_level, get_quizzes_by_lesson, save_quiz_result, get_user_quiz_stats,
    get_writing_prompts, save_writing_submission, get_user_writings,
    get_speaking_scenarios, get_speaking_scenario, complete_speaking_scenario, get_user_speaking_progress,
    get_all_badges, get_user_badges, check_and_award_badges,
    get_placement_questions, calculate_level,
    get_leaderboard, get_dashboard_stats
)
from seed_data import seed_all

app = Flask(__name__)
app.secret_key = os.urandom(32)
app.jinja_env.globals.update(max=max, min=min)

# ─── Initialize DB and Seed ───
with app.app_context():
    init_db()
    seed_all()


# ─── Auth Decorator ───
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


# ─── Context Processor ───
@app.context_processor
def inject_user():
    if 'user_id' in session:
        user = get_user(session['user_id'])
        return {'current_user': user}
    return {'current_user': None}


# ═══════════════════════════════════════════
# AUTH ROUTES
# ═══════════════════════════════════════════

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')

        if len(username) < 3:
            flash('Username must be at least 3 characters.', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters.', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match.', 'error')
            return render_template('register.html')

        user = create_user(username, email, password)
        if user:
            session['user_id'] = user['id']
            return redirect(url_for('placement_test'))
        else:
            flash('Username or email already exists.', 'error')

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = authenticate_user(username, password)
        if user:
            session['user_id'] = user['id']
            update_streak(user['id'])
            if not user['placement_done']:
                return redirect(url_for('placement_test'))
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))


# ═══════════════════════════════════════════
# PLACEMENT TEST
# ═══════════════════════════════════════════

@app.route('/placement-test')
@login_required
def placement_test():
    user = get_user(session['user_id'])
    if user['placement_done']:
        return redirect(url_for('dashboard'))
    questions = get_placement_questions()
    return render_template('placement_test.html', questions=questions)


@app.route('/placement-test/submit', methods=['POST'])
@login_required
def submit_placement():
    questions = get_placement_questions()
    score = 0
    total = len(questions)

    for q in questions:
        user_answer = request.form.get(f'q_{q["id"]}', '')
        if user_answer.strip().lower() == q['correct_answer'].strip().lower():
            score += 1

    level = calculate_level(score, total)
    update_user_level(session['user_id'], level)
    set_placement_done(session['user_id'])
    update_user_xp(session['user_id'], 50)

    return jsonify({
        'score': score,
        'total': total,
        'level': level,
        'percentage': round((score / total) * 100) if total > 0 else 0
    })


# ═══════════════════════════════════════════
# DASHBOARD
# ═══════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_user(session['user_id'])
    if not user['placement_done']:
        return redirect(url_for('placement_test'))
    update_streak(session['user_id'])
    stats = get_dashboard_stats(session['user_id'])
    return render_template('dashboard.html', stats=stats)


# ═══════════════════════════════════════════
# VOCABULARY
# ═══════════════════════════════════════════

@app.route('/vocabulary')
@login_required
def vocabulary():
    user = get_user(session['user_id'])
    selected_level = request.args.get('level', user['level'])
    if selected_level not in ('A1', 'A2', 'B1', 'B2'):
        selected_level = user['level']
    words = get_daily_vocabulary(user['id'], selected_level)
    all_words = get_all_vocabulary(selected_level)
    favorites = get_favorite_words(user['id'])
    fav_ids = {w['id'] for w in favorites}
    return render_template('vocabulary.html', words=words, all_words=all_words,
                         favorites=favorites, fav_ids=fav_ids,
                         selected_level=selected_level, user_level=user['level'])


@app.route('/vocabulary/learn/<int:vocab_id>', methods=['POST'])
@login_required
def learn_word(vocab_id):
    mark_word_learned(session['user_id'], vocab_id)
    update_user_xp(session['user_id'], 5)
    update_streak(session['user_id'])
    return jsonify({'success': True, 'xp_earned': 5})


@app.route('/vocabulary/favorite/<int:vocab_id>', methods=['POST'])
@login_required
def favorite_word(vocab_id):
    toggle_favorite_word(session['user_id'], vocab_id)
    return jsonify({'success': True})


# ═══════════════════════════════════════════
# GRAMMAR
# ═══════════════════════════════════════════

@app.route('/grammar')
@login_required
def grammar():
    user = get_user(session['user_id'])
    lessons = get_grammar_lessons(user['level'])
    progress = get_user_grammar_progress(user['id'])
    return render_template('grammar.html', lessons=lessons, progress=progress)


@app.route('/grammar/<int:lesson_id>')
@login_required
def grammar_lesson(lesson_id):
    lesson = get_grammar_lesson(lesson_id)
    if not lesson:
        flash('Lesson not found.', 'error')
        return redirect(url_for('grammar'))
    quizzes = get_quizzes_by_lesson(lesson_id)
    return render_template('grammar_lesson.html', lesson=lesson, quizzes=quizzes)


@app.route('/grammar/<int:lesson_id>/complete', methods=['POST'])
@login_required
def complete_lesson(lesson_id):
    data = request.get_json()
    score = data.get('score', 0)
    complete_grammar_lesson(session['user_id'], lesson_id, score)
    xp = 20 + (score * 2)
    update_user_xp(session['user_id'], xp)
    update_streak(session['user_id'])
    return jsonify({'success': True, 'xp_earned': xp})


# ═══════════════════════════════════════════
# QUIZZES
# ═══════════════════════════════════════════

@app.route('/quiz')
@login_required
def quiz():
    user = get_user(session['user_id'])
    return render_template('quiz.html', level=user['level'])


@app.route('/quiz/get', methods=['POST'])
@login_required
def get_quiz():
    user = get_user(session['user_id'])
    data = request.get_json() or {}
    level = data.get('level', user['level'])
    quizzes = get_quizzes_by_level(level, 10)

    for q in quizzes:
        if isinstance(q.get('options'), str):
            q['options'] = json.loads(q['options'])

    return jsonify({'quizzes': quizzes})


@app.route('/quiz/submit', methods=['POST'])
@login_required
def submit_quiz():
    data = request.get_json()
    results = data.get('results', [])
    correct_count = 0

    for r in results:
        is_correct = 1 if r.get('is_correct') else 0
        save_quiz_result(session['user_id'], r['quiz_id'], r['user_answer'], is_correct)
        if is_correct:
            correct_count += 1

    xp = correct_count * 10
    update_user_xp(session['user_id'], xp)
    update_streak(session['user_id'])

    return jsonify({
        'success': True,
        'correct': correct_count,
        'total': len(results),
        'xp_earned': xp
    })


# ═══════════════════════════════════════════
# WRITING
# ═══════════════════════════════════════════

@app.route('/writing')
@login_required
def writing():
    user = get_user(session['user_id'])
    prompts = get_writing_prompts(user['level'])
    history = get_user_writings(user['id'])
    return render_template('writing.html', prompts=prompts, history=history)


@app.route('/writing/check', methods=['POST'])
@login_required
def check_writing():
    data = request.get_json()
    prompt = data.get('prompt', '')
    content = data.get('content', '').strip()

    if not content:
        return jsonify({'error': 'Please write something.'}), 400

    feedback = []
    score = 100

    # Check sentence capitalization
    sentences = re.split(r'[.!?]+', content)
    for s in sentences:
        s = s.strip()
        if s and not s[0].isupper():
            feedback.append(f'Sentence should start with a capital letter: "{s[:30]}..."')
            score -= 5

    # Check punctuation
    if content and content[-1] not in '.!?':
        feedback.append('Your text should end with proper punctuation (. ! ?)')
        score -= 5

    # Check common grammar mistakes
    grammar_checks = [
        (r'\bi\b(?!\')', 'The pronoun "I" should always be capitalized.'),
        (r'\bdoesn\'t\s+\w+s\b', 'After "doesn\'t", use the base form of the verb (no -s).'),
        (r'\bdon\'t\s+\w+s\b', 'After "don\'t", use the base form of the verb (no -s).'),
        (r'\bmore\s+\w+er\b', 'Don\'t use "more" with comparative adjectives ending in -er.'),
        (r'\bhe\s+don\'t\b', 'Use "doesn\'t" with he/she/it, not "don\'t".'),
        (r'\bshe\s+don\'t\b', 'Use "doesn\'t" with he/she/it, not "don\'t".'),
        (r'\bit\s+don\'t\b', 'Use "doesn\'t" with he/she/it, not "don\'t".'),
        (r'\btheir\s+is\b', 'Did you mean "there is"? "Their" shows possession.'),
        (r'\bthey\s+is\b', 'Use "they are", not "they is".'),
        (r'\bwe\s+is\b', 'Use "we are", not "we is".'),
        (r'\byour\s+welcome\b', 'Did you mean "you\'re welcome"?'),
        (r'\bits\s+a\s+\w+\s+then\b', 'Did you mean "than" for comparison instead of "then"?'),
        (r'\bcould\s+of\b', 'Use "could have" instead of "could of".'),
        (r'\bshould\s+of\b', 'Use "should have" instead of "should of".'),
        (r'\bwould\s+of\b', 'Use "would have" instead of "would of".'),
    ]

    for pattern, message in grammar_checks:
        if re.search(pattern, content, re.IGNORECASE):
            feedback.append(message)
            score -= 10

    # Check word count
    words = content.split()
    if len(words) < 10:
        feedback.append('Try to write at least 10 words for better practice.')
        score -= 10
    elif len(words) >= 50:
        feedback.append('Great job writing a detailed response!')
        score += 5

    # Check for repeated words
    word_count = {}
    for w in words:
        clean = re.sub(r'[^\w]', '', w.lower())
        if clean and len(clean) > 3:
            word_count[clean] = word_count.get(clean, 0) + 1
    for w, c in word_count.items():
        if c > 3 and w not in ('that', 'this', 'with', 'from', 'have', 'they', 'been', 'were', 'your', 'their', 'about', 'would', 'there', 'which'):
            feedback.append(f'The word "{w}" is used {c} times. Try using synonyms for variety.')
            score -= 3

    score = max(0, min(100, score))

    if not feedback:
        feedback.append('Your writing looks good! Keep practicing to improve further.')

    xp = max(5, score // 5)
    update_user_xp(session['user_id'], xp)
    update_streak(session['user_id'])

    save_writing_submission(session['user_id'], prompt, content, json.dumps(feedback), score)

    return jsonify({
        'feedback': feedback,
        'score': score,
        'xp_earned': xp,
        'word_count': len(words)
    })


# ═══════════════════════════════════════════
# SPEAKING
# ═══════════════════════════════════════════

@app.route('/speaking')
@login_required
def speaking():
    user = get_user(session['user_id'])
    scenarios = get_speaking_scenarios(user['level'])
    progress = get_user_speaking_progress(user['id'])
    return render_template('speaking.html', scenarios=scenarios, progress=progress)


@app.route('/speaking/<int:scenario_id>')
@login_required
def speaking_scenario(scenario_id):
    scenario = get_speaking_scenario(scenario_id)
    if not scenario:
        flash('Scenario not found.', 'error')
        return redirect(url_for('speaking'))
    scenario['dialogue'] = json.loads(scenario['dialogue'])
    return render_template('speaking_scenario.html', scenario=scenario)


@app.route('/speaking/<int:scenario_id>/complete', methods=['POST'])
@login_required
def complete_speaking(scenario_id):
    complete_speaking_scenario(session['user_id'], scenario_id)
    update_user_xp(session['user_id'], 15)
    update_streak(session['user_id'])
    return jsonify({'success': True, 'xp_earned': 15})


# ═══════════════════════════════════════════
# PROFILE & SETTINGS
# ═══════════════════════════════════════════

@app.route('/profile')
@login_required
def profile():
    user = get_user(session['user_id'])
    earned_badges = get_user_badges(session['user_id'])
    stats = get_dashboard_stats(session['user_id'])
    return render_template('profile.html', user=user, earned_badges=earned_badges, stats=stats)


@app.route('/toggle-dark-mode', methods=['POST'])
@login_required
def toggle_dark():
    new_mode = toggle_dark_mode(session['user_id'])
    return jsonify({'dark_mode': new_mode})


@app.route('/change-level', methods=['POST'])
@login_required
def change_level():
    data = request.get_json()
    new_level = data.get('level', '')
    if new_level in ('A1', 'A2', 'B1', 'B2'):
        update_user_level(session['user_id'], new_level)
        return jsonify({'success': True, 'level': new_level})
    return jsonify({'success': False}), 400


# ═══════════════════════════════════════════
# LEADERBOARD & BADGES
# ═══════════════════════════════════════════

@app.route('/leaderboard')
@login_required
def leaderboard():
    leaderboard_data = get_leaderboard()
    return render_template('leaderboard.html', leaderboard=leaderboard_data)


@app.route('/badges')
@login_required
def badges():
    all_badges = get_all_badges()
    user_badges = get_user_badges(session['user_id'])
    earned_ids = {b['id'] for b in user_badges}
    return render_template('badges.html', all_badges=all_badges, earned_ids=earned_ids)


# ═══════════════════════════════════════════
# API HELPERS
# ═══════════════════════════════════════════

@app.route('/api/user-stats')
@login_required
def api_user_stats():
    stats = get_dashboard_stats(session['user_id'])
    return jsonify(stats)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
