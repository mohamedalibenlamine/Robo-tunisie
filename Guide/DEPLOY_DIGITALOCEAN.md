# 💧 Déployer sur DigitalOcean (Droplet - Production)

**DigitalOcean** est parfait pour une production vraie à petit prix (~5$/mois).

## 🌟 Avantages
✅ VPS complet (contrôle total)  
✅ Pas de limitations  
✅ Domaine personnel possible  
✅ Plus rapide et fiable  
✅ Pas de "sleep mode"  
✅ ~$5-6/mois (très abordable)  

---

## 📋 Prérequis

1. Compte DigitalOcean (https://www.digitalocean.com)
2. Carte de crédit (vraiment gratuit pour 60j)
3. Clé SSH générée (ou utiliser password)

---

## 💰 Coûts

- **Droplet Basic**: $5/mois (1 CPU, 1 GB RAM)
- **Droplet Professional**: $6/mois (1 CPU, 2 GB RAM)
- **Domaine**: ~$10/an (optionnel)
- **Total**: ~$65/an

---

## 🚀 Déploiement Complet

### Étape 1: Créer un Droplet

1. Allez sur https://cloud.digitalocean.com
2. Cliquez "Create" → "Droplets"
3. Sélectionnez:
   - **Region**: Francfort ou Amsterdam (plus proche Tunisie)
   - **Image**: Ubuntu 22.04 (LTS)
   - **Size**: Basic $5/mois
   - **Authentication**: SSH key (ou Password)
   - **Hostname**: robo-tunisie
4. Cliquez "Create Droplet"

### Étape 2: Accéder au Droplet

Vous recevez une IP (ex: 123.45.67.89)

**Via Terminal** (Linux/Mac):
```bash
ssh root@123.45.67.89
```

**Via PuTTY** (Windows):
1. Téléchargez PuTTY
2. Hostname: `123.45.67.89`
3. Cliquez "Open"

### Étape 3: Mettre à Jour le Système

```bash
apt update
apt upgrade -y
```

### Étape 4: Installer Python & Dépendances

```bash
# Python
apt install python3 python3-pip python3-venv -y

# Git
apt install git -y

# Nginx (serveur web reverse proxy)
apt install nginx -y

# Gunicorn (serveur WSGI)
pip3 install gunicorn
```

### Étape 5: Cloner le Projet

```bash
# Créez un dossier
mkdir -p /var/www/robo-tunisie
cd /var/www/robo-tunisie

# Clonez depuis GitHub
git clone https://github.com/VOTRE_USERNAME/robo-tunisie.git .

# Créez un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installez les dépendances
pip install -r requirements.txt
```

### Étape 6: Configurer Gunicorn

Créez `/var/www/robo-tunisie/gunicorn_config.py`:

```python
bind = "127.0.0.1:8000"
workers = 3
worker_class = "sync"
timeout = 30
debug = False
```

### Étape 7: Créer un Service Systemd

Créez `/etc/systemd/system/robo-tunisie.service`:

```ini
[Unit]
Description=ROBO TUNISIE Flask App
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/robo-tunisie
ExecStart=/var/www/robo-tunisie/venv/bin/gunicorn -c gunicorn_config.py robo_tunisie_app:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Puis:
```bash
systemctl daemon-reload
systemctl enable robo-tunisie
systemctl start robo-tunisie
systemctl status robo-tunisie  # Vérifiez qu'il tourne
```

### Étape 8: Configurer Nginx

Créez `/etc/nginx/sites-available/robo-tunisie`:

```nginx
server {
    listen 80;
    server_name _;  # Ou votre domaine

    client_max_body_size 20M;  # Pour uploads

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/robo-tunisie/static/;
    }

    location /uploads/ {
        alias /var/www/robo-tunisie/uploads/;
    }
}
```

Puis:
```bash
# Activez le site
ln -s /etc/nginx/sites-available/robo-tunisie /etc/nginx/sites-enabled/

# Vérifiez la syntaxe
nginx -t

# Redémarrez Nginx
systemctl restart nginx
```

### Étape 9: Initialiser la Base de Données

```bash
cd /var/www/robo-tunisie
source venv/bin/activate
python3 -c "from robo_tunisie_app import init_db; init_db()"
python3 seed_data.py  # (Optionnel - données de test)
```

### Étape 10: Ouvrir les Ports Firewall

```bash
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw enable
```

---

## ✅ C'est En Ligne!

Allez sur:
```
http://123.45.67.89
```

Remplacez par votre IP DigitalOcean.

---

## 🔒 HTTPS (SSL/TLS) - Gratuit

### Avec Let's Encrypt

```bash
# Installez Certbot
apt install certbot python3-certbot-nginx -y

# Générez le certificat
certbot certonly --nginx -d votre-domaine.com

# Configurez Nginx automatiquement
certbot --nginx -d votre-domaine.com
```

Relancez Nginx:
```bash
systemctl restart nginx
```

---

## 🌐 Domaine Personnel

### Ajouter un Domaine

1. Achetez un domaine (Namecheap, OVH, etc.)
2. Changez les nameservers vers DigitalOcean
3. Dans DigitalOcean → "Networking" → "Domains"
4. Ajoutez votre domaine
5. Créez des enregistrements A:
   - `@` → Votre IP
   - `www` → Votre IP

Puis modifiez la config Nginx:
```nginx
server_name votre-domaine.com www.votre-domaine.com;
```

---

## 📊 Gestion Continue

### Vérifier le statut
```bash
systemctl status robo-tunisie
```

### Voir les logs
```bash
journalctl -u robo-tunisie -n 50
```

### Redémarrer l'app
```bash
systemctl restart robo-tunisie
```

### Mettre à jour le code
```bash
cd /var/www/robo-tunisie
git pull
systemctl restart robo-tunisie
```

### Voir l'utilisation
```bash
# CPU/RAM
top

# Disque
df -h

# Processus Python
ps aux | grep gunicorn
```

---

## 🐛 Dépannage

### ❌ "502 Bad Gateway"
Le service Gunicorn ne tourne pas.
```bash
systemctl status robo-tunisie
systemctl restart robo-tunisie
```

### ❌ "Connection refused"
Vérifiez Nginx:
```bash
nginx -t
systemctl status nginx
```

### ❌ "Port already in use"
Changez le port dans `gunicorn_config.py`

### ❌ "Permission denied on uploads"
```bash
chown -R www-data:www-data /var/www/robo-tunisie/uploads
chmod 755 /var/www/robo-tunisie/uploads
```

---

## 🔄 Backups Automatiques

```bash
# Créez un script de backup
cat > /root/backup.sh << 'EOF'
#!/bin/bash
tar -czf /backups/robo-tunisie-$(date +%Y%m%d).tar.gz /var/www/robo-tunisie
# Gardez les 7 derniers backups
find /backups -name "robo-tunisie-*.tar.gz" -mtime +7 -delete
EOF

chmod +x /root/backup.sh

# Planifiez quotidiennement avec cron
crontab -e
# Ajoutez:
0 2 * * * /root/backup.sh
```

---

## 📈 Monitoring

### Simple: Cron check
```bash
# Crontab:
*/5 * * * * curl -s http://votre-domaine.com > /dev/null || systemctl restart robo-tunisie
```

### Avancé: New Relic (gratuit)
1. S'inscrire sur https://newrelic.com
2. Installer l'agent Python
3. Monitorer votre app

---

## 🎬 Résumé Rapide

```
1. Créer un Droplet DigitalOcean ($5/mois)
2. SSH dans le Droplet
3. Installer Python, Nginx, Gunicorn
4. Cloner le projet depuis GitHub
5. Configurer Gunicorn (service)
6. Configurer Nginx (reverse proxy)
7. Initialiser la base de données
8. Redémarrer les services
9. ✨ Accédez par l'IP du Droplet
10. (Optionnel) Ajouter domaine + HTTPS
```

**Durée**: 30-45 minutes

---

## 💡 Tips Pro

- **Auto-scaling**: Upgrade le Droplet si besoin
- **CDN**: Utiliser DigitalOcean Spaces pour les uploads
- **Monitoring**: Alertes email si app down
- **CI/CD**: GitHub Actions pour déployer auto

---

## 📞 Besoin d'aide?

- **Docs**: https://docs.digitalocean.com/
- **Community**: https://www.digitalocean.com/community/
- **Support**: Chat live en bas à droite

---

**Production professionnelle pour ~$5/mois! 🚀**
