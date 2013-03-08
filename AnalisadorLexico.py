#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re, exceptions
from Arquivo import arquivo

class AnalisadorLexico:
    log = None
    arquivoNome = None
    file = None
    dicionarioDeLexemas = None
    arquivoLinhas = None
    arquivoCaracteres = None
    arquivoNumLinhas = None
    arquivoNumCaracteries = None
    arquivoTemp = None
    
    # Init
    #    Contrutor básico do analizador Léxico
    #    Abre o arquivo principal, contas as linas
    #    e prepara o léxico para as próximas operações
    #    básicas.
    #
    def __init__(self,nome_arquivo,log_m = None):
        self.arquivoNome = nome_arquivo
        self.log = log_m
        try:
            self.file = open(self.arquivoNome, 'r')
            self.arquivoTemp = open('temp.txt','w')
            self.arquivoCaracteres = list()
            self.arquivoLinhas = []
            self.arquivoNumLinhas = 0
            for line in self.file:
                self.arquivoLinhas.append( line )
                self.arquivoNumLinhas += 1
        except:
            print "Erro na abertura e leitura do arquivo:",sys.exc_info()
    #
    # Num_linhas
    #    @return: apenas o número de linhas do arquivo original
    #
    def num_linhas(self):
        return self.arquivoNumLinhas
    #
    # Remover_comentarios
    #    Método que remove os comentários e cria um arquivo
    #    temporário que não contém os comentários.
    #    @return: Número delinhas que haviam comentários
    #
    def remover_comentarios(self):
        numComentarios = 0;
        for line in self.arquivoLinhas:
            lista = list(line)
            try:
                comeco = lista.index('#')
                line = line[:comeco] + line[len(lista)-1:]
                if comeco == 0:
                    line = '\n'
                numComentarios+=1;
            except ValueError:
                None
            self.arquivoTemp.write(line)
        self.arquivoTemp.close()
        self.arquivoTemp = open('temp.txt','r')
        return numComentarios
                      
    #
    # GetLinhas
    #    Esse é o método pela qual se chama linha específica
    #    do arquivo temp.txt, que contem o arquivo limpo.
    #    @return: Retorna o conteúdo da linha ou None
    #
    def getLinha(self,num_linha = None):
        if(num_linha > 0):
            if num_linha <= self.arquivoNumLinhas:
                return self.arquivoLinhas[num_linha-1]
            else:
                self.log.message(self, 'A linha não existe no arquivo.\n')
                return None
        else:
            return None
    #
    # Num_caracteries
    #    Pega do arquivo .temp.txt o número de
    #    caracteries válidos que há nele.
    #    @return: Número de cararecteries
    def num_caracteries(self):
        temp = open('temp.txt','U').read().splitlines()
        for linha in temp:
            for caract in linha:
                self.arquivoCaracteres.insert(0, caract)
        self.arquivoNumCaracteries = len(self.arquivoCaracteres)
        self.arquivoCaracteres.reverse()
        return self.arquivoNumCaracteries
    #
    # Lexemador
    #    Método que cria a partir do temp.txt os
    #    lexemas e o token a qual ele pertece.
    #    @return: Númerode lexemas processados
    #
    def criarLexemas(self):
        lexemas = QualLexema(self.arquivoTemp, self.log, self.arquivoCaracteres)
        lexemas.levantarLexemas()
    
    #
    # Close
    #    Método que finaliza a execução e fecha os
    #    os arquivos.
    #
    def close(self):
        os.remove('temp.txt')
        self.arquivoTemp.close()
        self.file.close()
       
#
# QualLexema
#    Classe que processa organizamente o temp.txt
#
class QualLexema:
    __arquivo               = None
    __processados           = None
    __processou             = None
    __log                   = None
    __arquivoCaracteres     = None
    __arquivoNumCaracteres  = None
    __caracterAtual         = None
    __expressaoRegular      = None
    def __init__(self,Arquivo,Log,arquivoCaracteres):
        self.__arquivo              = Arquivo
        self.__processados          = list()
        self.__log                  = Log
        self.__processou            = None
        self.__arquivoCaracteres    = arquivoCaracteres
        self.__caracterAtual        = -1
        self.__arquivoNumCaracteres = len(arquivoCaracteres)
        self.__expressaoRegular     = re.compile("[*0-9a-z,\"-.(){}=+;' *]")
    #  
    # GetProximoCaracter
    #    retorna o próximo caracterie até que não
    #    não haja mais caracteres
    #    @return: caracter ou None (final)
    #
    def getProximoCaracter(self):
        if self.__caracterAtual+1 < self.__arquivoNumCaracteres:
            self.__caracterAtual+=1
            return self.__arquivoCaracteres[self.__caracterAtual]
        else:
            return None
    #
    # isValido
    #    Método que retorna se o caracter é válido na linguagem
    #
    def isValido(self,caracter):
        self.__expressaoRegular = re.compile("[*0-9a-zV,\"-.(){}=+;<>^' *:*]")
        if self.__expressaoRegular.search(caracter):
            return 1
        else:
            return 0
        
    #
    # LevantarLexemas
    #    método pelo qual levanta todos os lexemas
    #    e tokens contidas no programa
    #
    def levantarLexemas(self):
        caracter = self.getProximoCaracter()
        while( caracter != None):
            try:
                self.q0(caracter)
            except Exception,e:
                print e
                break
            caracter = self.getProximoCaracter()
        else:
            print 'Final do arquivo'
    
    def q0(self,caracter):
        if self.isValido(caracter):
            if caracter == '"':
                self.q1(caracter)
            elif caracter == '0':
                self.q2(caracter)
            elif caracter == '1':
                self.q13(caracter)
            elif caracter == 'V':
                self.q31(caracter)
            elif caracter == '^':
                self.q33(caracter)
            elif caracter == '\'':
                self.q32(caracter)
            elif caracter == '-':
                self.q34(caracter)
            elif caracter == '<':
                self.q36(caracter)
            elif caracter == ':':
                self.q43(caracter)
            elif caracter == ';':
                self.q39(caracter)
            elif caracter == '}':
                self.q46(caracter)
            elif caracter == '{':
                self.q47(caracter)
            elif caracter == '(':
                self.q40(caracter)
            elif caracter == ')':
                self.q42(caracter)
            elif caracter == ' ':
                exit
            else:
                raise Exception, "10 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q0 com "+caracter+" não é valido!"
            
    def q1(self,processado):
        
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'f':
                self.q25(processado+caracter)
            elif caracter == 'v':
                self.q15(processado+caracter)
            elif caracter == 't':
                self.q14(processado+caracter)
            else:
                raise Exception, "q1 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q1 com "+caracter+" não é valido!"
    #
    # FINAL
    #     false_logico
    #    
    def q2(self,processado):
        inserir = {'lexema':processado,'token':'false', 'token_tipo':'logico'}
        self.__processados.append(inserir)
        print 'criado:',inserir
        
    #
    # FINAL
    #     true_logico
    #
    def q13(self,processado):
        inserir = {'lexema':processado,'token':'true','token_tipo':'logico'}
        self.__processados.append(inserir)
        print 'criado:',inserir

    def q14(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q41(processado+caracter)
            else:
               raise Exception, "q14 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q14 com "+caracter+" não é valido!"
         
    def q15(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q16(processado+caracter)
            elif caracter == '"':
                self.q13(processado+caracter)
            else:
                raise Exception, "q15 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q15 com "+caracter+" não é valido!"
      
    def q16(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q17(processado+caracter)
            else:
               raise Exception, "q16 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q16 com "+caracter+" não é valido!"
        
    def q17(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'd':
                self.q18(processado+caracter)
            else:
               raise Exception, "q17 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q17 com "+caracter+" não é valido!"

    def q18(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'a':
                self.q19(processado+caracter)
            else:
               raise Exception, "q18 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q18 com "+caracter+" não é valido!"               

    def q19(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'd':
                self.q20(processado+caracter)
            else:
               raise Exception, "q19 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q19 com "+caracter+" não é valido!"               
    
    def q20(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q21(processado+caracter)
            else:
               raise Exception, "q20 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q20 com "+caracter+" não é valido!"               
    
    def q21(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'i':
                self.q22(processado+caracter)
            else:
               raise Exception, "q21 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q21 com "+caracter+" não é valido!"               
    
    def q22(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q23(processado+caracter)
            else:
               raise Exception, "q22 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q22 com "+caracter+" não é valido!"               

    def q23(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'o':
                self.q24(processado+caracter)
            else:
               raise Exception, "q23 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q23 com "+caracter+" não é valido!"               

    def q24(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q13(processado+caracter)
            else:
               raise Exception, "q24 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q24 com "+caracter+" não é valido!"               
    
    def q25(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '\"':
                self.q2(processado+caracter)
            elif caracter == 'a':
                self.q26(processado+caracter)
            else:
                raise Exception, "q25 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q25 com "+caracter+" não é valido!"
        
    def q26(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'l':
                self.q27(processado+caracter)
            else:
                raise Exception, "q26 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q26 com "+caracter+" não é valido!"

    def q27(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 's':
                self.q28(processado+caracter)
            else:
                raise Exception, "q27 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q27 com "+caracter+" não é valido!"

    def q28(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'o':
                self.q29(processado+caracter)
            elif caracter == 'e':
                self.q29(processado+caracter)
            else:
                raise Exception, "q28 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q28 com "+caracter+" não é valido!"

    def q29(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q2(processado+caracter)
            else:
                raise Exception, "q29 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q29 com "+caracter+" não é valido!"
    #
    # FINAL
    #     operador_ou
    #    
    def q31(self,processado):
        inserir = {'lexema':processado,'token':'ou','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir

    #
    # FINAL
    #     operador_e
    #    
    def q32(self,processado):
        inserir = {'lexema':processado,'token':'negacao','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir
                        
    #
    # FINAL
    #     operador_e
    #    
    def q33(self,processado):
        inserir = {'lexema':processado,'token':'e','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir

    def q34(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '>':
                self.q35(processado+caracter)
            else:
               raise Exception, "q34 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q34 com "+caracter+" não é valido!"

    #
    # FINAL
    #     operador_condicional
    #    
    def q35(self,processado):
        inserir = {'lexema':processado,'token':'condicional','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir
        
    def q36(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '-':
                self.q37(processado+caracter)
            else:
               raise Exception, "q36 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q36 com "+caracter+" não é valido!"

    def q37(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '>':
                self.q38(processado+caracter)
            else:
               raise Exception, "q37 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q37 com "+caracter+" não é valido!"

    #
    # FINAL
    #     operador_bicondicional
    #    
    def q38(self,processado):
        inserir = {'lexema':processado,'token':'bicondicional','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir
    
    #
    # FINAL
    #     operador_bicondicional
    #    
    def q39(self,processado):
        inserir = {'lexema':processado,'token':'fim_comando','tipo_token':'fim_comando'}
        self.__processados.append(inserir)
        print 'criado:',inserir
    #
    # FINAL
    #     inicio_expressao
    #    
    def q40(self,processado):
        inserir = {'lexema':processado,'token':'inicio','tipo_token':'expressao' }
        self.__processados.append(inserir)
        print 'criado:',inserir
                        
    def q41(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'u':
                self.q45(processado+caracter)
            else:
               raise Exception, "q41 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q41 com "+caracter+" não é valido!"

    #
    # FINAL
    #     fim_expressao
    #    
    def q42(self,processado):
        inserir = {'lexema':processado,'token':'fim','tipo_token':'expressao' }
        self.__processados.append(inserir)
        print 'criado:',inserir
        
    def q43(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '=':
                self.q45(processado+caracter)
            else:
               raise Exception, "q41 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q41 com "+caracter+" não é valido!"
    #
    # FINAL
    #     operador_atribuicao
    #    
    def q44(self,processado):
        inserir = {'lexema':processado,'token':'atribuicao','tipo_token':'operador'}
        self.__processados.append(inserir)
        print 'criado:',inserir      

    def q45(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q48(processado+caracter)
            else:
               raise Exception, "q45 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q45 com "+caracter+" não é valido!"

    #
    # FINAL
    #     fim_bloco
    #    
    def q46(self,processado):
        inserir = {'lexema':processado,'token':'fim','tipo_token':'bloco' }
        self.__processados.append(inserir)
        print 'criado:',inserir

    #
    # FINAL
    #     inicio_bloco
    #    
    def q47(self,processado):
        inserir = {'lexema':processado,'token':'inicio','tipo_token':'bloco' }
        self.__processados.append(inserir)
        print 'criado:',inserir
                
    def q48(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q13(processado+caracter)
            else:
               raise Exception, "q48 com "+caracter+". Oops! Não sei o que fazer"
        else:
            raise Exception, "q48 com "+caracter+" não é valido!"    

    #
    # RetonraListaProcessados
    #    Retonar uma lista de dicionários que contém
    #    cada um dos lexemas e seus tokens
    #    @return: list(dict['lexema'=>'token'],...,dict['lexema'=>'token'])
    #
    def retornaListaProcessados(self):
        if(self.__processados):
            return self.__processado
        else:
            return self.__processados
        