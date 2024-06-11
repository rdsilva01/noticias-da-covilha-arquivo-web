from getEmbeddingsAndSimilarity import getThreeModelsSimilarities

#############
#############
## CULTURA ##
#############
#############
title_ref = "Chocalhos espera movimentar um milhão"
text_ref = "Festival da Transumância decorre entre sexta-feira e domingo Cerca de um milhão de euros deve mudar de mãos durante os três dias do festival Chocalhos, em Alpedrinha, Fundão, prevê a organização de uma das maiores festas da Beira Interior e que decorre este ano entre 16 a 18 de Setembro. As casas das principais artérias da vila transformam-se em tasquinhas, bares, restaurantes e lojas de artesanato, lado a lado com actividades ligadas à pastorícia e animação de rua permanente, até de madrugada. Basta contar os carros nos parques de estacionamento criados para o evento e a lotação dos autocarros, para concluir que nos últimos anos o Chocalhos tem atraído 30 mil visitantes a Alpedrinha, diz o vice-presidente da Câmara do Fundão, Paulo Fernandes. Contas feitas, o autarca calcula que haja pelo menos 15 mil famílias a fazer um consumo médio de 25 euros e que haja alguns milhares de pessoas em alojamentos a rondar os 100 euros para o período da festa. Segundo Paulo Fernandes, \"as unidades hoteleiras já estão lotadas\" no concelho para o fim-de-semana dos Chocalhos e há \"muitos alojamentos informais. Acho que em Alpedrinha não há quarto, sala ou chão que não tenha clientes nestes dias\". O festival decorre desde 2002 e para este ano prevêem-se números recorde de participação de artesãos e produtores, que devem chegar aos 100 (e pagam entre 25 a 130 euros cada para estarem presentes), e cerca de 30 grupos de animação. Ao mesmo tempo, a organização (Câmara do Fundão, empresa municipal de turismo e Junta de Freguesia de Alpedrinha) aposta no reforço das actividades ligadas à pastorícia e transumância, que estão na génese do evento. O programa inclui oficinas da lã e de instrumentos musicais pastoris, assim como um passeio e mostra de cães da Serra da Estrela, assim como de ovelhas. A organização dos Chocalhos sensibiliza ainda os estabelecimentos participantes a venderem produtos (tais como vinhos, queijos e doçaria) da região, para que o certame possa também servir de montra para o que de melhor existe no concelho. Existe mesmo uma norma no regulamento \"que obriga a que o vinho Alpedrinha, da Adega do Fundão, seja um dos que esteja à venda\". Táxis para transportar gente Este ano, além dos autocarros que asseguram o transporte entre os parques de estacionamento e zona histórica de Alpedrinha, onde decorre o festival, haverá táxis \"para necessidades pontuais de transporte\" durante a noite, revelou Paulo Fernandes. Mantém-se também a ligação de autocarro entre Alpedrinha e o Fundão, mas este ano cada viagem vai custar um euro. O festival Chocalhos custa cerca de 30 mil euros e é co-financiado a 70 por cento pelo Provere - Programa de Valorização Económica de Recursos Endógenos, sendo os restantes 30 por cento assegurados por receitas próprias, graças a patrocinadores e serviços prestados, nomeadamente com o valor pago por cada produtor participante. Segundo Paulo Fernandes, o co-financiamento está assegurado para as próximas três edições do certame, mas o objectivo é que, \"entretanto, as receitas próprias possam crescer, para que o festival se torne auto-suficiente\". Mais informações sobre o festival estão disponíveis em www.fundaoturismo.pt."
title_plus_text_ref = title_ref + ". " + text_ref

# GOOD
title_1 = "Jovens criadores mostram-se"
text_1 = "Em festival da Quarta Parede Teatro, performance e dança, com a multimédia como suporte, são a essência dos espectáculos escolhidos para a edição deste ano do 1ª Andar – Mostra de Criadores Emergentes, promovida pela associação de artes performativas Quarta Parede nos dias 29 e 30 de Novembro. As quatro criações, seleccionadas de um conjunto de 23 candidaturas, repartem-se entre a Covilhã e Castelo Branco, em sessões duplas. Raquel André e Tiago Cadete, com a peça \"No Digital\", sobem ao palco do Teatro das Beiras no dia 29, às 21h30. Segue-se, uma hora depois, a apresentação de Raquel Castro, \"Os Dias São Connosco\", uma performance autobiográfica que retrata a experiência de uma jovem mãe. Um dia depois é a vez do Cine Teatro Avenida acolher a espanhola Carolina Fernández com a performance multimédia \"Ni Príncipes Ni Hóstias\", em torno das questões do género, às 21h30, e pouco depois o \"Corpo (I)lógico\" de Anaísa Lopes, espectáculo de dança. Rui Sena, director artístico da Quarta Parede, destaca a qualidade das candidaturas, que torna cada vez mais difícil escolher apenas quatro. \"Implica uma maior observação e uma maior exigência\". (Peça completa na edição papel)"
title_plus_text_1 = title_1 + ". " + text_1

# GOOD
title_2 = "ASTA leva teatro às escolas"
text_2 = "Projecto no Teixoso A ASTA (Associação de Teatro e Outras Artes), em cooperação com o Agrupamento de Escolas do Teixoso, realiza a partir de segunda-feira, 20, o EnsinArte- I Mostra de Teatro Escolar do distrito de Castelo Branco. Este é, segundo a ASTA, um projecto inovador de formação, reflexão e mostra de trabalhos artísticos realizados em contexto escolar que pretende apresentar diversos trabalhos na área das artes de palco junto das escolas da região, \"captando a atenção e estimulando a criação artística de jovens\". O festival irá decorrer na Escola Básica do Teixoso e englobará a realização de workshops, um ciclo de conferências subordinadas à importância do teatro no currículo escolar e uma mostra de espectáculos de diversos grupos de teatros nas escolas. A primeira peça é do Grupo de Teatro da Escola Faria de Vasconcelos, esta segunda-feira, 20, pelas 15 horas. Seguem-se até dia 25 mais 11 representações de escolas de Castelo Branco, Vila Velha de Ródão, Teixoso, Covilhã e Fundão."
title_plus_text_2 = title_2 + ". " + text_2

# GOOD
title_3 = "Falta de dinheiro encurta ciclo de teatro universitário"
text_3 = "De 17 a 27 de Março, na Covilhã Um festival com menos dias, mas com mais espectáculos de companhias profissionais fruto da colaboração com a ASTA. Será assim este ano o 15º Ciclo de Teatro Universitário da Covilhã, organizado pelo Teatr'UBI, que decorre entre 17 e 27 de Março, no Teatro-Cine da Covilhã, sempre com espectáculos às 21 horas e 30. \"Reduzimos os dias do festival devido às dificuldades financeiras. E apostámos mais nos espectáculos com a ASTA para reduzir custos. Mas continuaremos a ter uma marcante presença espanhola e haverá algumas novidades, como aulas de dança universitárias espanholas\" afirma Rui Pires, presidente do Teatr'UBI, que lamenta mais uma vez a falta de apoios, embora este ano, para além da tradicional ajuda da Fundação Calouste Gulbenkian, conte com o apoio extra do BPI, \"com o qual não contávamos\", fruto de um protocolo com a UBI. Quanto à Câmara da Covilhã, dá apoio logístico e técnico, e cede as instalações. Rui Pires volta a lamentar que o teatro não seja valorizado pela UBI em termos educacionais, ao contrário do que fazem as universidades em Espanha, mas diz que apesar de tudo, desde que João Queiroz assumiu a Reitoria a colaboração \"tem sido diferente. Se calhar, há mais atenção ao que fazemos, mas gostava que ainda houvesse mais abertura\" deseja, lembrando que o Teatr'UBI também acaba por levar o nome da UBI além fronteiras. O orçamento para este ano é de 13 mil euros. Já Sérgio Novo, da ASTA, diz que a colaboração tem saldo positivo. \"Acreditamos nesta parceria\" assegura, lembrando que o ciclo universitário covilhanense é \"o único a nível nacional\" que se mantém desde o seu arranque, há 15 anos, e para as companhias profissionais que participam também acaba por ser bom devido à \"troca de experiências\" que se ganham. Quanto ao programa tem para dos dias 17 e 18 a nova peça conjunta do Teatr'UBI e ASTA intitulada \"Son(h)o dor-mente\". Dia 19, o Grupo de Teatro da Faculdade de Ciências da Universidade de Lisboa apresenta \"2º esquerdo\". Dia 20 a vez o Grupo de Teatro Académico de Leiria levar ao palco \"As criadas\" e no dia 21, a primeira presença espanhola na Covilhã. O Grupo de Teatro de Santander apresenta \"Centenas de pássaros impedem-te de andar\". Dia 22, a ASTA apresenta \"Passagem de nível\" e no dia seguinte \"Dia de ilusão\". Dia 24 a vez do Centro de Difusão Cultural de Sintra mostrar \"Sopa da pedra\". Dia 25 os espanhóis da Aula de Dança da Universidade da Corunha leva à cena \"Rede na rede\", enquanto que às 22 horas e 10 um grupo da Universidade de Santiago de Compostela apresenta \"Empatia\". Dia 26 os \"Maricastaña\", de Ourense, mostram \"Leve\"e dia 27 o Ciclo fecha com \"Marca'dor\", uma produção conjunta de ASTA e Teatr'UBI."
title_plus_text_3 = title_3 + ". " + text_3

# GOOD
title_4 = "Boom é o festival mais ecológico da Europa"
text_4 = "European Festival Awards atribui prémio O Festival Boom venceu o prémio de festival mais ecológico da Europa, atribuído no âmbito dos European Festival Awards. Os resultados foram anunciados em Groningen, na Holanda, onde decorreu a 12.ª edição da cerimónia. O festival que acontece de dois em dois anos no concelho de Idanha-a-Nova foi o único evento português nomeado para estes prémios, competindo na sua categoria com os festivais de Roskilde (Dinamarca) e Øya (Noruega). A utilização de casas de banho que dispensam o uso de água, o aproveitamento do sol para a produção de energia ou a recolha e uso de óleo alimentar usado para fazer funcionar os geradores do festival são algumas das soluções ecológicas adoptadas nas últimas edições. Esta é mais uma distinção para este festival de música e cultura alternativa, que nos últimos anos conquistou outros prémios como o Greener Festival Award Outstanding de 2008 e 2010. Além disso foi convidado pela ONU para fazer parte da United Nations Music & Environment Stakeholder Initiative. A última edição do Festival Boom decorreu em Agosto do ano passado."
title_plus_text_4 = title_4 + ". " + text_4

# GOOD
title_5 = "Festival Sefardita de regresso"
text_5 = "Começa domingo com um mercado kosher em Belmonte O II Festival Internacional da Memória Sefardita, a realizar entre 18 e 21 de Setembro na Serra da Estrela, vai destacar dois portugueses que, em 1940, salvaram mais de mil judeus, na Hungria, anunciou na passada segunda-feira, 5, a organização, em Trancoso. Durante o evento, a realizar nos concelhos de Guarda, Trancoso e Belmonte, será abordada a acção do embaixador Carlos Sampayo e do secretário Alberto Branquinho, na Hungria, durante a II Guerra Mundial, diz Jorge Patrão, presidente da Entidade de Turismo Serra da Estrela. Os dois portugueses \"levaram a cabo uma acção que salvou mais de mil judeus, nos anos de 1940\", referiu aquele responsável, na conferência de imprensa de apresentação do encontro que irá congregar comunidades judaicas oriundas da Península Ibérica e que se encontram espalhadas pelo mundo. O papel de Sampayo Garrido e de Alberto Branquinho será lembrado na Guarda, no dia 19, durante uma conferência sobre \"Os justos portugueses da II Guerra Mundial\", a realizar no Teatro Municipal, com a presença de familiares. No dia seguinte, em Trancoso, será discutida a obra de resgate do capitão Barros Basto, que no princípio do século XX iniciou \"uma acção para recuperar a identidade judaica portuguesa\", referiu Jorge Patrão. \"Essa história vai ser contada pela neta Isabel Lopes\", indica, salientando ainda a realização de uma exposição do espólio daquele militar, no Convento dos Frades. A organização também destaca a estreia do filme \"O Cônsul de Bordéus\", dedicado a Aristides de Sousa Mendes, do realizador Francisco Manso, que será exibido a 19, no Teatro Municipal da Guarda. \"Este filme vai ser algo importante e estamos a tentar que tenha uma dobragem em Hollywood, para que tenha uma distribuição mundial\", refere. O II Festival Internacional da Memória Sefardita também inclui um concerto da cantora Mor Karbasi, no dia 18, na Guarda. Segundo o presidente da Entidade de Turismo da Serra da Estrela, a cantora \"é do mais prestigiado que há a nível internacional e mesmo uma referência em Israel, embora viva em Londres\". Mor Karbasi irá interpretar temas em português arcaico e ladino \"uma língua que já não é falada há mais de 500 anos\", observa. Durante os trabalhos, que irão contar com participantes nacionais e estrangeiros, a organização também fará a apresentação pública da Rede Nacional de Judiarias e promove, em Belmonte, um mercado de produtos kosher (destinados à comunidade judaica). Jorge Patrão indica que o secretário de Estado da Cultura, Francisco José Viegas, marcará presença no festival que pretende \"divulgar a recuperação da identidade histórica de muitas das cidades e vilas da Serra da Estrela\", onde já foram identificadas \"mais de 500 marcas cruciformes\" associadas à cultura judaica."
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
title_9 = "Nada Catita este árbitro"
text_9 = "Covilhã perde em casa com o Estoril prejudicado pelo árbitro O Sporting da Covilhã voltou no último domingo a cair na zona de despromoção, após o jogo em casa com o Estoril, em que nenhum dos emblemas fez em campo o suficiente para vencer o jogo. A intervenção do árbitro, Luís Catita, resolveu no entanto o impasse, assinalando um penálti muito contestado contra os Leões da Serra aos 81 minutos e não marcando uma grande penalidade clara na área contrária, quando Lameirão cortou um remate com a mão. Os dois lances marcaram uma partida em que o árbitro foi o protagonista. Até ao final do jogo, a indignação foi subindo de tom nas bancadas, com muito apupos dirigidos a Luís Catita. Já após o apito final, e ao contrário do que é habitual, os adeptos serranos não arredaram pé até a equipa de arbitragem entrar no túnel de acesso, sob um coro de protestos e o estádio a gritar em uníssono \"gatuno, gatuno\". Numa altura em que as imediações do Complexo Desportivo da Covilhã já estavam desertas, apenas com dirigentes, e sem nenhuma ameaça aparente, o trio de arbitragem fez entrar a sua viatura dentro do estádio, até junto à porta, para daí seguir viagem. Só uma ocasião de golo na primeira parte Até aos lances da polémica, a partida tinha sido morna, sem nenhuma das equipas a evidenciar-se e as aproximações à baliza a não revelarem grande perigo. Mesmo disciplinarmente, só foram mostrados dois cartões amarelos, o primeiro ao forasteiro Erick aos 76 minutos e o segundo aos 81, a Wagnão. A primeira parte foi marcada pelo equilíbrio, com apenas uma ocasião flagrante de golo, criada pelos estorilistas, aos 28 minutos, quando Vinícius Reche rematou de fora da área, com o guardião Serginho a não agarrar à primeira e, na recarga, Alex Afonso atirou por cima, sem conseguir emendar. Mas foram os serranos foram os primeiros a fazerem pontaria à baliza adversária, por intermédio de Flávio, que rematou de longe, muito por cima. Rincón, aos 15 minutos, com Amessan ao lado, podia ter feito melhor, só que optou por rodopiar e atirar frouxo à figura. Ao minuto 40, Fofana ganhou a bola a Steven Vitória, isolou-se só que foi lento no remate e deixou-se antecipar à entrada da área, e, no minuto seguinte, Fofana, com um remate muito denunciado, permitiu a Vagner uma defesa fácil. O técnico, João Pinto, voltou a adoptar o 5x4x1, convertível num 3x5x2 quando a equipa atacava, mas ao Sporting da Covilhã faltava velocidade no ataque, rapidez na concretização e um maior acompanhamento das jogadas por parte dos médios, que a maioria das vezes chegavam atrasados. O Estoril, também a jogar com três centrais, bem organizado defensivamente, carecia de atrevimento no sector mais avançado. Penálti evidente por assinalar Com o regresso da chuva e o terreno mais molhado, os Leões da Serra foram os primeiros a assustar, através de um cabeceamento ao lado do poste de Fofana, a dar seguimento a um cruzamento de Ivo Pinto. O lateral, com indicação para subir no terreno, executou vários cruzamentos largos para a área, mas ninguém respondia à solicitação no segundo poste. Ao minuto 81 aconteceu o primeiro caso do jogo, quando o árbitro, Luís Catita, assinalou uma suposta falta cometida por Wagnão, central serrano. Jefferson rematou, Wagnão interceptou, na recarga o serrano alivia a bola mas Jefferson parece tocar o esférico instantes antes, embora seja difícil avaliar. Luís Catita estava de frente para o lance, assinalou penálti e, na conversão do castigo máximo, Vinicius Reche atirou rasteiro para o único golo da partida. Volvidos dois minutos, na área contrária, Lameirão cortou com o braço uma bola bombeada que ficaria à disposição de Amessan, mas nem Luís Catita nem nenhum dos seus assistentes assinalou a infracção. Severino, entrado para o lugar de Fofana, e o estreante Amien, ainda tentaram a igualdade, mas estava fixado o resultado final."
title_plus_text_9 = title_9 + ". " + text_9

# BAD
title_10 = "Chaló mais satisfeito com opções no plantel"
text_10 = "Técnico confia num bom campeonato Francisco Chaló, treinador do Sporting da Covilhã, da II Liga, diz que a chegada tardia de vários jogadores dificultou o seu trabalho, mas afirma sentir-se agora \"mais satisfeito\" e com matéria-prima para fazer um bom campeonato. O técnico lembra que alguns jogadores têm apenas cinco semanas de trabalho, quando o grupo começou a treinar há mais de três meses, e frisa que a falta de opções o condicionou, por exemplo na escolha do esquema táctico, por falta de avançados. \"Agora há mais opções e posso definir algumas coisas em função daquilo que tenho, e não do que me falta. Nesta altura há matéria-prima e o Francisco Chaló é um treinador mais satisfeito para desenvolver o seu trabalho, coisa que há um mês não era\", disse o treinador serrano. Os \"leões da serra\" foram eliminados na Taça da Liga e na Taça de Portugal, mas o treinador considera que o desempenho na II Liga \"até está a melhorar\" em relação ao ano passado, sublinhando o desempenho fora. A equipa tem apenas menos um ponto que na 9ª jornada da época transacta, \"mas tem mais jogos fora e estamos a apenas três pontos dos pontos conseguidos em casa do adversário em toda a primeira volta\", realça o técnico, optimista com a evolução da equipa. \"Nós acreditamos muito em nós e acho que temos crédito suficiente para acreditarmos em nós\", disse Francisco Chaló. (Artigo completo na edição papel)"
title_plus_text_10 = title_10 + ". " + text_10

titles = [title_1, title_2, title_3, title_4, title_5, title_6, title_7, title_8, title_9, title_10]
texts = [text_1, text_2, text_3, text_4, text_5, text_6, text_7, text_8, text_9, text_10]
titles_plus_texts = [title_plus_text_1, title_plus_text_2, title_plus_text_3, title_plus_text_4, title_plus_text_5, title_plus_text_6, title_plus_text_7, title_plus_text_8, title_plus_text_9, title_plus_text_10]

getThreeModelsSimilarities(title_ref=title_ref, text_ref=text_ref, title_plus_text_ref=title_plus_text_ref, titles=titles, texts=texts, titles_plus_texts=titles_plus_texts, type_name="CULTURA")