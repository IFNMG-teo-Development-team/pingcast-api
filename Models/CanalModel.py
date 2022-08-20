from app import db

class Canal(db.Model):
    __tablename__ = "canal"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(45), nullable=False)
    tema = db.Column(db.String(45), nullable=True)
    bio = db.Column(db.String(200), nullable=True)
    dono = db.Column(db.Integer, db.ForeignKey("perfil.id"))
    perfil = db.relationship('Perfil')

    def __repr__(self):
        return self.nome
