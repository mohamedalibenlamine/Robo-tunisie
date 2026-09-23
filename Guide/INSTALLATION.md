# ⚡ Installation Rapide ROBO TUNISIE

## 🎯 En 5 minutes, démarrez votre plateforme!

### Étape 1: Télécharger Python
Si vous n'avez pas Python:
- Allez sur https://www.python.org/downloads/
- Téléchargez Python 3.8+ (cochez "Add Python to PATH" si Windows)
- Installez

### Étape 2: Préparer le projet

```bash
# 1. Créez un dossier pour le projet
mkdir ROBO_TUNISIE
cd ROBO_TUNISIE

# 2. Copiez les fichiers:
# - robo_tunisie_app.py
# - requirements.txt
# - README.md
# - Dossier templates/ (avec tous les .html)
```

### Étape 3: Installez les dépendances

**Windows**:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux/Mac**:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Étape 4: Lancez l'application

```bash
python robo_tunisie_app.py
```

**Vous devriez voir** ✓
```
 * Running on http://127.0.0.1:5000
 * Restarting with reloader
```

### Étape 5: Accédez au site

**Depuis votre PC**:
```
http://localhost:5000
```

**Depuis un autre PC sur le réseau**:
```
http://<votre_ip>:5000
# Exemple: http://192.168.1.100:5000
```

---

## 🧪 Testez immédiatement!

### 1️⃣ Page d'accueil
- Allez sur http://localhost:5000
- Vous verrez un tableau vide (normal, pas de compétitions encore)

### 2️⃣ Créer un compte club
- Cliquez "Club Login" → "Créer un compte"
- Remplissez le formulaire:
  - Nom: `Mon Club Robotique`
  - Email: `monclub@example.com`
  - Mot de passe: `test123`
- Cliquez "Créer"

### 3️⃣ Créer votre première compétition
- Vous êtes maintenant connecté ✓
- Cliquez "Mon Club" → "Nouvelle Compétition"
- Remplissez:
  - Nom: `Robot Challenge 2024`
  - Date: `2024-04-15`
  - Lieu: `Tunis`
  - Description: `Une compétition incroyable!`
  - Email: `competiton@monclub.tn`
- Cliquez "Créer"

### 4️⃣ Ajouter des documents
- Cliquez "Éditer" sur votre compétition
- Onglet "Cahiers de Charges"
- Upload un fichier PDF (créez un fichier test.pdf vide si vous n'en avez pas)
- Donnez-lui un titre
- Cliquez "Uploader"

### 5️⃣ Ajouter des réseaux
- Onglet "Réseaux Sociaux"
- Plateforme: `Facebook`
- URL: `https://facebook.com/votreclub`
- Cliquez "Ajouter"

### 6️⃣ Voir le résultat public
- Cliquez "Voir" pour voir votre compétition
- Ou allez sur la page d'accueil
- Vous verrez votre compétition listée!

---

## 📁 Structure des fichiers (résumé)

```
ROBO_TUNISIE/
├── robo_tunisie_app.py           ← Application principale
├── requirements.txt               ← Dépendances (Flask, werkzeug)
├── robo_tunisie.db               ← BD SQLite (créée auto)
├── uploads/                       ← Documents uploadés
├── templates/
│   ├── base.html                 ← Mise en page commune
│   ├── public_index.html          ← Accueil
│   ├── competition_detail.html    ← Détails compétition
│   ├── club_login.html
│   ├── club_register.html
│   ├── club_dashboard.html        ← Espace club
│   ├── new_competition.html
│   ├── edit_competition.html      ← Éditer avec docs/réseaux
│   ├── 404.html et 500.html       ← Pages erreur
│   └── (autres templates)
├── README.md                      ← Documentation complète
└── INSTALLATION.md                ← Ce fichier
```

---

## 🎨 Personnaliser le design

Le design purple/pink est dans `templates/base.html`, section `<style>`.

**Changer les couleurs**:
```css
:root {
    --primary-purple: #7c3aed;  ← Changez-moi!
    --accent-pink: #ec4899;     ← Changez-moi!
}
```

---

## 🌐 Accès depuis un autre PC

1. Trouvez votre IP:
   - Windows: `ipconfig` → cherchez "IPv4 Address"
   - Linux/Mac: `ifconfig` → cherchez "inet"

2. Depuis l'autre PC, allez à:
   ```
   http://<votre_ip>:5000
   ```

3. **Important**: Les autres PC doivent être sur le même réseau WiFi/LAN

---

## 🛑 Arrêter l'application

```bash
Ctrl + C
```

(Si vous êtes dans l'environnement virtuel, il se désactive automatiquement)

---

## 📱 Redémarrer après fermeture

```bash
# Réactivez l'environnement virtuel
cd ROBO_TUNISIE

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

# Relancez
python robo_tunisie_app.py
```

---

## ✅ Checklist Déploiement

- [ ] Python 3.8+ installé
- [ ] Fichiers téléchargés dans un dossier
- [ ] `pip install -r requirements.txt` exécuté
- [ ] `python robo_tunisie_app.py` lancé sans erreur
- [ ] `http://localhost:5000` accessible
- [ ] Compte club créé avec succès
- [ ] Compétition créée avec succès
- [ ] Documents uploadés
- [ ] Réseaux sociaux ajoutés
- [ ] Page publique affiche la compétition

---

## 🆘 Aide Rapide

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError: flask` | `pip install -r requirements.txt` |
| Port 5000 occupé | `python robo_tunisie_app.py` puis changez port |
| Fichiers d'upload ne s'affichent pas | Vérifiez que dossier `uploads/` existe |
| Impossible de se connecter depuis un autre PC | Vérifiez que vous utilisez votre IP locale |
| BD corrompue | Supprimez `robo_tunisie.db` (sera recréée auto) |

---

## 🚀 C'est prêt! 

Votre plateforme ROBO TUNISIE fonctionne! 🎉

Pour plus d'infos, consultez `README.md` 📖
