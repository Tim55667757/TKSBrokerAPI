FROM python:3.11-slim

LABEL author="Timur Gilmullin"
LABEL vendor="Fuzzy Technologies"
LABEL version="1.6"
LABEL description="Secure CLI container for TKSBrokerAPI Trading Platform based on Python 3.11-slim"

ENV TZ=Europe/Moscow
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

ARG TKS_BUILD_VERSION

# Build docker image with the current version uploaded to PyPI, or use latest if local build
RUN if [ -z "$TKS_BUILD_VERSION" ]; then \
      echo "📦 Installing latest TKSBrokerAPI from PyPI..." && \
      pip install --no-cache-dir --pre tksbrokerapi; \
    else \
      echo "📦 Installing TKSBrokerAPI==$TKS_BUILD_VERSION from PyPI..." && \
      attempt=0; \
      until pip install --no-cache-dir tksbrokerapi==$TKS_BUILD_VERSION || [ $attempt -ge 5 ]; do \
        attempt=$((attempt+1)); \
        echo "⏳ Attempt $attempt/5: Waiting 5s for PyPI..." && sleep 5; \
      done; \
      if [ $attempt -ge 5 ]; then \
        echo "❌ Failed to install TKSBrokerAPI==$TKS_BUILD_VERSION after 5 attempts"; \
        exit 1; \
      fi; \
    fi

# Clean image
RUN find /usr/local/lib/python3.11/site-packages \( -name "*.pyc" -o -type d -name "__pycache__" \) -exec rm -rf {} +

# Safe user
RUN useradd -m -d /home/appuser -s /bin/bash appuser
RUN chown -R appuser /opt/app

USER appuser

ENTRYPOINT ["tksbrokerapi"]
CMD ["--version"]