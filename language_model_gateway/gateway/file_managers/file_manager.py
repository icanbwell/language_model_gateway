import logging
from typing import Optional

from starlette.responses import Response, StreamingResponse

logger = logging.getLogger(__name__)


class FileManager:
    # noinspection PyMethodMayBeStatic
    async def save_file_async(
        self,
        *,
        file_data: bytes,
        folder: str,
        filename: str,
        content_type: str = "image/png"
    ) -> Optional[str]:
        raise NotImplementedError("Must be implemented in a subclass")

    # noinspection PyMethodMayBeStatic
    def get_full_path(self, *, filename: str, folder: str) -> str:
        raise NotImplementedError("Must be implemented in a subclass")

    async def read_file_async(
        self, *, folder: str, file_path: str
    ) -> StreamingResponse | Response:
        raise NotImplementedError("Must be implemented in a subclass")

    @staticmethod
    async def extract_content(response: StreamingResponse) -> str:
        """
        Extracts and returns content from a streaming response.
        :param response: (StreamingResponse) s3 response for the file
        :return: returns the file content in string format.
        """
        extracted_content = ""
        async for chunk in response.body_iterator:
            # Decode the chunk, assuming it is UTF-8 encoded
            extracted_content += chunk.decode("utf-8")  # type: ignore

        return extracted_content
