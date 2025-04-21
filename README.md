# language_model_gateway

## Overview

This project is a language model gateway that provides an OpenAI compatible API for language models. It is built using FastAPI and GraphQL.

## Prerequisites

- Docker
- Docker Compose
- Make

## Getting Started

To run the project locally, follow these steps:

1. Clone the repository:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Create `docker.env` file in the root of the project based on the `docker.env.example`. 
Update the keys for the functionality/providers you're planning on using.
`AWS_CREDENTIALS_PROFILE` is the only one that is absolutely required to get going.  Set this to the AWS profile you're part of e.g., `admin_dev`.

3. Set up the development environment:
    ```sh
    make devsetup
    ```

4. Start the Docker containers:
    ```sh
    make down; make up
    ```

## Project Architecture

The project is structured into several main components:

- **API**: Built using FastAPI, it provides endpoints for interacting with the language models.
- **GraphQL**: Used for querying and mutating data.
- **Routers**: Define the routes for different functionalities like chat completions, image generation, etc.
- **Managers**: Handle the business logic for different functionalities.
- **Utilities**: Helper functions and classes used across the project.
- **Tools**: AI Agents that perform specific tasks like querying databases, calling APIs, etc.

## Dependencies

The main libraries and tools used in this project are:

- FastAPI
- GraphQL
- Docker
- Docker Compose
- Make
- Pipenv
- Uvicorn
- Datadog

## Usage Examples

Here are some sample API requests and responses:

### Chat Completions

**Request:**
```sh
curl -X POST "http://localhost:5050/api/v1/chat/completions" -H "Content-Type: application/json" -d '{
  "model": "gpt-3.5-turbo",
  "messages": [{"role": "user", "content": "Hello, how are you?"}]
}'
```

**Response:**
```json
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I am fine, thank you!"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 7,
    "total_tokens": 16
  }
}
```

## Running without OAuth
Just run the following commands to run OpenWebUI without OAuth:

```sh
make down; make up; make up-open-webui
```

## Running with OAuth
Since the OpenWebUI uses Keycloak on both server side and browser side, you need to create a host mapping for `keycloak`.

On Macs, this can be done by adding an entry to `/etc/hosts`:

```sh
127.0.0.1   keycloak
```

Then run:
```shell
make down; make up; make up-open-webui-auth
```

## Contributing

We welcome contributions to the project! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them with a clear message.
4. Push your changes to your fork.
5. Create a pull request to the main repository.

## Reporting Issues

If you encounter any issues, please report them by creating a new issue in the repository's issue tracker.

## Frequently Asked Questions (FAQs)

### How do I set up the environment variables?

Create a `docker.env` file in the root of the project based on the `docker.env.example` file. Update the keys for the functionality/providers you're planning on using.

### How do I run the tests?

You can run the tests using the following command:
```sh
make tests
```

### How do I add a new AI Agent?

Refer to the [add_new_agent.md](add_new_agent.md) file for detailed instructions on how to add a new AI Agent.

## Troubleshooting Tips

- If you encounter issues with Docker, try restarting the Docker service.
- Ensure that all environment variables are set correctly.
- Check the logs for any error messages and stack traces.
