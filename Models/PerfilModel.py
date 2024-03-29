from app import db
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Perfil(db.Model, Base):
    __tablename__ = "perfil"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(45), nullable=True)
    data_nascimento = db.Column(db.Date(), nullable=True)
    interesses = db.Column(db.String(45), nullable=True)
    descricao = db.Column(db.String(200), nullable=True)
    genero = db.Column(db.String(45), nullable=True)
    nome = db.Column(db.String(45), nullable=False)
    sobrenome = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(45), nullable=False)
    senha = db.Column(db.String(45), nullable=False)
    tipo_conta = db.Column(db.String(45), nullable=True)
    social_id = db.Column(db.String(45), nullable=True)
    canal = relationship('Canal', back_populates="perfil", cascade="all, delete-orphan")

    def __repr__(self):
        return self.nome
