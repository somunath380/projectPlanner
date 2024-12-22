# Project: Project Planner

## Description

A robust and user-friendly **Project Planner** application designed to simplify team collaboration, task management, and project tracking. This tool enables users to manage projects, organize teams, assign tasks, and monitor progress all in one centralized platform.

## Why FastAPI instead of Django
Since This project needed to have following things
1. Fast Performance
2. Lightweight
3. Ease of Working with Files
4. Scalability (For microservices architecture)
I have chosen FastAPI to develop this project

### Run the Server

1. Clone the repository: `git clone https://github.com/somunath380/projectPlanner`
2. Navigate to the project directory: `cd projectPlanner` where you have downloaded the project
3. run `pip install -r requirements.txt` command
4. then run `fastapi run app/main.py` command

### API Documentation and Usage

1. go to `http://0.0.0.0:8000/docs` to find all the api endpoints usage

### Improvements

1. should have added Unit Tests
2. As with FastAPI,  should have ensured atomic writes to avoid race conditions while writing data to the files
3. the Schemas for User, Team and Projects should have been more generalized
