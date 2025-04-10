Glassdoor Data Jobs ETL Automation using Apache Airflow
Overview:
Designed and implemented an end-to-end ETL pipeline to automate the processing of Glassdoor job listing data for data-related roles such as Data Engineers, Analysts, and Scientists. The pipeline is built using Apache Airflow and is structured into modular, scheduled tasks for scalability and monitoring.
________________________________________
 Workflow Phases (ETL Structure):
1.	🔹 Load Data (loading_data)
Raw job listing data (CSV) is read and prepared for transformation. This task sets up the foundation for downstream operations.
2.	🔹 Transform Data (transform_data)
o	Cleaned messy strings like "Employer Provided Salary:150000"
o	Extracted numeric values for salary, ratings, company size, and revenue
o	Parsed ranges like "50to100 million (USD)" into structured numeric values
o	Engineered features such as min_salary, max_salary, avg_salary
3.	🔹 Generate Insights (extracting_insights_from_data)
o	Identified top 10 job titles by average salary
o	Identified top 10 job titles by company rating
o	All insights are logged and can be exported via XCom for dashboarding
4.	🔹 Final Stage (final_stage)
Optionally loads the final transformed data and insights into a PostgreSQL database or writes to a .csv file for use in Power BI or Tableau dashboards.



Let’s see about the structure of the project:
 

Project: AIRFLOW_TEST_2
Core Airflow Setup
•	airflow.cfg: Configuration file for Airflow.
•	airflow.db: The SQLite database used by Airflow to track DAG runs, tasks, and metadata.
•	airflow-webserver.pid: PID file for the Airflow webserver process.
•	webserver_config.py: Additional settings for the Airflow webserver UI.
•	standalone_admin_password.txt: Stores the admin password created for the standalone Airflow instance.
________________________________________
airflow/dags/ – 
Contains files and data for your ETL pipeline:
•	etl_process.py: Main DAG file that defines the ETL workflow.
•	dag_functions.py: Custom helper functions used within your DAG.
•	glassdoor_jobs.csv: Raw dataset containing job listings scraped from Glassdoor.
•	cleaned_data.csv: The output of your transformation logic — cleaned dataset used for insights.
________________________________________
Docker & Dependencies
•	docker-compose.yml: Defines your multi-container Docker setup (Airflow scheduler, webserver, DB, etc.).
•	dockerfile: Builds a custom Docker image with necessary configurations.
•	requirements.txt: Lists the Python dependencies (like pandas, airflow providers, etc.).
________________________________________
 logs/
Stores logs for all Airflow DAG runs and tasks. Useful for debugging ETL processes.


THE FINAL SHOWDOWN
Results:
•	Created a modular, reproducible data pipeline that mimics real-world ETL flow
•	Automated job market insight generation with just one scheduled DAG

Skills & Tools:
•	Apache Airflow (DAGs, PythonOperators, XCom)
•	Pandas & Regex for transformation
•	Power BI (used for final dashboard)
•	Git for version control


