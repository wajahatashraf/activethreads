# Step 1: Use the official Python image as a base
FROM python:3.12.6

# Step 2: Set the working directory
WORKDIR /app

# Step 3: Copy the current directory contents into the container
COPY . /app

# Step 4: Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Expose the port Flask will run on
EXPOSE 5000

# Step 6: Set environment variables for Flask and PostgreSQL
ENV FLASK_APP=fetchcities.py
ENV FLASK_ENV=development

# Step 7: Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
