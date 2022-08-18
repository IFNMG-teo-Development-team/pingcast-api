from marshmallow import Schema


# Classes para definição dos campos de retorno de cada tabela
class PerfilSerializer(Schema):
    class Meta:
        fields = ("id", "username", "data_nascimento", "interesses", "descricao", "genero", "nome", "sobrenome", "tipo_conta")


# Classes para definição dos campos de retorno de cada tabela
class CanalSerializer(Schema):
    class Meta:
        fields = ("id", "nome", "tema", "bio", "dono")
