# Use an official Python runtime as a parent image
FROM continuumio/anaconda3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN conda install flask
RUN conda install -c lenskit lenskit
RUN conda install -c conda-forge flask-restful

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Run app.py when the container launches
CMD ["python", "app.py"]





# 1) remove the old dockers
# 2) build the image
# 3) run interactive shell 
# 4) run image
# 5) run image in background 
# docker rm imagerun
# docker build -t imagebuild .
# docker run -it --name imagerun -p 5000:5000 imagebuild /bin/bash
# docker run --name imagerun -p 5000:5000 imagebuild 
# docker run -d -p 4000:80 imagebuild


