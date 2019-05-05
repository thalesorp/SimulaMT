#!/usr/bin/env python 
# encoding: utf-8

import sys

class Simulador(object):

    # Construtor
    def __init__(self, opcao, n_steps, delimiter, arquivo):
        self.opcao = opcao
        self.n_steps = n_steps
        self.delimiter = delimiter
        self.arquivo = arquivo

        self.blocos = list()

        self.fita = list()
        self.fita_segunda = list()

        self.cabecote_fita = 0

        self.pilha_blocos = list()

        self.__armazena_codigo_fonte__()

    # Métodos
    def computa(self, palavra):
        self.__guarda_na_fita__(palavra)

        self.debug_mostra_fita()

        nome_bloco = "main"

        estado_atual = self.get_estado_inicial_bloco(nome_bloco)

        while True:
            letra_cabecote = self.get_letra_atual_cabecote()

            operacao = self.get_operacao(nome_bloco, estado_atual, letra_cabecote)
            if operacao == "erro":
                print "Deu ruim!"
                exit()

            if operacao[0] == "op":
                self.set_letra_cabecote_fita(operacao[3])
                self.move_cabecote(operacao[4])
                estado_atual = operacao[5]

                if estado_atual == "retorne": # Desempilha da pilha de blocos.
                    [nome_bloco, estado_atual] = self.pilha_blocos.pop()

            if operacao[0] == "func":
                self.pilha_blocos.append([nome_bloco, operacao[3]])
                nome_bloco = operacao[2]
                estado_atual = self.get_estado_inicial_bloco(nome_bloco)

            self.debug_mostra_fita()

    def set_letra_cabecote_fita(self, letra):
        if letra != "*":
            self.fita[self.cabecote_fita] = letra

    def move_cabecote(self, direcao):
        deslocamento = 0

        if direcao == "d":
            deslocamento = 1
        elif direcao == "e":
            deslocamento = -1

        if (self.cabecote_fita == len(self.fita)-1) and (deslocamento == 1):
            self.fita.append("_")
            self.cabecote_fita = self.cabecote_fita + deslocamento
            return

        if (self.cabecote_fita == 0) and (deslocamento == -1):
            self.fita.insert(0,"_")
            self.cabecote_fita = 0
            return

        self.cabecote_fita = self.cabecote_fita + deslocamento

    # Getters.
    def get_estado_inicial_bloco(self, nome_bloco):
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                return bloco[1]
        return "erro estado inicial bloco"

    def get_letra_atual_cabecote(self):
        #
        return self.fita[self.cabecote_fita]

    def get_operacao(self, nome_bloco, estado_atual, letra_cabecote):
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                for operacao in bloco[2]:
                    if operacao[1] == estado_atual:
                        if operacao[0] == "op":
                            if (operacao[2] == letra_cabecote) or (operacao[2] == "*"):
                                return operacao
                        elif operacao[0] == "func":
                            return operacao
        return "erro"

    # Métodos privados.
    def __armazena_codigo_fonte__(self):
        dentro_bloco = False

        arq = open(self.arquivo, 'r')
        texto = arq.readlines()
        
        for linha in texto:
            # Removendo tudo que existe após um ";".
            linha = linha.split(";")[0]
            # Remove espaços do início e fim da linha.
            linha = linha.strip()
            # Ignora linhas em branco.
            if linha:
                # Ignorando comentários.
                if linha[0] != ";":
                    linha = linha.split(" ")
                    if (dentro_bloco == False) and (linha[0] == "bloco"):
                        # Começa aqui a ler um bloco.
                        dentro_bloco = True
                        nome_bloco = linha[1]
                        estado_inicial = linha[2]

                        bloco_atual = list()
                        bloco_atual.append(nome_bloco)
                        bloco_atual.append(estado_inicial)
                        operacoes_atuais = list()
                        continue

                    if linha[0] == "fim":
                        # Termina aqui de ler o bloco.
                        dentro_bloco = False
                        bloco_atual.append(operacoes_atuais)
                        self.blocos.append(bloco_atual)
                    
                    if dentro_bloco == True:
                        # Verificando se é operação ou chamada de função, e inserido seus identificadores.
                        if linha[2] == "--":
                            del(linha[2])
                            linha.insert(0,"op") #['op', '01', 'a', '--', 'A', 'i', '10']
                        else:
                            linha.insert(0,"func") #['func','01', 'nome_funcao', '10']

                        operacoes_atuais.append(linha)
        arq.close()

    def __guarda_na_fita__(self, palavra):
        for letra in palavra:
            self.fita.append(letra)

    # Outros.
    def debug(self):

        '''print self.blocos        # Todos os blocos.
        print "\n"
        print self.blocos[0]        # Primeiro bloco.
        print "\n"
        print self.blocos[0][2]     # Lista de operações do primeiro bloco. 
        print "\n"
        print self.blocos[0][2][0]  # Primeira operação do primeiro bloco.
        print "\n"'''

        i = 1
        for bloco in self.blocos:
            print "Bloco ",i
            print "Nome:", bloco[0]
            print "Estado inicial:", bloco[1]
            i = i + 1
            print ""

        print ""

        i = 1
        for bloco in self.blocos:
            print "\nOperações do bloco ",i,":"
            for operacao in bloco[2]:
                print operacao
            i = i + 1

    def debug_mostra_fita(self):
        fita = list(self.fita)
        fita[self.cabecote_fita] = "["+fita[self.cabecote_fita]+"]"
        print "Fita:", fita
