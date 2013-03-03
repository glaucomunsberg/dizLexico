#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from Arquivo import arquivo 
class AnalisadorLexico:
    token = None
    file = None
    arquivoLinhas = None
    log = None
    arquivoNome = None
    arquivoNumLinhas = None
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
            self.file = open(self.arquivoNome, 'r');
            self.arquivoTemp = open('temp.txt','w')
            self.arquivoLinhas = []
            self.arquivoNumLinhas = 0
            for line in self.file:
                self.arquivoLinhas.append( line )
                self.arquivoNumLinhas += 1
        except:
            print "Erro na abertura e leitura do arquivo:",sys.exc_info()
    #
    # Num_linhas
    #    Retorno: apenas o número de linhas do arquivo original
    #
    def num_linhas(self):
        return self.arquivoNumLinhas
    #
    # Remover_comentarios
    #    Método que remove os comentários e cria um arquivo
    #    temporário que não contém os comentários.
    #    Retorno: Número delinhas que haviam comentários
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
        return numComentarios
                      
    #
    # GetLinhas
    #    Esse é o método pela qual se chama linha específica
    #    do arquivo temp.txt, que contem o arquivo limpo.
    #    Retorno: Retorna o conteúdo da linha ou None
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
    #    Retorno: Número de cararecteries
    def num_caracteries(self):
        temp = open('temp.txt','r')
        linhas =0
        for linha in temp:
            linhas +=1
            lista = list(linha)
            print lista
        return linhas
    
    
    #
    # Close
    #    Método que finaliza a execução e fecha os
    #    os arquivos.
    #
    def close(self):
        os.remove('temp.txt')
        self.arquivoTemp.close()
        self.file.close()