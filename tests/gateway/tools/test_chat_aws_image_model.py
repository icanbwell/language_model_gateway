import base64
import json
import os
from os import makedirs, path
from pathlib import Path
from shutil import rmtree

import boto3
import pytest


def create_bedrock_client() -> boto3.client:
    """Create and return a Bedrock client"""
    session1 = boto3.Session(profile_name=os.environ.get("AWS_CREDENTIALS_PROFILE"))
    bedrock_client = session1.client(
        service_name="bedrock-runtime",
        region_name="us-east-1",  # Replace with your preferred region
        # Add credentials if not using default AWS configuration:
        # aws_access_key_id='YOUR_ACCESS_KEY',
        # aws_secret_access_key='YOUR_SECRET_KEY'
    )
    return bedrock_client


def generate_image(
    prompt: str, style: str = "natural", image_size: str = "1024x1024"
) -> bytes:
    """Generate an image using Titan Image Generator"""

    # Create Bedrock client
    client = create_bedrock_client()

    # Prepare the request parameters
    request_body = {
        "textToImageParams": {"text": prompt},
        "taskType": "TEXT_IMAGE",
        "imageGenerationConfig": {
            "cfgScale": 8,
            "seed": 0,
            "width": 1024,
            "height": 1024,
            "numberOfImages": 1,
            "quality": "standard",
        },
    }

    try:
        # Invoke the model
        response = client.invoke_model(
            modelId="amazon.titan-image-generator-v2:0", body=json.dumps(request_body)
        )

        # Parse the response
        response_body = json.loads(response["body"].read())

        # Get the base64 encoded image
        base64_image = response_body["images"][0]

        # Convert base64 to bytes
        image_data = base64.b64decode(base64_image)

        return image_data

    except Exception as e:
        raise Exception(f"Error generating image: {str(e)}")


def save_image(image_data: bytes, filename: str = "generated_image.png") -> None:
    """Save the generated image to a file"""
    if image_data:
        with open(filename, "wb") as f:
            f.write(image_data)
        print(f"Image saved as {filename}")
    else:
        print("No image to save")


@pytest.mark.skipif(
    os.getenv("RUN_TESTS_WITH_REAL_LLM") != "1",
    reason="Requires AWS Credentials",
)
def test_chat_aws_image_model() -> None:
    data_dir: Path = Path(__file__).parent.joinpath("./")
    temp_folder = data_dir.joinpath("../temp")
    if path.isdir(temp_folder):
        rmtree(temp_folder)
    makedirs(temp_folder)

    # Define your image prompt
    # prompt = "A serene landscape with mountains and a lake at sunset"
    prompt = "A diagram showing the structure of a neural network"

    # Generate image with different styles
    # styles = ["natural", "cinematic", "digital-art", "pop-art"]
    styles = ["natural"]

    for style in styles:
        print(f"\nGenerating image with {style} style...")
        image_data = generate_image(prompt=prompt, style=style, image_size="1024x1024")

        if image_data:
            save_image(
                image_data, str(data_dir.joinpath(f"temp/generated_image_{style}.png"))
            )
