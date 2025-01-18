# NBA DataLake

## Overview

This project automates the configuration of an AWS environment using Terraform and Python. It sets up an S3 bucket and an AWS Glue database with a corresponding table schema using terraform. The python script retrieves data from an API, and stores the processed results back into the S3 bucket and also setup Amazon Athena that query the data and store the result in S3 bucket.

![Workflow](./Screenshot%202025-01-18%20023058.png)

## Prerequisites

Make sure you have the following installed:

* [Terraform](https://www.terraform.io/downloads.html)
* [Python 3.x](https://www.python.org/downloads/)
* [AWS CLI](https://aws.amazon.com/cli/)
* Required Python libraries: `boto3`, `requests` (install via pip)

## Setup

1. Clone the repository

   ```bash
   git clone https://github.com/fakiletemmytope/nba_player_data_lake.git
   cd nba_player_data_lake
   ```

2. Configure your AWS credentials either by running `aws configure` or by setting appropriate environment variables.
3. Navigate to the Terraform configuration directory and initialize Terraform:

   ```bash
   cd terraform
   terraform init
   ```

## Usage

1. Once the infrastructure is set up, you can run the bash script to apply terraform, fetch data from the API, store it into the S3 bucket, query the data using athena:

   ```bash
   ./script
   ```

2. Check the S3 bucket for the output files.
3. To clean up:

   Empty  the S3 bucket on AWS console and run the command: `./destry`

## Architecture

**Terraform** : Used to provision and configure:

* An S3 bucket for storing results.
* An AWS Glue database and table based on a defined schema.

**Python Script** :

* Calls an external API to retrieve data.
* Processes and stores the results in the specified S3 bucket.
* Configure Amazon Athena for querying data and storing the result in S3 bucket.

### **Future Enhancements**

1. Automate data ingestion with AWS Lambda
2. Implement a data transformation layer with AWS Glue ETL
3. Add advanced analytics and visualizations (AWS QuickSight)
