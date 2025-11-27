#docker build -t gcr.io/<projectID>/mowingestimationfinal:v2 .
#docker run -d -p 8080:8080 gcr.io/<projectID>/mowingestimationfinal:v2
#docker exec -it <containerID> bash
#copy json file
#docker commit <container_id_or_name> <new_image_name>:<tag>
#docker push <new_image_name>:<tag>
#check in container registry if docker tag created
#Manually deploy Cloud Run with this tag.
