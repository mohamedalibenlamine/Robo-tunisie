# 🚀 Déployer sur Render (Gratuit & Facile)

**Render** est la meilleure option pour déployer gratuitement une app Flask en ligne.

## 🌟 Avantages
✅ Gratuit (vraiment!)  
✅ URL public gratuit  
✅ HTTPS automatique  
✅ Déploiement auto depuis GitHub  
✅ Pas de carte de crédit requise  
✅ Base de données incluse  

---

## 📋 Prérequis

1. Compte GitHub (gratuit: https://github.com)
2. Compte Render (gratuit: https://render.com)
3. Tes fichiers du projet

---

## 🔧 Étape 1: Préparer les Fichiers

### 1.1 Créer `Procfile` (instructions pour Render)

Crée un fichier nommé `Procfile` (pas d'extension) à la racine:

```
web: gunicorn robo_tunisie_app:app
```

### 1.2 Mettre à jour `requirements.txt`

Ajoute `gunicorn` (serveur web production):

```
Flask==3.0.0
werkzeug==3.0.0
gunicorn==21.2.0
```

### 1.3 Créer `.gitignore` (fichiers à ignorer)

Crée `.gitignore`:

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
robo_tunisie.db
uploads/
.DS_Store
*.egg-info/
dist/
build/
```

### 1.4 Structure finale

```
ROBO_TUNISIE/
├── robo_tunisie_app.py
├── requirements.txt          ← MODIFIÉ (gunicorn ajouté)
├── Procfile                  ← NOUVEAU
├── .gitignore                ← NOUVEAU
├── seed_data.py
├── README.md
└── templates/
    └── (tous les fichiers HTML)
```

---

## 🔑 Étape 2: Mettre en Ligne sur GitHub

### 2.1 Créer un repo GitHub

1. Allez sur https://github.com/new
2. Remplissez:
   - **Repository name**: `robo-tunisie`
   - **Description**: `Plateforme compétitions robotique Tunisie`
   - **Public** (sélectionné)
3. Cliquez "Create repository"

### 2.2 Pousser le code (Command Line)

**Windows (PowerShell) ou Linux/Mac (Terminal)**:

```bash
# 1. Allez dans votre dossier du projet
cd ROBO_TUNISIE

# 2. Initialisez git
git init
git add .
git commit -m "Initial commit: ROBO TUNISIE app"

# 3. Connectez au repo GitHub
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/robo-tunisie.git

# 4. Poussez le code
git push -u origin main
```

**Remplacez `VOTRE_USERNAME`** par votre username GitHub.

### 2.3 Vérifier sur GitHub

Allez sur https://github.com/VOTRE_USERNAME/robo-tunisie  
Vous devriez voir tous vos fichiers ✓

---

## 🌐 Étape 3: Déployer sur Render

### 3.1 Créer un service Web

1. Allez sur https://render.com
2. Cliquez "Sign up" → GitHub (connexion facile)
3. Cliquez "+ New" → "Web Service"
4. Sélectionnez votre repo `robo-tunisie`
5. Cliquez "Connect"

### 3.2 Configurer le service

Remplissez les champs:

| Champ | Valeur |
|-------|--------|
| **Name** | `robo-tunisie` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn robo_tunisie_app:app` |
| **Instance Type** | `Free` |

### 3.3 Déployer!

Cliquez "Create Web Service"

**Attendre 2-3 minutes** pendant le déploiement... ⏳

---

## ✅ Votre Site est EN LIGNE!

Une fois terminé, vous verrez un URL comme:

```
https://robo-tunisie-xxxxx.onrender.com
```

**Copier cette URL et testez-la!** 🎉

---

## 🔄 Redéployer Automatiquement

Chaque fois que vous **poussez du code sur GitHub**:

```bash
git add .
git commit -m "Mes modifications"
git push
```

**Render redéploie automatiquement** en quelques secondes! ✨

---

## 🐛 Dépannage

### ❌ "Build failed"

Allez sur Render → Votre service → "Logs"  
Cherchez l'erreur

**Solution commune**: Oubli de `Procfile` ou typo

### ❌ "Application Error"

Vérifiez les logs dans Render (onglet "Logs")

### ❌ "Port Error"

Modifiez `robo_tunisie_app.py` (dernière ligne):

```python
if __name__ == '__main__':
    init_db()
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=int(port), debug=False)
```

Et ajoutez en haut du fichier:

```python
import os
```

### ❌ "Base de données vide"

Render peut réinitialiser la BD à chaque déploiement.

**Solution**: Modifier `robo_tunisie_app.py` pour utiliser une BD persistante:

```python
# Ligne 27 (modifier le chemin de la BD):
def init_db():
    conn = sqlite3.connect('/data/robo_tunisie.db')  # Render persistent volume
    # ... rest du code
```

Ou laisser la BD se réinitialiser, puis lancer `seed_data.py` en local.

---

## 📝 Variables d'Environnement (Optionnel)

Pour plus de sécurité, créez des variables:

1. Allez sur Render → Votre service → "Environment"
2. Ajoutez:

```
SECRET_KEY=votre_clé_secrète_ici
DEBUG=False
```

3. Dans `robo_tunisie_app.py`:

```python
import os

app.secret_key = os.environ.get('SECRET_KEY', 'robo_tunisie_secret_2024')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'
```

---

## 🎉 Résumé Rapide

| Étape | Durée | Action |
|-------|-------|--------|
| 1 | 5 min | Modifier `requirements.txt` + créer `Procfile` + `.gitignore` |
| 2 | 10 min | Créer repo GitHub + pousser le code |
| 3 | 5 min | Créer service Render |
| 4 | 3 min | Attendre déploiement |
| **TOTAL** | **23 min** | **Votre site est en ligne!** ✨ |

---

## 📱 Tester

1. Allez sur votre URL Render
2. Testez:
   - [ ] Page d'accueil charge
   - [ ] Créer compte club fonctionne
   - [ ] Créer compétition fonctionne
   - [ ] Upload documents fonctionne
   - [ ] URL publiquement accessible

---

## 🔗 Votre URL Public

```
https://robo-tunisie-xxxxx.onrender.com
```

**Partagez cette URL partout!** 📢

- Avec les clubs tunisiens
- Sur les réseaux sociaux
- Sur WhatsApp/Discord
- Sur votre CV

---

## 💡 Tips Avancés

### Domaine personnalisé
Pour https://robo-tunisie.tn (payant):
1. Achetez le domaine sur Namecheap/OVH (~5$/an)
2. Render → Votre service → "Custom Domain"
3. Suivez les instructions

### Base de données professionelle
Si vous avez besoin d'une vraie BD:
1. Render → "+ New" → "PostgreSQL"
2. Connectez à votre app (voir docs Render)

### Plus de puissance
Passez de `Free` à `Paid` ($7/mois) pour meilleure performance

---

## 📞 Besoin d'aide?

- **Docs Render**: https://render.com/docs
- **Forum Render**: https://render.com/community
- **Status**: https://status.render.com

---

**C'est fait! Votre site est maintenant accessible 24/7 de partout! 🌍✨**
