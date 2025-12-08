import boto3
from botocore.client import Config
from django.conf import settings
import io


def get_timestamp():
    """
    Generates a timestamped filename for uploads.
    :return: Formatted filename string
    """
    from datetime import datetime
    return datetime.now().strftime("%Y%m%d%H%M%S")


class FilebaseIPFS:

    def __init__(self):
        self.client = boto3.client(
            's3',
            endpoint_url='https://s3.filebase.com',
            aws_access_key_id=settings.FILEBASE_KEY,
            aws_secret_access_key=settings.FILEBASE_SECRET,
            config=Config(signature_version='s3v4')
        )
        self.bucket = settings.BUCKET_NAME

    def upload_and_get_cid(self, file_bytes_or_path, object_name=None):
        """
        Uploads either raw bytes or a file path to Filebase IPFS and returns its CID.

        :param file_bytes_or_path: bytes (raw file) or str (file path)
        :param object_name: Optional name to store in bucket
        :return: CID string if successful, else None
        """
        try:
            if not object_name:
                object_name = get_timestamp()

            if isinstance(file_bytes_or_path, (bytes, bytearray)):
                # Use BytesIO for uploading bytes
                file_obj = io.BytesIO(file_bytes_or_path)
                self.client.upload_fileobj(
                    Fileobj=file_obj,
                    Bucket=self.bucket,
                    Key=object_name,
                    ExtraArgs={'Metadata': {'ipfs': 'true'}}
                )
            elif isinstance(file_bytes_or_path, str):
                # File path
                self.client.upload_file(
                    file_bytes_or_path,
                    self.bucket,
                    object_name,
                    ExtraArgs={'Metadata': {'ipfs': 'true'}}
                )
            else:
                raise ValueError("file_bytes_or_path must be bytes or file path string")

            # Retrieve CID from metadata
            response = self.client.head_object(Bucket=self.bucket, Key=object_name)
            cid = response['Metadata'].get('cid')
            if not cid:
                print("CID not available in metadata.")
                return None
            return cid

        except Exception as e:
            print(f"Upload failed: {str(e)}")
            return None

    def get_file_by_cid(self, cid):
        """
        Downloads a file by CID and returns bytes and optional saved path.

        :param cid: IPFS CID
        :param save_path: Optional path or directory to save file
        :return: dict with 'bytes' and optional 'path'
        """
        try:
            # Find object key by CID
            paginator = self.client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket)
            object_key = None

            for page in page_iterator:
                for obj in page.get('Contents', []):
                    metadata = self.client.head_object(
                        Bucket=self.bucket,
                        Key=obj['Key']
                    )['Metadata']
                    if metadata.get('cid') == cid:
                        object_key = obj['Key']
                        break
                if object_key:
                    break

            if not object_key:
                print("CID not found in bucket.")
                return None

            # Get file bytes
            response = self.client.get_object(Bucket=self.bucket, Key=object_key)
            file_bytes = response['Body'].read()


            return  {'bytes': file_bytes}

        except Exception as e:
            print(f"Retrieval failed: {str(e)}")
            return None

    def delete_file_by_cid(self, cid):
        """
        Deletes a file from Filebase by CID.

        :param cid: IPFS CID
        :return: True if deleted, False otherwise
        """
        try:
            # Find object key by CID
            paginator = self.client.get_paginator('list_objects_v2')
            page_iterator = paginator.paginate(Bucket=self.bucket)
            object_key = None

            for page in page_iterator:
                for obj in page.get('Contents', []):
                    metadata = self.client.head_object(
                        Bucket=self.bucket,
                        Key=obj['Key']
                    )['Metadata']
                    if metadata.get('cid') == cid:
                        object_key = obj['Key']
                        break
                if object_key:
                    break

            if not object_key:
                print(f"CID {cid} not found in bucket.")
                return False

            self.client.delete_object(Bucket=self.bucket, Key=object_key)
            print(f"Successfully deleted file with CID: {cid}")
            return True

        except Exception as e:
            print(f"Deletion failed for CID {cid}: {str(e)}")
            return False

# ipfs = FilebaseIPFS()
#
# print(ipfs.get_file_by_cid("QmfMsrAi7qtd1Fq6QDkJHVsE19vKYwrFCZhPxBxfsgjjSE"))