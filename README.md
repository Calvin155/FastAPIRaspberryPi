For testing & building docker image locally use:
    sudo docker build --platform linux/arm64 -t image_name:version .

On raspberry Pi - Docker file build - 
    sudo docker build -t image_name:version .


To Run image in a container:
    sudo docker run -d -p 8000:8000 image_name:version