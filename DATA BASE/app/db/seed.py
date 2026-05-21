from sqlalchemy.orm import Session
from app.models.user import User
from app.models.student import Student
from app.models.company import Company

def seed_data(db: Session):

    if db.query(User).first():
        return

    student_user = User(
        first_name="Walid",
        last_name="Sat",
        email="walid@student.com",
        password_hash="hashed",
        role="student"
    )

    company_user = User(
        first_name="OCP",
        last_name="Recruiter",
        email="hr@ocpgroup.ma",
        password_hash="hashed",
        role="company"
    )

    db.add_all([student_user, company_user])
    db.commit()


#remplir la base automatiquement avec des données initiales
