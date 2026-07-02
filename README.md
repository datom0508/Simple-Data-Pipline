# Simple Data Pipeline

## Architecture & Tools

* **Google AI Studio (Gemini 2.5 Flash):** Chosen as the LLM and Vector Storage solution. The Assistant initialization and contextual querying are handled via code.
* **GitHub Actions:** Serves as the cloud scheduler for the daily cron job.
* **Docker:** Containerizes the application. The container runs the scraping/syncing job once and exits with code 0.

## Setup

* **Clear Commits:** Commit history is kept clean and descriptive.
* **No hard-coded keys:** The repository uses a `.env.sample` file. Do not commit your actual `.env` file.

1. Clone the repository:
   ```bash
   git clone [https://github.com/datom0508/Simple-Data-Pipline.git](https://github.com/datom0508/Simple-Data-Pipline.git)
   cd Simple-Data-Pipline

2. Set up your environment variables:
   ```bash
   cp .env.sample .env

3. Add your actual API key to the .env file

## How to run locally:

1. Build the Docker image:
   ```bash
   docker build -t sync-app .

2. Run the container. It will execute the `main.py` script once and exits 0:
   ```bash
   docker run -v "$(pwd):/app" --env-file .env sync-app

## Daily Job Logs
The scraping and syncing job runs daily at 00:00 UTC via GitHub Actions.
- View Job Logs: visit `https://github.com/datom0508/Simple-Data-Pipline/actions/workflows/daily_sync.yml` to view the GitHub Actions workflow logs.

## Assistant Sanity Check
Below is a screenshot demonstrating the Assistant successfully answering a sample question using the uploaded Markdown files, correctly following the system instructions and citing the URLs.

Sample Question: "How do I add a YouTube video?"

![Assistant Answer](https://drive.google.com/uc?export=view&id=1pEK_TZ-ZxEDjl_gekM1Gp7ADGEXLZ9Yj)

