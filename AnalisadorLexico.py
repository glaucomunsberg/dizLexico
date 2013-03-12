#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re
class AnalisadorLexico:
    log = None
    arquivoNome = None
    file = None
    dicionarioDeLexemas = None
    arquivoLinhas = None
    arquivoCaracteres = None
    arquivoNumLinhas = None
    arquivoNumCaracteries = None
    arquivoTemp = None
    
    # Init
    #    Contrutor básico do analizador Léxico
    #    Abre o arquivo principal, contas as linas
    #    e prepara o léxico para as próximas operações
    #    básicas.
    #
    def __init__(self,nome_arquivo,log_m = None):
        self.arquivoNome = nome_arquivo
        self.log = log_m
        try:
            self.log.write('Classe: AnalisadorLexico\n')
            self.file = open(self.arquivoNome, 'r')
            self.arquivoTemp = open('temp.txt','w')
            self.arquivoCaracteres = list()
            self.arquivoLinhas = []
            self.arquivoNumLinhas = 0
            for line in self.file:
                self.arquivoLinhas.append( line )
                self.arquivoNumLinhas += 1
        except:
            raise Exception, 'Erro na criação do arquivo temp.txt ou na abertura do arquivo '+self.arquivoNome+'.\n'
        
    #
    # Num_linhas
    #    @return: apenas o número de linhas do arquivo original
    #
    def num_linhas(self):
        return self.arquivoNumLinhas
    #
    # Remover_comentarios
    #    Método que remove os comentários e cria um arquivo
    #    temporário que não contém os comentários.
    #    @return: Número delinhas que haviam comentários
    #
    def remover_comentarios(self):
        numcomentarios = 0;
        for line in self.arquivoLinhas:
            lista = list(line)
            try:
                comeco = lista.index('#')
                line = line[:comeco] + line[len(lista)-1:]
                if comeco == 0:
                    line = '\n'
                numcomentarios+=1;
            except ValueError:
                None
            self.arquivoTemp.write(line)
        self.arquivoTemp.close()
        self.arquivoTemp = open('temp.txt','r')
        return numcomentarios

    #
    # Num_caracteries
    #    Pega do arquivo .temp.txt o número de
    #    caracteries válidos que há nele.
    #    @return: Número de cararecteries
    def num_caracteries(self):
        temp = open('temp.txt','U').read().splitlines()
        for linha in temp:
            for caract in linha:
                self.arquivoCaracteres.insert(0, caract)
        self.arquivoNumCaracteries = len(self.arquivoCaracteres)
        self.arquivoCaracteres.reverse()
        return self.arquivoNumCaracteries
    #
    # getLexemas
    #    Método que cria a partir do temp.txt os
    #    lexemas e o token a qual ele pertece.
    #    @return: Númerode lexemas processados
    #
    def getLexemas(self):
        lexemas = QualLexema(self.arquivoTemp, self.log, self.arquivoCaracteres)
        lexemas.levantarLexemas()
        return lexemas.getListaProcessada()

    #
    # Close
    #    Método que finaliza a execução e fecha os
    #    os arquivos.
    #
    def close(self):
        os.remove('temp.txt')
        self.arquivoTemp.close()
        self.log.write('Fim Sessão\n')
        self.file.close()
        self.log.close()
       
#
# QualLexema
#    Classe que processa organicamente o temp.txt
#
class QualLexema:
    __arquivo               = None
    __tokensProcessados     = None
    __processouTokens       = None
    __log                   = None
    __arquivoCaracteres     = None
    __arquivoNumCaracteres  = None
    __caracterAtual         = None
    __expressaoRegular      = None
    __expressaoIsAlfaNum    = None
    __expressaoNaoReserva   = None
    
    def __init__(self,Arquivo,log,arquivoCaracteres):
        self.__arquivo              = Arquivo
        self.__tokensProcessados    = list()
        self.__log                  = log
        self.__processouTokens      = None
        self.__arquivoCaracteres    = arquivoCaracteres
        self.__caracterAtual        = -1
        self.__arquivoNumCaracteres = len(arquivoCaracteres)
        self.__expressaoCaractVali  = re.compile("[*0-9a-zV,\"-.(){}=;<>^' \n\t\r\b*:*]")
        self.__expressaoIsAlfaNum   = re.compile("[*a-z0-9*]")
        self.__expressaoNaoReserva  = re.compile("[a-df-hj-np-z]")
        self.__log.write('Classe: QualLexema\n')
    #  
    # GetProximoCaracter
    #    retorna o próximo caracterie até que não
    #    não haja mais caracteres
    #    @return: caracter ou None (final)
    #
    def getProximoCaracter(self):
        if self.__caracterAtual+1 < self.__arquivoNumCaracteres:
            self.__caracterAtual+=1
            return self.__arquivoCaracteres[self.__caracterAtual]
        else:
            return None

    #
    # isValido
    #    Método que retorna se o caracter é válido na linguagem
    #
    def isValido(self,caracter):
        if caracter != None:
            if self.__expressaoCaractVali.search(caracter):
                return 1
            else:
                return 0
        else:
            return 0
    #
    # isAlfaNumerico
    #    Método que retorna se o caracter é válido entre a-zO-1
    #
    def isAlfaNumerico(self,caracter):
        if self.__expressaoIsAlfaNum.search(caracter):
            return 1
        else:
            return 0
        
    #
    #    método auxiliar para verificar se numerico
    #
    def isNaoReservado(self,caracter):
        if self.__expressaoNaoReserva.search(caracter):
            return 1
        else:
            return 0
    #
    # LevantarLexemas
    #    método pelo qual levanta todos os lexemas
    #    e tokens contidas no programa
    #
    def levantarLexemas(self):
        caracter = self.getProximoCaracter()
        while( caracter != None):
            try:
                self.q0(caracter)
                caracter = self.getProximoCaracter()
            except Exception,e:
                raise Exception,e
        else:
            self.__processouTokens = 1
            
    #
    # getListaProcessada
    #    Retonar uma lista de dicionários que contém
    #    cada um dos lexemas e seus tokens
    #    @return: list(dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'], ... ,dict['lexema'=>'valor','token'=>'valor','token_tipo'=>'valor'])
    #
    def getListaProcessada(self):
        if self.__processouTokens:
            return self.__tokensProcessados
        else:
            self.__log.write('\nAtenção! Não há tokens processados,chame antes o método levantarLexemas()\n')
            return self.__processouTokens


    #
    #                                 IMPORTANTE
    #    é importante ter em mente que os métodos aqui abaixo descritos e interados
    #    são reflexos dos autômatros criados e principalmente o comportamento geral
    #    visto no tokens e eles cada método tem o mesmo nome de cada estado.
    
    
    def q0(self,caracter):
        if self.isValido(caracter):
            if caracter == '"':
                self.q1(caracter)
            elif caracter == '0':
                self.q2(caracter)
            elif self.isNaoReservado(caracter):
                self.q3(caracter)
            elif caracter == '1':
                self.q13(caracter)
            elif caracter == 'V':
                self.q31(caracter)
            elif caracter == '^':
                self.q33(caracter)
            elif caracter == '\'':
                self.q32(caracter)
            elif caracter == '-':
                self.q34(caracter)
            elif caracter == '<':
                self.q36(caracter)
            elif caracter == ':':
                self.q43(caracter)
            elif caracter == ';':
                self.q39(caracter)
            elif caracter == '}':
                self.q46(caracter)
            elif caracter == '{':
                self.q47(caracter)
            elif caracter == '(':
                self.q40(caracter)
            elif caracter == ')':
                self.q42(caracter)
            elif caracter == 'e':
                self.q4(caracter)
            elif caracter == 'i':
                self.q5(caracter)
            elif caracter == 'o':
                self.q6(caracter)
            elif caracter == ',':
                self.q30(caracter)
            elif caracter == ' ' or caracter == '\n' or caracter == '\t' or caracter == '\b' or caracter == '\r':
                exit
            else:
                raise Exception, "Léxico::q0 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q0 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
            
    def q1(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'f':
                self.q25(processado+caracter)
            elif caracter == 'v':
                self.q15(processado+caracter)
            elif caracter == 't':
                self.q14(processado+caracter)
            else:
                raise Exception, "Léxico::q1 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q1 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
    #
    # FINAL
    #     false_logico
    #    
    def q2(self,processado):
        inserir = {'token':'valor_logico', 'lexema':processado}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
        
    #
    # Misto
    #       
    def q3(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                exit
            else:
                raise Exception, "Léxico::q3 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
        
    #
    # Misto
    #       
    def q4(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 'l':
                    self.q7(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q4 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # Misto
    #       
    def q5(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 'f':
                    self.q10(processado+caracter)
                elif caracter == 'n':
                    self.q11(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q5 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
            
    #
    # Misto
    #       
    def q6(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 'u':
                    self.q12(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q6 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # Misto
    #       
    def q7(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 's':
                    self.q8(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q7 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # Misto
    #       
    def q8(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 'e':
                    self.q9(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q8 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # Misto
    #       
    def q9(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                self.q3(processado+caracter)
            else:
                inserir = {'token':'else'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q9 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
            
    #
    # Misto
    #       
    def q10(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                self.q3(processado+caracter)
            else:
                inserir = {'token':'if'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q10 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # Misto
    #       
    def q11(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                self.q3(processado+caracter)
            else:
                inserir = {'token':'in'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q10 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

#
    # Misto
    #       
    def q12(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                if caracter == 't':
                    self.q49(processado+caracter)
                else:
                    self.q3(processado+caracter)
            else:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
            else:
                raise Exception, "Léxico::q12 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
                    
    #
    # FINAL
    #     true_logico
    #
    def q13(self,processado):
        inserir = {'token':'valor_logico','lexema':processado}
        self.__tokensProcessados.append(inserir)
        self.__log.write(str(inserir)+'\n')

    def q14(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q41(processado+caracter)
            else:
                raise Exception, "Léxico::q14 com "+caracter+"  não era esperado.\n"
        else:
            raise Exception, "Léxico::q14 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
         
    def q15(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q16(processado+caracter)
            elif caracter == '"':
                self.q13(processado+caracter)
            else:
                raise Exception, "Léxico::q15 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q15 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
      
    def q16(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q17(processado+caracter)
            else:
                raise Exception, "Léxico::q16 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q16 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
        
    def q17(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'd':
                self.q18(processado+caracter)
            else:
                raise Exception, "Léxico::q17 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q17 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    def q18(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'a':
                self.q19(processado+caracter)
            else:
                raise Exception, "Léxico::q18 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q18 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               

    def q19(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'd':
                self.q20(processado+caracter)
            else:
                raise Exception, "Léxico::q19 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q19 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               
    
    def q20(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q21(processado+caracter)
            else:
                raise Exception, "Léxico::q20 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q20 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               
    
    def q21(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'i':
                self.q22(processado+caracter)
            else:
                raise Exception, "Léxico::q21 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q21 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               
    
    def q22(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'r':
                self.q23(processado+caracter)
            else:
                raise Exception, "Léxico::q22 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q22 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               

    def q23(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'o':
                self.q24(processado+caracter)
            else:
                raise Exception, "Léxico::q23 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q23 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               

    def q24(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q13(processado+caracter)
            else:
                raise Exception, "Léxico::q24 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q24 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"               
    
    def q25(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '\"':
                self.q2(processado+caracter)
            elif caracter == 'a':
                self.q26(processado+caracter)
            else:
                raise Exception, "Léxico::q25 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q25 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
        
    def q26(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'l':
                self.q27(processado+caracter)
            else:
                raise Exception, "Léxico::q26 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q26 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    def q27(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 's':
                self.q28(processado+caracter)
            else:
                raise Exception, "Léxico::q27 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q27 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    def q28(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'o':
                self.q29(processado+caracter)
            elif caracter == 'e':
                self.q29(processado+caracter)
            else:
                raise Exception, "Léxico::q28 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q28 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"


    def q29(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q2(processado+caracter)
            else:
                raise Exception, "Léxico::q29 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q29 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"
        
    #
    # FINAL
    #     virgula_comando
    #    
    def q30(self,processado):
        inserir = {'token':'virgula' }
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
        
    #
    # FINAL
    #     operador_ou
    #    
    def q31(self,processado):
        inserir = {'token':'ou'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')

    #
    # FINAL
    #     operador_e
    #    
    def q32(self,processado):
        inserir = {'token':'negacao'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
                        
    #
    # FINAL
    #     operador_e
    #    
    def q33(self,processado):
        inserir = {'token':'e'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')

    def q34(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '>':
                self.q35(processado+caracter)
            else:
                raise Exception, "Léxico::q34 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q34 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # FINAL
    #     operador_condicional
    #    
    def q35(self,processado):
        inserir = {'token':'condicional'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
        
    def q36(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '-':
                self.q37(processado+caracter)
            else:
                raise Exception, "Léxico::q36 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q36 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    def q37(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '>':
                self.q38(processado+caracter)
            else:
                raise Exception, "Léxico::q37 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q37 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # FINAL
    #     operador_bicondicional
    #    
    def q38(self,processado):
        inserir = {'token':'bicondicional'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
    
    #
    # FINAL
    #     fim_comando
    #    
    def q39(self,processado):
        inserir = {'token':'fim_comando'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
    #
    # FINAL
    #     inicio_expressao
    #    
    def q40(self,processado):
        inserir = {'token':'inicio_expressao' }
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
                        
    def q41(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'u':
                self.q45(processado+caracter)
            else:
                raise Exception, "Léxico::q41 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q41 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # FINAL
    #     fim_expressao
    #    
    def q42(self,processado):
        inserir = {'token':'fim_expressao' }
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
        
    def q43(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '=':
                self.q44(processado+caracter)
            else:
                raise Exception, "Léxico::q43 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q43 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # FINAL
    #     operador_atribuicao
    #    
    def q44(self,processado):
        inserir = {'token':'atribuicao'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')      

    def q45(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == 'e':
                self.q48(processado+caracter)
            else:
                raise Exception, "Léxico::q45 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q45 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"

    #
    # FINAL
    #     fim_bloco
    #    
    def q46(self,processado):
        inserir = {'token':'fim_bloco' }
        self.__tokensProcessados.append(inserir)
        self.__log.write(str(inserir)+'\n')

    #
    # FINAL
    #     inicio_bloco
    #    
    def q47(self,processado):
        inserir = {'token':'inicio_bloco'}
        self.__tokensProcessados.append(inserir)
        self.__log.write( str(inserir)+'\n')
                
    def q48(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if caracter == '"':
                self.q13(processado+caracter)
            else:
                raise Exception, "Léxico::q48 com "+caracter+" não era esperado.\n"
        else:
            raise Exception, "Léxico::q48 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"   
        
    #
    # Misto
    #       
    def q49(self,processado):
        caracter = self.getProximoCaracter()
        if self.isValido(caracter):
            if self.isAlfaNumerico(caracter):
                self.q3(processado+caracter)
            else:
                inserir = {'token':'out'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n')
                self.q0(caracter)
        else:
            if caracter == None:
                inserir = {'lexema':processado,'token':'identificador'}
                self.__tokensProcessados.append(inserir)
                self.__log.write( str(inserir)+'\n' )
            else:
                raise Exception, "Léxico::q9 com "+caracter+" não é reconhecido pelo analisador Léxico.\n"         