# Notícias da Covilhã @ Arquivo Web

## Overview

This repository contains the project "ArquivoNC -- Notícias da Covilhã @ Arquivo Web" developed as part of a university course. The project aims to archive and retrieve news articles from the abandoned Notícias da Covilhã newspaper.

## Project Structure

### Root Directory
#### data-retrieval
1. **Data Extraction**
-  *FrontPageData.py*
-  *FrontPageImageData.py*
-  *FrontPageURLs.py*
-  *NewsPageData.py*
-  *NewsPageURLs.py*
  
2. **Data Validation**
- *downloadCapas.py*
- *downloadImages.py*
- *ExportData.py*
- *finalDataFormatting.py*
- *fixAuthors.py*
- *fixCategoria.py*
- *fixContent.py*
- *GetDateCapas.py*
- *getSpacyEntities.py*
- *imageDataset.py*
- *NewsPageDataValidation.py*
- *NewsPageURLsValidation.py*
- *populate_db.py*
- *testing.py*

3. **Data Statistics**
- *GetDataStatistics.py*

#### website
The front-end code for the web interface where users can access the archived news.
- **index.html**: The main HTML file for the website's homepage.
- **styles.css**: CSS file for styling the website.
- **app.js**: JavaScript file containing the front-end logic for interacting with the archived data.
- **assets/**: Directory containing images, icons, and other static assets used by the website.

### docs
Documentation files for the project.
- **architecture.md**: Detailed description of the project architecture.
- **user_guide.md**: Instructions on how to use the website and access the archived news.
- **developer_guide.md**: Guide for developers who want to contribute to the project.

## Technologies Used

- **Python**: 38.2%
- **HTML**: 32.6%
- **Jupyter Notebook**: 24.6%
- **JavaScript**: 3.1%
- **CSS**: 1.4%
- **Shell**: 0.1%

## Quick Retrieval
1. Clone the repository: 
   ```bash
   git clone https://github.com/rdsilva01/noticias-da-covilha-arquivo-web.git
   ```

2. Navigate to the project directory:
   ```bash
   cd noticias-da-covilha-arquivo-web
   ```

