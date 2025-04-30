# AirQualityRasp
Author: Calvin Lynch - K00271788
Project - Air Quality Metrics Using A Raspberry Pi 5
Language - Python
Raspberry PI 5 - Air Quality Metrics

Application for FastApi Rest Server
Required Database: Influx Database

Database Requirements: Ensure that you have a database set up & running live. This applciation uses influx database so a URL & an access token with write privelages is required. 
This will require some configuration: Locate the Database folder & then locate influxdb.py.
Locate the following: 

(Alternative to the below, if url or token cannot be added into .env on Raspberry Pi, add directly here)

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")

These variables will require valid values or the data will now be written - Either update the variable with the database URL:PORT & Token(Not recomended to put these values directly into the source code) or save these as enviromental variables on the system or in a keystore to add an additional layer of security for these variables as they are considerd sensitive.

Raspberry Pi Requirements: Network access, Docker CLI
Packages: Installed in docker container using Poetry Pytomel file

Where to Run this Application: This project is using AWS cloud - Run in Ec2 instance or somewhere publically accessible so rest-api's are available

How to Run: 

If using Ec2 instance on amazon - Clone this repository onto your server/virtual machine.

Ensure you have docker installed on your machine as it is needed to create a docker image of the applciation & to run the image in a docker container.

Step 1. Navigate to the root of the project. /FASTAPIRASPBERRYPI
step 2. Type: "sudo docker build -t 'name_your_image:_v_major_minor_patch' ." 
Note on step 2 -> Name your image & version it using 1.0.1(for versioning) & dont forget the dot at the of the command as this is required in the build command.

step 3. After successfully creating the image, run the Image in a docker container. (To See if the image has been created type: 'sudo docker images')
To run the image type: "sudo docker run -d -p 8000:8000 "image:version"

This is now accessible on port 8000 - Ensure you have security groups in palce to allow http traffic to access the ec2 instance if using AWS Cloud.

The above command will run the image in a docker conatiner - Since the image was built using poetry as a package manager there is no need to install any aditional dependecies to run this.

What is happening:
    sudo docker -> sudo is super user privelages(can be changed) calling docker to access functionality.
    run -> telling docker to run an image in a docker conatiner - Docker will take an image & run it on a isolated docker container.
    -d -> detatch - detatch the container from the main shell & run it is a seperate background task.
    -p 8000:8000 - Binding the docker container network to the host machines network to allow for this conatiner to be accessible. 

This should now successfully be running the application in a docker container.

If set up correctly, Rest-Apis will be accessble on port 8000 using http - URI's/endpoints can be seen in the controllers folder of this project.

Note: To get an influx database image, visit docker hub https://hub.docker.com/_/influxdb - This page also provides documentation on how to pull, run & access.

If creating a new influx db instance make sure to take note of the following:

Update the influx db class in this applciation:

INFLUXDB_URL = os.getenv("INFLUXDB_URL") - Mentioned above
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN") - Mentioned above
ORG="AQI" - When creating an ORG on the influx UI - type AQI or if changed, change in the influx db class
BUCKET="AQIMetrics" - When creating a Bucket on the influx UI - type AQIMetrics or if changed, change in the influx db class

Influx is necessary as fastApi is reading data from the database & returning it to the client.





