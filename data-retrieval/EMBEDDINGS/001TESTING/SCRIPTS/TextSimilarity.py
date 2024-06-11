import json
import os
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import numpy as np

# tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
# model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")

model = AutoModelForCausalLM.from_pretrained('neuralmind/bert-base-portuguese-cased')
tokenizer = AutoTokenizer.from_pretrained('neuralmind/bert-base-portuguese-cased', do_lower_case=False)

def square_rooted(x):
    from math import sqrt 
    return round(sqrt(sum([a*a for a in x])),3)

def Cosine(x,y):
    numerator = sum([a*b for a,b in zip(x,y)])
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

def similarity_per_text(text1, text2):
    input_ids = tokenizer.encode(text1, return_tensors="pt")
    outputs = model(input_ids, output_hidden_states=True)
    embeddings = outputs.hidden_states[-1]

    input_ids2 = tokenizer.encode(text2, return_tensors="pt")
    outputs2 = model(input_ids2, output_hidden_states=True)
    embeddings2 = outputs2.hidden_states[-1]

    # calcular a média dos embeddings
    mean_embedding1 = torch.mean(embeddings[0], dim=1)
    mean_embedding2 = torch.mean(embeddings2[0], dim=1)

    # Calcular a similaridade entre os embeddings
    cosine_similarity = Cosine(mean_embedding1.tolist(), mean_embedding2.tolist())
    print("SIMILARIDADE: ", cosine_similarity)
    
    return cosine_similarity

def similarity_per_text_list(text1, text_list):
    similarities = []
    for text2 in text_list:
        similarity = similarity_per_text(text1, text2)
        similarities.append(similarity)
    return similarities

def similarity_per_file(input_file, output_file):
    with open(input_file, 'r') as f:
        data = json.load(f)

    for i, article in enumerate(data):
        list_of_similarities = []
        current_nid = article['nid']
        current_title = article['title']
        current_text = article['content']
        if current_title == "":
            continue
        else:
            # Open the similarity file for each article to check for existing comparisons
            with open(output_file, 'r') as f:
                similarity_data = json.load(f)

            for article2 in similarity_data:
                if article2['nid'] != current_nid: # and article2['nid'] not in [x[2] for x in list_of_similarities]
                    title2 = article2['title']
                    text2 = article2['content']
                    if title2 == "":
                        continue
                    else:
                        if len(list_of_similarities) < 3:
                            similarity = similarity_per_text(current_title, title2)
                            similarity2 = similarity_per_text(current_text, text2)
                            mean_similarity = (similarity + similarity2) / 2
                            if mean_similarity > 0.75:
                                list_of_similarities.append((similarity, current_nid, article2['nid']))
            
            article['similarities'] = list_of_similarities
            print(f"Article {i} done")
            
    # Save the updated data file after processing all articles
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


# def main(year):
#     for year in range(year, year + 1):
#         input_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/validated_{year}.json'
#         output_file = f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/similarity_{year}.json'
#         # input_file = f'../data/data_{year}/validated{year}.json'
#         # output_file = f'../data/data_{year}/similarity_{year}.json'
#         if os.path.exists(input_file):
#             similarity_per_file(input_file, output_file)
#         else:
#             print(f"Input file not found for year {year}")
        
#main(2009)

# # similares
# text1 = "Queiroz quer ex-reitores como consultores"
# text2 = "João Queiroz toma posse sexta-feira"
# similarity = similarity_per_text(text1, text2)
# print("SIMILARES: ", similarity) 

# # não similares
# text1 = "Condutora condenada a quatro anos com pena suspensa"
# text2 = "O Sr. A e os medicamentos da memória"
# similarity = similarity_per_text(text1, text2)
# print("NÃO SIMILARES: ", similarity) 

def getTextEmbeddings(text):
    input_ids = tokenizer.encode(text, return_tensors="pt", truncation=True, max_length=100, add_special_tokens = True)
    outputs = model(input_ids, output_hidden_states=True)
    embeddings = outputs.hidden_states[-1]

    # mean_embedding = np.mean(np.array(embeddings.detach().numpy()), axis=2)
    mean_embedding = torch.mean(embeddings, dim=1)
    np_mean = mean_embedding[0].tolist()
    
    # voltar a converter para numpy quando se popular
    # print(np_mean)
    
    return np_mean

# GUARDAR OS EMBEDDINGS NUM JSON
def save_embeddings(year, start_nid=None):
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/validated_{year}.json', "r", encoding="utf8") as readfile:
        key_moments = json.load(readfile)
    
    # Sort key_moments by nid
    key_moments.sort(key=lambda x: x['nid'])
    
    if start_nid:
        # Find the index of the document with the specified nid
        start_index = next((i for i, doc in enumerate(key_moments) if doc['nid'] == start_nid), None)
        if start_index is None:
            print(f"Document with nid {start_nid} not found.")
            return
        # Start processing from the document with the specified nid
        key_moments = key_moments[start_index:]
    
    for i, doc in enumerate(key_moments):
        title = doc['title']
        content = doc['content']
        
        title_embedding = getTextEmbeddings(title)
        content_embedding = getTextEmbeddings(content)
        
        doc['title_embedding'] = title_embedding
        doc['content_embedding'] = content_embedding
        
        print(f"Embeddings for article {doc['nid']} done")
        
        # Save embeddings for this document
        if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_data') == False:
            os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_data')
        
        with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_data/embeddings_{year}_doc_{doc["nid"]}.json', "w") as writefile:
            json.dump(doc, writefile, indent=4, ensure_ascii=False)
        print(f"Embeddings for article {doc['nid']} saved")

    # Save all embeddings at the end
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_{year}.json', "w") as writefile:
        json.dump(key_moments, writefile, indent=4, ensure_ascii=False)
    print("All embeddings saved")

# GET SIMILARITY FROM FILES
def get_similarity_from_files(year, nid1, nid2):
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_data/embeddings_{year}_doc_{nid1}.json', "r") as readfile:
        doc1 = json.load(readfile)
    
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/embeddings_data/embeddings_{year}_doc_{nid2}.json', "r") as readfile:
        doc2 = json.load(readfile)
    
    title1_embedding = doc1['title_embedding']
    content1_embedding = doc1['content_embedding']
    
    title2_embedding = doc2['title_embedding']
    content2_embedding = doc2['content_embedding']
    
    title_similarity = Cosine(title1_embedding, title2_embedding)
    content_similarity = Cosine(content1_embedding, content2_embedding)
    
    print(f"Title similarity between documents {nid1} and {nid2}: {title_similarity}")
    print(f"Content similarity between documents {nid1} and {nid2}: {content_similarity}")
    
    return title_similarity, content_similarity

def get_great_similarity_from_nid(year, nid, value):
    # get the similarities from the nid that have a value greater than the value
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/final_similarities_{year}.json', "r") as readfile:
        articles = json.load(readfile)
    
    for article in articles:
        if article['nid'] == nid:
            similarities = article['similarities']
            for similarity in similarities:
                if similarity[1] > value:
                    print(f"Similarity greater than {value} found between documents {nid} and {similarity[2]}")
                    print(f"Title similarity: {similarity[0]}")
                    print(f"Content similarity: {similarity[1]}")
                    # print the title and content of the other document
                    for article2 in articles:
                        if article2['nid'] == similarity[2]:
                            nid2 = article2['nid']
                            print(f"Title: {article2['title']}")
                            print(f"Content: {article2['content']}")
                            
                            sim_dict = {
                                'nid_1': nid,
                                'nid_2': nid2,
                                'title_1': article['title'],
                                'content_1': article['content'],
                                'title_2': article2['title'],
                                'content_2': article2['content'],
                                'title_similarity': similarity[0],
                                'content_similarity': similarity[1]
                            }
                            
                            #save to a file with both nids
                            if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/single_similarities') == False:
                                os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/single_similarities')
                            
                            if os.path.exists(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/single_similarities/similarities_{year}_{nid}') == False:
                                os.makedirs(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/single_similarities/similarities_{year}_{nid}')
                                
                            with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/single_similarities/similarities_{year}_{nid}/similarities_{year}_{nid}_{nid2}.json', "w") as writefile:
                                json.dump(sim_dict, writefile, indent=4, ensure_ascii=False)
                            break
                    
def get_great_similarity_from_year(year, value, demo=False):
    # gets the articles nid from that year
    with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{year}/final_similarities_{year}.json', "r") as readfile:
        articles = json.load(readfile)
    
    if demo:
        articles = articles[:10]
        for article in articles:
            article_nid = article['nid']
            get_great_similarity_from_nid(year, article_nid, value)
            
    else:
        for article in articles:
            article_nid = article['nid']
            get_great_similarity_from_nid(year, article_nid, value)
        
    

# def main():
#     for i in range(2009, 2020):
#         # open the articles file for that year
#         with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{i}/embeddings_{i}.json', "r", encoding="utf8") as readfile:
#             articles = json.load(readfile)
            
#         for j, article in enumerate(articles):
#             # get the nid
#             nid = article['nid']
#             # compare to the rest of the articles
#             for k, article2 in enumerate(articles):
#                 if article2['nid'] != nid:
#                     nid2 = article2['nid']
#                     title_similarity, content_similarity = get_similarity_from_files(i, nid, nid2)
#                     # save the similarities with the nid2
#                     if article.get('similarities') is None:
#                         article['similarities'] = [(title_similarity, content_similarity, nid2)]
#                     else:
#                         article['similarities'].append((title_similarity, content_similarity, nid2))
#                     print(f"Similarities for articles {nid} and {nid2} saved")
            
#             print(f"Article {nid} done")
#         #save to a file
#         with open(f'/Users/rdsilva01/Documents/001DEV/003UBI/001PROJETO/noticias-da-covilha-arquivo-web/data/data_{i}/final_similarities_{i}.json', "w") as writefile:
#             json.dump(articles, writefile, indent=4, ensure_ascii=False)
#main()


# Example usage: starting processing from document with nid "123"
# save_embeddings(2009)
#save_embeddings(2010)
# save_embeddings(2011)
# save_embeddings(2012)
# save_embeddings(2013)
# save_embeddings(2014)
# save_embeddings(2015)
# save_embeddings(2016)
# save_embeddings(2017)
# save_embeddings(2018)
# save_embeddings(2019)

# # similares
# text1 = "Queiroz quer ex-reitores como consultores"
# text2 = "João Queiroz toma posse sexta-feira"
# similarity = similarity_per_text(text1, text2)
# print("SIMILARES: ", similarity) 

# # não similares
# text1 = "Condutora condenada a quatro anos com pena suspensa"
# text2 = "O Sr. A e os medicamentos da memória"
# similarity = similarity_per_text(text1, text2)
# print("NÃO SIMILARES: ", similarity) 

# emb1 = getTextEmbeddings("Apesar de ter perdido por uma bola com o Varzim, com quem disputava a permanência na Liga de Honra de futebol, o Sporting da Covilhã beneficiou da derrota do Chaves e garantiu na derradeira jornada a manutenção. Foto de arquivo")
# #emb2 = getTextEmbeddings("Covilhã perde 2-0 em casa com o Trofense e afunda-se na tabela O Sporting da Covilhã caiu na última jornada abaixo da linha de água, com os mesmos 15 pontos do 14º classificado, e bem se pode queixar de si próprio, dada a pálida exibição, embora a arbitragem tenha impedido os serranos de somarem um ponto, quando anulou o que seria o golo do empate, já nos descontos. Frente a um Trofense nos lugares cimeiros, actualmente no segundo posto da Liga de Honra, que também não deslumbrou, os Leões da Serra perderam por duas bolas. O primeiro golo resultou de um \"brinde\" do central Abdoulaye, apontado por Zé Manel aos 33 minutos. O segundo por intermédio de Licá, quando passavam três minutos dos 90, instantes depois de o árbitro, João Ferreira, ter anulado o tento, aparentemente \"limpo\", da igualdade dos serranos. Bahim, logo no primeiro minuto de jogo, rematou por cima e Nildo, aos 9, num livre junto à lateral, atirou forte para a defesa de Igor. Mas até à passagem da meia hora viu-se pouco futebol na Covilhã, com nenhuma das equipas a pegar na iniciativa de um jogo equilibrado, pouco disputado e a desenrolar-se a um ritmo muito lento. Jogados 26 minutos, Abdoulaye derrubou Serginho mesmo à entrada da área, num lance que lhe valeu o cartão amarelo. Na conversão de um livre potencialmente perigoso, Nildo chutou contra a barreira. Ao minuto 33, Abdoulaye, que há duas jornadas, frente à Oliveirense, já tinha cometido uma fífia semelhante, 'ofereceu' o primeiro golo aos forasteiros. O central, à vontade, foi displicente e passivo na recepção da bola, deixou-a escapar e Zé Manuel, em velocidade, isolou-se e atirou forte para o primeiro tento do encontro. Volvidos dois minutos, Nildo, de livre, rematou por cima da barra. Já os serranos, não conseguiram criar qualquer ocasião de perigo. Fofana, um dos mais persistentes, tentou uma flexão pelo meio e rematou rasteiro, sem assustar. Erro de arbitragem impede empate ao cair do pano No segundo tempo, já com Paulico e Severino nos lugares de Samson e de Vouho, foi o Trofense quem ameaçou pela primeira vez, mas o Sporting da Covilhã foi ganhando mais dinâmica, passou a praticar um futebol mais apoiado e a ser a equipa que mais vezes rondou a baliza adversária, embora quase sempre de forma consequente. Severino, ao segundo poste, rematou para a defesa de Marco. Pouco depois o esforço de Fofana, a tentar meter a bola na área, também foi infrutífero, por não aparecer ninguém para a finalização. A resposta veio por Zé Manel, que vindo pela esquerda, entrou pelo meio e testou Igor em zona frontal, tendo o guardião socado o esférico. Rincón, solicitado por Severino, que veio dar maior poder atacante à equipa, tentou a sorte de cabeça, mas Marco soube opor-se. Do lado contrário, Igor também negou o golo a Reguila, após desatenção da defensiva serrana. Nos minutos finais os serranos aumentaram a pressão e, já nos descontos, João Ferreira anulou o golo do empate a Rincón, por suposto fora-de-jogo, decisão muito contestada pelos Leões da Serra. Três minutos após os 90, os visitantes aproveitaram a desconcentração do Sporting da Covilhã, com os adeptos na bancada a protestarem da decisão do juiz de linha, para fixarem o resultado final, por intermédio de Licá, que tinha substituído Zé Manel aos 83 minutos.")
# emb2 = getTextEmbeddings("Se não começarmos a tentar inverter estas situações depressa a negrura que paira sobre 2011 vai ser pior do que pensamos O fim do ano acaba por ser uma época em que quase somos forçados a olhar para o tempo que passa. E a lembrar este e aquele caso, este e aquele doente, esta e aquela cara que, de alguma forma, nos tocaram e nos deixaram marcas. 2010 foi um ano muito rico em termos de boas lembranças, sobretudo de doentes que ultrapassaram em muito a relação profissional e se mostraram mais amigos que doentes. Recomecei o velho hábito de escrever um diário para manter as memórias destes casos que nos aquecem o coração. E também para manter as memórias do mal que encontrei –há que não esquecer. É uma frase aparentemente mais adequada aos campos de concentração e ao genocídio do Ruanda, mas a meu ver o mal, em formas mesquinhas ou em formas estrondosas é sempre mal. A história de dar a outra face com que somos embalados desde a infância na nossa cultura católica leva, a meu ver, a interpretações erróneas de como lidar com o mal. Afinal o dar a outra face, o perdoar, o amar os nossos inimigos, o fazer o politicamente correcto não passa de uma forma de cobardia moral. Como é uma forma de cobardia moral não apontarmos a dedo à corrupção, ao terrorismo sobre os funcionários exercido pelas instituições, à hiper-super-burocratização do País. É uma forma de cobardia moral continuarmos a cumprimentar socialmente patifes, que sabemos ser patifes e ladrões que sabemos ser ladrões. Não acredito que o Menino Jesus que mais tarde expulsou os vendilhões do Templo, nos peça isso. Assim, os meus votos para 2011 serão, parafraseando uma conversa de Festa de Natal, que deixemos de uma vez por todas de ser bonzinhos e tentemos ser pessoas e eventualmente bons, na acepção da palavra de justo, verdadeiro e defensor de quem não se consegue defender. Assim, este ano que vem vai dar um trabalhão. Mas ao darmos um passo nesta direcção estou certa de que vamos descobrir que a minoria que agracia as manchetes dos jornais e tem destruído o nosso País, é mesmo isso - uma minoria. O senhor Z, com 87 anos, tem uma visão aterrorizadora de 2011. Veio à consulta trazido por uma filha que se preocupava com o excesso de nervos do pai. E como é, sem dúvida, uma história portuguesa vale a pena contar. O senhor Z foi sempre agricultor - reformou-se e passou a ter uma reforma pequenina de 200 euros. Vive com a mulher e tem uma filha, um genro e dois netos. Até há mais ou menos dois anos, a vida do senhor Z era uma vida dita normal. Vivia numa casa fria, mal feita – mas nunca teve melhor. Tinha galinhas e cultivava ele e a esposa uma série de leiras. Punha a maior parte da comida na mesa para ele e para a casa da filha desde abóboras a batatas e a couves. Não foi estimulado a fazer mais, nem a tentar mudar o tipo de cultura, nem a vender, nem a fazer uma empresa agrícola. Não sei se teve a ver com o medo de sobressair (e atrair \"o mal de inveja\"… ) ou se por comodismo. Manteve-se igual ao pai dele e a si próprio e trabalhava muito, o que lhe dá só por si um enorme mérito. E gostava do que fazia, e da terra e de ver crescer as coisas. Há dois anos, na altura dos 85 anos, a sua portugalidade tocou-o - fez uma fractura do colo do fémur e foi tratado – mal - no SNS. Ficou a coxear, com mais dificuldade de equilíbrio. No estrangeiro, teria direito a uma indemnização, aqui nem se falou nisso - afinal o senhor Z era velho e não havia mais nada a fazer (o que não deixa muitas vezes de ser a saída mais fácil, independentemente dos anos que o doente tem!). E pronto – o senhor Z deixou de poder trabalhar. A esposa, típica mulher portuguesa a tratar da casa, das galinhas e do senhor Z não conseguiu aguentar. As leiras foram abandonadas. O senhor Z passa a tarde em frente da TV- vê os quatro telejornais e como está completamente lúcido recebe todas as mensagens aterrorizadoras que vêm da \"caixa mágica\". Vê a terra abandonada, e o genro e o neto a gastar dinheiro - ao fim de semana nas comezainas, à semana no supermercado. E literalmente \" passa-se\"- grita com toda a gente, lança profecias da fome que vem aí e da vergonha que é nenhum deles especificamente trabalhar a terra para dar de comer à família. Um médico não deve intervir em situações familiares e manter a neutralidade nestes casos é o ideal por todas as razões. Mas a imagem daquele homem a bradar contra uma sociedade que se afunda lentamente, a par ou provavelmente porque a terra está a afundar-se também, fez-me lembrar os agricultores da minha aldeia, e o respeito pela terra que nos era inculcado – a terra que não possuímos, mas que nos possui e por onde passamos. Tive de dar razão ao senhor Z. Parece-me que, para pena da filha, que esperava um diagnóstico de Alzheimer e uma benzodiazepina que o sentasse num sofá a dormir \" como um velho normal\". Triste País em que os lúcidos são rotulados de dementes. Não me atrevo a dizer o que penso da sanidade mental de alguns figurões, mas se não começarmos a tentar inverter estas situações depressa a negrura que paira sobre 2011 vai ser pior do que pensamos.")
# print(Cosine(emb1, emb2))

get_great_similarity_from_year(2009, 0.89)