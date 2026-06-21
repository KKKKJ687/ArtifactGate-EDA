FROM python:3.11-slim

WORKDIR /workspace
COPY . /workspace
RUN python -m pip install --upgrade pip && python -m pip install -e ".[dev]"
CMD ["artifactgate", "--help"]

