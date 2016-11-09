from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, Date
from sqlalchemy.orm import sessionmaker

from .app import OpenChannelDataViewer

# DB Engine, sessionmaker and base
engine = OpenChannelDataViewer.get_persistent_store_engine('open_channel_data_viewer_db')
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()


# SQLAlchemy ORM definition for the table
class OpenChannelData(Base):
    """
    Example SQLAlchemy DB Model
    """
    __tablename__ = 'open_channel_data'

    # Columns
    id = Column(Integer, primary_key=True)
    name = Column(String)
    record_date = Column(Date)
    sampling_method = Column(String)
    drainage_area = Column(Float)
    avg_flow = Column(Float)
    tot_bedload_rate = Column(Float)
    avg_depth = Column(Float)
    avg_cross_sectional_area = Column(Float)
    avg_velocity = Column(Float)

    def __init__(self, name, drainage_area, sampling_method, record_date, avg_flow, tot_bedload_rate, avg_depth,
                 avg_cross_sectional_area, avg_velocity):
        """
        """
        self.name = name
        self.drainage_area = drainage_area
        self.sampling_method = sampling_method
        self.record_date = record_date
        self.avg_flow = avg_flow
        self.tot_bedload_rate = tot_bedload_rate
        self.avg_depth = avg_depth
        self.avg_cross_sectional_area = avg_cross_sectional_area
        self.avg_velocity = avg_velocity
