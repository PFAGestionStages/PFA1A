from app.database import SessionLocal
from app.models import Utilisateur, Administrateur
from passlib.hash import bcrypt

db = SessionLocal()

admins = [
    {"email": "admin1@plateforme.com", "nom": "Admin", "prenom": "Principal", "mdp": "admin123"},
    {"email": "admin2@plateforme.com", "nom": "Admin", "prenom": "Secondaire", "mdp": "admin123"},
    {"email": "admin3@plateforme.com", "nom": "Admin", "prenom": "Tertiaire", "mdp": "admin123"},
]

for a in admins:
    existing = db.query(Utilisateur).filter(Utilisateur.email == a["email"]).first()
    if existing:
        print(f"⚠️ {a['email']} existe déjà")
        continue
    
    hashed = bcrypt.hash(a["mdp"])
    user = Utilisateur(
        email=a["email"],
        mot_de_passe=hashed,
        nom=a["nom"],
        prenom=a["prenom"],
        role="admin",
        est_actif=True
    )
    db.add(user)
    db.flush()
    
    admin = Administrateur(
        user_id=user.id,
        niveau_acces="super_admin"
    )
    db.add(admin)

db.commit()
print("✅ 3 comptes administrateurs créés avec succès !")
db.close()