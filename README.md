# Mini App Flask – Déploiement gratuit (Render)

## 1) Préparer le dépôt
- Fichiers importants :
  - `app.py` (application Flask)
  - `requirements.txt` (dépendances)
  - `Procfile` (commande de démarrage)
  - `templates/index.html` (page d'accueil)
  - `static/` (si tu as des assets)

## 2) Déployer sur Render (gratuit)
1. Crée un dépôt GitHub et pousse ces fichiers.
2. Va sur https://render.com > *New* > *Web Service* > *Build and deploy from a Git repo*.
3. Sélectionne le dépôt.
4. Paramètres :
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
5. Déploie. Render donnera une URL publique (`https://xxx.onrender.com`).

## 3) Éviter l'endormissement
- Crée un compte UptimeRobot (gratuit).
- Ajoute un *HTTP monitor* sur `https://xxx.onrender.com/ping` toutes les 5 minutes.

## 4) Tester
- Ouvre l'URL publique dans un navigateur.
- Vérifie `/ping` → doit renvoyer `{"status":"OK"}`.

## 5) Modifier ta page
- Édite `templates/index.html` à ta convenance, pousse sur GitHub → Render redéploie.

---

> Astuce : Si tu utilises d'autres routes (API), garde `/ping` ultra-légère pour accélérer le "cold start".
