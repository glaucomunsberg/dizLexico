#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo contém os métodos de manipulação do arquivo
# COMO EXECUTAR
#
#     $ python Principal.py exemplo.txt log.txt

import sys
from Arquivo import arquivo
from AnalisadorSintatico import AnalisadorSintatico
from AnalisadorLexico import AnalisadorLexico
    
if __name__ == "__main__":
    lexico = AnalisadorLexico(sys.argv[1])
    log_message = arquivo('log.txt')
    print 'Número de linhas: ', lexico.num_linhas()
    print 'Número de comentários: ', lexico.remover_comentarios()
    print 'Numero de caracteries: ',lexico.num_caracteries()
    lexico.getLexemas()
