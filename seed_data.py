#!/usr/bin/env python3
"""
Script pour ajouter des données de test à ROBO TUNISIE
Utile pour voir comment fonctionne le site avant de créer vos propres compétitions
"""

import sqlite3
from werkzeug.security import generate_password_hash

def seed_database():
    """Ajoute des données de test à la base de données"""
    
    conn = sqlite3.connect('robo_tunisie.db')
    c = conn.cursor()
    
    # Clubs de test
    clubs_data = [
        ('EPI Robotics', 'contact@epirobotics.tn', '123456', '+216 70 000 000', 'Tunis', 'https://facebook.com/epirobotics', 'https://instagram.com/epirobotics', None),
        ('FSM Robots Club', 'info@fsmrobots.tn', '123456', '+216 71 000 000', 'Sfax', 'https://facebook.com/fsmrobots', None, None),
        ('ISET Sousse Robotique', 'robotics@isetsousse.tn', '123456', '+216 73 000 000', 'Sousse', 'https://facebook.com/isetsousserobotic', 'https://instagram.com/isetsousserobotic', None),
        ('ESPRIT Robotics', 'espritrobots@esprit.tn', '123456', '+216 70 111 111', 'Tunis', 'https://facebook.com/espritrobots', None, None),
        ('ENIM ROBOT Lab', 'robot@enim.tn', '123456', '+216 73 222 222', 'Monastir', 'https://facebook.com/enimrobot', 'https://instagram.com/enimrobot', None),
        ('ENI Carthage Robotique', 'robotics@enicarthage.tn', '123456', '+216 70 333 333', 'Carthage', 'https://facebook.com/enicarthagerobotics', None, None),
    ]
    
    print("📝 Ajout des clubs de test...")
    for club in clubs_data:
        try:
            # Hash du mot de passe
            hashed_pwd = generate_password_hash(club[2])
            c.execute('''INSERT INTO clubs (name, email, password, phone, city, facebook, instagram, linkedin)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                     (club[0], club[1], hashed_pwd, club[3], club[4], club[5], club[6], club[7]))
            print(f"  ✓ {club[0]}")
        except sqlite3.IntegrityError:
            print(f"  ⚠️  {club[0]} déjà existe")
    
    conn.commit()
    
    # Récupérer les IDs des clubs
    clubs = {}
    for club_name in [c[0] for c in clubs_data]:
        result = c.execute('SELECT id FROM clubs WHERE name = ?', (club_name,)).fetchone()
        if result:
            clubs[club_name] = result[0]
    
    # Compétitions de test
    competitions_data = [
        (clubs['EPI Robotics'], 'EPI Robots Day 5.0', '2024-04-19', 'École Polytechnique de Tunisie', 
         'Découvrez la 5ème édition de notre compétition annuelle de robotique!',
         'Défi de navigation autonome, sumo robots, construction créative',
         50, '2024-04-10', 'day@epirobotics.tn', '+216 70 000 001'),
        
        (clubs['FSM Robots Club'], 'FSM JUNIOR 1.0', '2024-04-19', 'Faculté des Sciences de Sfax',
         'Une compétition spécialement conçue pour les jeunes talents en robotique.',
         'Épreuves pour débutants et intermédiaires, focus sur l\'apprentissage',
         40, '2024-04-12', 'junior@fsmrobots.tn', '+216 71 000 001'),
        
        (clubs['ISET Sousse Robotique'], 'SQUIDBOTS 6.0', '2024-04-26', 'ISET Sousse',
         'La plus grande compétition de Sousse avec équipes de toute la Tunisie!',
         'Compétition multidisciplinaire: football robotique, défis de navigation, combats sumo',
         100, '2024-04-18', 'squid@isetsousse.tn', '+216 73 000 001'),
        
        (clubs['ESPRIT Robotics'], 'ESPRIT RAS ROBOTS 4.0', '2024-04-26', 'ESPRIT',
         'Rejoignez le challenge robotique le plus compétitif de Tunis.',
         'Équipes avancées, épreuves difficiles, prix attractifs',
         60, '2024-04-16', 'ras@espritrobots.tn', '+216 70 111 112'),
        
        (clubs['ENIM ROBOT Lab'], 'ENIM ROBOT 11', '2024-05-03', 'École Nationale d\'Ingénieurs de Monastir',
         'Événement annuel majeur pour la robotique en Tunisie Centrale.',
         'Défi de construction, course autonome, présentations techniques',
         75, '2024-04-25', 'competition@enim.tn', '+216 73 222 223'),
        
        (clubs['ENI Carthage Robotique'], 'CarthaBot 1.0', '2024-05-10', 'ENI Carthage',
         'Première édition de notre compétition prestigieuse à Carthage.',
         'Toutes catégories bienvenues, atmosphère conviviale et compétitive',
         80, '2024-04-30', 'carthabot@enicarthage.tn', '+216 70 333 334'),
    ]
    
    print("\n🤖 Ajout des compétitions de test...")
    competition_ids = {}
    for idx, comp in enumerate(competitions_data):
        try:
            c.execute('''INSERT INTO competitions 
                        (club_id, name, date, location, description, challenges, max_participants, registration_deadline, contact_email, contact_phone)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', comp)
            comp_id = c.lastrowid
            competition_ids[comp[1]] = comp_id
            print(f"  ✓ {comp[1]}")
        except sqlite3.IntegrityError as e:
            print(f"  ⚠️  {comp[1]} déjà existe")
    
    conn.commit()
    
    # Réseaux sociaux de test
    print("\n🌐 Ajout des réseaux sociaux...")
    for comp_name, comp_id in competition_ids.items():
        try:
            c.execute('INSERT INTO social_links (competition_id, platform, url) VALUES (?, ?, ?)',
                     (comp_id, 'Facebook', f'https://facebook.com/{comp_name.replace(" ", "").lower()}'))
            c.execute('INSERT INTO social_links (competition_id, platform, url) VALUES (?, ?, ?)',
                     (comp_id, 'Instagram', f'https://instagram.com/{comp_name.replace(" ", "_").lower()}'))
            print(f"  ✓ Réseaux pour {comp_name}")
        except:
            pass
    
    conn.commit()
    
    print("\n✅ Données de test ajoutées avec succès!")
    print("\n📝 Comptes de test créés:")
    print("  Email: contact@epirobotics.tn")
    print("  Mot de passe: 123456")
    print("\n" + "="*50)
    print("⚠️  IMPORTANT: Changez ces mots de passe en production!")
    print("="*50)
    
    conn.close()

if __name__ == '__main__':
    print("🌱 ROBO TUNISIE - Générateur de données de test\n")
    try:
        seed_database()
    except Exception as e:
        print(f"❌ Erreur: {e}")
        print("   Assurez-vous que l'application a déjà créé la base de données.")
        print("   Lancez d'abord: python robo_tunisie_app.py")
