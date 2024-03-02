# Notícias da Covilhã @ Arquivo Web

**[![wakatime](https://wakatime.com/badge/user/018cfa2b-6d3b-4537-9f07-a84184b9a93b/project/018dd20f-71eb-4c86-8c1f-08cc4b94ac5a.svg)](https://wakatime.com/badge/user/018cfa2b-6d3b-4537-9f07-a84184b9a93b/project/018dd20f-71eb-4c86-8c1f-08cc4b94ac5a) Time spent (aprox.)**

## Prologue
**Notícias da Covilha @ Arquivo Web** is a final project in (âmbito) of the curricular unity of Projeto (at [UBI](https://ubi.pt))

## Step 1 - Data
### Data Extraction and Data Validation
  - **Data Extraction**
  The first step of the data extraction is getting the news URLs, so the function created takes the URL of the page, in this case [noticiasdacovilha.pt](noticiasdacovilha.pt), and with the use of a package created by** Professor Ricardo Campos** and a previous student of his, **Diogo Correia** (might need to fix this line), that package which I'm going to complement with my work, contributing to create a (even) more composed package (fix this too). So what this package does is by giving it a URL link, it uses the [Arquivo.PT](https://arquivo.pt) API to retrieve all the links from that URL, that are stored there.
  The function does a pre-validation to fix the problem of having repetitive URL links, so that we don't have repetitive news, which take space and time.
    - **Script**
    Now passing to the function that extracts the data, the approach was saving each URLs in json files per year, so that when we access it we can decide which years we want. With the help of packages such as `requests` and `beautifulsoup4`, the first one to get the HTML data from the URL link and the second one to search the data, the first thing to search is a `div` that has the **category** and the **subcategory**, which are on the top side of the page. Then it searches for another `div` with the id `div_conteudo_left`, that contains that unique news info, everything. 
    - **Image and its Description**
    To get the image it searched for the `img` element and retrieve it `src`, that contains the source (URL) of the image.
    So to get the image description the algorithm that was thought about was reversing the string that we got from the source attribute and iterate it until it reaches a /, because the name of the image (the file) was the last element after the last /, given that, after cleaning it, we got a image name that could be used to associate the image to a person/entity
    - **Main Text**
    The paragraph content is divided into 2 sections, the text snippet and the paragraphs, to get the text snippet it scraps the first line (that is in reality the first paragraph sometimes) and saves it in a different variable than the rest, then, with the help of a package called `cleantext`, and using a function from that called clean, it was possible to clean all the *garbage* from the text (unicode chars, etc...), all that in a cicle for which it was used to iterate through all the paragraphs and with that I could save each one as a String, to later append it to a list of Strings (to better use later).
    - **Keywords**
    To retrieve the keywords from the paragraphs it was used a software called YAKE, installing the YAKE through pip to use it in our code, **(explain here how YAKE works, simply and easy)**, it retrieved the top 10 keywords of each paragraph and saved it also.
    - **spaCy**
    SpaCy is another package, used to retrieve all the entities from the paragraph, that will be super useful to implement the top Entities of that year, it's possible with that. **(need to add more development to this and to the Keywords)**
    - **The Rest**
    What's missing is the author, the tags and the date are obtained by searching all the span regions, where they are all in, and obtain the text, clean it and save it.
  - **Data Validation**
  - **Data Saving**
  The json format was the data structure choosed to save the data, more convenient.
  The format is `validated_urls_XXXX.json`, where `XXXX` is the year, to the URLs json file
  The news are stored in a file called `raw_XXXX.json`, where, again, `XXXX` is the year.
---
## Step 2 - Search
### Algorithms
  - **Elastic Search**
---
## Step 3 - Website