# 🐍 Déployer sur PythonAnywhere (Gratuit & Simple)

**PythonAnywhere** est spécialisée en Python et super facile pour Flask!

## 🌟 Avantages
✅ Gratuit avec limite généreuse  
✅ Spécialisée en Python  
✅ Pas de "sleep mode" sur le plan gratuit limité  
✅ Interface web simple  
✅ Accès SFTP/SSH  
✅ Base de données incluse  

---

## 📋 Prérequis

1. Compte PythonAnywhere (gratuit: https://www.pythonanywhere.com)
2. Tes fichiers du projet
3. Pas besoin de GitHub

---

## 🚀 Déploiement Étape par Étape

### Étape 1: Créer un Compte

1. Allez sur https://www.pythonanywhere.com/registration/register/beginner/
2. Remplissez le formulaire:
   - **Username**: Votre username (sera dans l'URL)
   - **Email**: Votre email
   - **Password**: Mot de passe
3. Cliquez "Register"
4. Vérifiez votre email

### Étape 2: Ouvrir une Console Web

1. Une fois connecté, allez dans l'onglet "Consoles"
2. Cliquez "New console" → "Bash console"
3. Vous verrez un terminal

### Étape 3: Créer le Dossier du Projet

Dans la console:

```bash
# Créez le dossier
mkdir robo-tunisie
cd robo-tunisie

# Clonez depuis GitHub (ou uploadez les fichiers manuellement)
git clone https://github.com/VOTRE_USERNAME/robo-tunisie.git .
# (remplacez VOTRE_USERNAME)

# Ou téléchargez les fichiers directement (voir "Files" dans PythonAnywhere)
```

### Étape 4: Créer un Environnement Virtuel

Dans la console:

```bash
# Créez l'environnement virtuel
mkvirtualenv --python=/usr/bin/python3.9 robo-env

# Installez les dépendances
pip install Flask==3.0.0 werkzeug==3.0.0
```

(L'environnement s'active automatiquement)

### Étape 5: Configurer le Web App

1. Allez dans l'onglet "Web"
2. Cliquez "+ Add a new web app"
3. Sélectionnez votre domaine (ex: `votre_username.pythonanywhere.com`)
4. Cliquez "Next"
5. Sélectionnez "Flask"
6. Sélectionnez "Python 3.9"
7. Validez

### Étape 6: Modifier le Fichier WSGI

1. Dans "Web", cliquez sur "Code" → "WSGI configuration file"
2. Remplacez le contenu par:

```python
# ========== PythonAnywhere WSGI ==========
import sys
import os

# Ajouter le chemin du projet
path = '/home/{your_username}/robo-tunisie'
if path not in sys.path:
    sys.path.insert(0, path)

# Charger l'app
from robo_tunisie_app import app as application

# Configuration
application.secret_key = 'robo_tunisie_secret_2024'
```

**Remplacez `{your_username}`** par votre username PythonAnywhere.

### Étape 7: Configurer le Virtualenv

1. Dans "Web", trouvez "Virtualenv"
2. Entrez le chemin: `/home/votre_username/.virtualenvs/robo-env`

### Étape 8: Recharger

1. Cliquez le bouton "Reload" en haut de la page Web
2. Attendez 10-15 secondes

---

## ✅ C'est En Ligne!

Votre app est maintenant sur:

```
https://VOTRE_USERNAME.pythonanywhere.com
```

**Exemple**: `https://john.pythonanywhere.com`

---

## 🐛 Dépannage

### ❌ "ModuleNotFoundError: No module named 'flask'"

```bash
# Allez dans "Consoles" → "Bash console"
workon robo-env  # Activez l'environnement
pip install Flask==3.0.0 werkzeug==3.0.0
```

### ❌ "500 Internal Server Error"

1. Allez dans "Web" → "Log files"
2. Lisez le fichier `error.log`
3. Cherchez l'erreur

**Causes communes**:
- Import d'un module manquant
- Erreur dans WSGI config
- Chemin du projet incorrect

### ❌ "Can't find robo_tunisie_app"

Dans le fichier WSGI, vérifiez que:
```python
path = '/home/VOTRE_USERNAME/robo-tunisie'  # ← Correct?
```

### ❌ "Base de données non trouvée"

PythonAnywhere sauvegarde les fichiers.

Créez la base de données:

```bash
# Dans Bash console
cd /home/votre_username/robo-tunisie
python3 -c "from robo_tunisie_app import init_db; init_db()"

# Ou ajoutez les données de test
python3 seed_data.py
```

---

## 📁 Structure PythonAnywhere

```
/home/votre_username/
├── robo-tunisie/
│   ├── robo_tunisie_app.py
│   ├── requirements.txt
│   ├── templates/
│   ├── uploads/
│   └── robo_tunisie.db
└── .virtualenvs/
    └── robo-env/
        └── lib/python3.9/site-packages/
```

---

## 💾 Uploader les Fichiers

### Méthode 1: GitHub (Recommandée)
```bash
# Dans Bash console
cd /home/votre_username
git clone https://github.com/VOTRE_USERNAME/robo-tunisie.git
```

### Méthode 2: Interface Web
1. Onglet "Files"
2. Cliquez "Upload a file"
3. Sélectionnez vos fichiers

### Méthode 3: SFTP
1. Allez dans votre profil
2. Trouvez les détails SFTP
3. Utilisez FileZilla pour uploader

---

## 🔄 Redéployer (Mettre à Jour)

Si vous modifiez votre code:

### Depuis GitHub:
```bash
# Bash console
cd /home/votre_username/robo-tunisie
git pull
```

### Depuis des fichiers:
```bash
# Bash console
# Téléchargez vos fichiers via "Files"
```

### Puis rechargez:
1. Allez dans "Web"
2. Cliquez "Reload"

---

## 📊 Plan Gratuit vs Payant

| Feature | Gratuit | Payant |
|---------|---------|--------|
| Apps | 1 | Illimité |
| RAM | 512 MB | 1-2 GB |
| CPU | Partagé | Dédié |
| Uptime | Complet | Complet |
| Bases de données | SQLite | MySQL |
| Prix | Gratuit | $5/mois |

---

## 🎬 Résumé Rapide

```
1. Créez un compte PythonAnywhere
2. Ouvrez une Bash console
3. Uploadez les fichiers
4. Créez un virtualenv
5. Installez Flask
6. Configurez le WSGI
7. Reloadez
8. ✨ C'est en ligne!
```

**Durée**: 15-20 minutes

---

## 🌐 Accès Public

Votre URL:
```
https://VOTRE_USERNAME.pythonanywhere.com
```

**Partagez partout!**

---

## 📞 Support

- **Docs**: https://help.pythonanywhere.com/
- **Forum**: https://www.pythonanywhere.com/forums/
- **Chat**: Support live en haut à droite

---

**Votre app est maintenant en ligne 24/7! 🎉**
