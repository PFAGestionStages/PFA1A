# app/services/notification_service.py
import os
from typing import List, Dict, Optional
from app.utils.email import send_email
from app.database import SessionLocal
from app.models import Utilisateur, Etudiant, Entreprise, Ecole, Enseignant, OffreStage, Candidature, Affectation

# ============================================================
# FONCTIONS UTILITAIRES (récupération d'emails depuis la BD)
# ============================================================

def get_email_by_etudiant_id(etudiant_id: int) -> Optional[str]:
    """Récupère l'email d'un étudiant depuis son ID"""
    db = SessionLocal()
    try:
        etudiant = db.query(Etudiant).filter(Etudiant.id == etudiant_id).first()
        if not etudiant:
            return None
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == etudiant.user_id).first()
        return utilisateur.email if utilisateur else None
    finally:
        db.close()

def get_email_by_entreprise_id(entreprise_id: int) -> Optional[str]:
    """Récupère l'email d'une entreprise depuis son ID"""
    db = SessionLocal()
    try:
        entreprise = db.query(Entreprise).filter(Entreprise.id == entreprise_id).first()
        if not entreprise:
            return None
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == entreprise.user_id).first()
        return utilisateur.email if utilisateur else None
    finally:
        db.close()

def get_email_by_ecole_id(ecole_id: int) -> Optional[str]:
    """Récupère l'email d'une école depuis son ID"""
    db = SessionLocal()
    try:
        ecole = db.query(Ecole).filter(Ecole.id == ecole_id).first()
        if not ecole:
            return None
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == ecole.user_id).first()
        return utilisateur.email if utilisateur else None
    finally:
        db.close()

def get_email_by_enseignant_id(enseignant_id: int) -> Optional[str]:
    """Récupère l'email d'un enseignant depuis son ID"""
    db = SessionLocal()
    try:
        enseignant = db.query(Enseignant).filter(Enseignant.id == enseignant_id).first()
        if not enseignant:
            return None
        utilisateur = db.query(Utilisateur).filter(Utilisateur.id == enseignant.user_id).first()
        return utilisateur.email if utilisateur else None
    finally:
        db.close()

def get_admin_emails() -> List[str]:
    """Récupère la liste des emails de tous les administrateurs"""
    db = SessionLocal()
    try:
        admins = db.query(Utilisateur).filter(Utilisateur.role == "admin").all()
        return [admin.email for admin in admins]
    finally:
        db.close()


# ============================================================
# 1. INSCRIPTION ET VALIDATION DES COMPTES
# ============================================================

def send_demande_inscription_entreprise(email_entreprise: str, nom_entreprise: str):
    """Envoyé à l'admin quand une entreprise s'inscrit"""
    admin_emails = get_admin_emails()
    for admin_email in admin_emails:
        send_email(
            to=admin_email,
            subject="📋 Nouvelle demande d'inscription entreprise",
            body_html=f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <h2>Nouvelle demande d'inscription</h2>
                    <p>L'entreprise <strong>{nom_entreprise}</strong> ({email_entreprise}) a demandé à s'inscrire sur la plateforme.</p>
                    <p>Connectez-vous à l'interface d'administration pour valider ou refuser cette demande.</p>
                    <a href="https://votreplateforme.com/admin/entreprises">Gérer les demandes →</a>
                </body>
            </html>
            """
        )

def send_demande_inscription_ecole(email_ecole: str, nom_ecole: str):
    """Envoyé à l'admin quand une école s'inscrit"""
    admin_emails = get_admin_emails()
    for admin_email in admin_emails:
        send_email(
            to=admin_email,
            subject="📋 Nouvelle demande d'inscription école",
            body_html=f"""
            <html>
                <body>
                    <h2>Nouvelle demande d'inscription</h2>
                    <p>L'école <strong>{nom_ecole}</strong> ({email_ecole}) a demandé à s'inscrire sur la plateforme.</p>
                    <a href="https://votreplateforme.com/admin/ecoles">Gérer les demandes →</a>
                </body>
            </html>
            """
        )

def send_validation_compte_entreprise(email_entreprise: str, nom_entreprise: str):
    """Envoyé à l'entreprise quand son compte est validé"""
    send_email(
        to=email_entreprise,
        subject="✅ Votre compte entreprise a été validé",
        body_html=f"""
        <html>
            <body>
                <h2>Félicitations {nom_entreprise} !</h2>
                <p>Votre compte sur la plateforme ENSIAS Stages a été <strong>validé</strong> par l'administrateur.</p>
                <p>Vous pouvez dès à présent :</p>
                <ul>
                    <li>Publier des offres de stage</li>
                    <li>Consulter les candidatures</li>
                    <li>Contacter les étudiants</li>
                </ul>
                <a href="https://votreplateforme.com/login">Se connecter →</a>
            </body>
        </html>
        """
    )

def send_validation_compte_ecole(email_ecole: str, nom_ecole: str):
    """Envoyé à l'école quand son compte est validé"""
    send_email(
        to=email_ecole,
        subject="✅ Votre compte école a été validé",
        body_html=f"""
        <html>
            <body>
                <h2>Félicitations {nom_ecole} !</h2>
                <p>Votre compte sur la plateforme ENSIAS Stages a été <strong>validé</strong> par l'administrateur.</p>
                <p>Vous pouvez dès à présent :</p>
                <ul>
                    <li>Importer la liste de vos étudiants</li>
                    <li>Valider les conventions de stage</li>
                    <li>Suivre vos étudiants en stage</li>
                </ul>
                <a href="https://votreplateforme.com/login">Se connecter →</a>
            </body>
        </html>
        """
    )

def send_refus_compte_entreprise(email_entreprise: str, nom_entreprise: str, motif: str):
    """Envoyé à l'entreprise quand son compte est refusé"""
    send_email(
        to=email_entreprise,
        subject="❌ Votre demande d'inscription a été refusée",
        body_html=f"""
        <html>
            <body>
                <h2>Demande d'inscription refusée</h2>
                <p>Bonjour <strong>{nom_entreprise}</strong>,</p>
                <p>Votre demande d'inscription sur la plateforme ENSIAS Stages a été <strong>refusée</strong> par l'administrateur.</p>
                <p><strong>Motif :</strong> {motif}</p>
                <p>Vous pouvez nous contacter pour plus d'informations.</p>
            </body>
        </html>
        """
    )


# ============================================================
# 2. CRÉATION DES COMPTES ÉTUDIANTS (IMPORT CSV)
# ============================================================

def send_notification_import_etudiants(email_ecole: str, nb_etudiants: int, fichier: str):
    """Envoyé à l'école pour confirmer l'import des étudiants"""
    send_email(
        to=email_ecole,
        subject="📊 Import des étudiants réussi",
        body_html=f"""
        <html>
            <body>
                <h2>Import terminé !</h2>
                <p><strong>{nb_etudiants}</strong> étudiants ont été importés depuis le fichier <strong>{fichier}</strong>.</p>
                <p>Chaque étudiant va recevoir ses identifiants de connexion par email.</p>
                <a href="https://votreplateforme.com/ecole/etudiants">Voir la liste des étudiants →</a>
            </body>
        </html>
        """
    )

def send_identifiants_etudiant(email_etudiant: str, nom: str, prenom: str, mot_de_passe_temporaire: str):
    """Envoyé à l'étudiant avec ses identifiants temporaires"""
    send_email(
        to=email_etudiant,
        subject="🎓 Bienvenue sur la plateforme ENSIAS Stages",
        body_html=f"""
        <html>
            <body>
                <h2>Bienvenue {prenom} {nom} !</h2>
                <p>Votre école vous a inscrit sur la plateforme de gestion des stages.</p>
                <p><strong>Vos identifiants de connexion :</strong></p>
                <ul>
                    <li><strong>Identifiant :</strong> {email_etudiant}</li>
                    <li><strong>Mot de passe temporaire :</strong> {mot_de_passe_temporaire}</li>
                </ul>
                <p><em>⚠️ Nous vous conseillons de changer votre mot de passe dès la première connexion.</em></p>
                <a href="https://votreplateforme.com/login">Se connecter →</a>
            </body>
        </html>
        """
    )


# ============================================================
# 3. PREMIÈRE CONNEXION / VÉRIFICATION
# ============================================================

def send_code_verification(email_etudiant: str, nom: str, code: str):
    """Envoyé à l'étudiant lors de la première connexion (code de vérification)"""
    send_email(
        to=email_etudiant,
        subject="🔐 Votre code de vérification",
        body_html=f"""
        <html>
            <body>
                <h2>Bonjour {nom},</h2>
                <p>Voici votre code de vérification pour vous connecter à la plateforme :</p>
                <div style="font-size: 32px; font-weight: bold; background: #f0f0f0; padding: 20px; text-align: center;">
                    {code}
                </div>
                <p>Ce code expire dans 15 minutes.</p>
                <p>Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.</p>
            </body>
        </html>
        """
    )

def send_confirmation_changement_mdp(email_utilisateur: str, nom: str):
    """Envoyé après un changement de mot de passe réussi"""
    send_email(
        to=email_utilisateur,
        subject="🔒 Votre mot de passe a été modifié",
        body_html=f"""
        <html>
            <body>
                <h2>Bonjour {nom},</h2>
                <p>Votre mot de passe a été <strong>modifié avec succès</strong>.</p>
                <p>Si vous n'êtes pas à l'origine de cette modification, contactez immédiatement l'administrateur.</p>
                <a href="https://votreplateforme.com/login">Se connecter →</a>
            </body>
        </html>
        """
    )


# ============================================================
# 4. OFFRES ET CANDIDATURES
# ============================================================

def send_nouvelle_offre_entreprise(email_entreprise: str, offre_titre: str):
    """Confirmation à l'entreprise qu'une offre a été publiée"""
    send_email(
        to=email_entreprise,
        subject="📢 Votre offre a été publiée",
        body_html=f"""
        <html>
            <body>
                <h2>Offre publiée avec succès</h2>
                <p>Votre offre <strong>"{offre_titre}"</strong> est maintenant visible par tous les étudiants.</p>
                <a href="https://votreplateforme.com/entreprise/offres">Voir mes offres →</a>
            </body>
        </html>
        """
    )

def send_offre_match_etudiant(email_etudiant: str, nom_etudiant: str, offre_titre: str, entreprise_nom: str):
    """Envoyé aux étudiants qui correspondent au profil d'une nouvelle offre"""
    send_email(
        to=email_etudiant,
        subject="🎯 Nouveau stage correspondant à votre profil !",
        body_html=f"""
        <html>
            <body>
                <h2>Bonjour {nom_etudiant},</h2>
                <p>Une nouvelle offre de stage pourrait vous intéresser :</p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 10px;">
                    <h3>{offre_titre}</h3>
                    <p><strong>Entreprise :</strong> {entreprise_nom}</p>
                </div>
                <a href="https://votreplateforme.com/offres">Voir l'offre et postuler →</a>
            </body>
        </html>
        """
    )

def send_confirmation_candidature(email_etudiant: str, nom_etudiant: str, offre_titre: str):
    """Envoyé à l'étudiant pour confirmer que sa candidature a bien été envoyée"""
    send_email(
        to=email_etudiant,
        subject="📝 Confirmation de votre candidature",
        body_html=f"""
        <html>
            <body>
                <h2>Merci d'avoir postulé, {nom_etudiant} !</h2>
                <p>Votre candidature pour le stage <strong>"{offre_titre}"</strong> a bien été envoyée.</p>
                <p>Vous pouvez suivre l'état de vos candidatures dans votre espace personnel.</p>
                <a href="https://votreplateforme.com/etudiant/candidatures">Suivre mes candidatures →</a>
            </body>
        </html>
        """
    )

def send_notification_candidature_entreprise(email_entreprise: str, offre_titre: str, etudiant_nom: str):
    """Envoyé à l'entreprise quand un étudiant postule"""
    send_email(
        to=email_entreprise,
        subject="📬 Nouvelle candidature reçue",
        body_html=f"""
        <html>
            <body>
                <h2>Nouvelle candidature</h2>
                <p>L'étudiant <strong>{etudiant_nom}</strong> a postulé à votre offre <strong>"{offre_titre}"</strong>.</p>
                <a href="https://votreplateforme.com/entreprise/candidatures">Consulter les candidatures →</a>
            </body>
        </html>
        """
    )


# ============================================================
# 5. PRÉSÉLECTION / ACCEPTATION / REFUS
# ============================================================

def send_preselection_etudiant(email_etudiant: str, nom_etudiant: str, offre_titre: str, entreprise_nom: str):
    """Envoyé à l'étudiant quand il est présélectionné"""
    send_email(
        to=email_etudiant,
        subject="⭐ Félicitations ! Vous avez été présélectionné(e)",
        body_html=f"""
        <html>
            <body>
                <h2>Bonne nouvelle, {nom_etudiant} !</h2>
                <p>L'entreprise <strong>{entreprise_nom}</strong> vous a <strong>présélectionné(e)</strong> pour le stage <strong>"{offre_titre}"</strong>.</p>
                <p>Connectez-vous pour accepter ou refuser cette proposition.</p>
                <div style="margin-top: 20px;">
                    <a href="https://votreplateforme.com/candidatures?accepter=true" style="background: green; color: white; padding: 10px 20px; text-decoration: none; margin-right: 10px;">✅ Accepter</a>
                    <a href="https://votreplateforme.com/candidatures?refuser=true" style="background: red; color: white; padding: 10px 20px; text-decoration: none;">❌ Refuser</a>
                </div>
            </body>
        </html>
        """
    )

def send_reponse_etudiant_entreprise(email_entreprise: str, offre_titre: str, etudiant_nom: str, accepte: bool, remarque: str = None):
    """Envoyé à l'entreprise quand l'étudiant répond (accepte ou refuse)"""
    if accepte:
        subject = "✅ Un étudiant a accepté votre offre"
        titre = "a accepté"
        couleur = "green"
    else:
        subject = "❌ Un étudiant a refusé votre offre"
        titre = "a refusé"
        couleur = "red"

    remarque_html = f"<p><strong>Remarque :</strong> {remarque}</p>" if remarque else ""

    send_email(
        to=email_entreprise,
        subject=subject,
        body_html=f"""
        <html>
            <body>
                <h2 style="color: {couleur};">Réponse de l'étudiant</h2>
                <p>L'étudiant <strong>{etudiant_nom}</strong> <strong>{titre}</strong> l'offre <strong>"{offre_titre}"</strong>.</p>
                {remarque_html}
                <a href="https://votreplateforme.com/entreprise/candidatures">Voir le détail →</a>
            </body>
        </html>
        """
    )


# ============================================================
# 6. VALIDATION PÉDAGOGIQUE (ÉCOLE / ENSEIGNANT)
# ============================================================

def send_demande_validation_ecole(email_ecole: str, etudiant_nom: str, offre_titre: str, entreprise_nom: str, stage_id: int):
    """Envoyé à l'école pour valider une affectation"""
    send_email(
        to=email_ecole,
        subject="📋 Action requise : Valider un stage",
        body_html=f"""
        <html>
            <body>
                <h2>Validation pédagogique requise</h2>
                <p>L'étudiant <strong>{etudiant_nom}</strong> a accepté un stage proposé par <strong>{entreprise_nom}</strong> pour le poste <strong>"{offre_titre}"</strong>.</p>
                <p>Veuillez vérifier que ce stage correspond bien au cursus.</p>
                <div style="margin-top: 20px;">
                    <a href="https://votreplateforme.com/ecole/stages/{stage_id}/valider" style="background: green; color: white; padding: 10px 20px; text-decoration: none; margin-right: 10px;">✅ Valider</a>
                    <a href="https://votreplateforme.com/ecole/stages/{stage_id}/refuser" style="background: red; color: white; padding: 10px 20px; text-decoration: none;">❌ Refuser avec remarque</a>
                </div>
            </body>
        </html>
        """
    )

def send_validation_ecole_etudiant_entreprise(email_etudiant: str, email_entreprise: str, etudiant_nom: str, offre_titre: str, valide: bool, remarque: str = None):
    """Envoyé à l'étudiant et à l'entreprise après validation/refus de l'école"""
    if valide:
        subject_etudiant = "✅ Votre stage a été validé par l'école"
        subject_entreprise = "✅ Le stage a été validé par l'école"
        message = "validé"
        couleur = "green"
    else:
        subject_etudiant = "❌ Votre stage n'a pas été validé par l'école"
        subject_entreprise = "❌ Le stage n'a pas été validé par l'école"
        message = "refusé"
        couleur = "red"

    remarque_html = f"<p><strong>Remarque de l'école :</strong> {remarque}</p>" if remarque else ""

    # Email à l'étudiant
    send_email(
        to=email_etudiant,
        subject=subject_etudiant,
        body_html=f"""
        <html>
            <body>
                <h2 style="color: {couleur};">Décision de l'école</h2>
                <p>Votre stage <strong>"{offre_titre}"</strong> a été <strong>{message}</strong> par votre école.</p>
                {remarque_html}
                <a href="https://votreplateforme.com/etudiant/stages">Voir le détail →</a>
            </body>
        </html>
        """
    )

    # Email à l'entreprise
    send_email(
        to=email_entreprise,
        subject=subject_entreprise,
        body_html=f"""
        <html>
            <body>
                <h2 style="color: {couleur};">Décision pédagogique</h2>
                <p>Le stage de l'étudiant <strong>{etudiant_nom}</strong> pour l'offre <strong>"{offre_titre}"</strong> a été <strong>{message}</strong> par l'école.</p>
                {remarque_html}
                <a href="https://votreplateforme.com/entreprise/stages">Voir le détail →</a>
            </body>
        </html>
        """
    )

def send_verification_missions_enseignant(email_enseignant: str, etudiant_nom: str, offre_titre: str, missions: str):
    """Envoyé à l'enseignant pour vérifier les missions assignées"""
    send_email(
        to=email_enseignant,
        subject="📋 Vérification des missions de stage",
        body_html=f"""
        <html>
            <body>
                <h2>Vérification des missions</h2>
                <p>L'étudiant <strong>{etudiant_nom}</strong> a reçu des missions pour le stage <strong>"{offre_titre}"</strong>.</p>
                <p><strong>Missions proposées :</strong></p>
                <div style="background: #f5f5f5; padding: 15px; border-radius: 10px;">
                    {missions}
                </div>
                <div style="margin-top: 20px;">
                    <a href="https://votreplateforme.com/enseignant/missions/valider" style="background: green; color: white; padding: 10px 20px; text-decoration: none; margin-right: 10px;">✅ Valider ces missions</a>
                    <a href="https://votreplateforme.com/enseignant/missions/refuser" style="background: orange; color: white; padding: 10px 20px; text-decoration: none;">🔧 Proposer des modifications</a>
                </div>
            </body>
        </html>
        """
    )


# ============================================================
# 7. FONCTIONS GÉNÉRIQUES (SI BESOIN)
# ============================================================

def send_custom_email(to: str, subject: str, body_html: str):
    """Envoi d'un email personnalisé"""
    return send_email(to=to, subject=subject, body_html=body_html)

def send_notification_to_all_admins(subject: str, body_html: str):
    """Envoie une notification à tous les administrateurs"""
    admin_emails = get_admin_emails()
    success = True
    for email in admin_emails:
        if not send_email(to=email, subject=subject, body_html=body_html):
            success = False
    return success