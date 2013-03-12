#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo contém os métodos de manipulação do arquivo
# COMO EXECUTAR
#
#     $ python Principal.py exemplo.txt log.txt

import sys, time, datetime
from AnalisadorSintatico import AnalisadorSintatico
from AnalisadorLexico import AnalisadorLexico
    
if __name__ == "__main__":
    timeNow     = time.time()
    nomelog     = datetime.datetime.fromtimestamp(timeNow).strftime('%Y-%m-%d')
    horaSessao  = datetime.datetime.fromtimestamp(timeNow).strftime('%H:%M:%S')
    log = open(nomelog+'.log', 'a')
    log.write('\n\n====Sessão Início====\n')
    log.write('Hora: '+horaSessao+'\n')
    log.write('Arquivo: '+sys.argv[1]+'\n')
    try:
        lexico = AnalisadorLexico(sys.argv[1],log)
        numLinhas       = lexico.num_linhas()
        log.write('Número de linhas: '+str(numLinhas)+'\n')
        
        numComentarios  = lexico.remover_comentarios()
        log.write('Número de comentários: '+str(numComentarios)+'\n')
        
        numCaracteres   = lexico.num_caracteries()
        log.write('Número de caracteres: '+str(numCaracteres)+'\n')
        
        listaLexemas = lexico.getLexemas()
        if listaLexemas == 0:
            raise Exception, 'Principal::Algo de errado ocorreu no levantamento dos tokens\n'
        else:
            sintatico = AnalisadorSintatico(listaLexemas,log)
            sintatico.iniciar()
        lexico.close()
    except Exception,mensagem:
        log.write(str(mensagem))
        print 'false'
    else:
        print 'true'
