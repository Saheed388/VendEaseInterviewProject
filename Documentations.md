

The Real-Time Data Pipeline project is a robust and sophisticated system designed to extract, transform, validate, analyze, and store data from multiple sources. The pipeline ensures that other data teams have real-time access to clean and structured data for analysis, predictions, and model development. This comprehensive solution integrates advanced technologies such as Kafka for real-time data streaming, BigQuery as the data warehouse, and Docker containers for scalability, portability, and seamless deployment. Additionally, open-source tools like Jupyter Notebook enable exploratory data analysis (EDA).

project aim

The aim of my project is to build a sophisticated yet cost-effective data pipeline capable of handling real-time data ingestion, transformation, validation, and storage from multiple sources. The pipeline is designed to ensure high performance, scalability, and reliability while minimizing costs. By leveraging open-source tools like Apache Kafka for real-time streaming, Docker for containerization, and BigQuery as the data warehouse, the pipeline efficiently supports data analysis, predictive modeling, and visualization, providing real-time access to structured and clean data for the data teams.


Link to the project architectuer:
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/VendeaseDataPipeline.gif




































kafka-console-consumer --bootstrap-server localhost:9093 --topic userInteraction --from-beginning


kafka-console-producer --bootstrap-server localhost:9093 --topic userInteraction

docker exec -it broker kafka-console-producer --bootstrap-server localhost:29092 --topic userInteraction


docker-compose up -d --build


docker exec -it <producer_container_name> /bin/sh
# Inside the container shell, run:
nc -vz host.docker.internal 9092


 docker exec -it broker kafka-topics --create   --topic userInteraction   --bootstrap-server broker:29092   --partitions 1   --replication-factor 1

 docker exec -it broker kafka-topics --list   --bootstrap-server broker:29092

 connet it
 
 docker start kafka-rest
docker exec -it --user root kafka-rest bash
 yum install net-tools


docker build -t user_interaction_producer .

docker run --rm user_interaction_producer
