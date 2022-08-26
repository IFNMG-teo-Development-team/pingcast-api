from app import db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Podcast(db.Model, Base):
    __tablename__ = "podcast"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duracao = db.Column(db.Time, nullable=True)
    data_postagem = db.Column(db.Date, nullable=False)
    participantes = db.Column(db.String(45), nullable=True)
    descricao = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)
    post_podcast = db.Column(db.Integer, db.ForeignKey("canal.id"))
    canal = relationship('Canal', passive_deletes=True)

    def __repr__(self):
        return self.nome
