# Inspector Dockerfile
# Root.io/JFrog-hardened base image via the internal ECR mirror, instead of pulling
# node:20-alpine directly from Docker Hub (Aikido "use root images from our repositories").
FROM 856965016623.dkr.ecr.us-east-1.amazonaws.com/root-mirror/node:20-alpine

# Install git
RUN apk add --no-cache git

# Clone the MCP Inspector repository
RUN git clone https://github.com/modelcontextprotocol/inspector.git /app
WORKDIR /app

# Install dependencies and build
RUN npm install && npm run build

# Set environment variables if needed
ENV DANGEROUSLY_OMIT_AUTH=true

# Expose the default port
EXPOSE 6277

# Switch to the root user to perform user management tasks
USER root

# Create a restricted user (appuser) and group (appgroup) for running the application
RUN addgroup -S appgroup && adduser -S -h /etc/appuser appuser -G appgroup

# Ensure that the appuser owns the application files and directories.
# Security fix (Aikido "container runs as root", BAI-441): this previously referenced
# ${PROJECT_DIR} and ${PROMETHEUS_MULTIPROC_DIR}, neither of which is defined anywhere in
# this Dockerfile (they expand to empty strings), plus a Python site-packages path that
# doesn't exist in this Node image — leftover from copying a Python service's Dockerfile.
# As a result /app (this image's actual WORKDIR, containing the cloned+built inspector)
# was never chowned to appuser, so although USER below did switch the running UID, the
# non-root user didn't actually own the files it needs to read/write at runtime. Chown the
# real paths this image uses instead: /app and npm's global install directories.
RUN chown -R appuser:appgroup /app /usr/local/lib/node_modules /usr/local/bin

# Switch to the restricted user to enhance security
USER appuser

# Start the inspector
CMD ["npm", "start"]
