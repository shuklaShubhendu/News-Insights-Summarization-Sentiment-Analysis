# **News Analyzer Pro**

This repository contains a comprehensive news article analysis tool, **News Analyzer Pro**, built using Python. It offers functionalities such as article summarization, sentiment analysis, key points extraction, and reading statistics, making it ideal for quickly digesting news content. The tool also includes features for saving articles, tracking history, and exporting data to CSV.

## **Features**

- **Article Summarization**: Condenses lengthy articles into concise summaries, making it easier to understand the main points.
- **Sentiment Analysis**: Analyzes the sentiment of the article and classifies it as positive, negative, or neutral using TextBlob.
- **Key Points Extraction**: Extracts key points to help focus on the most essential information.
- **Reading Statistics**: Provides metrics like word count, sentence count, and estimated reading time for better content understanding.
- **History Management**: Tracks articles you've analyzed and allows you to load them for later use.
- **CSV Export**: Exports article analysis (summary, sentiment, etc.) into CSV format.
- **Save Articles**: Saves articles locally in the app for quick access and future analysis.
- **User-Friendly GUI**: Built with Tkinter for easy interaction and smooth user experience.

## **Requirements**

Before running the project, make sure you have the following dependencies installed:

- Python 3.x
- Tkinter (for the graphical user interface)
- TextBlob (for sentiment analysis and text processing)
- re (for regular expression operations)
- os (for file handling operations)
- csv (for exporting article data)

Install the required dependencies by running:

```bash
pip install textblob tk
```

# Getting Started
1. Clone the Repository
```bash

git clone https://github.com/your-username/News-Analyzer-Pro.git
cd News-Analyzer-Pro
```
2. Running the Application
To start the application, run the following command:

```bash

python main.py
```
3. Using the Tool
- **Input Article URL:** Paste the URL of the article you want to analyze.
- **Summarize:** Click on the “Summarize” button to generate a summary of the article.
- **View Sentiment:** Check the sentiment analysis results (positive, negative, or neutral).
- **Extract Key Points:** View the extracted key points that highlight the article’s most important information.
- **Check Reading Stats:** See the word count, sentence count, and estimated reading time.
- **Save to History:** Save articles for later access under the "History" tab.
- **Export Data:** Export the analysis results to a CSV file by clicking the “Export to CSV” button.
4. Help Guide
Click on the "Help" button to access a detailed user guide, FAQs, and troubleshooting tips.

# Project Structure
Here’s the structure of the project:

```bash

News-Analyzer-Pro/
│
├── main.py                  # Main script to run the application
├── README.md                # This file
├── data/                    # Directory for storing article-related data
│   ├── articles/            # Folder with analyzed articles in JSON format
│   └── exports/             # Folder to save exported CSV files
└── history/                 # Folder to store saved articles (JSON format)
```
# Model Architecture
News Analyzer Pro leverages multiple key features to analyze articles:

- **Summarization:** Uses Natural Language Processing (NLP) techniques to extract a meaningful summary of the article.
- **Sentiment Analysis:** Utilizes TextBlob for analyzing sentiment and classifying it as positive, negative, or neutral.
- **Key Points Extraction:** Identifies the most important points of an article using text processing algorithms.
- **Reading Stats:** Computes metrics like word count, sentence count, and reading time for the article.
# Contributing
We welcome contributions to News Analyzer Pro. If you'd like to improve the tool or add a feature, follow these steps:

- Fork the repository.
- Create a new branch (git checkout -b feature-name).
- Make your changes and commit them (git commit -am 'Add feature').
- Push the branch to your fork (git push origin feature-name).
- Open a pull request to merge your changes.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
- **TextBlob:** For providing easy-to-use sentiment analysis and text processing tools.
- **Tkinter:** For building the graphical user interface (GUI).
- **CSV:** For exporting article data to a format that can be easily shared or analyzed further.
- **JSON:** For storing and managing article data in a structured format.
