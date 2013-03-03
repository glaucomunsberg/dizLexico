#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo contém os métodos de manipulação do arquivo
#

import sys	
class arquivo:
	file = None
	arquivoNome = None
	def __init__(self,nome_arquivo):
		self.arquivoNome = nome_arquivo
		try:
			self.file = open(self.arquivoNome, 'w')
		except:
			print "Erro na abertura do arquivo:",sys.exc_info()
	def message(self,linha):
		file.write(linha)