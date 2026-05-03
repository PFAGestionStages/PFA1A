from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base
import enum

class RoleUtilisateur(str, enum.Enum):
    ADMIN = "admin"
    ECOLE = "ecole"
    ENTREPRISE = "entreprise"
    ETUDIANT = "etudiant"
    ENSEIGNANT = "enseignant"

class StatutCandidature(str, enum.Enum):
    EN_ATTENTE = "en_attente"
    EN_COURS = "en_cours"
    SELECTIONNE = "selectionne"
    ACCEPTE = "accepte"
    REFUSE = "refuse"

class Utilisateur(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nom = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    mot_de_passe = Column(String, nullable=False)
    role = Column(Enum(RoleUtilisateur), nullable=False)
    est_actif = Column(Integer, default=1)
    date_inscription = Column(DateTime, default=datetime.now)

class Etudiant(Base):
    __tablename__ = "etudiants"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), unique=True)
    niveau = Column(String, nullable=False)
    filiere = Column(String, nullable=False)
    competences = Column(Text)
    cv_url = Column(String)
    lettre_motivation_url = Column(String)
    statut_stage = Column(String, default="recherche")

class Entreprise(Base):
    __tablename__ = "entreprises"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("utilisateurs.id"), unique=True)
    raison_sociale = Column(String, nullable=False)
    secteur = Column(String)
    ville = Column(String)
    contact_rh_nom = Column(String)
    contact_rh_email = Column(String)
    site_web = Column(String)

class OffreStage(Base):
    __tablename__ = "offres_stage"
    id = Column(Integer, primary_key=True, index=True)
    entreprise_id = Column(Integer, ForeignKey("entreprises.id"))
    titre = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    competences_requises = Column(Text)
    duree = Column(String)
    lieu = Column(String)
    gratification = Column(String)
    nb_places = Column(Integer, default=1)
    places_restantes = Column(Integer, default=1)
    date_limite = Column(DateTime)
    est_active = Column(Integer, default=1)
    date_publication = Column(DateTime, default=datetime.now)

class Candidature(Base):
    __tablename__ = "candidatures"
    id = Column(Integer, primary_key=True, index=True)
    etudiant_id = Column(Integer, ForeignKey("etudiants.id"))
    offre_id = Column(Integer, ForeignKey("offres_stage.id"))
    statut = Column(Enum(StatutCandidature), default=StatutCandidature.EN_ATTENTE)
    cv_url = Column(String)
    lettre_url = Column(String)
    commentaires = Column(Text)
    commentaires_ecole = Column(Text, nullable=True)
    commentaires_entreprise = Column(Text, nullable=True)
    score_matching = Column(Float, default=0.0)
    date_candidature = Column(DateTime, default=datetime.now)