# MindQuest

## Overview

This RAG chatbot is a simple design for non-technical users. Done with streamlit the UI is minimalistic yet content. This is made as part of the Information Retrieval project presentation.

## Key Features

- Text Embedding
- Vector Indexing
- User-Friendly Summaries

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them:
Python libraries as listed in the `requirements.txt` file

### Installation

Follow these detailed steps to get a development environment running:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/SiddhuSiddharth/MindQuest.git
   cd MindQuest
   ```

2. **Import specific requirements**:
  
   ```bash
   virtualenv -p python3.xx.xx <virtualenvname>
   pip install -r requirements.txt
   ```
   This was the command used to create virtual environment using specific py version. Create a virtual environment and install all libraries.
   
3. **Run the application**:
  
   ```bash
   streamlit run Streamlit.py
   ```
   Now connect your code with the model and run it. 

### Usage

Navigate to `http://localhost:8501/` in your web browser to access the user interface.

## Development

### Architecture

This project is built using the Streamlit for the UI and Python for the Models and embeddings. The embeddings function is performed using `distilbert-base-uncase` with the vector index database being `CromeDB`. The Model used here is `Cohere command-xlarge-nightly`.

## Team

- 20PD28 Siddharth Subramanian
- 20PD30 Sree Aditya G S
- 20PD07 Devavarapu Atchutha Manga Satya Prasad

## Credits

- We thank Tata's 1mg for providing a reliable drug database, essential for the accurate functioning of our chatbot.
- We thank our mentor Dr. Sridevi U K for her guidance and support in building this chatbot.
