FROM public.ecr.aws/lambda/python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/task

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir mangum

# Copy binary manually
COPY bin/fpcalc /usr/local/bin/fpcalc
RUN chmod +x /usr/local/bin/fpcalc && ln -s /usr/local/bin/fpcalc /usr/bin/fpcalc

# Copy app and model files
COPY app app/
COPY models models/

# Lambda entrypoint
CMD ["app.main.lambda_handler"]