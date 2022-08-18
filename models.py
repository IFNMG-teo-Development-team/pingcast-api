from app import db


class Perfil(db.Model):
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

    def __repr__(self):
        return self.nome

class Canal(db.Model):
    __tablename__ = "canal"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    tema = db.Column(db.String(45), nullable=True)
    bio = db.Column(db.String(200), nullable=True)
    perfil_id = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    perfil = db.relationship(Perfil, backref = db.backref("canal", cascade="all, delete_orphan"))
    def __repr__(self):
        return self.nome