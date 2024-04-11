from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# para efeitos de embeddings, considera-se a última camada
def square_rooted(x):
    from math import sqrt 
    return round(sqrt(sum([a*a for a in x])),3)

def Cosine(x,y):
    numerator = sum([a*b for a,b in zip(x,y)])
    denominator = square_rooted(x)*square_rooted(y)
    return round(numerator/float(denominator),3)

tokenizer = AutoTokenizer.from_pretrained("NOVA-vision-language/GlorIA-1.3B")
model = AutoModelForCausalLM.from_pretrained("NOVA-vision-language/GlorIA-1.3B")

text = "Infra-estrutura substituirá as duas estações de tratamento que se encontram nos extremos da cidade A nova Estação de Tratamento de Águas Residuais (ETAR) de Castelo Branco, orçada em 15 milhões de euros, vai ser construída a partir de Maio de 2011, informou na passada semana o presidente da Câmara, Joaquim Morão. A nova estação de tratamento será construída pela empresa Águas do Centro e vai substituir as duas estações de tratamento que se encontram nas entradas sul e norte de cidade. A nova estrutura ocupará uma área de 27 mil metros quadrados, em terrenos paralelos à auto-estrada A23, entre o nó do Hospital Amato Lusitano e a saída norte para Castelo Branco. Segundo o presidente da Câmara a autorização do Ministério do Ambiente para a realização do investimento foi garantido \"esta semana na visita que a ministra da tutela efectuou a Castelo Branco\". O concurso para a construção da nova Etar já foi efectuado pela Águas do Centro, numa lógica de concepção-construção. A nova Etar obrigará à construção de uma estação elevatória na actual Etar Norte, de forma a encaminhar o esgoto que aí é tratado para a nova estrutura, e uma ligação do colector da actual Etar Sul para a nova Etar. A obra deverá demorar cerca de dois anos a ser concluída e terá capacidade para tratar dos efluentes de mais de 95 mil habitantes. \"Deste modo é dado um passo importante para melhorar a cidade. Castelo Branco tem hoje duas ETAR em entradas da cidade, com todos os incómodos que isso acarreta. Ao construirmos uma nova estrutura permite-nos eliminá-las e dar um melhor aspecto ambiental e mais competitividade a Castelo Branco\", afirma o autarca."
input_ids = tokenizer.encode(text, return_tensors="pt")
# print(input_ids.shape)  # torch.Size([1, 6]) para o text="Olá, tudo bem?"
outputs = model(input_ids, output_hidden_states=True)
embeddings = outputs.hidden_states[-1]

text2 = "Padre Fernando Brito é homenageado no domingo. Ao NC conta a sua ligação ao semanário Quando, aos 24 anos, deixou Loriga, concelho de Seia, em Setembro de 1959 (tinha sido ordenado padre um mês antes), Fernando Brito dos Santos, o padre Fernando, longe estaria de pensar que os próximos 60 anos seriam passados na Covilhã, e, além das funções sacerdotais que iria ter, passaria mais de meio século agarrado a um jornal. Não no sentido literal da palavra, mas com uma ligação quase umbilical a um semanário com mais de uma centena de anos: o Notícias da Covilhã (NC). \"Eu entrei na paróquia de Nossa Senhora da Conceição a 2 de Setembro de 1959. Como o jornal estava adstrito à paróquia, acabei por entrar nele também, pois eu era o coadjutor do padre José de Andrade. E passei também por assim dizer, a coadjutor do jornal, que se localizava em instalações precárias, na Rua Comendador Mendes Veiga. Ficava na cave de uma casa, onde estava a máquina de impressão, ali ao lado do Abrigo dos Pequeninos\" explica ao NC o seu ex-director, que no passado mês de Dezembro deixou o cargo. Que ocupou nos últimos nove anos, embora a ligação ao NC já exista, em diversos cargos, há cerca de 60. Desde que chegou à Cidade Neve. \"Acompanhei todas as mudanças\" E, como muito boa gente, foi por baixo que o padre Fernando começou. A fazer funções do mais básico que havia. Mas importantes. \" À quinta-feira íamos, eu e o padre Andrade, buscar o jornal à máquina. À mão, para levarmos para outras instalações do Notícias, de modo a dobrá-lo, cintá-lo, para poder ir para os correios. Eu vim para dobrar o jornal\" graceja Fernando Brito, que diz que era \"grande preocupação\" do padre José Andrade, na altura director do NC, ter tudo pronto a horas. \"Ele acompanhava tudo do jornal. E eu também. Na altura, o NC tinha poucos trabalhadores, para aí uns seis, mas depois foi crescendo\" frisa. (Reportagem completa na edição papel)"
input_ids2 = tokenizer.encode(text2, return_tensors="pt")
# print(input_ids2.shape)  # torch.Size([1, 6]) para o text="Olá, tudo bem?"
outputs2 = model(input_ids2, output_hidden_states=True)
embeddings2 = outputs2.hidden_states[-1]

# calcular a média dos embeddings
mean_embedding1 = torch.mean(embeddings[0], dim=1)
mean_embedding2 = torch.mean(embeddings2[0], dim=1)

# Calcular a similaridade entre os embeddings
cosine_similarity = Cosine(mean_embedding1.tolist(), mean_embedding2.tolist())
print(cosine_similarity)