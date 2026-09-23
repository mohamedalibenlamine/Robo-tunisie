# ⚡ QUICKSTART - Démarrer en 10 minutes!

## 📦 Prérequis
- Python 3.8+ (https://python.org)
- Les fichiers du projet

---

## 🚀 Démarrage (Copy/Paste Ready!)

### Windows (PowerShell)

```powershell
# 1. Créez le dossier et accédez
mkdir ROBO_TUNISIE
cd ROBO_TUNISIE

# 2. Copiez-y tous les fichiers du projet

# 3. Créez environnement virtuel
python -m venv venv
venv\Scripts\activate

# 4. Installez les dépendances
pip install -r requirements.txt

# 5. Lancez l'application
python robo_tunisie_app.py

# 6. Ouvrez votre navigateur
# http://localhost:5000
```

### Linux / Mac

```bash
# 1. Créez le dossier et accédez
mkdir ROBO_TUNISIE
cd ROBO_TUNISIE

# 2. Copiez-y tous les fichiers du projet

# 3. Créez environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 4. Installez les dépendances
pip install -r requirements.txt

# 5. Lancez l'application
python robo_tunisie_app.py

# 6. Ouvrez votre navigateur
# http://localhost:5000
```

---

## 🧪 Tester Immédiatement

### Étape 1: Ajouter données de test (OPTIONNEL)

```bash
python seed_data.py
```

Vous verrez:
```
📝 Ajout des clubs de test...
  ✓ EPI Robotics
  ✓ FSM Robots Club
  ...
✅ Données de test ajoutées avec succès!
```

### Étape 2: Vérifier dans le navigateur

**Si vous avez ajouté les données de test**:
- Allez à http://localhost:5000
- Vous verrez 6 compétitions listées
- Cliquez sur l'une pour voir les détails

**Créer votre propre compétition**:
1. Cliquez "Club Login" (en haut à droite)
2. Cliquez "Créer un compte"
3. Remplissez le formulaire:
   - Nom: `Mon Super Club`
   - Email: `monclub@example.com`
   - Mot de passe: `test123`
4. Cliquez "Créer"
5. Cliquez "Mon Club" → "Nouvelle Compétition"
6. Remplissez et créez votre compétition!

---

## 📱 Accès depuis un autre PC

**Trouvez votre IP**:
```bash
# Windows
ipconfig

# Linux/Mac
ifconfig
```

Cherchez `IPv4 Address` (Windows) ou `inet` (Linux/Mac) → quelque chose comme `192.168.1.100`

**Depuis l'autre PC**:
```
http://192.168.1.100:5000
```

---

## 🛑 Arrêter l'application

```bash
Ctrl + C
```

### Relancer après fermeture

```bash
# Réactivez l'environnement virtuel
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Relancez
python robo_tunisie_app.py
```

---

## 📝 Fichiers Importants

| Fichier | Rôle |
|---------|------|
| `robo_tunisie_app.py` | Application Flask principale |
| `templates/` | Pages HTML |
| `robo_tunisie.db` | Base de données (créée auto) |
| `uploads/` | Dossier pour les documents |
| `requirements.txt` | Dépendances Python |

---

## 🎨 Personnaliser

### Changer les couleurs
Ouvrez `templates/base.html`, cherchez:
```css
:root {
    --primary-purple: #7c3aed;  ← Changez!
    --accent-pink: #ec4899;     ← Changez!
    ...
}
```

### Changer le port (5000)
Ouvrez `robo_tunisie_app.py`, à la fin:
```python
if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5001)  # ← Changez 5001
```

---

## ⚠️ Problèmes Courants & Solutions

### ❌ "Port 5000 already in use"
```bash
# Changez le port dans robo_tunisie_app.py (voir ci-dessus)
# OU trouvez ce qui utilise le port:
# Windows: netstat -ano | findstr :5000
# Linux: lsof -i :5000
```

### ❌ "ModuleNotFoundError: No module named 'flask'"
```bash
pip install -r requirements.txt
```

### ❌ "Cannot connect from another PC"
1. Vérifiez que vous utilisez votre IP locale (pas `localhost`)
2. Vérifiez que les deux PC sont sur le même réseau WiFi
3. Vérifiez que le firewall n'arre pas le port 5000

### ❌ "Fichiers uploadés ne s'affichent pas"
```bash
# Créez le dossier uploads s'il n'existe pas
mkdir uploads
```

### ❌ "Base de données corrompue"
```bash
# Supprimez simplement:
rm robo_tunisie.db
# Relancez - elle sera recréée automatiquement
python robo_tunisie_app.py
```

---

## 📖 Pour Plus d'Infos

- **Installation complète**: `INSTALLATION.md`
- **Documentation complète**: `README.md`
- **Manifeste du projet**: `MANIFEST.md`

---

## ✅ Checklist Finale

- [ ] Python 3.8+ installé
- [ ] Fichiers téléchargés
- [ ] `pip install -r requirements.txt` ✓
- [ ] `python robo_tunisie_app.py` ✓
- [ ] http://localhost:5000 accessible ✓
- [ ] (Optionnel) `python seed_data.py` ✓
- [ ] Club créé ✓
- [ ] Compétition créée ✓
- [ ] Compétition visible publiquement ✓

---

## 🎉 Vous êtes Prêt!

Félicitations! Votre plateforme ROBO TUNISIE est fonctionnelle! 🚀

**Prochaines étapes**:
1. Créer plus de compétitions
2. Inviter d'autres clubs
3. Ajouter les documents réels
4. Personnaliser le design
5. Héberger en ligne

---

**Besoin d'aide?** Consultez `README.md` 📖
