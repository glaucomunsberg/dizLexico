#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo contém os métodos de manipulação do arquivo
# COMO EXECUTAR
#
#     $ python Principal.py exemplo.txt log.txt

import sys
from Arquivo import leitor
from Arquivo import escritor
from AnalizadorSintatico import AnalizadorSintatico
from AnalizadorLexico import AnalizadorLexico

if __name__ == "__main__":
    arquivoParaLer = leitor(sys.argv[1])
    arquivoDeEscrita = escritor(sys.argv[2])
    print arquivoParaLer.num_linhas()