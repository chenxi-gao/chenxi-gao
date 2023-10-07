# AWS-based stream data pipeline and data analyze.
Because my AWS service trial period has ended, I have recorded detailed documentation for this project using **Notion**. 
# Click Here 👇
[Please visit this link to view](https://www.notion.so/TORQATA-PIZZA-BUSINESS-7375585a4b3e4d7c9d028f9c4261bc9b)

## Overview
Pizza Data Reporting Tool offers a comprehensive analysis of pizza-related data, providing insights into the top-selling pizza combinations across different U.S. states.

## Features

### State-wise Data Reporting:
- View the top three best-selling pizza combinations for any U.S. state.
- Fetch details like:
  * Total sales volume for each pizza type.
  * Total sales revenue (in USD).
  * Average sales revenue per pizza.
  * The number of unique customers purchasing each pizza type.

### Performance:
- Low-latency, high-speed data querying.
- Data loads within 5 seconds when adjusting state filters.
- Each order becomes visible in the data warehouse within 15 minutes of placement.
- Daily data refresh at 2:00 AM.

## Architecture and Technology Stack

1. **Amazon Redshift**: Our primary data warehouse for storing and analyzing large volumes of data.
2. **Real-time Data Streaming**: Utilizes AWS API Gateway and Lambda functions, combined with Amazon Kinesis Data Firehose to stream data.
3. **Static Data Source Processing**: Customer data is stored in AWS RDS MySQL database, with AWS Glue managing ETL operations.
4. **Third-Party Data**: Integration of external data sources such as the U.S. Census Bureau for enhanced reporting.
5. **ETL Operations**: AWS Glue is instrumental in performing ETL operations to process and load data into Redshift.

## How To Use

1. **Front-end Interface**: Select a U.S. state from the dropdown list.
2. **Data Display**: Instantly view the top three best-selling pizza combinations for the selected state with all relevant details.
3. **Data Refresh**: Behind the scenes, data is automatically refreshed at 2:00 AM daily to ensure you always have the most recent insights.

## Setup and Installation

1. Set up an **`Amazon Redshift cluster`** with the required configurations.
2. Configure **`AWS API Gateway`** to handle incoming order requests.
3. Create and setup a **`MySQL database in AWS RDS`** for static data.
4. Ensure setup and permissions for **`AWS Glue Crawlers`** and ETL jobs.
5. Use Python scripts to simulate data or connect to your live environment.
6. Set up and configure **`AWS Lambda`** for any custom data processing or refreshing tasks.

## Performance and Optimization

- For optimal query performance, make use of **Sort Keys** and **Distribution Keys** in Redshift.
- Continually monitor the system using **Amazon CloudWatch** and fine-tune components like Kinesis Data Firehose and Redshift for maximum efficiency.
- Ensure the highest standards of data security with regular audits, data encryption, and fine-tuning of IAM roles.

## Future Prospects

1. **Granular Insights**: Dive deeper with data reporting at city or neighborhood levels.
2. **Temporal Patterns**: Understand peak pizza ordering times for better business management.
3. **Customer Segmentation**: Use advanced analytics to segment customers and personalize offerings.
4. **Predictive Analytics**: Employ ML and AI for predicting future sales trends.

## Authors

Chenxi Gao  

gao.chenx@northeastern.edu

## Version History

* 0.1
    * Initial Release of all three pipelines.
