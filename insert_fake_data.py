# insert_fake_data.py (version avec bcrypt corrigé)
from app.database import SessionLocal
from app.models import (
    Utilisateur, Etudiant, Entreprise, OffreStage, Candidature
)
import bcrypt
from datetime import datetime, timedelta
import random

db = SessionLocal()

# Fonction pour hacher un mot de passe
def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

# ============================================================
# NETTOYAGE
# ============================================================
print(" Nettoyage des anciennes données...")
db.query(Candidature).delete()
db.query(OffreStage).delete()
db.query(Etudiant).delete()
db.query(Entreprise).delete()
db.query(Utilisateur).delete()
db.commit()
print("   Anciennes données supprimées.\n")

print(" Création des données fictives...\n")

# ============================================================
# 1. ADMINISTRATEURS
# ============================================================
admins_data = [
    {"email": "admin1@plateforme.com", "nom": "Admin", "prenom": "Alpha", "mdp": "admin123", "role": "admin"},
    {"email": "admin2@plateforme.com", "nom": "Admin", "prenom": "Beta", "mdp": "admin123", "role": "admin"},
    {"email": "admin3@plateforme.com", "nom": "Admin", "prenom": "Gamma", "mdp": "admin123", "role": "admin"},
]

# ============================================================
# 2. ENTREPRISES
# ============================================================
entreprises_data = [
    {"email": "contact@ocp.ma", "nom": "OCP", "prenom": "SA", "mdp": "entreprise123", "role": "entreprise", 
     "raison_sociale": "OCP Group", "secteur": "Mines", "ville": "Casablanca", "contact_rh": "rh@ocp.ma"},
    {"email": "rh@inwi.ma", "nom": "Inwi", "prenom": "", "mdp": "entreprise123", "role": "entreprise", 
     "raison_sociale": "Inwi", "secteur": "Télécoms", "ville": "Rabat", "contact_rh": "recrutement@inwi.ma"},
    {"email": "contact@attijari.ma", "nom": "Attijari", "prenom": "Bank", "mdp": "entreprise123", "role": "entreprise", 
     "raison_sociale": "Attijariwafa Bank", "secteur": "Banque", "ville": "Casablanca", "contact_rh": "rh@attijari.ma"},
    {"email": "rh@maroctelecom.ma", "nom": "Maroc Telecom", "prenom": "", "mdp": "entreprise123", "role": "entreprise", 
     "raison_sociale": "Maroc Telecom", "secteur": "Télécoms", "ville": "Rabat", "contact_rh": "candidature@iam.ma"},
    {"email": "contact@capgemini.ma", "nom": "Capgemini", "prenom": "", "mdp": "entreprise123", "role": "entreprise", 
     "raison_sociale": "Capgemini", "secteur": "Conseil IT", "ville": "Casablanca", "contact_rh": "rh.maroc@capgemini.com"},
]

# ============================================================
# 3. ÉTUDIANTS (30 étudiants)
# ============================================================
etudiants_data = []
niveaux = ["Bac2", "Bac3", "Bac4", "Bac5"]
filiers = ["Informatique", "Réseaux", "Big Data", "Sécurité", "IA", "Cloud Computing"]
competences_list = [
    "Python, SQL, Git",
    "Java, Spring Boot, Angular",
    "React, Node.js, MongoDB",
    "Machine Learning, TensorFlow",
    "DevOps, Docker, Kubernetes",
]

for i in range(1, 31):
    etudiants_data.append({
        "email": f"etudiant{i}@ensias.ma",
        "nom": f"Nom{i}",
        "prenom": f"Prenom{i}",
        "mdp": f"etu{i}123",
        "role": "etudiant",
        "numero_etudiant": f"2024{i:04d}",
        "niveau": random.choice(niveaux),
        "filiere": random.choice(filiers),
        "competences": random.choice(competences_list),
        "statut_stage": random.choice(["recherche", "recherche", "recherche", "affecte"]),
    })

# ============================================================
# 4. OFFRES DE STAGE
# ============================================================
offres_data = [
    {"entreprise": "OCP Group", "titre": "Stage Data Engineer", "description": "Pipeline de données", "duree": "4 mois", "lieu": "Casablanca", "gratification": "3500 DH", "nb_places": 2},
    {"entreprise": "Inwi", "titre": "Stage Data Analyst", "description": "Analyse de données clients", "duree": "3 mois", "lieu": "Rabat", "gratification": "2800 DH", "nb_places": 1},
    {"entreprise": "Attijariwafa Bank", "titre": "Stage Développeur Full Stack", "description": "Application bancaire", "duree": "5 mois", "lieu": "Casablanca", "gratification": "4000 DH", "nb_places": 3},
    {"entreprise": "Maroc Telecom", "titre": "Stage DevOps", "description": "CI/CD", "duree": "4 mois", "lieu": "Rabat", "gratification": "3000 DH", "nb_places": 2},
    {"entreprise": "Capgemini", "titre": "Stage Consultant Cloud", "description": "Migration cloud", "duree": "4 mois", "lieu": "Casablanca", "gratification": "3200 DH", "nb_places": 2},
]

# ============================================================
# INSERTION
# ============================================================

user_ids = {}
entreprise_ids = {}
etudiant_ids = {}
offre_ids = {}

print(" Insertion des administrateurs...")
for a in admins_data:
    hashed = hash_password(a["mdp"])
    user = Utilisateur(
        email=a["email"], mot_de_passe=hashed, nom=a["nom"], prenom=a["prenom"],
        role=a["role"], est_actif=1
    )
    db.add(user)
    db.flush()
    user_ids[a["email"]] = user.id

print(" Insertion des entreprises...")
for e in entreprises_data:
    hashed = hash_password(e["mdp"])
    user = Utilisateur(
        email=e["email"], mot_de_passe=hashed, nom=e["nom"], prenom=e["prenom"],
        role=e["role"], est_actif=1
    )
    db.add(user)
    db.flush()
    user_ids[e["email"]] = user.id
    entreprise = Entreprise(
        user_id=user.id, raison_sociale=e["raison_sociale"], secteur=e["secteur"],
        ville=e["ville"], contact_rh_email=e["contact_rh"]
    )
    db.add(entreprise)
    db.flush()
    entreprise_ids[e["raison_sociale"]] = entreprise.id

print(" Insertion des étudiants...")
for e in etudiants_data:
    hashed = hash_password(e["mdp"])
    user = Utilisateur(
        email=e["email"], mot_de_passe=hashed, nom=e["nom"], prenom=e["prenom"],
        role=e["role"], est_actif=1
    )
    db.add(user)
    db.flush()
    user_ids[e["email"]] = user.id
    etudiant = Etudiant(
        user_id=user.id, niveau=e["niveau"], filiere=e["filiere"],
        competences=e["competences"], statut_stage=e["statut_stage"]
    )
    db.add(etudiant)
    db.flush()
    etudiant_ids[e["email"]] = etudiant.id

print(" Insertion des offres de stage...")
for o in offres_data:
    offre = OffreStage(
        entreprise_id=entreprise_ids[o["entreprise"]],
        titre=o["titre"], description=o["description"], duree=o["duree"],
        lieu=o["lieu"], gratification=o["gratification"], nb_places=o["nb_places"],
        places_restantes=o["nb_places"], date_limite=datetime.now() + timedelta(days=30),
        est_active=1
    )
    db.add(offre)
    db.flush()
    offre_ids[o["titre"]] = offre.id

print(" Insertion des candidatures...")
etudiant_id_list = list(etudiant_ids.values())
offre_id_list = list(offre_ids.values())
for i in range(20):
    cand = Candidature(
        etudiant_id=random.choice(etudiant_id_list),
        offre_id=random.choice(offre_id_list),
        statut=random.choice(["en_attente", "en_cours", "selectionne"]),
        score_matching=random.randint(60, 95)
    )
    db.add(cand)

db.commit()

db.close()