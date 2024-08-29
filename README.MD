# Vacancy gRPC Load Test with Locust

## Overview
This project contains a Locust load testing script that interacts with a gRPC vacancy server to test its performance. The script performs various actions like creating, updating, fetching, and deleting vacancies as well as fetching all vacancies in the background.

## Pre-requirements
1. Create three users on the server (SignUpUser).
2. Verify the users' email (VerifyEmail).
3. Store the credentials for later use in `credentials/user_credentials.json`.

## Project Structure
- **locustfile.py**: The main Locust load testing script.
- **proto/**: Contains the `.proto` files for gRPC communication.
- **credentials/**: Stores user credentials.
- **requirements.txt**: Lists all the dependencies.
- **.gitignore**: Excludes unnecessary files from Git.
- **README.md**: Project documentation.

## Setup and Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/vacancy-grpc-load-test.git
   cd vacancy-grpc-load-test
