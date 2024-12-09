import logging
from typing import Optional, Generator, override, Tuple

from botocore.exceptions import ClientError
from starlette.responses import Response, StreamingResponse

from language_model_gateway.gateway.aws.aws_client_factory import AwsClientFactory
from language_model_gateway.gateway.file_managers.file_manager import FileManager
from language_model_gateway.gateway.utilities.url_parser import UrlParser

logger = logging.getLogger(__name__)


class AwsS3FileManager(FileManager):
    def __init__(self, *, aws_client_factory: AwsClientFactory) -> None:
        self.aws_client_factory = aws_client_factory
        assert self.aws_client_factory is not None
        assert isinstance(self.aws_client_factory, AwsClientFactory)

    @override
    async def save_file_async(
        self, *, image_data: bytes, folder: str, filename: str
    ) -> Optional[str]:
        """
        Save the generated image to S3

        :param image_data: Image bytes to save
        :param filename: Filename to use in S3
        :param folder: Folder to save the image in
        """
        # Parse S3 URL
        bucket_name: str
        prefix: str
        bucket_name, prefix = self.get_bucket(filename=filename, folder=folder)

        s3_full_path: str = self.get_full_path(folder=bucket_name, filename=prefix)

        s3_client = self.aws_client_factory.create_client(service_name="s3")
        if not image_data:
            logger.error("No image to save")
            return None

        try:
            # Upload the image to S3
            s3_client.put_object(
                Bucket=bucket_name,
                Key=prefix,
                Body=image_data,
                ContentType="image/png",  # Adjust content type as needed
            )

            logger.info(f"Image saved to S3: {s3_full_path}")
            return s3_full_path

        except ClientError as e:
            logger.error(f"Error saving image to S3: {e}")
            raise

    @override
    def get_full_path(self, *, filename: str, folder: str) -> str:
        # Convert Path to string for S3 key
        assert folder
        assert filename
        s3_full_path = f"s3://" + UrlParser.combine_path(folder, filename)
        return s3_full_path

    # noinspection PyMethodMayBeStatic
    def get_bucket(self, *, filename: str, folder: str) -> Tuple[str, str]:
        bucket_name: str
        prefix: str
        full_path = UrlParser.combine_path(folder, filename=filename)
        bucket_name, prefix = UrlParser.parse_s3_uri(full_path)
        assert bucket_name
        assert prefix
        return bucket_name, prefix

    @override
    async def read_file_async(
        self, *, folder: str, file_path: str
    ) -> StreamingResponse | Response:
        s3_client = self.aws_client_factory.create_client(service_name="s3")

        try:
            bucket_name: str
            prefix: str
            bucket_name, prefix = self.get_bucket(filename=file_path, folder=folder)

            s3_full_path: str = self.get_full_path(folder=bucket_name, filename=prefix)
            logger.info(f"Reading file from S3: {s3_full_path}")

            response = s3_client.get_object(Bucket=folder, Key=prefix)

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
                logger.error(f"File not found: {file_path} in bucket {folder}")
                logger.exception(e)
                return Response(
                    status_code=404,
                    content=f"File not found: {file_path} in bucket {folder}",
                )
            elif error_code == "NoSuchBucket":
                logger.error(f"Bucket not found: {folder}")
                logger.exception(e)
                return Response(status_code=404, content=f"Bucket not found: {folder}")
            else:
                logger.exception(e)
                return Response(
                    status_code=500, content=f"Internal server error: {e} {e.response}"
                )
