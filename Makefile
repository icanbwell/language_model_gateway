export LANG

.PHONY: Pipfile.lock
Pipfile.lock: # Locks Pipfile and updates the Pipfile.lock on the local file system
	docker compose --progress=plain build --no-cache --build-arg RUN_PIPENV_LOCK=true dev && \
	docker compose --progress=plain run dev sh -c "cp -f /tmp/Pipfile.lock /usr/src/language_model_gateway/Pipfile.lock"

.PHONY:devsetup
devsetup: ## one time setup for devs
	brew install mkcert && \
	make up && \
	make setup-pre-commit && \
	make tests && \
	make up

.PHONY:build
build: ## Builds the docker for dev
	docker compose build --parallel

.PHONY: up
up: ## starts docker containers
	docker compose up --build -d && \
	echo "waiting for language_model_gateway service to become healthy" && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "healthy" ] && [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "unhealthy" ] && [ "`docker inspect --format {{.State.Status}} language_model_gateway`" != "restarting" ]; do printf "." && sleep 2; done && \
	if [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "healthy" ]; then docker ps && docker logs language_model_gateway && printf "========== ERROR: language_model_gateway did not start. Run docker logs language_model_gateway =========\n" && exit 1; fi && \
	echo ""
	@echo language_model_gateway Service: http://localhost:5050/graphql

.PHONY: up-integration
up-integration: ## starts docker containers
	docker compose -f docker-compose.yml -f docker-compose-integration.yml up --build -d && \
	echo "waiting for language_model_gateway service to become healthy" && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "healthy" ] && [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "unhealthy" ] && [ "`docker inspect --format {{.State.Status}} language_model_gateway`" != "restarting" ]; do printf "." && sleep 2; done && \
	if [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway`" != "healthy" ]; then docker ps && docker logs language_model_gateway && printf "========== ERROR: language_model_gateway did not start. Run docker logs language_model_gateway =========\n" && exit 1; fi && \
	echo ""
	@echo language_model_gateway Service: http://localhost:5050/graphql


.PHONY: up-open-webui
up-open-webui: clean_database ## starts docker containers
	docker compose --progress=plain -f docker-compose-openwebui.yml up --build -d
	echo "waiting for open-webui service to become healthy" && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ]; do printf "." && sleep 2; done && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ] && [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "unhealthy" ] && [ "`docker inspect --format {{.State.Status}} language_model_gateway-open-webui-1`" != "restarting" ]; do printf "." && sleep 2; done && \
	if [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ]; then docker ps && docker logs language_model_gateway-open-webui-1 && printf "========== ERROR: language_model_gateway-open-webui-1 did not start. Run docker logs language_model_gateway-open-webui-1 =========\n" && exit 1; fi && \
	echo ""
	@echo OpenWebUI: http://localhost:3050

.PHONY: up-open-webui-ssl
up-open-webui-ssl: clean_database ## starts docker containers
	docker compose --progress=plain -f docker-compose-openwebui.yml -f docker-compose-openwebui-ssl.yml up --build -d
	echo "waiting for open-webui service to become healthy" && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ]; do printf "." && sleep 2; done && \
	while [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ] && [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "unhealthy" ] && [ "`docker inspect --format {{.State.Status}} language_model_gateway-open-webui-1`" != "restarting" ]; do printf "." && sleep 2; done && \
	if [ "`docker inspect --format {{.State.Health.Status}} language_model_gateway-open-webui-1`" != "healthy" ]; then docker ps && docker logs language_model_gateway-open-webui-1 && printf "========== ERROR: language_model_gateway-open-webui-1 did not start. Run docker logs language_model_gateway-open-webui-1 =========\n" && exit 1; fi && \
	echo ""
	@echo OpenWebUI: http://localhost:3050 https://open-webui.localhost

.PHONY: up-open-webui-auth
up-open-webui-auth: clean_database create-certs ## starts docker containers
	docker compose --progress=plain -f docker-compose-openwebui.yml -f docker-compose-openwebui-ssl.yml -f docker-compose-openwebui-auth.yml up --build -d
	echo "waiting for open-webui service to become healthy" && \
	max_attempts=30 && \
	attempt=0 && \
	while [ $$attempt -lt $$max_attempts ]; do \
		container_status=$$(docker inspect --format '{{.State.Health.Status}}' language_model_gateway-open-webui-1 2>/dev/null) && \
		container_state=$$(docker inspect --format '{{.State.Status}}' language_model_gateway-open-webui-1 2>/dev/null) && \
		if [ "$$container_status" = "healthy" ]; then \
			echo "" && \
			break; \
		elif [ "$$container_status" = "unhealthy" ] || [ "$$container_state" = "restarting" ]; then \
			echo "" && \
			echo "========== ERROR: Container became unhealthy ==========" && \
			docker ps && \
			docker logs language_model_gateway-open-webui-1 && \
			printf "========== ERROR: language_model_gateway-open-webui-1 is unhealthy. Run docker logs language_model_gateway-open-webui-1 =========\n" && \
			exit 1; \
		fi; \
		printf "." && \
		sleep 2 && \
		attempt=$$((attempt + 1)); \
	done && \
	if [ $$attempt -ge $$max_attempts ]; then \
		echo "" && \
		echo "========== ERROR: Container did not become healthy within timeout ==========" && \
		docker ps && \
		docker logs language_model_gateway-open-webui-1 && \
		printf "========== ERROR: language_model_gateway-open-webui-1 did not start. Run docker logs language_model_gateway-open-webui-1 =========\n" && \
		exit 1; \
	fi
	make insert-admin-user
	make set-admin-user-role
	@echo OpenWebUI: http://localhost:3050  https://open-webui.localhost tester/password
	@echo Keycloak: http://keycloak:8080 admin/password
	@echo OIDC debugger: http://localhost:8085

.PHONY: down
down: ## stops docker containers
	docker compose down --remove-orphans

.PHONY:update
update: Pipfile.lock setup-pre-commit  ## Updates all the packages using Pipfile
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
	docker compose run --rm --name language_model_gateway_tests dev pytest tests

.PHONY:tests-integration
tests-integration: ## Runs all the tests
	docker compose run --rm -e RUN_TESTS_WITH_REAL_LLM=1 --name language_model_gateway_tests dev pytest tests

.PHONY:shell
shell: ## Brings up the bash shell in dev docker
	docker compose run --rm --name language_model_gateway_shell dev /bin/sh

.PHONY:clean-pre-commit
clean-pre-commit: ## removes pre-commit hook
	rm -f .git/hooks/pre-commit

.PHONY:setup-pre-commit
setup-pre-commit:
	cp ./pre-commit-hook ./.git/hooks/pre-commit

.PHONY:run-pre-commit
run-pre-commit: setup-pre-commit
	./.git/hooks/pre-commit pre_commit_all_files

.PHONY: clean
clean: down clean_database ## Cleans all the local docker setup

.PHONY: clean_database
clean_database: down ## Cleans all the local docker setup
ifneq ($(shell docker volume ls | grep "language_model_gateway"| awk '{print $$2}'),)
	docker volume ls | grep "language_model_gateway" | awk '{print $$2}' | xargs docker volume rm
endif

.PHONY: insert-admin-user
insert-admin-user:
	docker exec -i language_model_gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "INSERT INTO public.\"user\" (id,name,email,\"role\",profile_image_url,api_key,created_at,updated_at,last_active_at,settings,info,oauth_sub) \
    SELECT '8d967d73-99b8-40ff-ac3b-c71ac19e1286','User','admin@localhost','admin','/user.png',NULL,1735089600,1735089600,1735089609,'{"ui": {"version": "0.4.8"}}','null',NULL \
    WHERE NOT EXISTS (SELECT 1 FROM public.\"user\" WHERE id = '8d967d73-99b8-40ff-ac3b-c71ac19e1286');"

.PHONY: set-admin-user-role
set-admin-user-role:
	docker exec -i language_model_gateway-open-webui-db-1 psql -U myapp_user -d myapp_db -p 5431 -c \
    "UPDATE public.\"user\" SET \"role\"='admin' WHERE name='admin@tester.com';"

CERT_DIR := certs
CERT_KEY := $(CERT_DIR)/open-webui.localhost-key.pem
CERT_CRT := $(CERT_DIR)/open-webui.localhost.pem

.PHONY: all install-ca create-certs

# Install local Certificate Authority
install-ca:
	mkcert -install

# Create certificates
create-certs: install-ca
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
