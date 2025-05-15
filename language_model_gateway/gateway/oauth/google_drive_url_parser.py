import re
from urllib.parse import urlparse, parse_qs
from typing import Optional


class GoogleDriveURLParser:
    """
    Utility class to parse and extract file ID from various Google Drive URLs
    """

    @staticmethod
    def extract_file_id(url: str) -> Optional[str]:
        """
        Extract file ID from different types of Google Drive URLs.

        Supported URL formats:
        - https://docs.google.com/spreadsheets/d/FILE_ID/edit
        - https://docs.google.com/document/d/FILE_ID/edit
        - https://drive.google.com/file/d/FILE_ID/view
        - Shortened sharing links

        Args:
            url (str): Google Drive sharing URL

        Returns:
            Optional[str]: Extracted file ID or None
        """
        # Patterns for different URL formats
        patterns = [
            r"/d/([a-zA-Z0-9-_]+)",  # Standard drive URL pattern
            r"^([a-zA-Z0-9-_]+)$",  # Bare file ID
        ]

        # Sanitize and normalize the URL
        url = url.strip()

        # Try regex patterns first
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Parse URL components
        try:
            parsed_url = urlparse(url)

            # Handle different domain variations
            if parsed_url.netloc in [
                "docs.google.com",
                "drive.google.com",
                "drive.google.com/file",
            ]:
                # Extract from path
                path_parts = parsed_url.path.split("/")

                # Look for 'd' segment in path
                try:
                    d_index = path_parts.index("d")
                    if d_index + 1 < len(path_parts):
                        return path_parts[d_index + 1]
                except ValueError:
                    pass

            # Try query parameters
            query_params = parse_qs(parsed_url.query)
            if "id" in query_params:
                return query_params["id"][0]

        except Exception:
            pass

        return None
