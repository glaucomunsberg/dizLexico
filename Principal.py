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
    log.write(horaSessao+' Sessão Início\n')
    try:
        lexico = AnalisadorLexico(sys.argv[1],log)
        print 'Número de linhas: ', lexico.num_linhas()
        print 'Número de comentários: ', lexico.remover_comentarios()
        print 'Numero de caracteries: ',lexico.num_caracteries()
        lexico.getLexemas()
    except Exception,e:
        log.write('\n'+str(e))
        print 'false'
    else:
        print 'true'
