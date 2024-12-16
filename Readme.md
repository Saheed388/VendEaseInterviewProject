

The Real-Time Data Pipeline project is a robust and sophisticated system designed to extract, transform, validate, analyze, and store data from multiple sources. The pipeline ensures that other data teams have real-time access to clean and structured data for analysis, predictions, and model development. This comprehensive solution integrates advanced technologies such as Kafka for real-time data streaming, BigQuery as the data warehouse, and Docker containers for scalability, portability, and seamless deployment. Additionally, open-source tools like Jupyter Notebook enable exploratory data analysis (EDA).

***Project aim**

The aim of my project is to build a sophisticated yet cost-effective data pipeline capable of handling real-time data ingestion, transformation, validation, and storage from multiple sources. The pipeline is designed to ensure high performance, scalability, and reliability while minimizing costs. By leveraging open-source tools like Apache Kafka for real-time streaming, Docker for containerization, and BigQuery as the data warehouse, the pipeline efficiently supports data analysis, predictive modeling, and visualization, providing real-time access to structured and clean data for the data teams.


*Link to the project architectuer:*
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/VendeaseDataPipeline.gif


*Project Structure Outline:*

**1. Data Ingestion and Storage Optimization:**

*Pipeline Design*
- The data ingestion pipeline was designed to efficiently capture high-velocity, unstructured data from multiple sources:

User Data
Transactions Data
System Performance Data

**1. Tools and Technologies:**

*Producers:*
Custom producer applications (Producer App1, Producer App2, Producer App3) extract data from the respective sources and push them into the Kafka Brokers. Kafka ensures high throughput and fault-tolerant data streaming.

*Kafka Brokers:*
- Purpose: Act as a distributed messaging platform for real-time ingestion. Kafka topics ensure reliable and ordered streaming of data.
- Reason: Kafka was chosen because it supports scalability, durability, and near real-time data ingestion for high-velocity data, and also an open source tool which is easy to use.
- Dockerized Environment: All ingestion applications (Producer Apps) and (Consumer Apps) are containerized using Docker to ensure portability, easy deployment, and consistency across environments.

*Storage:*
- BigQuery (Data Warehouse): Once the data is ingested and consumed, it is stored in BigQuery to support transformation, analytics, and visualization.
- Reason for choice: BigQuery is a scalable cloud-based data warehouse optimized for real-time analytics with built-in capabilities to query large datasets efficiently.

*Host Machine Choice: Google Compute Engine*

```Although I initially considered deploying Docker using Google Compute Engine, limited access to Google Cloud services and challenges with card verification made me explore alternative options. Ultimately, Google Compute Engine (GCE) stood out as the best choice because of its ability to handle large-scale, persistent workflows effectively.```

Why Google Compute Engine?
- Full Customization and Scalability:
GCE allows for a fully customizable architecture tailored to the project’s needs, including real-time data ingestion, transformation, and analytics. This flexibility ensures the infrastructure can handle varying data loads efficiently.

*Persistent and Real-Time Processing:*
For a company that processes large datasets and requires consistent, reliable workflows, GCE provides a robust environment for running pipelines without interruption.

*Cost Efficiency and Flexibility:*
GCE allows us to select the appropriate VM configurations based on the data volume and project requirements. This adaptability ensures we can optimize resource usage while keeping long-term costs manageable.

*Scalable Foundation:*
GCE provides a strong, scalable foundation for both batch and real-time workflows, which are essential for supporting business-critical analytics and predictive modeling.

By leveraging GCE, the pipeline is reliable, cost-effective, and built to scale with the business, ensuring seamless handling of real-time and batch data workflows.


**2. Data Transformation and Cleaning**

Transformation Process

Data transformation was handled in both Producer and Consumer Applications before and after injection after ingestion:

Raw Data → Structured Format

Raw, unstructured data is parsed, formatted, and structured into meaningful tables (fact and dimension tables) for downstream processes.

*Data Cleaning:*

Duplicate removal
Missing value handling
Standardization of fields like timestamps, product names, and user IDs.
Check for negetive values in column.
Ensure accurate data types.
Z-score for Anomaly detection

*Reusable Scripts:*
Python scripts with libraries such as Pandas, NumPy, and Os automate the transformation workflows.
Transformations ensure consistency across datasets and generate clean, structured tables for BigQuery.

*Process Overview:*
Data Format: JSON → Structured Data → Stored in BigQuery Tables.

*Reason for json format:*
Is a lightweight, text-based data format that is easy to read, write, and understand for both humans and machines.
JSON uses minimal syntax with fewer characters, making it faster to transmit over the network compared to XML or CSV.
Its lightweight nature reduces data payload size, improving application performance.

*ETL Workflow:*
Extract: Kafka → Consumers
Transform: Custom Python scripts for parsing and cleaning
Load: Structured data is loaded into BigQuery tables

*Image of the producer and comsumer communicating*
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/system_performance%20image.PNG
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/transaction%20poducer%20and%20consumer.PNG
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/userInteractionImage.PNG


**3. Data Quality Check**

*Data Validation Process:*
A custom data quality handling process was implemented to validate incoming data and ensure accuracy:

*Validation Rules:*
Data completeness: Check for missing fields.
Schema validation: Ensure all records match the expected schema (user interactions, transactions, system performance).
Logical consistency: e.g., negative values for transaction amounts are rejected.
Invalid Data Handling:
Invalid data is rejected and logged into a separate Kafka topic or temporary storage.
A retry mechanism processes invalid data after corrections are made.
A 6-second sleep method was implemented to prevent the program from crashing. Additionally, I ensured that the producer does not send any data when there is no new data available. Instead, the program prints: "No new data for now"

*Automation:*
Scripts automatically validate data, log errors, and retry processing.


**4. Exploratory Data Analysis (EDA)**

Using Jupyter Notebook, an Exploratory Data Analysis was performed on the cleaned datasets to identify errors and anomalies:

*Steps:*
Analyzed user activity trends, session durations, and anomalies.
Detected potential data quality issues like missing values and inconsistencies.
Generated visualizations for transaction trends and system performance.

*Tools Used:*
Python libraries: Pandas, Matplotlib, Seaborn
Jupyter Notebook for interactive exploration and visual analysis.

*Link to the notebook*
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/EDA_Analysis.ipynb


**5. Data Pipeline Architecture Diagram**

- The following diagram summarizes the real-time streaming data pipeline architecture:

[Attach the architecture diagram provided above]
Extraction: Producers → Kafka Brokers
Transformation: Consumers → Data Cleaning and Structuring → BigQuery
Exploratory Analysis: Jupyter Notebook


*Link to the project architectuer:*
https://github.com/Saheed388/VendEaseInterviewProject/blob/main/imagesFromProject/VendeaseDataPipeline.gif


***6. Dockerized Application***
- The entire application is dockerized to ensure seamless deployment and scalability:
- Components Dockerized:

Producer Applications
Consumer Applications
BigQuery Integration

*Docker Benefits:*

Portability: Runs consistently across environments.
Scalability: Easily scales Kafka producers/consumers as the data volume grows.

*Docker Configuration:*
Dockerfiles for all components
Docker Compose to orchestrate multiple containers

*Conclusion*
The designed real-time data pipeline optimizes ingestion, transformation, and storage processes, ensuring high data quality and enabling robust analytics in BigQuery. This architecture effectively supports the e-commerce platform's need for real-time insights and scalability.


**I would be honored to be considered for this role, and I firmly believe that, together with the other team members, we can drive the company to new heights of success.**



























