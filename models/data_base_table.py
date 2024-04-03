from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON

metadata = MetaData()

movie = Table(
    "movie",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("name", String, nullable = False),
    Column("description", String, nullable = False),
    Column("time", Integer, nullable = False),
    Column("date_start", TIMESTAMP, nullable = False),
    Column("date_end", TIMESTAMP, nullable = False)
)

session = Table(
    "session",
    metadata,
    Column("id", Integer, primary_key = True),
    Column("id_movie", Integer, ForeignKey('movie.id')),
    Column("date", TIMESTAMP, nullable = False),
    Column("cinema_hall", Integer, nullable= False)
)


