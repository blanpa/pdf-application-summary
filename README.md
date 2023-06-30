# pdf-application-summary
pdf-application-summary

Run the following command to build the Docker container:

    docker build -t pdf-app .

Open a web browser and go to the address http://localhost:8501 to access the Streamlit application.

These steps will create and run a Docker container that contains the Streamlit application. The container is based on a Python 3.9 image, installs the required packages from the requirements.txt file, and copies the entire contents of the current directory into the container. The Streamlit server is then started and the application is made available via port 8501.

Please make sure that you have Docker installed on your system and that you have run the Docker daemon before executing the above commands.

When running the container, you can use the -v flag to mount volumes. Here is an example command that mounts the /path/to/local/folder folder into the container:

    docker run -p 8501:8501 -v /data:/app/data pdf-app

Using -v /path/to/local/folder:/app/local_folder will connect the local folder outside the container to the /app/local_folder directory inside the container. This allows the application to access the contents of the local folder.

In the Python script, you can then use the path local_folder to access the files inside the mounted volume.

Please note that the path /path/to/local/folder must exist on your host system and contain the necessary files for the application to access.

Translated with www.DeepL.com/Translator (free version)