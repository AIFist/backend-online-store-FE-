from server.db.db import Base, engine, db

Base.metadata.create_all(engine)


session = db  