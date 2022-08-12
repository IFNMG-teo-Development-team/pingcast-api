from marshmallow import Schema


# Classes para definição dos campos de retorno de cada tabela
class PerfilSerializer(Schema):
    class Meta:
        fields = ("id", "username", "data_nascimento", "interesses", "descricao", "genero", "nome", "tipo_conta")


# Classes para definição dos campos de retorno de cada tabela
class PodcastsSerializer(Schema):
    class Meta:
        fields = ("id", "username", "data_nascimento", "interesses", "descricao", "genero", "nome", "tipo_conta")
