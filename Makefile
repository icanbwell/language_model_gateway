export LANG

.PHONY: uv.lock
uv.lock: down create-docker-network ## Locks dependencies and updates uv.lock on the local file system
	docker compose --progress=plain build --no-cache --build-arg RUN_UV_LOCK=true language-model-gateway && \
	docker compose --progress=plain run language-model-gateway sh -c "cp -f /tmp/uv.lock /usr/src/language_model_gateway/uv.lock"

.PHONY:devsetup
devsetup: ## one time setup for devs
	brew install mkcert && \
	make up && \
	make setup-pre-commit && \
	make tests && \
	make up

.PHONY: create-docker-network
create-docker-network: ## creates the docker network
	@set -e; \
	docker network rm language-model-gateway_web >/dev/null 2>&1 && echo "Removed existing web network" || true; \
	echo "Creating web docker network with compose labels"; \
	docker network create --driver bridge \
		--label com.docker.compose.project=baileyai \
		--label com.docker.compose.network=language-model-gateway_web \
		language-model-gateway_web >/dev/null

.PHONY:build
build: down create-docker-network ## Builds the docker for dev
	docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose.yml \
	-f docker-compose-openwebui.yml \
	-f docker-compose-mcp-server-gateway.yml \
	-f docker-compose-mongo.yml \
	-f docker-compose-fhir.yml \
	-f docker-compose-embedding.yml \
	-f docker-compose-mcp-fhir-agent.yml \
	 build --parallel;

.PHONY: up
up: create-docker-network fix-script-permissions ## starts docker containers
	docker compose --progress=plain \
	-f docker-compose-keycloak.yml \
	 -f docker-compose-mongo.yml up -d && \
	sh scripts/wait-for-healthy.sh language-model-gateway-keycloak-1 150 2 || exit 1 && \
	sh scripts/wait-for-healthy.sh language-model-gateway-mongo-1 || exit 1 && \
	docker compose --progress=plain \
	-f docker-compose.yml up -d && \
	sh scripts/wait-for-healthy.sh language-model-gateway || exit 1 && \
	echo ""
	@echo language-model-gateway Service: http://localhost:5050/graphql

.PHONY: up-integration
up-integration: fix-script-permissions ## starts docker containers
	docker compose -f docker-compose.yml -f docker-compose-integration.yml up --build -d && \
	sh scripts/wait-for-healthy.sh language-model-gateway && \
	if [ $? -ne 0 ]; then exit 1; fi && \
	echo ""
	@echo language-model-gateway Service: http://localhost:5050/graphql

.PHONY: up-open-webui
up-open-webui: fix-script-permissions clean-database ## starts docker containers
	UID=$$(id -u) GID=$$(id -g) docker compose --progress=plain -f docker-compose-openwebui.yml up --build -d
	sh scripts/wait-for-healthy.sh language-model-gateway-open-webui-1 || exit 1
	@echo ""
	@echo OpenWebUI: http://localhost:3050

.PHONY: up-open-webui-ssl
up-open-webui-ssl: fix-script-permissions clean-database ## starts docker containers
	UID=$$(id -u) GID=$$(id -g) docker compose --progress=plain -f docker-compose-openwebui.yml -f docker-compose-openwebui-ssl.yml up --build -d
	sh scripts/wait-for-healthy.sh language-model-gateway-open-webui-1 || exit 1
	@echo ""
	@echo OpenWebUI: http://localhost:3050 https://open-webui.localhost

.PHONY: up-open-webui-auth
up-open-webui-auth: create-docker-network fix-script-permissions create-certs check-cert-expiry ## starts docker containers
	docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose-mongo.yml \
	-f docker-compose.yml \
	-f docker-compose-mcp-server-gateway.yml \
	up -d
	sh scripts/wait-for-healthy.sh language-model-gateway-keycloak-1 150 2 || exit 1 && \
	sh scripts/wait-for-healthy.sh language-model-gateway-mongo-1 || exit 1 && \
	sh scripts/wait-for-healthy.sh language-model-gateway-mcp_server_gateway-1 || exit 1
	UID=$$(id -u) GID=$$(id -g) docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose-mongo.yml \
	-f docker-compose.yml \
	-f docker-compose-openwebui.yml \
	-f docker-compose-openwebui-ssl.yml \
	-f docker-compose-openwebui-auth.yml \
	-f docker-compose-mcp-server-gateway.yml \
	-f docker-compose-otel.yml \
	up -d
	sh scripts/wait-for-healthy.sh language-model-gateway-open-webui-1 || exit 1 && \
	make insert-admin-user \
	&& make insert-admin-user-2 \
	&& make import-open-webui-pipe
	@echo "======== Services are up and running ========"
	@echo OpenWebUI: https://open-webui.localhost
	@echo Click 'Continue with Keycloak' to login
	@echo Use the following credentials:
	@echo Admin User: admin/password
	@echo Normal User: tester/password
	@echo Keycloak: http://keycloak:8080 admin/password
	@echo OIDC debugger: http://localhost:8085
	@echo Language Model Gateway Auth Test: http://localhost:5050/auth/login
	@echo Publish Skill to Marketplace: http://localhost:5050/skills/publish
	@echo OpenWebUI API docs: https://open-webui.localhost//docs
	@echo Jaeger UI: http://localhost:16686

.PHONY: up-mcp-fhir-agent
up-mcp-fhir-agent:
	docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose-mongo.yml \
	-f docker-compose-fhir.yml \
	-f docker-compose-embedding.yml \
	-f docker-compose-mcp-fhir-agent.yml \
	up -d
	sh scripts/wait-for-healthy.sh language-model-gateway-mcp-fhir-agent-1 || exit 1 && \
	sh scripts/wait-for-healthy.sh language-model-gateway-mcp-fhir-agent-dev-1 || exit 1

.PHONY: up-mcp-server-gateway
up-mcp-server-gateway:
	docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose.yml \
	-f docker-compose-mcp-server-gateway.yml \
	up -d
	sh scripts/wait-for-healthy.sh language-model-gateway-mcp_server_gateway-1

.PHONY: up-all
up-all: up-open-webui-auth up-mcp-fhir-agent up-mcp-inspector ## starts all docker containers
	@echo "======== All Services are up and running ========"
	@echo OpenWebUI: https://open-webui.localhost
	@echo Click 'Continue with Keycloak' to login
	@echo Use the following credentials:
	@echo Admin User: admin/password
	@echo Normal User: tester/password
	@echo Keycloak: http://keycloak:8080 admin/password
	@echo OIDC debugger: http://localhost:8085
	@echo Language Model Gateway Auth Test: http://localhost:5050/auth/login
	@echo Publish Skill to Marketplace: http://localhost:5050/skills/publish
	@echo OpenWebUI API docs: https://open-webui.localhost//docs
	@echo Jaeger UI: http://localhost:16686

.PHONY: up-mcp-inspector
up-mcp-inspector:
	docker compose \
	-f docker-compose-keycloak.yml \
	-f docker-compose-mongo.yml \
	-f docker-compose-fhir.yml \
	-f docker-compose-embedding.yml \
	-f docker-compose-mcp-fhir-agent.yml \
	-f docker-compose-mcp-inspector.yml \
	up -d
	@echo "MCP Inspector: http://localhost:6274/"

.PHONY: down
down: ## stops docker containers
	docker compose --progress=plain \
	  -f docker-compose-keycloak.yml \
	-f docker-compose.yml \
	-f docker-compose-openwebui.yml -f docker-compose-openwebui-ssl.yml -f docker-compose-openwebui-auth.yml \
	-f docker-compose-mcp-server-gateway.yml \
	down --remove-orphans

.PHONY:update
update: uv.lock setup-pre-commit  ## Updates all the packages using pyproject.toml
	make build && \
	make run-pre-commit && \
	echo "In PyCharm, do File -> Invalidate Caches/Restart to refresh" && \
	echo "If you encounter issues with remote sources being out of sync, click on the 'Remote Python' feature on" && \
	echo "the lower status bar and reselect the same interpreter and it will rebuild the remote source cache." && \
	echo "See this link for more details:" && \
	echo "https://intellij-support.jetbrains.com/hc/en-us/community/posts/205813579-Any-way-to-force-a-refresh-of-external-libraries-on-a-remote-interpreter-?page=2#community_comment_360002118020"


.DEFAULT_GOAL := help
.PHONY: help
help: ## Show this help.
	# from https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY:tests
tests: ## Runs all the tests
	docker compose run --rm --name language-model-gateway_tests language-model-gateway pytest tests

.PHONY:tests-integration
tests-integration: ## Runs all the tests
	docker compose run --rm -e RUN_TESTS_WITH_REAL_LLM=1 --name language-model-gateway_tests language-model-gateway pytest tests

.PHONY:shell
shell: ## Brings up the bash shell in dev docker
	docker compose run --rm --name language-model-gateway_shell language-model-gateway /bin/sh

.PHONY:clean-pre-commit
clean-pre-commit: ## removes pre-commit hook
	rm -f .git/hooks/pre-commit

.PHONY:setup-pre-commit
setup-pre-commit:
	cp ./pre-commit-hook ./.git/hooks/pre-commit

.PHONY:run-pre-commit
run-pre-commit: setup-pre-commit ## runs pre-commit on all files
	./.git/hooks/pre-commit pre_commit_all_files

.PHONY: clean
clean: down clean-database ## Cleans all the local docker setup

.PHONY: nuclear
nuclear: clean ## Cleans fully docker storage
	docker system prune -a -y
	docker builder prune --force || true
	docker rmi $$(docker images -a -q) --force || true

.PHONY: clean-database
clean-database: down ## Cleans all the local docker setup
ifneq ($(shell docker volume ls | grep "language-model-gateway"| awk '{print $$2}'),)
	docker volume ls | grep "language-model-gateway" | awk '{print $$2}' | xargs docker volume rm
endif

.PHONY: insert-admin-user
insert-admin-user: ## Inserts an admin user with email 'admin@localhost' if it does not already exist
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "INSERT INTO public.\"user\" (id, name, email, \"role\", profile_image_url, created_at, updated_at, last_active_at, settings, info, username, bio, gender, date_of_birth, profile_banner_image_url, timezone, presence_state, status_emoji, status_message, status_expires_at, oauth) \
    SELECT '8d967d73-99b8-40ff-ac3b-c71ac19e1286', 'User', 'admin@localhost.com', 'admin', '/user.png', 1735089600, 1735089600, 1735089609, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL \
    WHERE NOT EXISTS (SELECT 1 FROM public.\"user\" WHERE id = '8d967d73-99b8-40ff-ac3b-c71ac19e1286');"

.PHONY: insert-admin-user-2
insert-admin-user-2: ## Inserts an admin user with email 'admin@tester.com' and api_key 'sk-my-api-key' if it does not already exist
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "INSERT INTO public.\"user\" (id, name, email, \"role\", profile_image_url, created_at, updated_at, last_active_at, settings, info, username, bio, gender, date_of_birth, profile_banner_image_url, timezone, presence_state, status_emoji, status_message, status_expires_at, oauth) \
    SELECT 'f841d162-89a8-46f7-89c2-bf112029d19c', 'admin@tester.com', 'admin@tester.com', 'admin', '/user.png', 1756681388, 1756681388, 1756681389, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL \
    WHERE NOT EXISTS (SELECT 1 FROM public.\"user\" WHERE email='admin@tester.com');" && \
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "INSERT INTO public.api_key (id, user_id, \"key\", \"data\", expires_at, last_used_at, created_at, updated_at) \
    SELECT '2e9a3b4c-1234-5678-9abc-def012345678', 'f841d162-89a8-46f7-89c2-bf112029d19c', 'sk-my-api-key', NULL, NULL, NULL, 1756681388, 1756681388 \
    WHERE NOT EXISTS (SELECT 1 FROM public.api_key WHERE \"key\"='sk-my-api-key');"

.PHONY: set-admin-user-role
set-admin-user-role: ## Sets the role of the user 'admin@tester.com' to admin
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "UPDATE public.\"user\" SET \"role\"='admin' WHERE name='admin@tester.com';"

CERT_DIR := certs
CERT_KEY := $(CERT_DIR)/open-webui.localhost-key.pem
CERT_CRT := $(CERT_DIR)/open-webui.localhost.pem

.PHONY: all install-ca create-certs check-cert-expiry
# Install local Certificate Authority
install-ca: ## Installs a local CA using mkcert
	mkcert -install

# Check certificate expiry
check-cert-expiry: ## Checks if the SSL certificate expires within 1 day and fails if not valid
	@if [ -f "$(CERT_CRT)" ]; then \
		expiry_date=$$(openssl x509 -enddate -noout -in $(CERT_CRT) | cut -d= -f2); \
		echo "DEBUG: checking certificate is '$(CERT_CRT)'"; \
		echo "DEBUG: expiry_date is '$$expiry_date'"; \
		expiry_epoch=$$(date -j -f "%b %d %H:%M:%S %Y %Z" "$$expiry_date" "+%s" 2>/dev/null); \
		echo "DEBUG: expiry_epoch is '$$expiry_epoch'"; \
		now_epoch=$$(date "+%s"); \
		echo "DEBUG: now_epoch is '$$now_epoch'"; \
		diff_days=$$(( ($$expiry_epoch - $$now_epoch) / 86400 )); \
		echo "DEBUG: diff_days is '$$diff_days'"; \
		if [ -z "$$expiry_epoch" ]; then \
			echo "ERROR: Could not parse expiry date: $$expiry_date"; \
			exit 1; \
		fi; \
		if [ "$$diff_days" -lt 1 ]; then \
			echo "ERROR: Certificate $(CERT_CRT) is valid for less than 1 day ($$expiry_date)"; \
			exit 1; \
		else \
			echo "Certificate $(CERT_CRT) is valid for $$diff_days more days ($$expiry_date)"; \
		fi; \
	else \
		echo "Certificate $(CERT_CRT) not found."; \
		exit 1; \
	fi

# Create certificates
create-certs: install-ca ## Creates self-signed certificates for open-webui.localhost
	@if [ ! -f "$(CERT_CRT)" ]; then \
		mkdir -p $(CERT_DIR); \
		mkcert open-webui.localhost localhost 127.0.0.1 ::1; \
		mv ./open-webui.localhost+3.pem $(CERT_CRT); \
		mv ./open-webui.localhost+3-key.pem $(CERT_KEY); \
		echo "Certificates generated in $(CERT_DIR)"; \
	else \
		echo "Certificates already exist at $(CERT_CRT)"; \
	fi

clean_certs:
	rm -rf $(CERT_DIR)

.PHONY: import-open-webui-pipe
import-open-webui-pipe: ## Imports the OpenWebUI function pipe into OpenWebUI
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
	"DELETE FROM public.function WHERE id='language_model_gateway';"
	docker run --rm -it --name openid-function-creator \
        --network language-model-gateway_web \
        --mount type=bind,source="${PWD}"/openwebui-config/functions,target=/app \
        python:3.12-alpine \
        sh -c "pip install --root-user-action=ignore --upgrade pip && \
               pip install --root-user-action=ignore authlib requests && \
               cd /app && \
               python3 import_pipe.py \
               --url 'http://language-model-gateway-open-webui-1:8080' \
               --api-key 'sk-my-api-key' \
               --json 'language_model_gateway_pipe.json' \
               --file 'language_model_gateway_pipe.py'"

.PHONY: configure-openai-connection
configure-openai-connection: ## Configurates OpenWebUI to use direct connection
	docker exec -i language-model-gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
	"DELETE FROM public.function WHERE id='language_model_gateway';"
	docker run --rm -it --name openid-function-creator \
        --network language-model-gateway_web \
        --mount type=bind,source="${PWD}"/openwebui-config/functions,target=/app \
        python:3.12-alpine \
        sh -c "pip install --root-user-action=ignore --upgrade pip && \
               pip install --root-user-action=ignore authlib requests && \
               cd /app && \
               python3 configure_openai_connection.py \
               --url 'http://language-model-gateway-open-webui-1:8080' \
               --api-key 'sk-my-api-key' \
               --connection-url='http://language-model-gateway:5000/api/v1' \
               "

.PHONY: fix-script-permissions
fix-script-permissions:
	chmod +x ./scripts/wait-for-healthy.sh

.PHONY:show-dependency-graph
show-dependency-graph: build ## Generates a dependency graph of the Python packages and writes to dependency_graph.json
	@docker compose run --rm --name language-model-gateway_shell language-model-gateway \
	sh -c "pip install pipdeptree >/dev/null 2>&1 && pipdeptree --reverse --output json-tree" > dependency_graph_reverse.json && \
		echo "Dependency graph written to dependency_graph_reverse.json"
	@docker compose run --rm --name language-model-gateway_shell language-model-gateway \
	sh -c "pip install pipdeptree >/dev/null 2>&1 && pipdeptree --reverse" > dependency_graph_reverse.txt && \
		echo "Dependency graph written to dependency_graph_reverse.txt"
	@docker compose run --rm --name language-model-gateway_shell language-model-gateway \
	sh -c "pip install pipdeptree >/dev/null 2>&1 && pipdeptree" > dependency_graph.txt && \
		echo "Dependency graph written to dependency_graph.txt"


.PHONY: inspector
inspector:
	docker run --rm \
	  -p 127.0.0.1:6274:6274 \
	  -p 127.0.0.1:6277:6277 \
	  -e HOST=0.0.0.0 \
	  -e MCP_AUTO_OPEN_ENABLED=false \
	  ghcr.io/modelcontextprotocol/inspector:latest
