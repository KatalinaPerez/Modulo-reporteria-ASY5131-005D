import boto3
from keys import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, REGION_NAME

def get_s3():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        aws_session_token=AWS_SESSION_TOKEN,
        region_name=REGION_NAME
    )

def upload_s3(file_bytes,bucket_name, s3_key):
    try:
        s3=get_s3()
        s3.put_object(Bucket=bucket_name, Key=s3_key, Body=file_bytes)
        print(f"✅Archivo subido exitosamente a s3://{bucket_name}/{s3_key}")
        return True
    except Exception as e:
        print(f"❌ Error al subir archivo a S3: {e}")
        return False
    
def download_s3(bucket_name, s3_key, download_path):
    try:
        s3 = get_s3()
        s3.download_file(bucket_name, s3_key, download_path)
        print(f"📥 Archivo descargado a: {download_path}")
        return True
    except Exception as e:
        print(f"❌ Error al descargar archivo: {e}")
        return False

def list_files_s3(bucket_name, prefix=''):
    try:
        s3 = get_s3()
        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        archivos = [item['Key'] for item in response.get('Contents', [])]
        print(f"📂 Archivos en s3://{bucket_name}/{prefix}:")
        for archivo in archivos:
            print(f" - {archivo}")
        return archivos
    except Exception as e:
        print(f"❌ Error al listar archivos: {e}")
        return []
