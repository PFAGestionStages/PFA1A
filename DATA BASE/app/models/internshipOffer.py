class InternshipOffer(Base):
    __tablename__ = "internship_offers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(UUID(as_uuid=True), ForeignKey("companies.id"))
    title = Column(String(255), nullable=False)
    description = Column(String)
    company = relationship("Company", backref="offers")

