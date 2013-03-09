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
        numLinhas       = lexico.num_linhas()
        log.write('Número de Linhas: '+str(numLinhas)+'\n')
        numComentarios  = lexico.remover_comentarios()
        log.write('Número de Comentários: '+str(numComentarios)+'\n')
        numCaracteres   = lexico.num_caracteries()
        log.write('Número de Caracteres'+str(numCaracteres)+'\n')
        lexico.getLexemas()
        lexico.close()
    except Exception,e:
        log.write('\n'+str(e))
        print 'false'
    else:
        print 'true'
