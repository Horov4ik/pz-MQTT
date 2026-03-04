FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
# Ensure templates are copied into the image so Flask's render_template can find them
COPY templates ./templates
# If a standalone index.html exists at project root (fallback), copy it too
COPY index.html ./index.html
CMD ["python", "app.py"]
