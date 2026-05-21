from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import relationship

class Student(Base):
    __tablename__ = "students"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    school_id = Column(UUID(as_uuid=True), ForeignKey("schools.id"))
    program = Column(String(255))
    profile_completion = Column(Integer, default=0)

    user = relationship("User", backref="student")


