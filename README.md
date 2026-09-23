# 🤖 ROBO TUNISIE - Plateforme des Compétitions de Robotique

Une plateforme web moderne pour découvrir et gérer les compétitions de robotique en Tunisie.

## 🎯 Fonctionnalités

### 🌐 Pour les Visiteurs/Participants
- 📋 Catalogue complet de toutes les compétitions
- 🔍 Filtrage par date et lieu
- 📄 Accès aux cahiers de charges
- 🌐 Liens vers les réseaux sociaux des clubs
- 📞 Informations de contact
- 📝 Inscription à une compétition (à venir)

### 🏛️ Pour les Clubs/Organisateurs
- **Authentification sécurisée** : Login/Register
- **Dashboard personnel** : Vue d'ensemble de vos compétitions
- **Création de compétitions** : Formulaire complet
- **Édition avancée** :
  - Informations détaillées
  - Upload cahiers de charges (PDF, DOC, DOCX)
  - Gestion des liens réseaux sociaux
  - Contact et informations techniques

## 📋 Structure du Projet

```
ROBO_TUNISIE/
├── robo_tunisie_app.py          # Application Flask principale
├── robo_tunisie.db              # Base de données SQLite (créée auto)
├── requirements.txt              # Dépendances Python
├── templates/
│   ├── base.html                # Template de base
│   ├── public_index.html         # Accueil public
│   ├── competition_detail.html   # Détails compétition
│   ├── club_login.html           # Connexion club
│   ├── club_register.html        # Inscription club
│   ├── club_dashboard.html       # Dashboard club
│   ├── new_competition.html      # Créer compétition
│   ├── edit_competition.html     # Éditer compétition
│   ├── 404.html                  # Page erreur
│   └── 500.html                  # Page erreur
├── uploads/                      # Dossier documents uploadés
└── README.md                     # Ce fichier
```

## 🚀 Installation & Lancement

### Prérequis
- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes d'Installation

#### 1️⃣ Cloner/Télécharger le projet
```bash
git clone <votre-repo>
cd ROBO_TUNISIE
```

#### 2️⃣ Créer un environnement virtuel (recommandé)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

#### 4️⃣ Lancer l'application
```bash
python robo_tunisie_app.py
```

#### 5️⃣ Accéder au site
```
Local : http://localhost:5000
Réseau : http://<votre_ip>:5000
```

## 🌐 Utilisation

### 👥 Flux Visiteur

1. **Consulter les compétitions**
   - Allez sur http://localhost:5000
   - Parcourez le tableau de toutes les compétitions
   - Cliquez sur "Détails" pour voir plus

2. **Voir les détails**
   - Consultez les informations complètes
   - Téléchargez les cahiers de charges
   - Accédez aux réseaux sociaux du club

### 🏛️ Flux Club

#### Inscription
1. Cliquez sur "Club Login" en haut
2. Cliquez "Créer un compte"
3. Remplissez le formulaire d'inscription
4. Confirmez → Vous êtes automatiquement connecté

#### Créer une Compétition
1. Allez dans "Mon Club" (apparaît si connecté)
2. Cliquez "Nouvelle Compétition"
3. Remplissez les informations :
   - Nom, Date, Lieu
   - Description et Défis
   - Contact et paramètres
4. Cliquez "Créer"

#### Éditer une Compétition
1. Dans le dashboard, cliquez "Éditer" sur la compétition
2. **Onglet Informations** : Modifiez les détails
3. **Onglet Cahiers de Charges** :
   - Uploadez des fichiers PDF/DOC/DOCX
   - Donnez un titre à chaque document
   - Supprimez si nécessaire
4. **Onglet Réseaux** :
   - Ajoutez les liens Facebook, Instagram, etc.
   - Les participants verront ces liens

#### Se Déconnecter
- Cliquez "Déconnexion" dans la navigation

## 🎨 Design & Palette

- **Couleurs** : Purple (#7c3aed) → Pink (#ec4899) → Accent Gold
- **Typographie** : 
  - Titres : Playfair Display (serif élégant)
  - Texte : Poppins (sans-serif moderne)
- **Thème** : Dark mode avec gradient purple/pink
- **Responsive** : Fonctionne sur PC, tablettes, mobiles

## 📊 Base de Données

SQLite avec 4 tables principales :

```sql
-- Clubs
clubs (id, name, email, password, phone, city, socials...)

-- Compétitions
competitions (id, club_id, name, date, location, description, challenges...)

-- Documents (Cahiers de charges)
documents (id, competition_id, title, file_path, file_type...)

-- Réseaux Sociaux
social_links (id, competition_id, platform, url)
```

La base de données est **créée automatiquement** au premier lancement.

## 🔐 Sécurité

- ✅ Mots de passe hashés avec werkzeug.security
- ✅ Sessions Flask sécurisées
- ✅ Vérification propriété (clubs ne peuvent éditer que leurs compétitions)
- ✅ Validation des fichiers uploadés
- ✅ Protection des téléchargements

## 🚀 Déploiement Réseau Local

Pour accéder depuis un autre PC sur le même réseau :

```bash
# Trouvez votre IP
ipconfig  # Windows
ifconfig  # Linux/Mac

# Lancez l'app (accessible sur toutes les interfaces)
python robo_tunisie_app.py
# (Déjà configuré avec host='0.0.0.0')

# Accédez depuis un autre PC
http://<votre_ip>:5000
```

## 📝 TODO & Améliorations Futures

- [ ] Système d'inscription des équipes (formulaire + gestion)
- [ ] Tableaux de résultats en live
- [ ] Notifications par email
- [ ] Statistiques et graphiques (Chart.js)
- [ ] Upload de photos de la compétition
- [ ] Système de commentaires/avis
- [ ] Export PDF des cahiers
- [ ] Calendrier iCal
- [ ] Version mobile app
- [ ] Intégration avec Instagram/Facebook API

## 🛠️ Troubleshooting

### Erreur : "Port 5000 already in use"
```bash
# Changez le port dans robo_tunisie_app.py ligne 262
app.run(debug=True, host='0.0.0.0', port=5001)  # ← Changez en 5001
```

### Erreur : "ModuleNotFoundError: No module named 'flask'"
```bash
pip install Flask==3.0.0 werkzeug==3.0.0
```

### Fichiers uploadés non trouvés
Vérifiez que le dossier `uploads/` existe. S'il ne existe pas :
```bash
mkdir uploads  # Linux/Mac
mkdir uploads  # Windows
```

### Réinitialiser la base de données
```bash
# Supprimez simplement le fichier
rm robo_tunisie.db
# Relancez l'app - une nouvelle base sera créée
python robo_tunisie_app.py
```

## 📞 Support & Contact

Pour les questions ou suggestions, veuillez :
- Ouvrir une issue sur GitHub
- Contacter l'administrateur

## 📄 Licence

MIT License - Libre d'utilisation

---

**Développé avec ❤️ pour la communauté robotique tunisienne** 🇹🇳

Bienvenue sur ROBO TUNISIE! 🤖✨
