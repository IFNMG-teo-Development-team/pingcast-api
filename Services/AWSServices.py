from app import s3, s3_client
import boto3

# s3.Bucket("pingcast").download_file('teste.png')

def setFileBucket(file, perfil, podcast):
    s3.Bucket('pingcast').put_object(Key=f"{perfil}_{podcast}.mp3", Body=file)
    return {"Upload realizado com sucesso! "}, 200


def getFileBucket(key):

    url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': "pingcast",
            'Key': key,
        },
        ExpiresIn=600
    )

    return url


def deleteFileBucket(key):
    s3.Object('pingcast', key).delete()
