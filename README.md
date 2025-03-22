# Sentiment analysis and NLP Based Text-Processing

A complete NLP pipeline for text extraction, cleaning, and analysis using Python. The project includes sentiment scoring and readability metrics for structured text data.

## Project Overview
This project involves data extraction, processing, and analysis using Python scripts. The primary functionalities include:
- Extracting articles from URLs provided in an Excel sheet (`Data_extraction.py`)
- Cleaning and processing text data (`data_analysis.py`)
- Performing sentiment and readability analysis (`metrices.py`)

## Folder Structure
```
.
├── Data_extraction.py   # Script for extracting article text from URLs
├── data_analysis.py     # Script for cleaning and processing text data
├── metrices.py         # Script for sentiment and readability analysis
```

## Dependencies
Ensure you have the following dependencies installed before running the scripts:
```sh
pip install pandas requests beautifulsoup4 nltk openpyxl
```

## Usage
### Step 1: Data Extraction
Run `Data_extraction.py` to extract article text from URLs in `input.xlsx`. Extracted articles will be stored in the `articles/` folder.
```sh
python Data_extraction.py
```

### Step 2: Data Analysis
Run `data_analysis.py` to clean and preprocess the extracted articles.
```sh
python data_analysis.py
```

### Step 3: Metrics Calculation
Run `metrices.py` to compute sentiment and readability metrics. The results will be saved in `Output Data Structure.xlsx`.
```sh
python metrices.py
```

## Note
- **Dataset and Code Availability:** Due to certain constraints, the dataset and some parts of the code cannot be uploaded to GitHub. Please ensure you have the necessary input files (`input.xlsx`, dictionaries, stop words, etc.) before running the scripts.
- **Ensure Folder Structure:** The scripts assume specific folder structures for stop words, master dictionaries, and extracted articles.

## Contact
For any queries, please reach out via GitHub issues.


