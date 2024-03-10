# Notícias da Covilhã @ Arquivo Web

**[![wakatime](https://wakatime.com/badge/user/018cfa2b-6d3b-4537-9f07-a84184b9a93b/project/018dd20f-71eb-4c86-8c1f-08cc4b94ac5a.svg)](https://wakatime.com/badge/user/018cfa2b-6d3b-4537-9f07-a84184b9a93b/project/018dd20f-71eb-4c86-8c1f-08cc4b94ac5a) Time spent (aprox.)**

# ==PT==

## Agradecimentos
Gostaria de expressar o meu agradecimento a todas as pessoas que das mais variadas
formas me ajudaram neste projeto. Como não é possível enunciar cada um vou
apenas salientar algumas das pessoas que não poderia deixar de destacar.

Ao Professor Doutor Ricardo Campos por ter aceite ser o meu orientador, por toda a
disponibilidade e ajuda nas dificuldades que foram aparecendo guiando-me sempre
no caminho mais correto.

Por fim, mas não menos importantes, gostaria de agradecer à minha família, namorada e amigos por todo o apoio que sempre demonstraram e que sem eles teria sido
bem mais difícil.

## Prólogo
**Notícias da Covilha @ Arquivo Web** is a final project in (âmbito) of the curricular unity of Projeto (at [UBI](https://ubi.pt))

# ==IMPORTANTE==
- **How does the tesseract (OCR) works?**
- **Generally how the packages I use work**

## ==REQUISITOS
### tesseract
- required `brew`
- `brew install tesseract`

## PASSO 1
### Extração e Validação de Dados
- **==Extração de Dados==**
  O primeiro passo da extração de dados é obter os URLs das notícias. Para isso, a função criada recebe o URL da página, neste caso, [noticiasdacovilha.pt](noticiasdacovilha.pt), e utiliza um pacote criado pelo **Professor Ricardo Campos** e um antigo aluno seu, **Diogo Correia**. Este pacote será complementado com o meu trabalho, contribuindo para criar um pacote mais completo.

O que este pacote faz é, ao fornecer um URL, utilizar a API do [Arquivo.PT](https://arquivo.pt) para recuperar todos os links daquele URL que estão armazenados lá. A função realiza uma pré-validação para corrigir o problema de ter links de URL repetitivos, para evitar notícias repetitivas que ocupam espaço e tempo.

- **==Script==**
  Passando à função que extrai os dados, a abordagem foi salvar cada URL em arquivos json por ano, para que quando acessássemos pudéssemos decidir quais anos queremos. Com a ajuda de pacotes como `requests` e `beautifulsoup4`, o primeiro para obter os dados HTML do link do URL e o segundo para pesquisar os dados, a primeira coisa a ser pesquisada é uma `div` que tem a **categoria** e a **subcategoria**, que estão no topo da página. Em seguida, ela procura outra `div` com o id `div_conteudo_left`, que contém as informações únicas da notícia, tudo isso.

- **==A Página Inicial==**
  O Notícias da Covilhã é um jornal semanal, a cada semana há uma nova página inicial de notícias, que está presente em cada página de notícias (do site).

  A primeira abordagem foi procurar a partir de todas as possíveis páginas iniciais de jornais do site, as imagens da primeira página (com ajuda de *packages* como *BeautifulSoup* e *requests*). Para isso, foi utilizado um OCR(**ACRÓNIMO**) chamado tesseract, que é um reconhecimento de imagens, que as transforma em texto (super útil), e com isso era possível extrair a data nela presente. No entanto não era suficientemente exato, sendo que algumas das datas não eram as que correspondiam à data da imagem.

  Dado isto foi preciso pensar noutra alternativa, que passou pela criação de um algoritmo para que dado a primeira data de cada ano, através do *URL* da imagem era possível obter um *id* (identificador), com isto era possível associar ao primeiro *url* a primeira data, que era introduzida manualmente (como argumento ou por *user input*). Na teoria, caso os dados fossem lineares, ou seja, a maneira como os identificadores eram dados fosse linear (neste caso cada incremento do *id* equivalia a 7 dias, dado ser um jornal semanal), mas não era, sendo possível verificar isso com o OCR, no caso de haver uma mudança repentida do mês, ou então vendo manualmente iria haver 1 discrepância, causando que todas as primeiras páginas tivessem a data errada.

  **Algoritmo**
  *(inserir pseudo codigo)*
  - **1º PASSO:** Dados os URLs da página inicial, encontrar o URL da imagem, com a ajuda do pacote `BeautifulSoup`.
  - **2º PASSO:** Para cada URL da imagem (faça um ciclo), usando o pacote `requests`, obtenha o conteúdo dela.
  - **3º PASSO:** 

- **==Imagem e Descrição==**
  Para obter a imagem, procurou-se o elemento `img` e recuperou-se seu `src`, que contém a origem (URL) da imagem.
  Portanto, para obter a descrição da imagem, o algoritmo pensado foi inverter a string que obtivemos do atributo de origem e iterar até atingir uma /, porque o nome da imagem (o arquivo) era o último elemento após a última /, considerando isso, após limpá-lo, obtivemos um nome de imagem que poderia ser usado para associar a imagem a uma pessoa/entidade.

- **==Parágrafo==**
  O conteúdo do parágrafo é dividido em 2 seções, o trecho de texto e os parágrafos. Para obter o trecho de texto, ele raspa a primeira linha (que na realidade é o primeiro parágrafo às vezes) e o salva em uma variável diferente do resto, então, com a ajuda de um pacote chamado `cleantext`, e usando uma função dele chamada clean, foi possível limpar toda a *sujidade* do texto (caracteres unicode, etc...), tudo isso em um ciclo para o qual foi usado para iterar por todos os parágrafos e com isso pude salvar cada um como uma String, para depois apendê-lo a uma lista de Strings (para usar melhor posteriormente).

- **==Palavras-Chave==**
  Para recuperar as palavras-chave dos parágrafos, foi utilizado um software chamado YAKE, instalando o YAKE através do pip para usá-lo em nosso código. Ele recuperou as 10 principais palavras-chave de cada parágrafo e também as salvou.
  
  - **==spaCy==**
  SpaCy é outro pacote, usado para recuperar todas as entidades do parágrafo, o que será super útil para implementar as principais Entidades dessa semana/mês/ano, é possível com isso. **(precisa adicionar mais desenvolvimento a isso e às Palavras-Chave)** Modelo de precisão usado.
  
  - **==O Restante==**
  O que falta é o autor, as tags e a data são obtidos pesquisando todas as regiões de span, onde todos eles estão, e obtendo o texto, limpando-o e salvando-o.

- **==Validação de Dados==**
  Ao mesmo tempo que os dados estão sendo extraídos, o que é feito para evitar a repetição de notícias é, antes de mais nada, reverter o *url* da notícia para extrair seu id, esse mesmo id é salvo em uma lista para ser comparado posteriormente com a notícia atual que está sendo extraída.

- **==Salvamento de Dados==**
  O formato json foi a estrutura de dados escolhida para salvar os dados, mais conveniente. O formato é `validated_urls_XXXX.json`, onde `XXXX` é o ano, para o arquivo json dos URLs. As notícias são armazenadas em um arquivo chamado `XXXX.json`, onde, novamente, `XXXX` é o ano.

## Passo 2 - Website
### Tecnologias
  - **Flask**
  Flask é um framework Python para construir sites full-stack, e por que Flask e não outro framework? Os algoritmos de busca que são usados são todos baseados em Python, então por que não usar um framework Python, mais fácil de usar e manipular dados.
  Um breve resumo sobre Flask:
  
## Passo 3 - Busca
### Algoritmos
  - **Elastic Search**




# ==EN==

## Prologue
**Notícias da Covilha @ Arquivo Web** is a final project in (âmbito) of the curricular unity of Projeto (at [UBI](https://ubi.pt))

# ==IMPORTANT QUESTIONS==
- **How does the tesseract (OCR) works?**
- **Generally how the packages I use work**

## ==INSTALL TESSERACT ON MAC==
- required `brew`
- `brew install tesseract`

## Step 1 - Data
### Data Extraction and Data Validation
- **==Data Extraction==**
  The first step of the data extraction is getting the news URLs, so the function created takes the URL of the page, in this case [noticiasdacovilha.pt](noticiasdacovilha.pt), and with the use of a package created by **Professor Ricardo Campos** and a previous student of his, **Diogo Correia** (might need to fix this line), that package which I'm going to complement with my work, contributing to create a (even) more composed package (fix this too). So what this package does is by giving it a URL link, it uses the [Arquivo.PT](https://arquivo.pt) API to retrieve all the links from that URL, that are stored there.
  The function does a pre-validation to fix the problem of having repetitive URL links, so that we don't have repetitive news, which take space and time.
  
  - **==Script==**
  	Now passing to the function that extracts the data, the approach was saving each URLs in json files per year, so that when we access it we can decide which years we want. With the help of packages such as `requests` and `beautifulsoup4`, the first one to get the HTML data from the URL link and the second one to search the data, the first thing to search is a `div` that has the **category** and the **subcategory**, which are on the top side of the page. Then it searches for another `div` with the id `div_conteudo_left`, that contains that unique news info, everything. 

  - **==News Front Page==**
    The Notícias da Covilhã is a weekly newspaper, each week there is a new news front page, that every news page (from the website) has it there.
    The first approach was to display every possible newspaper front page from the website, to do that it was used an OCR called tesseract, it is an image recognition that transforms it in text (super useful), and given that it extracts the date from it, so it can be tagged as so and later displayed.
    - **1ST STEP:** Given the front page URLs, find the image url, with the help of the `BeautifulSoup` package
    - **2ND STEP:** For each one of the image urls (do a cicle), using the package `requests`, get the content of it
    - **3RD STEP:** 
    
   - **==Image and its Description==**
    To get the image it searched for the `img` element and retrieve it `src`, that contains the source (URL) of the image.
    So to get the image description the algorithm that was thought about was reversing the string that we got from the source attribute and iterate it until it reaches a /, because the name of the image (the file) was the last element after the last /, given that, after cleaning it, we got a image name that could be used to associate the image to a person/entity.
    
   - **==Main Text==**
    The paragraph content is divided into 2 sections, the text snippet and the paragraphs, to get the text snippet it scraps the first line (that is in reality the first paragraph sometimes) and saves it in a different variable than the rest, then, with the help of a package called `cleantext`, and using a function from that called clean, it was possible to clean all the *garbage* from the text (unicode chars, etc...), all that in a cicle for which it was used to iterate through all the paragraphs and with that I could save each one as a String, to later append it to a list of Strings (to better use later).
    
   - **==Keywords==**
    To retrieve the keywords from the paragraphs it was used a software called YAKE, installing the YAKE through pip to use it in our code, **(explain here how YAKE works, simply and easy)**, it retrieved the top 10 keywords of each paragraph and saved it also.
    
    - **==spaCy==**
    SpaCy is another package, used to retrieve all the entities from the paragraph, that will be super useful to implement the top Entities of that week/month/year, it's possible with that. **(need to add more development to this and to the Keywords)** Accuracy model used
    
    - **==The Rest==**
    What's missing is the author, the tags and the date are obtained by searching all the span regions, where they are all in, and obtain the text, clean it and save it.
    
    - **==Data Validation==**
    At the same time the data is being extracted, what its done to avoid repetition of news is, first of all, the *url* of the news is being reversed to extract its id, that same id is saved in a list to later be compared to the current news being extracted.
    
    - **==Data Saving==**
    The json format was the data structure choosed to save the data, more convenient. The format is `validated_urls_XXXX.json`, where `XXXX` is the year, to the URLs json file. The news are stored in a file called `XXXX.json`, where, again, `XXXX` is the year.

## Step 2 - Website
### Technlogies
  - **Flask**
  Flask is a Python framework to build full-stack websites, and why Flask and not another framework? The search algorithms that are used are all python based, so why not using a python framework, easier to use and manipulate data.
  A little brief about Flask: 
  
## Step 3 - Search
### Algorithms
  - **Elastic Search**

