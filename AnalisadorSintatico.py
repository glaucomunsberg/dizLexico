#!/usr/bin/env python
# -*- coding: utf-8 -*-
class AnalisadorSintatico:
    __listaTokens   = None
    __posicaoLista  = None
    __tamanhoLista  = None
    __log           = None
    
    #
    # AnalisadorSintatico
    #    recebe como parametro uma lista de dicionários.
    #    Os dicionários devem conter: o lexema
    #    Veja abaixo um exemplo
    #        lista := list(dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'], ... ,dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'])
    def __init__(self,listaTokens,log):
        self.__log          = log
        self.__log.write('iniciando AnalisadorSintatico\n')
        try:
            self.__listaTokens  = listaTokens
            self.__posicaoLista = 0;
            self.__tamanhoLista = len( self.__listaTokens )
        except:
            raise Exception, 'Algo de errado ocorreu na inicialização do Analisador Sintático\n'
            
    #
    # ProximoToken
    #    Retira tokens da lista por ordem ou
    #    pela posicao desejada
    #
    def proximoToken(self,posicao = 0):
        try:
            return self.__listaTokens.pop(0)
        except:
            self.__log.write('Fim da lista\n')
            return None
    #
    # Inicia a verificação os lexemas
    #    
    def iniciar(self):
        token = self.proximoToken()
        while(token != None):
            print token
            token = self.proximoToken()