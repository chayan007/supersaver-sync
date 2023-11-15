from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class FIPData(Base):
    __tablename__ = 'super_sync_fip_data'

    id = Column(Integer, primary_key=True)

    mobile = Column(String)

    consent_id = Column(String)
    consent_status = Column(String)

    fip_data_status = Column(String)
    fip_data_s3_url = Column(String)

    def __repr__(self):
        return f"<FIPData(consent_id={self.consent_id})>"
