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
        self.__expressaoRegular = re.compile("[*0-9a-z,\"-.(){}=+;' *]")
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
        inserir = {'lexema':processado,'token':'false'}
        self.__processados.append(inserir)
        print 'criado:',inserir
        
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
        