# Notícias da Covilhã @ Arquivo Web

## Overview

This repository contains the project ***ArquivoNC -- Notícias da Covilhã @ Arquivo Web*** developed as part of the final Bsc. project in the 1st cicle of *Engenharia Informática* at UBI. The project aims to archive and retrieve news articles from the abandoned Notícias da Covilhã newspaper.

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
The website where users can access the archived news.
- **newsletter**: The newsletter operations.
- **redis**: Contains the redis operations.
- **static**: Contains the static data, such as images, audio, css, js.
- **templates**: Contains all the HTML files that will later be rendered.

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

## Contact

For any questions or issues, please open an issue on the repository or contact rd.silva@ubi.pt.
