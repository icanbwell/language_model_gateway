import pytest

from language_model_gateway.gateway.oauth.google_drive_file_downloader import (
    GoogleDriveFileDownloader,
)


# Pytest configuration and tests
def test_google_drive_file_download() -> None:
    """
    Integration test for downloading a file from Google Drive.

    Prerequisites:
    1. Set GOOGLE_TEST_FILE_ID environment variable
    2. Ensure proper authentication is set up
    """
    # URL parsing
    url = "https://docs.google.com/spreadsheets/d/17fUUdYrIOy7Q6jv-yJT9uyCXk3Gh_lpflGK9iWeX4Ps/edit?usp=sharing"

    # Attempt to download the file
    try:
        # Download file
        file_content = GoogleDriveFileDownloader.download_from_url(url=url)

        # Assertions
        assert file_content, "Downloaded file content should not be empty"
        assert isinstance(file_content, bytes), "File content should be in bytes"

        # Optional: Check file size (adjust as needed)
        assert len(file_content) > 0, "File should have some content"

        # Optional: Print file size for debugging
        print(f"Downloaded file size: {len(file_content)} bytes")

    except Exception as e:
        # Provide detailed error information
        pytest.fail(f"File download failed: {str(e)}")
