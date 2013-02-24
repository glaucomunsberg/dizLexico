#!/usr/bin/env python
# -*- coding: utf-8 -*-
class AnalizadorSintatico:
    token = None
    def __init__(self,token_nome):
        self.token = token_nome