from .model import engine, SessionMaker, Base, OpenChannelData


def init_db(first_time):
    """
    An example persistent store initializer function
    """
    # Create tables
    Base.metadata.create_all(engine)
