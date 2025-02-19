# Use AWS Lambda Python Base Image
FROM public.ecr.aws/lambda/python:3.11

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Install Mangum for AWS Lambda compatibility
RUN pip install mangum

# Command to run the Lambda function
CMD ["app.main.lambda_handler"]