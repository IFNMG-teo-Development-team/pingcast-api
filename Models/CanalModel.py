from app import db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Canal(db.Model, Base):
    __tablename__ = "canal"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    tema = db.Column(db.String(45), nullable=True)
    bio = db.Column(db.String(200), nullable=True)
    dono = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    perfil = relationship('Perfil', back_populates="canal", passive_deletes=True)

    def __repr__(self):
        return self.nome
