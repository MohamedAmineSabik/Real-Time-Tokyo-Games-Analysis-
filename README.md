# Real-Time-Tokyo-Games-Analysis-
## 1-Introduction
In this project , we will perform  a real time data analysis by leveraging  the capabilities  of data streaming platforms primarly kafka and spark.
## 2-Context of the project : 
Our Analysis will be conducted on countries achievements in olympic games concerning the 2020 edition held at Tokyo .

Olympic games are the world's leading international sporting events. They feature summer and winter sports competitions in which thousands of athletes from around the world participate in a variety of competitions. 

Returing to the context of the project , we will scrape ranking table from the official website of Olympic games using beatiful Soup library and to do that , we will reference to our programming language python.

The image above , shows the table we will extract : 

![Tokyo-Games  - Page 3](imgs/Tokyo_golden_medals.png)

## 3-Architecture of the project : 
![Architecure  - Page 4](imgs/Building_Architecture.png)

The underligning architecture reveals the components of our project , it aims to establish a real-time data analysis system for capturing and processing data extracted from Tokyo games olympics using a distributed and scalable data piepeline.
The main tasks including : 
-  <b> Web Scraping :</b> Data Scraping using Beatiful Soup.
- <b> Data Orchestration :</b>  we will use airflow to automate some workflow related to streaming data to kafka.
- <b> Real Time data Streaming :</b> we used the fancy data platefrom kafka in order to stream data into kafka broker.
- <b> Data Processing :</b>  Spark will be used as processing system known for its advanced data analytics.
- <b> Data Ingestion :</b>  we will store data in a no sql database such as cassandra.
