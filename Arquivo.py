#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Arquivo contém os métodos de manipulação do arquivo
#

import sys
class leitor:
	file = None
	arquivoNome = None
	arquivoNumLinhas = None
	
	#Construtor do arquivo e o programa
	def __init__(self,nome_arquivo):
		self.arquivoNome = nome_arquivo
		try:
			self.file = open(self.arquivoNome, 'r');
			self.arquivoNumLinhas = sum(1 for line in open(self.arquivoNome))
		except:
			print "Erro na abertura e leitura do arquivo:",sys.exc_info()
	def num_linhas(self):
		return self.arquivoNumLinhas
	
class escritor:
	file = None
	arquivoNome = None
	def __init__(self,nome_arquivo):
		self.arquivoNome = nome_arquivo
		try:
			self.file = open(self.arquivoNome, 'w+');
		except:
			print "Erro na abertura do arquivo:",sys.exc_info()
	def escrever(self,linha):
		file.write(str(linha))