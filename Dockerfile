#Use python:3.11-slim since assignment suggest
FROM python:3.11-slim

#Set working directory
WORKDIR /app

#Copy and install all the dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy all the project files to the working directory
COPY . .

#Set the flask
ENV FLASK_APP=app.py

# expose port 5000
EXPOSE 5000


CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]