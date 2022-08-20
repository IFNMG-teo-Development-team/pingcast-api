from app import db

class Podcast(db.Model):
    __tablename__ = "podcast"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    duracao = db.Column(db.Time, nullable=False)
    data_postagem = db.Column(db.Date, nullable=False)
    participantes = db.Column(db.String(45), nullable=True)
    descricao = db.Column(db.String(45), nullable=False)
    nome = db.Column(db.String(45), nullable=False)
    post_podcast = db.Column(db.Integer, db.ForeignKey("canal.id"))
    canal = db.relationship('Canal')

    def __repr__(self):
        return self.nome


