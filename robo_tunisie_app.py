from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import sqlite3
import os
from datetime import datetime
from functools import wraps

# ============ CONFIGURATION ============
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-robo-2026')

# Créer les dossiers nécessaires
os.makedirs('uploads', exist_ok=True)
os.makedirs('instance', exist_ok=True)

# Base de données
DATABASE = 'robo_tunisie.db'
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# ============ DATABASE ============
def get_db():
    """Connexion base de données"""
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Créer les tables si elles n'existent pas"""
    try:
        db = get_db()
        c = db.cursor()
        
        # Table clubs
        c.execute('''CREATE TABLE IF NOT EXISTS clubs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        
        # Table competitions
        c.execute('''CREATE TABLE IF NOT EXISTS competitions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            club_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            date TEXT NOT NULL,
            location TEXT NOT NULL,
            description TEXT,
            challenges TEXT,
            max_participants TEXT,
            registration_deadline TEXT,
            website TEXT,
            contact_email TEXT NOT NULL,
            contact_phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(club_id) REFERENCES clubs(id)
        )''')
        
        # Table documents
        c.execute('''CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            file_path TEXT NOT NULL,
            file_type TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(competition_id) REFERENCES competitions(id) ON DELETE CASCADE
        )''')
        
        # Table social_links
        c.execute('''CREATE TABLE IF NOT EXISTS social_links (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            competition_id INTEGER NOT NULL,
            platform TEXT NOT NULL,
            url TEXT NOT NULL,
            FOREIGN KEY(competition_id) REFERENCES competitions(id) ON DELETE CASCADE
        )''')
        
        db.commit()
        db.close()
        print("✅ Base de données initialisée")
    except Exception as e:
        print(f"❌ Erreur init_db: {e}")

# Initialiser la base de données
init_db()

# ============ HELPERS ============
def allowed_file(filename):
    """Vérifier l'extension du fichier"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def login_required_club(f):
    """Décorateur vérifier connexion"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'club_id' not in session:
            return redirect(url_for('club_login'))
        return f(*args, **kwargs)
    return decorated_function

# ============ PUBLIC ROUTES ============
@app.route('/')
def index():
    """Accueil - voir toutes les compétitions"""
    try:
        search = request.args.get('search', '').strip()
        location_filter = request.args.get('location', '').strip()
        
        db = get_db()
        c = db.cursor()
        
        if search:
            c.execute("""SELECT id, name, date, location, description, club_id 
                        FROM competitions 
                        WHERE name LIKE ? OR description LIKE ? OR location LIKE ?
                        ORDER BY date DESC""", 
                     (f'%{search}%', f'%{search}%', f'%{search}%'))
        else:
            c.execute("SELECT id, name, date, location, description, club_id FROM competitions ORDER BY date DESC")
        
        competitions = c.fetchall()
        
        # Ajouter le nom du club
        competitions_with_club = []
        for comp in competitions:
            c.execute("SELECT name FROM clubs WHERE id = ?", (comp['club_id'],))
            club = c.fetchone()
            competitions_with_club.append({
                'id': comp['id'],
                'name': comp['name'],
                'date': comp['date'],
                'location': comp['location'],
                'description': comp['description'],
                'club_name': club['name'] if club else 'Club'
            })
        
        db.close()
        return render_template('public_index.html', competitions=competitions_with_club)
    except Exception as e:
        print(f"❌ Erreur index: {e}")
        return render_template('500.html'), 500

@app.route('/competition/<int:comp_id>')
def competition_detail(comp_id):
    """Détails d'une compétition"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("SELECT * FROM competitions WHERE id = ?", (comp_id,))
        competition = c.fetchone()
        
        if not competition:
            return render_template('404.html'), 404
        
        # Info club
        c.execute("SELECT name FROM clubs WHERE id = ?", (competition['club_id'],))
        club = c.fetchone()
        
        # Documents
        c.execute("SELECT * FROM documents WHERE competition_id = ?", (comp_id,))
        documents = c.fetchall()
        
        # Réseaux
        c.execute("SELECT * FROM social_links WHERE competition_id = ?", (comp_id,))
        social_links = c.fetchall()
        
        db.close()
        
        return render_template('competition_detail.html',
                             competition=competition,
                             club_name=club['name'] if club else 'Club',
                             documents=documents,
                             social_links=social_links)
    except Exception as e:
        print(f"❌ Erreur competition_detail: {e}")
        return render_template('500.html'), 500

@app.route('/downloads/<path:filename>')
def download_file(filename):
    """Télécharger un fichier"""
    try:
        file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
        if not os.path.exists(file_path):
            return render_template('404.html'), 404
        return send_file(file_path, as_attachment=True)
    except Exception as e:
        print(f"❌ Erreur download: {e}")
        return render_template('500.html'), 500

# ============ AUTH ROUTES ============
@app.route('/club/login', methods=['GET', 'POST'])
def club_login():
    """Connexion club"""
    if request.method == 'POST':
        try:
            email = request.form.get('email', '').strip()
            password = request.form.get('password', '').strip()
            
            if not email or not password:
                return render_template('club_login.html', error="Email et mot de passe requis")
            
            db = get_db()
            c = db.cursor()
            c.execute("SELECT * FROM clubs WHERE email = ?", (email,))
            club = c.fetchone()
            db.close()
            
            if club and check_password_hash(club['password'], password):
                session['club_id'] = club['id']
                session['club_name'] = club['name']
                return redirect(url_for('club_dashboard'))
            else:
                return render_template('club_login.html', error="Email ou mot de passe incorrect")
        except Exception as e:
            print(f"❌ Erreur login: {e}")
            return render_template('club_login.html', error="Erreur interne")
    
    return render_template('club_login.html')

@app.route('/club/register', methods=['GET', 'POST'])
def club_register():
    """Créer un compte club"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            phone = request.form.get('phone', '').strip()
            city = request.form.get('city', '').strip()
            password = request.form.get('password', '').strip()
            
            if not all([name, email, password]):
                return render_template('club_register.html', error="Nom, email et mot de passe requis")
            
            db = get_db()
            c = db.cursor()
            
            hashed_pw = generate_password_hash(password)
            c.execute("""INSERT INTO clubs (name, email, phone, city, password)
                        VALUES (?, ?, ?, ?, ?)""",
                     (name, email, phone, city, hashed_pw))
            db.commit()
            
            # Auto-login
            c.execute("SELECT id FROM clubs WHERE email = ?", (email,))
            club_id = c.fetchone()['id']
            session['club_id'] = club_id
            session['club_name'] = name
            
            db.close()
            return redirect(url_for('club_dashboard'))
        except sqlite3.IntegrityError:
            return render_template('club_register.html', error="Email ou nom déjà utilisé")
        except Exception as e:
            print(f"❌ Erreur register: {e}")
            return render_template('club_register.html', error="Erreur interne")
    
    return render_template('club_register.html')

@app.route('/club/logout')
def club_logout():
    """Déconnexion"""
    session.clear()
    return redirect(url_for('index'))

# ============ CLUB DASHBOARD ============
@app.route('/club/dashboard')
@login_required_club
def club_dashboard():
    """Dashboard du club"""
    try:
        db = get_db()
        c = db.cursor()
        c.execute("""SELECT * FROM competitions 
                    WHERE club_id = ? 
                    ORDER BY created_at DESC""",
                 (session['club_id'],))
        competitions = c.fetchall()
        db.close()
        
        return render_template('club_dashboard.html',
                              competitions=competitions,
                              club_name=session.get('club_name', 'Club'))
    except Exception as e:
        print(f"❌ Erreur dashboard: {e}")
        return render_template('500.html'), 500

@app.route('/club/new-competition', methods=['GET', 'POST'])
@login_required_club
def new_competition():
    """Créer une compétition"""
    if request.method == 'POST':
        try:
            name = request.form.get('name', '').strip()
            date = request.form.get('date', '').strip()
            location = request.form.get('location', '').strip()
            description = request.form.get('description', '').strip()
            challenges = request.form.get('challenges', '').strip()
            contact_email = request.form.get('contact_email', '').strip()
            contact_phone = request.form.get('contact_phone', '').strip()
            
            if not all([name, date, location, contact_email, contact_phone]):
                return render_template('new_competition.html', error="Champs obligatoires manquants")
            
            db = get_db()
            c = db.cursor()
            c.execute("""INSERT INTO competitions 
                        (club_id, name, date, location, description, challenges, 
                         contact_email, contact_phone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                     (session['club_id'], name, date, location, description, 
                      challenges, contact_email, contact_phone))
            db.commit()
            
            comp_id = c.lastrowid
            db.close()
            
            return redirect(url_for('edit_competition', comp_id=comp_id))
        except Exception as e:
            print(f"❌ Erreur new_competition: {e}")
            return render_template('new_competition.html', error="Erreur interne")
    
    return render_template('new_competition.html')

@app.route('/club/edit-competition/<int:comp_id>', methods=['GET', 'POST'])
@login_required_club
def edit_competition(comp_id):
    """Éditer une compétition"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("""SELECT * FROM competitions 
                    WHERE id = ? AND club_id = ?""",
                 (comp_id, session['club_id']))
        competition = c.fetchone()
        
        if not competition:
            return render_template('404.html'), 404
        
        if request.method == 'POST':
            name = request.form.get('name', '').strip()
            date = request.form.get('date', '').strip()
            location = request.form.get('location', '').strip()
            description = request.form.get('description', '').strip()
            contact_email = request.form.get('contact_email', '').strip()
            contact_phone = request.form.get('contact_phone', '').strip()
            
            c.execute("""UPDATE competitions 
                        SET name=?, date=?, location=?, description=?, 
                            contact_email=?, contact_phone=?
                        WHERE id=? AND club_id=?""",
                     (name, date, location, description, contact_email, 
                      contact_phone, comp_id, session['club_id']))
            db.commit()
        
        c.execute("SELECT * FROM documents WHERE competition_id = ?", (comp_id,))
        documents = c.fetchall()
        
        c.execute("SELECT * FROM social_links WHERE competition_id = ?", (comp_id,))
        social_links = c.fetchall()
        
        db.close()
        
        return render_template('edit_competition.html',
                              competition=competition,
                              documents=documents,
                              social_links=social_links)
    except Exception as e:
        print(f"❌ Erreur edit_competition: {e}")
        return render_template('500.html'), 500

# ============ FILE UPLOAD ============
@app.route('/club/upload-document/<int:comp_id>', methods=['POST'])
@login_required_club
def upload_document(comp_id):
    """Uploader un document"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("SELECT club_id FROM competitions WHERE id = ?", (comp_id,))
        competition = c.fetchone()
        
        if not competition or competition['club_id'] != session['club_id']:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403
        
        file = request.files.get('file')
        title = request.form.get('title', '').strip()
        
        if not file or file.filename == '' or not title:
            db.close()
            return jsonify({'error': 'File and title required'}), 400
        
        if not allowed_file(file.filename):
            db.close()
            return jsonify({'error': 'File type not allowed'}), 400
        
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)
        
        c.execute("""INSERT INTO documents 
                    (competition_id, title, file_path, file_type) 
                    VALUES (?, ?, ?, ?)""",
                 (comp_id, title, filename, filename.rsplit('.', 1)[1].lower()))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Erreur upload: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/club/delete-document/<int:doc_id>', methods=['POST'])
@login_required_club
def delete_document(doc_id):
    """Supprimer un document"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("""SELECT d.*, c.club_id FROM documents d 
                    JOIN competitions c ON d.competition_id = c.id 
                    WHERE d.id = ?""", (doc_id,))
        doc = c.fetchone()
        
        if not doc or doc['club_id'] != session['club_id']:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403
        
        file_path = os.path.join(UPLOAD_FOLDER, doc['file_path'])
        if os.path.exists(file_path):
            os.remove(file_path)
        
        c.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Erreur delete_document: {e}")
        return jsonify({'error': str(e)}), 500

# ============ SOCIAL LINKS ============
@app.route('/club/add-social/<int:comp_id>', methods=['POST'])
@login_required_club
def add_social(comp_id):
    """Ajouter un réseau social"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("SELECT club_id FROM competitions WHERE id = ?", (comp_id,))
        competition = c.fetchone()
        
        if not competition or competition['club_id'] != session['club_id']:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403
        
        platform = request.form.get('platform', '').strip()
        url = request.form.get('url', '').strip()
        
        c.execute("""INSERT INTO social_links (competition_id, platform, url) 
                    VALUES (?, ?, ?)""",
                 (comp_id, platform, url))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Erreur add_social: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/club/delete-social/<int:social_id>', methods=['POST'])
@login_required_club
def delete_social(social_id):
    """Supprimer un réseau social"""
    try:
        db = get_db()
        c = db.cursor()
        
        c.execute("""SELECT s.*, c.club_id FROM social_links s 
                    JOIN competitions c ON s.competition_id = c.id 
                    WHERE s.id = ?""", (social_id,))
        social = c.fetchone()
        
        if not social or social['club_id'] != session['club_id']:
            db.close()
            return jsonify({'error': 'Unauthorized'}), 403
        
        c.execute("DELETE FROM social_links WHERE id = ?", (social_id,))
        db.commit()
        db.close()
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"❌ Erreur delete_social: {e}")
        return jsonify({'error': str(e)}), 500

# ============ ERROR HANDLERS ============
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('500.html'), 500

# ============ MAIN ============
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)