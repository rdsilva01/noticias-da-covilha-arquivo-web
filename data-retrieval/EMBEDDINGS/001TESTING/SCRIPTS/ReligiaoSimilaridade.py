from getEmbeddingsAndSimilarity import getThreeModelsSimilarities

##############
##############
## POLÍTICA ##
##############
##############
title_ref = "Ajudar quem precisa: imperativo do Natal"
text_ref = "Mensagem do Bispo da Guarda \"É Natal. Vivei a alegria do Evangelho Jesus nasceu em Belém, no seio de uma família que não teve lugar na cidade. E Ele era o Filho de Deus, o Salvador anunciado pelo coro dos anjos aos pastores que, também fora da cidade, pernoitavam com os seus rebanhos pelos descampados da região. Jesus nasceu, de facto, no seio de uma família que espelhava o amor de Deus. E continua a ser verdade que o amor de um homem e de uma mulher que se escolhem um ao outro, o amor de um pai e de uma mãe comprometidos a viver a total comunhão das suas vidas são condições indispensáveis para uma criança nascer e se desenvolver até atingir a plena maturidade humana. A família feita da complementaridade entre homem e mulher, pai e mãe, filhos e irmãos e mesmo mais alargada é a primeira escola de vida e de relação social. E sem esta escola as outras não podem cumprir a sua missão. A experiência, porém, diz-nos que este desígnio de famílias estáveis e com relações fortes entre todos os seus membros nem sempre se cumpre, o que constitui grande prejuízo para os próprios e para a sociedade. Mais ainda, sabemos que, quando isso acontece, as pessoas sofrem e muito. O Natal convida-nos também a estarmos próximos destas situações de sofrimento, acompanhando as pessoas e ajudando-as a irem até onde puderem no exercício das suas responsabilidades familiares. O Presépio diz-nos que Jesus nasceu fora da cidade, porque lá não havia lugar para Ele. E os primeiros a visitá-lo foram também aqueles que viviam fora da cidade, os pastores, escolhidos para serem os primeiros a quem foi anunciado o nascimento do Salvador. Disse-lhes o anjo: Anuncio-vos uma grande alegria. Hoje, na cidade de David, nasceu o Salvador. E eles, sendo pobres que não tinham negócios para tratar nem riquezas para guardar, partiram apressados e alegres ao encontro do Salvador. O caminho da humildade e da opção pelos mais pobres foi o caminho de Jesus e continua a ser o caminho dos seus discípulos para cumprirem no mundo o mandato de evangelizar recebido de Cristo. Por isso, ser comunidade em saída para as periferias, qual hospital de campanha, sempre no terreno, para atender os que mais precisam utilizando palavras do Papa Francisco, é o nosso estatuto de Igreja e de cristãos. Por sua vez, as obras sociais que a Igreja tutela, prestando embora valiosos serviços na construção e reconstrução do tecido humano e comunitário, têm de ser mais do que IPSS. Têm de ser expressão da caridade generosa, do amor e do serviço desinteressado dos outros, segundo o espírito do Evangelho. Onde houver pessoas a necessitar de ajuda, enquadrada ou não nas situações tipificadas pela tutela pública de acção social, nós queremos estar lá, para responder dentro das nossas possibilidades. E este é grande imperativo do Natal. Vivemos o Natal entre dois sínodos sobre a família. Que este Natal de Jesus nascido em Belém lembre a todas as nossas famílias que elas são, antes de mais, o santuário da vida e do amor, qual Igreja doméstica que pretende viver e espelhar para o mundo a bondade e a ternura sem limites do próprio Deus. Que este Natal possa lembrar também à nossa sociedade e à própria cultura dominante que o propósito de criar condições de vida digna aos cidadãos passa pela defesa dos direitos das famílias e seu correcto enquadramento legal. Boas festas, diante do Presépio de Belém."
title_plus_text_ref = title_ref + ". " + text_ref

# GOOD
title_1 = "Bispo está há dez anos na Diocese"
text_1 = "Prelado faz revisão desta década Faz hoje dez anos que cheguei à Diocese da Guarda para exercer o Ministério Episcopal, por nomeação do Papa João Paulo II. A doença do Sr. D. António dos Santos tinha-o afastado da Diocese e eu fui recebido na Casa Episcopal pelo Rev.do Padre Cartaxo, em seu nome, e pelas irmãs Adelina, Lúcia e Miraldina. Era um dia frio, mas cheio de sol. Saí da Casa Patriarcal de Lisboa, pela manhã e, às 15H00, iniciava-se a celebração de acolhimento e início do Ministério nesta nossa querida Diocese da Guarda. Essa celebração, presidida pelo arcebispo da nossa província eclesiástica e Patriarca de Lisboa, cardeal D. José Policarpo, na ausência do Sr. D. António dos Santos, começou na Igreja da Misericórdia, com cortejo para a Sé, onde foi celebrada a Eucaristia. Os dias que se seguiram continuaram frios, pois parti de casa sempre pela manhã com 6/7 graus negativos e cheguei igualmente com temperaturas muito baixas. Mas o calor do acolhimento que senti, sobretudo nos sacerdotes que ia visitando e também nos fiéis e nas suas comunidades, compensou largamente o frio que as condições atmosféricas impunham. O ano de 2005 foi tempo para um primeiro conhecimento da Diocese, dos sacerdotes, movimentos, serviços e obras de apostolado, dos arciprestados e também das paróquias. No ano de 2006, iniciei o processo das visitas pastorais, por arciprestados, com a preocupação de chegar a todos os diferentes lugares, contactar cada pároco e seus mais directos cooperadores pastorais, assim como as diferentes instituições eclesiais, que fazem o tecido pastoral da nossa diocese. Também houve preocupação de dialogar com as instituições da sociedade civil, por onde necessa­riamente passam as opções que são feitas em cada comunidade e, assim, condicionam a vidas das pessoas. Em cada uma das paróquias visitadas, depois dos diálogos estabelecidos com o pároco e seus mais directos colaboradores, mas também com as várias instituições quer pertencentes à comunidade paroquial quer da sociedade civil, foi elaborado um relatório, que, no encerramento da respectiva visita, foi lido à comunidade e deixado na paróquia para ser arquivado. Nele se fez a descrição do acontecido, mas também se deram indicações sobre alguns caminhos de acção pastoral recomendáveis. No final das visitas pastorais a todas as paróquias do mesmo arciprestado houve também preocupação por elaborar um outro relatório sobre os indicadores mais relevantes dos caminhos de acção pastoral aconselháveis para o conjunto das paróquias desse arciprestado. No final ficou a sensação de que significativo número de paróquias, devido ao reduzido número dos seus residentes, já não têm possibilidade de sozinhas cumprirem todas as dimensões da missão que é cometida à instituição paróquia enquanto tal. Por isso, indepen­dentemente de reformar o número das paróquias, o mais decisivo parece ser criar a nova mentalidade de que as paróquias têm de se abrir muito mais à cooperação pastoral entre si e que o arciprestado tem de ser cada vez mais a base da acção pastoral comum a todas as suas paróquias e conjuntos de paróquias. Também tomámos consciência de que para isso há um instrumento que temos de desenvolver e aproveitar o mais possível, que é o conselho pastoral arciprestal. Este programa de visitas pastorais terminou em dezembro de 2012. O Concílio do Vaticano II Paralelamente, impôs-se a verificação de que era necessário orientar­mos as nossas prioridades pastorais para a formação cristã de adultos. Fizemos um primeiro esforço para retomar o estudo do catecismo da Igreja católica, ao longo de quatro anos, dedicando cada um deles a uma das suas quatro partes. E elaborámos os respectivos textos de apoio. Fizemos, a seguir um segundo esforço, que durou três anos, com o objectivo de remotivar os nossos fiéis e comunidades da Fé para o encontro com a Palavra de Deus e a Bíblia. Pretendemos que fossem criados grupos bíblicos e para tal procurámos a ajuda de missio­nários redentoristas e do Verbo Divino que percorreram os diversas paróquias e arciprestados ao longo destes anos. Quisemos, a seguir, voltar a nossa atenção para o cinquentenário da celebração do Concílio Vaticano II e rever a sua recepção na nossa Diocese e nas nossas comunidades. Para nos motivarmos, começá­mos por lembrar o entusiasmo inicial que suscitou o Concílio em vários sectores de sacerdotes e leigos desta Diocese, nos anos subsequentes ao mesmo Concílio. E procurámos incluir no nosso plano pastoral previsto para quatro anos o desejo de retomar a revisão das formas como as orientações do Concílio estão a ser assumido nas nossas comunidades. Pretendemos concluir este esforço em 2017, com a resposta ao pedido que foi feito para que seja convocada uma assembleia de representantes de toda a nossa Diocese. Nela desejamos definir linhas de prioridade pastoral para os próximos anos, tendo em conta o esforço feito durante os três anos que a antecedem. No primeiro destes 4 anos, que já passou, interrogámo-nos sobre a forma como estamos a aplicar o modelo de Igreja proposto pela Lumen Gentium e a Gaudium et Spes. Naquele que está a decorrer interrogamo-nos sobre as formas de evangelização e catequese exigidas pela presente conjuntura eclesial e social e tendo como inspiração Dei Verbum do Concílio Vaticano II. No ano que se seguirá queremos perguntar-nos pela forma como as nossas comunidades estão a celebrar a Fé de acordo com as orientações da Constituição Conciliar Sacrossantum Concilium. Encontros com os párocos O ano de 2014 foi marcado pela preocupação de fazer-me encontrar com cada um dos nossos párocos e depois também com os seus colaboradores. Sem excluir qualquer outro assunto, procurámos, nestes encontros, avaliar como está a ser feita em nós sacerdotes e nas nossas comunidades a recepção do modelo conciliar da Igreja. Esse encontro com cada pároco foi precedido da recolha de alguns dados sobre o movimento eclesial e social de cada paróquia e conjunto de paróquias. Em geral, este encontro com cada um dos párocos e seus cooperadores foi seguido de um outro encontro, a nível de arciprestado, onde foi apresentado um relatório sobre dados relevantes que indiciam caminhos pastorais de maior colaboração entre as distintas paróquias e conjuntos de paróquias, valorizando sempre e o mais possível a estrutura do arciprestado."
title_plus_text_1 = title_1 + ". " + text_1

# GOOD
title_2 = "Procissão dos Passos no domingo"
text_2 = "Celebrações da Semana Santa na Covilhã A Santa Casa da Misericórdia, em parceria com a Câmara da Covilhã e outras entidades do concelho, realiza, mais uma vez, as celebrações da Semana Santa na cidade. Este ano, com duas procissões. A primeira, já no próximo domingo, 13, a partir das 15 horas. Trata-se da procissão do Senhor dos Passos, com saída da Igreja da Misericórdia, passagens pelos largos 5 de Outubro, rua do Sporting, Rua Direita, Praça do Município, Rua Rui Faleiro, Rua Gregório Geraldes e chegada ao Calvário. Já no dia 25 de Março, Sexta-feira Santa, realiza-se, pelas 21 horas, a procissão do Enterro do Senhor, com saída da Igreja da Misericórdia e passagens pelas ruas Direita, Fernão Penteado, Azedo Gneco, Bombeiros Voluntários, Olivença, António Augusto de Aguiar, Praça do Município e retorno à Igreja da Misericórdia, onde decorrerá o sermão. A Santa Casa lembra que os percursos de mantém os estipulados, \"mais curtos e acessíveis, permitindo a mais pessoas, nomeadamente crianças e idosos, nela participem\"."
title_plus_text_2 = title_2 + ". " + text_2

# GOOD
title_3 = "D. António Luciano ordenado domingo"
text_3 = "Às 16 horas, na Sé da Guarda O novo Bispo de Viseu, D. António Luciano dos Santos Costa, é ordenado no próximo domingo, 17, pelas 16 horas, na Sé da Guarda, com o cortejo a arrancar da Igreja da Misericórdia em direcção à Sé. O ordenante será o Bispo da Guarda, D. Manuel Felício. O conhecido padre Luciano já disse que \"não esperava\" esta nomeação do Papa, no início de Maio, mas promete empenho para desempenhar o cargo da melhor forma. Mais informação na edição papel desta semana."
title_plus_text_3 = title_3 + ". " + text_3

# GOOD
title_4 = "Padre Luciano é o novo Bispo de Viseu"
text_4 = "Ordenado a 17 de Junho na Guarda António Luciano dos Santos Costa, mais conhecido na Covilhã, onde foi pároco e capelão da UBI, como padre Luciano, é o novo Bispo de Viseu, sucedendo no cargo a Ilídio Leandro, que resignou. Uma nomeação que diz, o apanhou de surpresa. \"Não estava à espera. Recebi notícia com muita surpresa, com uma grande emoção interior\" frisa. O Bispo da Guarda, D. Manuel Felício, elogia o percurso de Luciano Costa e diz que esta nomeação é também \"uma distinção\" à própria Diocese. Mais informação na edição papel desta semana."
title_plus_text_4 = title_4 + ". " + text_4

# GOOD
title_5 = "Bispo quer mais condições para vocações"
text_5 = "Dia Mundial de oração pelas vocações É preciso \"criar as condições, nas famílias, nas comunidades paroquiais e outras, e também nos ambientes da vida em sociedade, para que o discernimento vocacional possa acontecer, na vida de cada um, a começar pelas idades iniciais.\" É este o apelo deixado pelo Bispo da Guarda. D. Manuel Felício, numa altura em que se comemora o Dia Mundial de oração pelas vocações, que se celebra no próximo domingo, 22, Domingo do Bom Pastor. Uma efeméride que se assinala pela 55ª vez. Para este ano, em que se realiza, no próximo mês de Outubro, o Sínodo sobre os jovens, a Fé e o discernimento vocacional, o Papa Francisco propõe as seguintes três atitudes para todos: escutar, discernir e viver o chamamento do Senhor. \"Sobre a atitude do escutar, lembra-nos o Papa Francisco que Deus vem de forma discreta, sem se impor à nossa liberdade. Daí a redobrada atenção que cada um deve dar aos sinais discretos desta presença de Deus, que sempre interpela cada um pessoalmente para percorrer o seu caminho próprio ou seja a sua vocação\" explica D. Manuel. Já sobre a atitude do discernir, \"remete-nos para o que diz o documento preparatório do Sínodo, onde se afirma que o discernimento espiritual é um processo pelo qual cada pessoa, em diálogo com Deus e na escuta da voz do Espírito, realiza as suas opções fundamentais, a começar pela do estado de vida. Temos de reconhecer que o grande défice do percurso das pessoas em geral, a começar na idade juvenil, é a falta de ambientes e de disponibilidade pessoal, mas também de alguma ajuda externa para que esta caminhada de discernimento se faça. Parece que a vocação de cada pessoa é o que menos conta nos percursos de formação oferecidos na actualidade\" critica o Bispo da Guarda. Sobre o viver em resposta ao chamamento do Senhor, \"diz o Papa que essa é a grande urgência na vida de cada pessoa. Daí ser necessário que cada um assuma o risco de fazer escolhas, segundo a certeza de que viver é escolher. Por isso, quem escolhe bem vive bem, quem escolhe mal vive mal e quem não é capaz de assumir o risco da escolha ainda vive pior\" afirma D. Manuel. Que acrescenta que o Papa continua a dizer que \"a vocação não é algo do passado ou que se possa adiar indefinidamente para o futuro, mas de hoje. Sendo assim, cada um é chamado a ser testemunha do mesmo Senhor, quer na vida matrimonial, que no ministério ordenado, quer na vida de especial consagração.\""
title_plus_text_5 = title_5 + ". " + text_5

# BAD
title_6 = "António Cunha: uma vida pelo Covilhã"
text_6 = "António Cunha, 77 anos, foi cobrador dos serranos durante mais de quatro décadas Dez quilos. É quanto pesa a pasta em cabedal, com os dados dos sócios, a quem cobra a mensalidade. Foi com ela que percorreu quilómetros, durante quase meio século. Foi com ela na mão que se tornou uma referência do Sporting da Covilhã, clube que em Junho próximo o volta a homenagear, desta vez com atribuição do diploma de sócio de mérito. António Cunha, 77 anos, foi cobrador dos serranos até ao final de Agosto último, altura em que a vontade \"das pernas\" se sobrepôs à sua. Agora, continua a frequentar diariamente a sede, enquanto acompanha o seu sucessor na tarefa, João Salcedas. António Cunha entrou para a fábrica aos 13 anos e tornou-se depois tecelão, a profissão de toda a vida. Quando deixava para trás o barulho dos teares, ia a casa, na zona do Castelo, e saía para a cobrança. Começou no Águias de Santa Maria, esteve ao serviço no Rodrigo e passou mais tarde a trabalhar nos \"leões da serra\", de que já era sócio. Até hoje. E tenciona continuar a ajudar no que puder, \"até morrer\". (Reportagem completa na edição desta semana)"
title_plus_text_6 = title_6 + ". " + text_6

# BAD
title_7 = "O livro perdido da Covilhã"
text_7 = "Um povo que o podia ser de criadores acaba por ser uma matilha de aldrabões Eduardo Lourenço tem-nos questionado permanentemente sobre a nossa origem / condições ou inevitabilidade quiçá o nosso destino quase fatal como pessoas e País. Um destes dias fui ouvir Gabriel Magalhães que conhecia de alguns escritos e me deixou maravilhado ante a riqueza de pensamento reflectido em \"Madrugada na tua alma\". A partir desta obra realço alguns aspectos que utilizarei como termo de análise / comparação. Parafraseando sem distorcer, \"não admira que num País como o nosso, tão dado a esquecer os seus talentos, possuidores de enormes qualidades, nos deparemos amiúde com essas virtudes transformadas em defeitos\". A nossa criatividade que caracteriza esse excesso de imaginação dos portugueses \"só em Portugal podia haver um Fernando Pessoa\". Mas é pena que a criatividade, hoje, só nos serve para o nosso defeito de trafulhice. Um povo que o podia ser de criadores acaba por ser uma matilha de aldrabões. Não deixa de ser soberba a questão que se coloca: \"Já imaginaram o que seria o nosso Portugal se a energia que se aplica na vigarice se orientasse para actividades dignas?\" Para de imediato concordar com o distinto professor e (re) sublinhar o quanto este pormenor mostra como \"a nossa criatividade, que podia servir para tanta coisa boa, se está a reduzir a uma mera trafulhice do mero oportunismo.\" Em tempos não muito recuados, quando uma figura pública veio a terreiro lançar a confusão sobre a alegada orientação sexual de José Sócrates, atribuindo-lhe o gosto por outros colos, fiquei bastante indignado com essa atitude e o resultado da opinião pública eleitoral, não o foi menor. Nos alvores do Verão passado uma \"alegada caravana\" da revista Visão, e a pretexto de uma questão pessoal, se veio desse modo ofender a dignidade de Carlos Pinto, recorrendo ao nome de seu pai, de forma vil e despeitada. Manifestei-lhe de imediato a minha solidariedade e indignação pelo ato. Não gostei como é óbvio. Os ataques recentes a Carlos Casteleiro não passam de mais um desses procedimentos atávicos, onde a sua grandeza e heroicidade, é transformada em farsa e Carnaval de \"pretensos políticos a fazerem de conta que são de vistas cultas, requisitados intelectuais, e não passam de espertalhões com uma ou duas ideias eleitorais\". Termino segundo Gabriel Magalhães, \"Os verdadeiros heróis são pessoas humildes. Lúcidos. Que fazem aquilo que têm a fazer, sem dar nas vistas. A heroicidade a sério não se vê: não tem palco incluído\". \"A discrição é o terreno próprio da verdadeira valentia. Quem precisa de palmas é porque é covarde. Ou de como ser português, também tem sido isto: aprender a viver com a doença da portugalidade.\" Mas não devia ser isto, não devia…e fico triste, por isso\"."
title_plus_text_7 = title_7 + ". " + text_7

# BAD
title_8 =  "Mais de mil na UBI"
text_8 = "Os caloiros que entram na primeira fase do concurso ao Ensino Superior A Beira Interior tem mais 1845 alunos. Foi isso que ditou a primeira fase de concurso de acesso ao Ensino Superior, divulgado no passado fim-de-semana, com a Universidade da Beira Interior a ser a instituição que mais alunos recebe: 1114 novos alunos. Das 1240 vagas disponíveis na UBI, restam 126. Os cursos com mais procura foram Medicina Engenharia Aeronáutica e Ciências Farmacêuticas. Para a segunda fase, os dois cursos com mais lugares vagos são Engenharia Civil e Optometria – Ciências da Visão. Segundo a instituição, entre as quatro universidades e sete politécnicos do \"arco interior\", a UBI destaca-se por ser a que coloca mais alunos e também a que apresenta melhor percentagem de preenchimento de vagas. Quanto ao Instituto Politécnico de Castelo Branco, foram colocados 422 candidatos, não chegando a metade das 876 vagas abertas. Vários cursos, na ESA e na EST, ficaram sem estudantes colocados. No entanto, também existem cursos, como por exemplo, os da Escola Superior de Educação de Serviço Social, com as vagas colocadas a concurso completas. No Instituto Politécnico da Guarda, mais de metade das vagas ficam por ocupar. Das 676 vagas disponíveis, foram preenchidas 309. O curso de Desporto fica com 36 lugares livres e o de Contabilidade com 32. (Notícia completa na edição papel)"
title_plus_text_8 = title_8 + ". " + text_8

# BAD
title_9 = "Uma escola de música com 200 anos"
text_9 = "A Banda do Paul completa esta quinta-feira, 30, dois séculos de existência David benze-se, tira o trompete do estojo aveludado e desce, nervoso, as escadas, para a audição onde vai mostrar o que já aprendeu na Escola de Música da Banda do Paul, frequentada por 14 crianças. Uns mais descontraídos que outros, todos denotam a responsabilidade de tocar para um auditório lotado. Há quem aperte exageradamente o bocal na mão, à espera da sua vez, quem fique estático a rever a pauta, quem fique irrequieto até ser chamado. Na sala de ensaios, com as paredes forradas com caixas de ovos, para melhorar a insonorização, Santa Cecília em lugar de destaque, ao lado do quadro, e as estantes arrumadas a um canto, para dar lugar às cadeiras onde as famílias se sentam, os sons não saem ainda com fluidez, mas cada curta actuação é aplaudida efusivamente, num gesto de incentivo. As debilidades, as notas ao lado e alguns enganos são desvalorizados. O que importa, num sistema de ensino em que as crianças começam a mexer nos instrumentos ao mesmo tempo que aprendem solfejo, para não se saturarem, é acentuar a progressão já feita. \"É tão bom vê-los assim evoluir de uma audição para a outra\", incita Cidália Barata, a presidente da instituição paulense que esta quinta-feira, 30, completa 200 anos. Ao olhar para os mais novos, a dirigente, que entrou para a banda aos 11 anos para aprender trompete, vislumbra a necessária renovação e vê a escola como \"o garante\" do futuro. (Reportagem completa na edição papel)"
title_plus_text_9 = title_9 + ". " + text_9

# BAD
title_10 = "Chaló mais satisfeito com opções no plantel"
text_10 = "Técnico confia num bom campeonato Francisco Chaló, treinador do Sporting da Covilhã, da II Liga, diz que a chegada tardia de vários jogadores dificultou o seu trabalho, mas afirma sentir-se agora \"mais satisfeito\" e com matéria-prima para fazer um bom campeonato. O técnico lembra que alguns jogadores têm apenas cinco semanas de trabalho, quando o grupo começou a treinar há mais de três meses, e frisa que a falta de opções o condicionou, por exemplo na escolha do esquema táctico, por falta de avançados. \"Agora há mais opções e posso definir algumas coisas em função daquilo que tenho, e não do que me falta. Nesta altura há matéria-prima e o Francisco Chaló é um treinador mais satisfeito para desenvolver o seu trabalho, coisa que há um mês não era\", disse o treinador serrano. Os \"leões da serra\" foram eliminados na Taça da Liga e na Taça de Portugal, mas o treinador considera que o desempenho na II Liga \"até está a melhorar\" em relação ao ano passado, sublinhando o desempenho fora. A equipa tem apenas menos um ponto que na 9ª jornada da época transacta, \"mas tem mais jogos fora e estamos a apenas três pontos dos pontos conseguidos em casa do adversário em toda a primeira volta\", realça o técnico, optimista com a evolução da equipa. \"Nós acreditamos muito em nós e acho que temos crédito suficiente para acreditarmos em nós\", disse Francisco Chaló. (Artigo completo na edição papel)"
title_plus_text_10 = title_10 + ". " + text_10

titles = [title_1, title_2, title_3, title_4, title_5, title_6, title_7, title_8, title_9, title_10]
texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7, text_8, text_9, text_10]
titles_plus_texts = [title_plus_text_1, title_plus_text_2, title_plus_text_3, title_plus_text_4, title_plus_text_5, title_plus_text_6, title_plus_text_7, title_plus_text_8, title_plus_text_9, title_plus_text_10]

getThreeModelsSimilarities(title_ref=title_ref, text_ref=text_ref, title_plus_text_ref=title_plus_text_ref, titles=titles, texts=texts, titles_plus_texts=titles_plus_texts, type_name="RELIGIAO")