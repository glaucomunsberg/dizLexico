#!/usr/bin/env python
# -*- coding: utf-8 -*-
class AnalisadorSintatico:
    token = None
    def __init__(self,token_nome):
        self.token = token_nome