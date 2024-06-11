import json

def order_authors():
    # add a number to the image name to each author and save it in a json file
    with open('./news_data/authors.json', 'r') as f:
        data = json.load(f)
    
    authors = {}
    for i, author in enumerate(data):   
        authors[author] = f'image_{i}.jpg'
    
    with open('./news_data/authors2.json', 'w') as f:
        json.dump(authors, f, indent=4, ensure_ascii=False)
        

order_authors()


def change_author():
    
    # Alexandre Salgueiro   
    # Alberto Alçada Rosa
    # Ana Rita Pinto: Ana Rito Pinto
    # António Pinto Pires: Pinto Pires,
    # António Rodrigues de Assunção
    # Assunção Vaz Patto: A.Vaz Patto
    # Avelino Gonçalves
    # José Ayres de Sá: Ayres de Sá
    # Carlos Madaleno
    # Carlos Pinto
    # Cristela Bairrada
    # D. Manuel Felício: (Manuel Felício, Bispo da Guarda), (D. Manuel Felício, Bispo da Guarda)
    # Eduardo Alves
    # Filipe Pinto
    # Francisco Rodrigues S.J.
    # João Cunha
    # João de Jesus Nunes
    # João Filipe Pereira
    # João Morgado
    # João Santos
    # Joaquim Paulo Serra: Paulo Serra
    # Jorge Saraiva
    # José Gameiro
    # José Pinheiro Fonseca
    # José Rodrigues Pires Manso: J.R. Pires Manso, Pires Manso, José R. Pires Manso
    # José Vincente Ferreira
    # Luis Fiadeiro
    # Maria Eduarda Ribeiro
    # Neuza Correia
    # Paulo Antunes
    # Paulo Neves
    # Pedro Ferreira
    # Ricardo Cocchi
    # Rui Delgado
    # Rui Manique
    # Sérgio Gaspar Saraiva: Sergio Saraiva, Sergio Gaspar Saraiva, Sérgio Saraiva
    # Susana Garrido
    # Susana Proença
    # Tiago Serrão
    # Vítor Pereira
    # Vitor Pinho
    
    for year in range(2009, 2020):
        with open(f'./news_data/{year}/key_moments_{year}.json', 'r') as f:
            data = json.load(f)
        
        for article in data:
            if article['author'] == "Ana Robeiro Rodrigues" or article['author'] == "Ana Ribiero Rodrigues" or article['author'] == "ARR" or article['author'] == "ana ribeiro rodrigues":
                article['author'] = "Ana Ribeiro Rodrigues"
                
            elif article['author'] == "JA" or article['author'] == "João Alves, com RCB" or article['author'] == "joão alves" or article['author'] == "joão Alves" or article['author'] == "João alves":
                article['author'] = "João Alves"
            
            elif article["author"] == "Ana Rita Pinto" or article['author'] == "ana rito pinto":
                article['author'] = "Ana Rita Pinto"
                
            elif article['author'] == "rui delgado":
                article['author'] = "Rui Delgado"
                
            elif article['author'] == "alberto alçada rosa":
                article['author'] = "Alberto Alçada Rosa"
                
            elif article['author'] == "pinto pires" or article['author'] == "Pinto Pires" or article['author'] == "Pinto pires" or article['author'] == "pinto Pires":
                article['author'] = "António Pinto Pires"
                
            elif article['author'] == "antónio rodrigues de assunção":
                article['author'] = "António Rodrigues de Assunção"
                
            elif article['author'] == "a.vaz patto" or article['author'] == "A.Vaz Patto" or article['author'] == "A. Vaz Patto" or article['author'] == "A. Vaz patto" or article['author'] == "a. vaz patto" or article['author'] == "a vaz patto" or article['author'] == "A Vaz Patto" or article['author'] == "A. Vaz patto" or article['author'] == "assunção vaz patto":
                article['author'] = "Assunção Vaz Patto"
            
            elif article['author'] == "ayres de sá" or article['author'] == "Ayres de Sá" or article['author'] == "Ayres de sá" or article['author'] == "ayres de sa" or article['author'] == "Ayres de sa" or article['author'] == "ayres de Sa" or article['author'] == "ayres de Sá":
                article['author'] = "José Ayres de Sá"
                
            elif article['author'] == "carlos madaleno" or article["author"] == "Carlos madaleno" or article["author"] == "carlos Madaleno":
                article['author'] = "Carlos Madaleno"
                
            elif article['author'] == "carlos pinto" or article['author'] == "Carlos pinto" or article["author"] == "carlos Pinto":
                article['author'] = "Carlos Pinto"
                
            elif article['author'] == "cristela bairrada" or article['author'] == "cristela Bairrada" or article['author'] == "cristela bairrada":
                article['author'] = "Cristela Bairrada"
                
            elif article['author'] == "manuel felício" or article['author'] == "Manuel Felício" or article['author'] == "D. Manuel Felício" or article['author'] == "D. Manuel Felício, Bispo da Guarda" or article['author'] == "D. Manuel Felício, Bispo da Guarda" or article["author"] == "D. Manuel Felício, Bispo da Guarda" or article['author'] == "d. manuel felício, bispo da guarda":
                article['author'] = "Manuel Felício"
                
            elif article['author'] == "eduardo alves" or article['author'] == "Eduardo alves" or article['author'] == "eduardo Alves":
                article['author'] = "Eduardo Alves"
                
            elif article['author'] == "filipe pinto" or article['author'] == "Filipe pinto" or article['author'] == "filipe Pinto":
                article['author'] = "Filipe Pinto"
            
            elif article['author'] == "francisco rodrigues s.j." or article['author'] == "Francisco rodrigues s.j." or article['author'] == "Francisco Rodrigues S.J." or article['author'] == "francisco rodrigues s.j" or article['author'] == "francisco rodrigues s.j" or article['author'] == "francisco rodrigues s.j":
                article['author'] = "Francisco Rodrigues S.J."
                
            elif article['author'] == "joão cunha" or article['author'] == "João cunha" or article['author'] == "joão Cunha":
                article['author'] = "João Cunha"
                
            elif article['author'] == "joão de jesus nunes" or article['author'] == "João de jesus nunes" or article['author'] == "joão de Jesus nunes":
                article['author'] = "João de Jesus Nunes"
                
            elif article['author'] == "joão filipe pereira" or article['author'] == "João filipe pereira" or article['author'] == "joão Filipe pereira":
                article['author'] = "João Filipe Pereira"
            
            elif article['author'] == "joão morgado" or article['author'] == "João morgado" or article['author'] == "joão Morgado":
                article['author'] = "João Morgado"
            
            elif article['author'] == "joão santos" or article['author'] == "João santos" or article['author'] == "joão Santos":
                article['author'] = "João Santos"
            
            elif article['author'] == "joaquim paulo serra" or article['author'] == "Joaquim paulo serra" or article['author'] == "joaquim Paulo serra":
                article['author'] = "Joaquim Paulo Serra"
            
            elif article['author'] == "paulo serra" or article['author'] == "Paulo serra" or article['author'] == "paulo Serra":
                article['author'] = "Joaquim Paulo Serra"
                
            elif article['author'] == "jorge saraiva" or article['author'] == "Jorge saraiva" or article['author'] == "jorge Saraiva":
                article['author'] = "Jorge Saraiva"
                
            elif article['author'] == "josé gameiro" or article['author'] == "José gameiro" or article['author'] == "josé Gameiro":
                article['author'] = "José Gameiro"
            
            elif article['author'] == "josé pinheiro fonseca" or article['author'] == "José pinheiro fonseca" or article['author'] == "josé Pinheiro fonseca":
                article['author'] = "José Pinheiro Fonseca"
            
            elif article['author'] == "j.r. pires manso" or article['author'] == "j.r. pires manso" or article['author'] == "J.R. Pires Manso" or article['author'] == "j.r. Pires manso" or article['author'] == "j.r. pires Manso" or article['author'] == "j.r. Pires Manso" or article['author'] == "pires manso" or article['author'] == "Pires manso" or article['author'] == "pires Manso" or article['author'] == "Pires Manso" or article['author'] == "josé r. pires manso" or article['author'] == "José r. pires manso" or article['author'] == "josé R. pires manso" or article['author'] == "José R. pires manso":
                article['author'] = "José Rodrigues Pires Manso"
                
            elif article['author'] == "josé vincente ferreira" or article['author'] == "José vincente ferreira" or article['author'] == "josé Vincente ferreira":
                article['author'] = "José Vincente Ferreira"
                
            elif article['author'] == "luis fiadeiro" or article['author'] == "Luis fiadeiro" or article['author'] == "luis Fiadeiro":
                article['author'] = "Luis Fiadeiro"
                
            elif article['author'] == "maria eduarda ribeiro" or article['author'] == "Maria eduarda ribeiro" or article['author'] == "maria Eduarda ribeiro":
                article['author'] = "Maria Eduarda Ribeiro"
                
            elif article['author'] == "neuza correia" or article['author'] == "Neuza correia" or article['author'] == "neuza Correia":
                article['author'] = "Neuza Correia"
                
            elif article['author'] == "paulo antunes" or article['author'] == "Paulo antunes" or article['author'] == "paulo Antunes":
                article['author'] = "Paulo Antunes"
            
            elif article['author'] == "paulo neves" or article['author'] == "Paulo neves" or article['author'] == "paulo Neves":
                article['author'] = "Paulo Neves"
                
            elif article['author'] == "pedro ferreira" or article['author'] == "Pedro ferreira" or article['author'] == "pedro Ferreira":
                article['author'] = "Pedro Ferreira"
            
            elif article['author'] == "ricardo cocchi" or article['author'] == "Ricardo cocchi" or article['author'] == "ricardo Cocchi":
                article['author'] = "Ricardo Cocchi"
            
            elif article['author'] == "rui delgado" or article['author'] == "Rui delgado" or article['author'] == "rui Delgado":
                article['author'] = "Rui Delgado"
                
            elif article['author'] == "rui manique" or article['author'] == "Rui manique" or article['author'] == "rui Manique":
                article['author'] = "Rui Manique"
                
            elif article['author'] == "sergio saraiva" or article['author'] == "Sergio saraiva" or article['author'] == "sergio Saraiva":
                article['author'] = "Sérgio Gaspar Saraiva"
                
            elif article['author'] == "susana garrido" or article['author'] == "Susana garrido" or article['author'] == "susana Garrido":
                article['author'] = "Susana Garrido"
                
            elif article['author'] == "susana proença" or article['author'] == "Susana proença" or article['author'] == "susana Proença":
                article['author'] = "Susana Proença"
            
            elif article['author'] == "tiago serrão" or article['author'] == "Tiago serrão" or article['author'] == "tiago Serrão":
                article['author'] = "Tiago Serrão"
                
            elif article['author'] == "vítor pereira" or article['author'] == "Vítor pereira" or article['author'] == "vítor Pereira" or article['author'] == "Vitor pereira" or article['author'] == "Vitor Pereira" or article['author'] == "vitor pereira" or article['author'] == "vitor Pereira":
                article['author'] = "Vítor Pereira"
            
            elif article['author'] == "vitor pinho" or article['author'] == "Vitor pinho" or article['author'] == "vitor Pinho":
                article['author'] = "Vitor Pinho"
            
        with open(f'./news_data/{year}/key_moments_{year}', 'w') as f:
            json.dump(data, f, indent=4)

change_author()
            