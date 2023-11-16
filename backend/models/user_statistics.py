from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from models.fip_data import FIPData

Base = declarative_base()


class UserStatistics(Base):
    __tablename__ = 'super_sync_user_statistics'

    id = Column(Integer, primary_key=True)

    mobile = Column(String)

    fip_data_id = ForeignKey(FIPData.id)

    fip_data_status = Column(String)
    fip_data_s3_url = Column(String)

    def __repr__(self):
        return f"<UserStatistics(mobile={self.mobile})>"
