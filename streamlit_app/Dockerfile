# Dockerfile, Image, Container

#Import the base Image of the Python
FROM python:3.8-slim-buster

#TO be able to define the streamlit port when it runs on EC2
EXPOSE 8501

#Setup a working directory in the container with a name code. While running the code in a container, the Docker will create a folder with a name code in container
WORKDIR /code


# Copy the requirement file from our local folder to container folder
COPY ./requirements.txt ./

#Command to install the python packages or dependecies listed in the requirement file
RUN pip install --no-cache-dir -r requirements.txt

#Copy the local src folder to the src folder in container
COPY ./ ./

#Specify the command to execute the code inside the container. This will launch the streamlit. It is anlalogous to righting "streamlit run ./src/main.py"
CMD [ "streamlit", "run", "./main.py" ]


#Build the docker
#docker build . -t cdk_streamlit_docker_image

#Run the container
#docker run --name cdk_streamlit_container -p 8501:8501 -d -v ${PWD}:/app cdk_streamlit_docker_image