from app.utils.email import send_email

send_email(
    to="plateforme.stages.ensias@gmail.com",subject="Test API Gmail - Plateforme Stages",
    body_html="""
    <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>🎉 Félicitations !</h2>
            <p>Votre plateforme peut maintenant envoyer des emails via l'API Gmail.</p>
            <p>Ceci est un test de votre configuration.</p>
            <hr>
            <p style="color: gray;">Plateforme de Gestion des Stages - ENSIAS</p>
        </body>
    </html>
    """
)