import logging
from typing import Optional, Generator, override

import boto3
from botocore.exceptions import ClientError
from starlette.responses import Response, StreamingResponse

from language_model_gateway.gateway.aws.aws_client_factory import AwsClientFactory
from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.utilities.s3_url import S3Url
from language_model_gateway.gateway.utilities.url_parser import UrlParser

logger = logging.getLogger(__name__)


class AwsS3FileManager(FileManager):
    def __init__(self, *, aws_client_factory: AwsClientFactory) -> None:
        self.aws_client_factory = aws_client_factory
        assert self.aws_client_factory is not None
        assert isinstance(self.aws_client_factory, AwsClientFactory)

    @override
    async def save_file_async(
        self,
        *,
        file_data: bytes,
        folder: str,
        filename: str,
        content_type: str = "image/png",
    ) -> Optional[str]:
        """
        Save the given file to S3

        :param file_data: File bytes to save
        :param filename: Filename to use in S3
        :param folder: Folder to save the image in
        :param content_type: Content type of the image
        """
        assert "s3://" in folder, "folder should contain s3://"
        assert "s3://" not in filename, "filename should not contain s3://"

        # Parse S3 URL
        # bucket_name: str
        # prefix: str
        s3_url: S3Url = self.get_bucket(filename=filename, folder=folder)

        s3_full_path: str = s3_url.url

        s3_client = self.aws_client_factory.create_client(service_name="s3")
        if not file_data:
            logger.error("No file to save")
            return None

        try:
            # Upload the image to S3

            s3_client.put_object(
                Bucket=s3_url.bucket,
                Key=s3_url.key,
                Body=file_data,
                ContentType=content_type,  # Adjust content type as needed
            )

            logger.info(f"File saved to S3: {s3_full_path}")
            return s3_full_path

        except ClientError as e:
            logger.error(f"File saving image to S3: {e}")
            raise

    @override
    def get_full_path(self, *, filename: str, folder: str) -> str:
        # Convert Path to string for S3 key
        assert folder
        assert filename
        s3_full_path = "s3://" + UrlParser.combine_path(folder, filename)
        return s3_full_path

    # noinspection PyMethodMayBeStatic
    def get_bucket(self, *, filename: str, folder: str) -> S3Url:
        assert folder
        assert filename
        if not folder.startswith("s3://"):
            folder = f"s3://{folder}"
        full_path = UrlParser.combine_path(folder, filename=filename)
        s3_url = S3Url(full_path)
        return s3_url

    @override
    async def read_file_async(
        self, *, folder: str, file_path: str
    ) -> StreamingResponse | Response:
        s3_client: boto3.client = self.aws_client_factory.create_client(
            service_name="s3"
        )

        assert "s3://" not in folder, (
            "folder should not contain s3://.  It should be the bucket name"
        )
        assert "s3://" not in file_path, (
            "file_path should not contain s3://.  It should be the file path"
        )
        s3_url: S3Url = self.get_bucket(folder=f"s3://{folder}", filename=file_path)
        try:
            s3_full_path: str = self.get_full_path(
                folder=s3_url.bucket, filename=s3_url.key
            )

            logger.info(
                f"Reading file from S3: {s3_full_path}, bucket: {s3_url.bucket}, key: {s3_url.key}"
            )
            response = s3_client.get_object(Bucket=s3_url.bucket, Key=s3_url.key)

            content_type = response.get("ContentType", "application/octet-stream")

            def iterate_bytes() -> Generator[bytes, None, None]:
                for chunk in response["Body"].iter_chunks():
                    yield chunk

            return StreamingResponse(
                iterate_bytes(),
                media_type=content_type,
                headers={
                    "Content-Length": str(response["ContentLength"]),
                    "Last-Modified": response["LastModified"].strftime(
                        "%a, %d %b %Y %H:%M:%S GMT"
                    ),
                    "ETag": response["ETag"],
                    # 'Cache-Control': f'public, max-age={self.cache_max_age}',
                    "Accept-Ranges": "bytes",
                },
            )

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            if error_code == "NoSuchKey":
                logger.error(f"File not found: {s3_url.key} in bucket {s3_url.bucket}")
                logger.exception(e)
                # Verify the exact path
                # List objects to debug
                try:
                    objects = s3_client.list_objects_v2(
                        Bucket=s3_url.bucket,
                        Prefix="/".join(s3_url.key.split("/")[:-1]) + "/",
                    )
                    existing_keys = [obj["Key"] for obj in objects.get("Contents", [])]
                    logger.error(f"Existing keys in similar path: {existing_keys}")
                except Exception as list_error:
                    logger.error(f"Error listing objects: {list_error}")
                return Response(
                    status_code=404,
                    content=f"File not found: {s3_url.key} in bucket {s3_url.bucket}",
                )
            elif error_code == "NoSuchBucket":
                logger.error(f"Bucket not found: {s3_url.bucket}")
                logger.exception(e)
                return Response(
                    status_code=404, content=f"Bucket not found: {s3_url.bucket}"
                )
            else:
                logger.exception(e)
                return Response(
                    status_code=500, content=f"Internal server error: {e} {e.response}"
                )
