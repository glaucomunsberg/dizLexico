#!/usr/bin/env python
# -*- coding: utf-8 -*-
class AnalisadorSintatico:
    __listaTokens   = None
    __posicaoLista  = None
    __tamanhoLista  = None
    __log           = None
    contadorParen   = 0
    
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
        
    def insereProximoToken(self,token):
        try:
            self.__listaTokens.insert(0,token)
        except:
            raise Exception, 'Não inseriu na lista'
        
    def isBalanceado(self):
        if self.contadorParen == 0:
            return 1
        else:
            return None
        
    #
    # Inicia a verificação os lexemas
    #    
    def iniciar(self):
        token = self.proximoToken()
        while(token != None):
            self.init(token)
            token = self.proximoToken()
            
    def isOperador(self,token):
        if token['token'] == 'bicondicional' or token['token'] == 'condicional' or token['token'] == 'e' or token['token'] == 'ou':
            return 1
        else:
            return None
        
    def init(self,token):
        if token == None:
            return 1
        elif token['token'] == 'in':
            self.in1(token)
        elif token['token'] == 'out':
            self.out1(token)
        elif token['token'] == 'identificador':
            self.iden1(token)
    
    def in1(self,token): 
        proxToken = self.proximoToken()
        if proxToken['token'] == 'identificador':
            self.in2(proxToken)
        else:
            raise Exception, 'In1 não correto!'
        
    def in2(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'virgula':
            self.in1(proxToken)
        elif proxToken['token'] == 'fim_comando':
            if self.contadorParen == 0:
                None
            else:
                raise Exception, 'Erro in2 não balanceado'
        else:
            raise Exception, 'In2 não correto!'
      
    def out1(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'valor_logico':
            self.out2(proxToken)
        elif proxToken['token'] == 'identificador':
            self.out3(proxToken)
        #elif proxToken['token'] == 'inicio_expressao':
            #self.contadorParen+=1
            #self.out1(proxToken)
            #proxToken = self.proximoToken()
            #if proxToken['token'] == 'fim_expressao':
                #self.contadorParen-=1
                #None
            #else:
                #raise Exception, 'Out1 expressao não correta!'
        else:
            raise Exception, 'out1 não correto'
            
             
    def out2(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'fim_comando':
            if self.contadorParen == 0:
                None
            else:
                raise Exception, 'Erro in2 não balanceado'
        elif self.isOperador(proxToken):
            self.out1(proxToken)
        else:
            raise Exception, 'out2 não correto!'
        
    def out3(self,token):
        proxToken = self.proximoToken()
        if self.isOperador(proxToken):
            self.out1(proxToken)
        elif proxToken['token'] == 'fim_comando':
            None
        elif proxToken['token'] == 'virgula':
            self.out1(proxToken)
        elif proxToken['token'] =='negacao':
            self.out3(proxToken)
        #elif proxToken['token'] == 'fim_expressao':
            #self.insereProximoToken(proxToken)
            #None
        else:
            raise Exception, 'out3 não correto!'
        
    def iden1(self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'atribuicao':
            self.iden2(proxToken)
        else:
            raise Exception, 'iden1 não válido'
        
    def iden2(self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'valor_logico':
            self.iden3(proxToken)
        elif proxToken['token'] == 'identificador':
            self.iden3(proxToken)
        else:
            raise Exception, 'iden2 não válido'
        
    def iden3(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'fim_comando':
            None
        elif proxToken['token'] == 'negacao':
            self.iden3(proxToken)
        elif self.isOperador(proxToken):
            self.iden2(proxToken)
        else:
            raise Exception, 'iden3 não é válido'
            