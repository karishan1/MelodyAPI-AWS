FROM public.ecr.aws/lambda/python:3.11

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /var/task

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app app/
COPY models models/

RUN pip install --no-cache-dir mangum

CMD ["app.main.lambda_handler"]