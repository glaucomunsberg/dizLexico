#####################################################################################################################
#                                  DizLexico - Analisador Léxico e Sintático
#####################################################################################################################
#
#   1. Introduçao
#   2. Implementação
#	3. I/0 (entrada e saida)
#   4. Execução
#   5. Resultados e Conclusão
#   6. Bibliografia
#
#   @autor Glauco Roberto M. dos Santos 
#   @autor Lúcio Leal
#	@autor Inessa Diniz Luerce
#   @github  git@github.com:glaucomunsberg/dizLexico.git
#   @version 0.5
#
#####################################################################################################################
#   1. Introduçao
#####################################################################################################################
#
#       O projeto dizLexico se propõem a realizar o trabalho de Linguagens Formais, idealizado por Prof. Luciana Foss.
#   O desenvolvimento tem como objetivo a criação um analisador que:
#           ✓ Seja capaz de analisar lexicamente um arquivo
#           	✓ Que identifique tokens dos arquivos
#           	✓ Capaz de remover comentários
#           	✓ Calcular o número de linhas e caracteres
#           ✓ Seja capaz de analisar Sintaticamente um arquivo
#				✓ Analisar a seguência de tokens e se estas estão coerentes com a linguagem definida (item 2.1)
#		Obs.: O analisador aqui está ligado apenas a fazer o processo de Análise Léxica e Análise Sintática, ficando
#	assim excluido a análise Semântica da linguagem Proposicional aqui tratata
#
#####################################################################################################################
#   2. Implementação
#####################################################################################################################
#
#       Na implementação do Projeto dizLexico optou-se por utilizar a linguagem Python e atendendo os paradigmas da
#   orientação a objeto. Trabalho este realizado Glauco Roberto M. Santos, Lúcio Leal e Inessa Luerce. Utilizando o
#	GitHub como versionador e forma de manter o código conciso e para fácil acesso aos interessados.
#
#	2.1 Linguagem Reconhecida
#		A linguagem reconhecida pelo analisador é a de Lógica Proposicional, proposta prof. Luciana Foss e mais
#	detalhado no diretório 'def' deste mesmo repositório no arquivo 'definicao_de_linguagem.pdf' e no arquivo
#	'erratas'.
#
#   2.2 Classes do Projeto
#       Foram modeladas classes que ao mesmo tempo podesse ser autoexplicativas e mais próximas possíveis das
#	entidades envolvidas em uma analisador lexico e sintático.
#		Fica assim o trabalho resumido as classes
#			✓ Principal
#			✓ AnalisadorLexico
#			✓ AnalisadorSintatico
#
#       Vejamos um pouco sobre cada uma delas abaixo e sua ação no projeto:
#           -> Principal.py
#               A classe principal está exclusivamente ligada ao processo de execução do analisador, ela exerce a
#				mesma função que teria o compilador: levantar os tokens e processar sua analise sintática;
#           -> AnalisadorLexico.py
#               Funciona com as mesmas funções que se espera de um analisador Léxico. Faz a abertura do arquivo passado
#				como parâmetro, faz a remoção de comentários, conta o número de linhas, conta o número de caracteres e
#				e faz o levantamento de tokens nos arquivo;
#           -> AnalisadorSintatico.py
#               A partir do levantamento feito pelo analisador Léxico, o analisador sintático é capaz se a estruturação
#				do arquivo é correta e atende a linguagem definida (item 2.1);
#
#	2.3 Autômatos
#		Foi impresendivel a criação de autômatos para o entendimento dos estados para reconhecimento dos tokens e para
#	a análise sintática do projeto. Para isso foi utilizado J-FLAP para o auxílio e modelagem dos autômatos.
#		Os autômatos estão disponíveis no diretório 'def/automatos' e estão classificados com o nome token* e sintatico*.
#	Sendo o primeiro referente aos tokens de reconhecimento dos lexemas do analisador léxico e sintatico referente aos
#	aos arquivos de autômatos que reconhece a seguência correta das entradas.
#
#####################################################################################################################
#   3. I/0
#####################################################################################################################
#		O programa do projeto dizLexico conta com algumas expecificações que devem ser atendidas para que seja
#	executado e acha um resultado adequado. Veja abaixo
#
#	3.1 Entrada
#		A simulação precisa de apenas uma informação de entrada que é o arquivo com as intruções. Vejamos que esse 
#	precisa estar codificado com utf-8 ou com compatibilidade a ASCII. Como exemplos, existe o diretório 'exemplos'
#	que contém 7 arquivos de exemplo para você realizar a execução.
#
#		3.1.2 Parâmetro [nome_arquivo]
#			Casos como os arquivos do diretório 'exemplos'
#
#	3.2 Saída
#		A saída do programa se resume a apenas duas possibilidades:
#			true  - Caso a análise sintática e léxica esteja correta ( mais leia 2.1);
#			false - Caso exista algum erro léxico, sintático ou de outra origem ( mais leia 3.3)
#
#	3.3 Log
#		Devido a expecificação proposta por FOSS a saída do programa não apresenta qualquer outra informação, porém
#	para maiores informações sobre como foi realizado a execução e se houve alguma ocorrência, o programa produz um
#	arquivo de log que tem o nome [ANO-MES-DIA].log
#		Consulte-o para maiores informações da execução, ele está dividido por sessões, ou seja, por execução do
#	programa.
#
#####################################################################################################################
#   4. Execução
#####################################################################################################################
#
#       Através do repositório no GitHub ( glaucomunsberg/dizLexico) é possível obter os arquivos individuais para a 
#   execução do projeto dizLexico ou até mesmo uma versão mais recente dos arquivos listado abaixo.
#   Podendo inclusive baixar e executar os arquivos do diretório 'exemplos'.
#
#   4.1 Configuração Mínima
#       ✓ Python Versão 2.7 (ou maior)
#       ✓ Arquivos Mínima
#            * Principal.py
#            * AnalisadorLexico.py
#            * AnalisadorSintatico.py
#			 * __init__.py
#            * [arquivo_tratavel] (mais leia 3.1)
#		Obs.: O projeto está compatível com Linux, não foi realisados testes de retrocompatibilidade com comandos
#				específicos de outros Sistemas Operacionais
#
#	4.2 Execução do dizLexico
#           Antes de simular no terminal, deve-se garantir que está conforme a item 3.1. Para simular no terminal
#               $ python Principal.py [nome_arquivo]
#
#     4.2.1 Exemplo:
#           Abaixo está o comando para execução do exemplo com o arquivo mais simples e o mais complexo respetivamente:
#
#               $ python Principal.py exmeplos/exemplo_1.txt
#				$ python Principal.py exemplos/exemplo_7.txt
#
#####################################################################################################################
# 5. Resultados e Conclusão
#####################################################################################################################
#
#       Os resultados obtidos nas execuçõe com os arquivos padrões disponíveis por FOSS, levantam corretamente os
#	lexemas e retornam 'true' como resposta. O que se acredita que faz o dizLexico estar dentro do esperado.
#
#	5.1 Erros e questionamentos levantados
#		Durante a implementação foram levantados questionamentos e o histórico destes e suas soluções estão disponíveis
#		no endereço https://github.com/glaucomunsberg/dizLexico/issues?state=closed
#
#####################################################################################################################
# 6.Bibliografia
#####################################################################################################################
#
#   FOSS, Luciana. Definição da Linguagem. [online] Disponível na Internet via WWW. URL:
#		'http://avainstitucional.ufpel.edu.br/file.php/282/definicao_da_linguagem.pdf'. Em 28/02/2013
#	SEBESTA,Robert W. Conceitos de Linguagens de Programacao. [online] Disponível na Internet via WWW. URL:
#		'http://books.google.com.br/books/?id=b0tcn_uPLoAC&redir_esc=y'. Em 28/02/2013
#
#####################################################################################################################