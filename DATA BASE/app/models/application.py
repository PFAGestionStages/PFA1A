class Application(Base):
    __tablename__ = "applications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"))
    offer_id = Column(UUID(as_uuid=True), ForeignKey("internship_offers.id"))
    status = Column(
        Enum(
            "submitted",
            "under_company_review",
            "accepted_by_company",
            "approved_by_school",
            name="application_status"
        ),
        default="submitted"
    )
    student = relationship("Student", backref="applications")
    offer = relationship("InternshipOffer", backref="applications")

 


