from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import psycopg
from psycopg.rows import dict_row
from psycopg import IntegrityError
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)

# Configuration (Support variables d'environnement)
app.secret_key = os.environ.get('SECRET_KEY', 'robo_tunisie_secret_2024')
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

# Configuration
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Database path (Support Render persistent volume)
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    raise RuntimeError('DATABASE_URL environment variable is required for PostgreSQL')

# Database initialization
def init_db():
    """Créer les tables PostgreSQL si elles n'existent pas"""
    with get_db() as conn:
        with conn.cursor() as c:
            c.execute('''CREATE TABLE IF NOT EXISTS clubs (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                phone TEXT,
                city TEXT,
                facebook TEXT,
                instagram TEXT,
                linkedin TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            c.execute('''CREATE TABLE IF NOT EXISTS competitions (
                id BIGSERIAL PRIMARY KEY,
                club_id BIGINT NOT NULL REFERENCES clubs(id),
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                location TEXT NOT NULL,
                description TEXT,
                challenges TEXT,
                max_participants INTEGER,
                registration_deadline TEXT,
                website TEXT,
                contact_email TEXT,
                contact_phone TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            c.execute('''CREATE TABLE IF NOT EXISTS documents (
                id BIGSERIAL PRIMARY KEY,
                competition_id BIGINT NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                file_path TEXT NOT NULL,
                file_type TEXT,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            c.execute('''CREATE TABLE IF NOT EXISTS social_links (
                id BIGSERIAL PRIMARY KEY,
                competition_id BIGINT NOT NULL REFERENCES competitions(id) ON DELETE CASCADE,
                platform TEXT NOT NULL,
                url TEXT NOT NULL
            )''')

# Helper functions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_db():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row, connect_timeout=15)


def login_required_club(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'club_id' not in session:
            return redirect(url_for('club_login'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== PUBLIC PAGES ====================

@app.route('/')
def index():
    """Page d'accueil - liste toutes les compétitions"""
    conn = get_db()
    
    # Filtres
    search = request.args.get('search', '').lower()
    location_filter = request.args.get('location', '').lower()
    
    query = '''SELECT c.*, cl.name as club_name, cl.facebook, cl.instagram, cl.linkedin
               FROM competitions c
               JOIN clubs cl ON c.club_id = cl.id
               ORDER BY c.date ASC'''
    
    competitions = conn.execute(query).fetchall()
    
    # Appliquer filtres
    competitions = [
        comp for comp in competitions
        if (search == '' or search in comp['name'].lower() or search in comp['club_name'].lower())
        and (location_filter == '' or location_filter in comp['location'].lower())
    ]
    
    locations = set(comp['location'] for comp in conn.execute(
        'SELECT DISTINCT location FROM competitions'
    ).fetchall())
    
    conn.close()
    
    return render_template('public_index.html', 
                         competitions=competitions,
                         locations=sorted(locations),
                         search=search,
                         location_filter=location_filter)

@app.route('/competition/<int:competition_id>')
def competition_detail(competition_id):
    """Détails d'une compétition"""
    conn = get_db()
    
    comp = conn.execute('''
        SELECT c.*, cl.name as club_name, cl.facebook, cl.instagram, cl.linkedin, cl.phone, cl.email
        FROM competitions c
        JOIN clubs cl ON c.club_id = cl.id
        WHERE c.id = %s
    ''', (competition_id,)).fetchone()
    
    if not comp:
        conn.close()
        return redirect(url_for('index'))
    
    # Documents
    documents = conn.execute(
        'SELECT * FROM documents WHERE competition_id = %s ORDER BY upload_date DESC',
        (competition_id,)
    ).fetchall()
    
    # Social links
    socials = conn.execute(
        'SELECT platform, url FROM social_links WHERE competition_id = %s',
        (competition_id,)
    ).fetchall()
    
    conn.close()
    
    return render_template('competition_detail.html',
                         competition=comp,
                         documents=documents,
                         socials=socials)

@app.route('/downloads/<filename>')
def download_file(filename):
    """Télécharger un fichier"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# ==================== CLUB AUTHENTICATION ====================

@app.route('/club/login', methods=['GET', 'POST'])
def club_login():
    """Login pour les clubs"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        conn = get_db()
        club = conn.execute('SELECT * FROM clubs WHERE email = %s', (email,)).fetchone()
        conn.close()
        
        if club and check_password_hash(club['password'], password):
            session['club_id'] = club['id']
            session['club_name'] = club['name']
            session['club_email'] = club['email']
            return redirect(url_for('club_dashboard'))
        else:
            return render_template('club_login.html', error='Email ou mot de passe incorrect')
    
    return render_template('club_login.html')

@app.route('/club/register', methods=['GET', 'POST'])
def club_register():
    """Inscription pour les clubs"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone', '')
        city = request.form.get('city', '')
        
        conn = get_db()
        
        # Vérifier doublon
        existing = conn.execute('SELECT * FROM clubs WHERE email = %s OR name = %s', 
                               (email, name)).fetchone()
        if existing:
            conn.close()
            return render_template('club_register.html', 
                                 error='Email ou nom de club déjà utilisé')
        
        # Créer le club
        try:
            conn.execute('''INSERT INTO clubs (name, email, password, phone, city)
                           VALUES (%s, %s, %s, %s, %s)''',
                        (name, email, generate_password_hash(password), phone, city))
            conn.commit()
            conn.close()
            
            # Auto-login
            club = get_db().execute('SELECT id FROM clubs WHERE email = %s', (email,)).fetchone()
            session['club_id'] = club['id']
            session['club_name'] = name
            session['club_email'] = email
            
            return redirect(url_for('club_dashboard'))
        except Exception as e:
            conn.close()
            return render_template('club_register.html', error=f'Erreur: {str(e)}')
    
    return render_template('club_register.html')

@app.route('/club/logout')
def club_logout():
    session.clear()
    return redirect(url_for('index'))

# ==================== CLUB DASHBOARD ====================

@app.route('/club/dashboard')
@login_required_club
def club_dashboard():
    """Dashboard du club"""
    conn = get_db()
    
    competitions = conn.execute('''
        SELECT * FROM competitions WHERE club_id = %s ORDER BY date DESC
    ''', (session['club_id'],)).fetchall()
    
    conn.close()
    
    return render_template('club_dashboard.html', competitions=competitions)

@app.route('/club/new-competition', methods=['GET', 'POST'])
@login_required_club
def new_competition():
    """Créer une nouvelle compétition"""
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        description = request.form.get('description')
        challenges = request.form.get('challenges')
        max_participants = request.form.get('max_participants', 0)
        registration_deadline = request.form.get('registration_deadline')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        
        conn = get_db()
        
        try:
            cursor = conn.execute('''
                INSERT INTO competitions 
                (club_id, name, date, location, description, challenges, 
                 max_participants, registration_deadline, contact_email, contact_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', (session['club_id'], name, date, location, description, challenges,
                  max_participants, registration_deadline, contact_email, contact_phone))
            
            conn.commit()
            competition_id = cursor.fetchone()['id']
            conn.close()
            
            return redirect(url_for('edit_competition', competition_id=competition_id))
        except Exception as e:
            conn.close()
            return render_template('new_competition.html', error=str(e))
    
    return render_template('new_competition.html')

@app.route('/club/edit-competition/<int:competition_id>', methods=['GET', 'POST'])
@login_required_club
def edit_competition(competition_id):
    """Éditer une compétition"""
    conn = get_db()
    
    comp = conn.execute('''
        SELECT * FROM competitions WHERE id = %s AND club_id = %s
    ''', (competition_id, session['club_id'])).fetchone()
    
    if not comp:
        conn.close()
        return redirect(url_for('club_dashboard'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')
        location = request.form.get('location')
        description = request.form.get('description')
        challenges = request.form.get('challenges')
        max_participants = request.form.get('max_participants', 0)
        registration_deadline = request.form.get('registration_deadline')
        contact_email = request.form.get('contact_email')
        contact_phone = request.form.get('contact_phone')
        
        try:
            conn.execute('''
                UPDATE competitions 
                SET name=%s, date=%s, location=%s, description=%s, challenges=%s,
                    max_participants=%s, registration_deadline=%s, contact_email=%s, contact_phone=%s
                WHERE id = %s
            ''', (name, date, location, description, challenges,
                  max_participants, registration_deadline, contact_email, contact_phone, competition_id))
            
            conn.commit()
            conn.close()
            
            return redirect(url_for('edit_competition', competition_id=competition_id, 
                                  message='Compétition mise à jour'))
        except Exception as e:
            conn.close()
            return render_template('edit_competition.html', competition=comp, error=str(e))
    
    # Documents et réseaux
    documents = conn.execute(
        'SELECT * FROM documents WHERE competition_id = %s', (competition_id,)
    ).fetchall()
    
    socials = conn.execute(
        'SELECT * FROM social_links WHERE competition_id = %s', (competition_id,)
    ).fetchall()
    
    conn.close()
    
    return render_template('edit_competition.html', 
                         competition=comp,
                         documents=documents,
                         socials=socials,
                         message=request.args.get('message'))

# ==================== DOCUMENTS & SOCIALS ====================

@app.route('/club/upload-document/<int:competition_id>', methods=['POST'])
@login_required_club
def upload_document(competition_id):
    """Upload un cahier de charges"""
    conn = get_db()
    
    # Vérifier ownership
    comp = conn.execute(
        'SELECT club_id FROM competitions WHERE id = %s', (competition_id,)
    ).fetchone()
    
    if not comp or comp['club_id'] != session['club_id']:
        conn.close()
        return jsonify({'error': 'Non autorisé'}), 403
    
    if 'file' not in request.files:
        return jsonify({'error': 'Pas de fichier'}), 400
    
    file = request.files['file']
    title = request.form.get('title', file.filename)
    
    if file.filename == '':
        return jsonify({'error': 'Fichier vide'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Format non autorisé (PDF, DOC, DOCX)'}), 400
    
    filename = secure_filename(f"{competition_id}_{int(datetime.now().timestamp())}_{file.filename}")
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    conn.execute('''
        INSERT INTO documents (competition_id, title, file_path, file_type)
        VALUES (%s, %s, %s, %s)
    ''', (competition_id, title, filename, file.filename.rsplit('.', 1)[1].lower()))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True}), 201

@app.route('/club/delete-document/<int:doc_id>', methods=['POST'])
@login_required_club
def delete_document(doc_id):
    """Supprimer un document"""
    conn = get_db()
    
    doc = conn.execute('SELECT d.*, c.club_id FROM documents d JOIN competitions c ON d.competition_id = c.id WHERE d.id = %s', (doc_id,)).fetchone()
    
    if not doc or doc['club_id'] != session['club_id']:
        conn.close()
        return jsonify({'error': 'Non autorisé'}), 403
    
    # Supprimer le fichier
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], doc['file_path'])
    if os.path.exists(filepath):
        os.remove(filepath)
    
    conn.execute('DELETE FROM documents WHERE id = %s', (doc_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

@app.route('/club/add-social/<int:competition_id>', methods=['POST'])
@login_required_club
def add_social(competition_id):
    """Ajouter un lien réseaux"""
    conn = get_db()
    
    comp = conn.execute(
        'SELECT club_id FROM competitions WHERE id = %s', (competition_id,)
    ).fetchone()
    
    if not comp or comp['club_id'] != session['club_id']:
        conn.close()
        return jsonify({'error': 'Non autorisé'}), 403
    
    platform = request.form.get('platform')
    url = request.form.get('url')
    
    conn.execute('''
        INSERT INTO social_links (competition_id, platform, url)
        VALUES (%s, %s, %s)
    ''', (competition_id, platform, url))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True}), 201

@app.route('/club/delete-social/<int:social_id>', methods=['POST'])
@login_required_club
def delete_social(social_id):
    """Supprimer un lien réseaux"""
    conn = get_db()
    
    social = conn.execute('SELECT s.*, c.club_id FROM social_links s JOIN competitions c ON s.competition_id = c.id WHERE s.id = %s', (social_id,)).fetchone()
    
    if not social or social['club_id'] != session['club_id']:
        conn.close()
        return jsonify({'error': 'Non autorisé'}), 403
    
    conn.execute('DELETE FROM social_links WHERE id = %s', (social_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    init_db()
    
    # Support port dynamique (Render, Heroku, etc.)
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=DEBUG
    )
