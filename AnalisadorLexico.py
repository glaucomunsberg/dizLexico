#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os, re
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
    def lexemador(self):
        self.listaLexemas = list()
        self.listaLexemaTipo = list()
        lexemas = QualLexema(self.arquivoTemp, self.log, self.arquivoCaracteres)
        caracterResgatado = lexemas.getProximoCaracter()
        while(caracterResgatado != None):
            print 'Caracter: ', caracterResgatado
            caracterResgatado = lexemas.getProximoCaracter()
        else:
            print 'Final'
    
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
    __arquivo           = None
    __processados       = None
    __processou         = None
    __log               = None
    __arquivoCaracteres = None
    __arquivoNumCaracteres = None
    __caracterAtual     = None
    def __init__(self,Arquivo,Log,arquivoCaracteres):
        self.__arquivo              = Arquivo
        self.__processados          = list()
        self.__log                  = Log
        self.__processou            = None
        self.__arquivoCaracteres    = arquivoCaracteres
        self.__caracterAtual        = -1
        self.__arquivoNumCaracteres = len(arquivoCaracteres)
    #  
    # GetProximoCaracter
    #    retorna o próximo caracterie até que não
    #    não haja mais caracteres
    #    @return: caracter ou None (final)
    #
    def getProximoCaracter(self):
        if self.__caracterAtual <= self.__arquivoNumCaracteres:
            self.__caracterAtual+=1
            return self.__arquivoCaracteres[self.__caracterAtual]
        else:
            return None
    
    def q0(self):
        caracter = self.getProximoCaracter()
        if caracter == '"':
            self.q1(caracter)
        elif re.search('[2-9]', caracter):
            self.q42(caracter)
        elif ('a','b','c','d','g','h','j','l','m','n','p','q','r','s','t','u','w','x','y','w').index(caracter):
            self.q45(caracter)
        elif re.search('[A-Z]', caracter):
            self.q45(caracter)
        elif caracter == 'i':
            self.q3(caracter)
        elif caracter == 'o':
            self.q6(caracter)
        elif caracter == 'e':
            self.q9(caracter)
        elif caracter == 'f':
            self.q25(caracter)
        elif caracter == 'v':
            self.q15(caracter)
        elif caracter == 'V':
            self.q31(caracter)
        elif caracter == '1':
            self.q13(caracter)
        elif caracter == '+':
            self.q40(caracter)
        elif caracter == '0':
            self.q14(caracter)
        elif caracter == '-':
            self.q34(caracter)
        elif caracter == '\'':
            self.q32(caracter)
        elif caracter == '^':
            self.q33(caracter)
        elif caracter == '<':
            self.q36(caracter)
        elif caracter == ';':
            self.q39
        elif caracter == '=':
            self.q43
        elif caracter == '}':
            self.q46(caracter)
        elif caracter == '{':
            self.q7(caracter)
        else:
            self.q45(caracter)
            
    def q1(self,processado):
        proximo = self.getProximoCaracter()
        if(proximo == '"'):
            processado = processado+'"'
            self.q2(processado)
        else:
            processado = processado+proximo
            self.q1(processado)
    
    def q2(self,processado):
        inserir = {'lexema':processado,'token':'string'}
        self.__processados.append(inserir)
        print 'processou!'
    
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
        