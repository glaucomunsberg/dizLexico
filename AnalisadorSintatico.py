#!/usr/bin/env python
# -*- coding: utf-8 -*-
class AnalisadorSintatico:
    __listaTokens   = None
    __posicaoLista  = None
    __tamanhoLista  = None
    __log           = None
    __contadorParen   = 0

    
    #
    # AnalisadorSintatico
    #    recebe como parametro uma lista de dicionários.
    #    Os dicionários devem conter: o lexema
    #    Veja abaixo um exemplo
    #        lista := list(dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'], ... ,dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'])
    def __init__(self,listaTokens,log):
        self.__log          = log
        self.__log.write('Classe: AnalisadorSintatico \n')
        try:
            self.__listaTokens  = listaTokens
            self.__posicaoLista = 0;
            self.__tamanhoLista = len( self.__listaTokens )
        except:
            raise Exception, '__init__: Algo de errado ocorreu na inicialização do Analisador Sintático\n'
            
    #
    # ProximoToken
    #    Retira tokens da lista por ordem ou
    #    pela posicao desejada
    #
    def proximoToken(self,posicao = 0):
        try:
            topo = self.__listaTokens.pop(0)
            #print 'Próximo: '+str(topo)
            return topo
        except:
            return None
        
    def insereProximoToken(self,token):
        try:
            self.__listaTokens.insert(0,token)
        except:
            raise Exception, 'Sintatico::InsereProximoToken Não inseriu na lista o token '+str(token)+'\n'
        
    def isBalanceado(self):
        if self.__contadorParen == 0:
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
            return 0
        elif token['token'] == 'in':
            self.in1(token)
        elif token['token'] == 'out':
            self.out1(token)
        elif token['token'] == 'identificador':
            self.iden1(token)
        elif token['token'] == 'if':
            self.if1(token)
        elif token['token'] == 'fim_comando':
            if self.__contadorParen % 2 != 0:
                raise Exception, 'Sintatico::Init fim_comando balanceamento está incorreto. Token '+str(token)+'\n'
            else:
                None
        elif token['token'] == 'fim_expressao':
            self.__contadorParen -= 1
            if self.__contadorParen % 2 != 0:
                raise Exception, 'Sintatico::Init fim_expressao balanceamento está incorreto. Token '+str(token)+'\n'
            else:
                None
        else:
            raise Exception, 'Init token '+str(token)+' não esperado.\n'
    
    def in1(self,token): 
        proxToken = self.proximoToken()
        if proxToken['token'] == 'identificador':
            self.in2(proxToken)
        else:
            raise Exception, 'In1 token '+str(token)+' não esperado.\n'
        
    def in2(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'virgula':
            self.in1(proxToken)
        elif proxToken['token'] == 'fim_comando':
            if self.__contadorParen == 0:
                None
            else:
                raise Exception, 'Sintatico::In2 Não balanceado.\n'
        else:
            raise Exception, 'Sintatico::In2 token '+str(token)+' não esperado.\n'
      
    def out1(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'valor_logico':
            self.out2(proxToken)
        elif proxToken['token'] == 'identificador':
            self.out3(proxToken)
        elif proxToken['token'] == 'inicio_expressao':
            self.__contadorParen+=1
            self.expres1(proxToken)
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
            raise Exception, 'Sintatico::Out1 token '+str(proxToken)+' não esperado.\n'
            
             
    def out2(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'fim_comando':
            if self.__contadorParen == 0:
                None
            else:
                raise Exception, 'Erro in2 não balanceado'
        elif self.isOperador(proxToken):
            self.out1(proxToken)
        elif proxToken['token'] == 'virgula':
            self.out1(proxToken)
        else:
            raise Exception, 'Sintatico::Out2 token '+str(proxToken)+' não esperado.\n'
        
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
            raise Exception, 'Sintatico::Out3 token '+str(proxToken)+' não esperado.\n'
        
    def iden1(self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'atribuicao':
            self.iden2(proxToken)
        else:
            raise Exception, 'Sintatico::Iden1 token '+str(proxToken)+' não esperado.\n'
        
    def iden2(self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'valor_logico':
            self.iden3(proxToken)
        elif proxToken['token'] == 'identificador':
            self.iden3(proxToken)
        else:
            raise Exception, 'Sintatico::Iden2 token '+str(proxToken)+' não esperado.\n'
    
    def expres1(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'identificador':
            self.expres2(token)
        elif proxToken['token'] == 'valor_logico':
            self.expres2(token)
        elif proxToken['token'] == 'inicio_expressao':
            self.__contadorParen+=1
            self.expres1(proxToken)
        else:
            raise Exception, 'Sintatico::Express1 token '+str(proxToken)+' não esperado.\n'
        proxToken = self.proximoToken()
        
    def expres2(self, token):
        proxToken = self.proximoToken()
        if self.isOperador(proxToken):
            self.expres1(proxToken)
        elif proxToken['token'] == 'negacao':
            self.expres2(proxToken)
        elif proxToken['token'] == 'fim_expressao':
            self.__contadorParen -=1
            None
        else:
            raise Exception, 'Sintatico::Express2 token '+str(proxToken)+' não esperado.\n'
            
    def iden3(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'fim_comando':
            None
        elif proxToken['token'] == 'negacao':
            self.iden3(proxToken)
        elif self.isOperador(proxToken):
            self.iden2(proxToken)
        else:
            raise Exception, 'Sintatico::Express3 token '+str(proxToken)+' não esperado.\n'
    
    def if1(self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'inicio_expressao':
            self.__contadorParen+=1
            self.if2(proxToken)
        else:
            raise Exception, 'Sintatico::If1 token '+str(proxToken)+' não esperado.\n'

    def if2 (self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'valor_logico':
            self.if3(proxToken)
        elif proxToken['token'] == 'identificador':
            self.if3(proxToken)
        else:
            raise Exception, 'Sintatico::If2 token '+str(proxToken)+' não esperado.\n'
        
    def if3 (self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'fim_expressao':
            self.if4(proxToken)
        elif proxToken['token'] == 'negacao':
            self.if3(proxToken)
        elif self.isOperador(proxToken):
            self.if2(proxToken)
        else:
            raise Exception, 'Sintatico::If3 token '+str(proxToken)+' não esperado.\n'

    # bloco
    def if4 (self, token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'inicio_bloco':
            self.if5(proxToken)
        else:
            raise Exception, 'Sintatico::If4 token '+str(proxToken)+' não esperado.\n'

    def if5 (self, token):
        proxToken = self.proximoToken()
        while proxToken != None and proxToken['token'] != 'fim_bloco':
            self.init(proxToken)
            proxToken = self.proximoToken()
        else:
            if proxToken == None:
                None
            else:
                self.if6(proxToken)
                
    def if6(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'else':
            self.if7(proxToken)
        else:
            raise Exception, 'Sintatico::If6 token '+str(proxToken)+' não esperado.\n'
        
    def if7(self,token):
        proxToken = self.proximoToken()
        if proxToken['token'] == 'inicio_bloco':
            self.if8(proxToken)
        else:
            raise Exception, 'Sintatico::If7 token '+str(proxToken)+' não esperado.\n'
        
    def if8(self, token):
        proxToken = self.proximoToken()
        while proxToken != None and proxToken['token'] != 'fim_bloco':
            self.init(proxToken)
            proxToken = self.proximoToken()
        else:
            if proxToken == None:
                None
            else:
                print 'veio para cá com'+str(proxToken)
            
            
            
            
            
            