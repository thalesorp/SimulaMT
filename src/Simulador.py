#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class Simulador(object):

    # Construtor
    def __init__(self, arquivo, opcao, n_steps, delimiter):
        self.opcao = opcao
        self.n_steps = n_steps
        self.delimiter = delimiter
        self.arquivo = arquivo

        self.blocos = list()

        self.fita = list()
        self.fita_segunda = ["_"]

        self.cabecote_fita = 0

        self.pilha_blocos = list()

        self.__armazena_codigo_fonte__()

    # Métodos
    def computa(self, palavra):
        # Guarda na fita, a palavra a ser computada.
        for letra in palavra:
            self.fita.append(letra)

        nome_bloco = "main"

        estado_atual = self.get_estado_inicial_bloco(nome_bloco)

        self.mostra_computacao(nome_bloco, estado_atual)


        resultado = None
        while (resultado == None):

            if estado_atual == "pare_aceita":
                resultado = True
                continue
            if estado_atual == "pare_rejeita":
                resultado = False
                continue

            operacao = self.get_operacao(nome_bloco, estado_atual)

            if operacao == "erro":
                resultado = False
                continue

            if operacao[0] == "op": # ['op', estado, caractere_atual, caractere_a_escrever, movimento, estado_destino ]
                self.set_letra_cabecote_fita(operacao[3])
                self.move_cabecote(operacao[4])
                estado_atual = operacao[5] # Atualiza o estado atual depois de computar.

            elif operacao[0] == "func": # ['func', estado_atual, nome_funcao, estado_destino]
                self.pilha_blocos.append([nome_bloco, operacao[3]])
                nome_bloco = operacao[2]
                estado_atual = self.get_estado_inicial_bloco(nome_bloco)

            elif operacao[0] == "copi": # ['copi', estado_atual, copiar, estado_destino]
                self.set_letra_cabecote_fita_segunda(self.get_letra_atual_cabecote())
                estado_atual = operacao[3] # Atualiza o estado atual depois de computar.

            elif operacao[0] == "cola": # ['cola', estado_atual, colar, estado_destino]
                self.set_letra_cabecote_fita(self.get_letra_fita_segunda())
                estado_atual = operacao[3] # Atualiza o estado atual depois de computar.

            if estado_atual == "retorne": # Desempilha da pilha de blocos.
                [nome_bloco, estado_atual] = self.pilha_blocos.pop()

            self.mostra_computacao(nome_bloco, estado_atual)


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

    # Getters e setters.
    def get_estado_inicial_bloco(self, nome_bloco):
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                return bloco[1]
        return "erro estado inicial bloco"

    def get_operacao(self, nome_bloco, estado_atual):
        #print "Entrou em get_operação, com nome_bloco=", nome_bloco, "e estado_atual=", estado_atual
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                for operacao in bloco[2]:
                    if operacao[1] == estado_atual:
                        
                        # ['op', estado, caractere_atual, caractere_a_escrever, movimento, estado_destino ]
                        if operacao[0] == "op":

                            # Verifica se é uma operação da primeira fita.
                            if len(operacao[2]) == 1:
                                if (operacao[2] == self.get_letra_atual_cabecote()) or (operacao[2] == "*"):
                                    return operacao
                            
                            # Verifica se é uma operação da segunda fita.
                            elif len(operacao[2]) == 3:
                                # Removendo "[]" do caractere atual.
                                caractere_atual = operacao[2][1]
                                if (caractere_atual == self.get_letra_fita_segunda()) or (caractere_atual == "*"):
                                    return operacao
                        
                        elif (operacao[0] == "func") or (operacao[0] == "copi") or (operacao[0] == "cola"):
                            return operacao

        return "erro"

    def get_letra_atual_cabecote(self):
        #
        return self.fita[self.cabecote_fita]

    def get_letra_fita_segunda(self):
        #
        return self.fita_segunda[0]

    def set_letra_cabecote_fita(self, letra):
        if letra != "*":
            self.fita[self.cabecote_fita] = letra

    def set_letra_cabecote_fita_segunda(self, letra):
        if letra != "*":
            self.fita_segunda[0] = letra

    # UI.
    def mostra_computacao(self, nome_bloco, estado_atual):
        caractere = "_"
        metadeEsquerda = 25
        metadeDireita = 25
        tFita = list(self.fita)

        # Remove underlines quando o cabeçote não está nas pontas.
        if tFita[0] == "_" and self.cabecote_fita != 0:
                tFita = tFita[1:len(tFita)]
        if tFita[len(tFita)-1] == "_" and self.cabecote_fita != len(tFita):
                tFita = tFita[0:(len(tFita)-1)]

        # Adiciono os delimitadores do cabeçote na posição correta.
        if self.cabecote_fita == 0:
            tFita.insert(self.cabecote_fita, self.delimiter[0])
            tFita.insert(self.cabecote_fita + 2, self.delimiter[1])
        else:
            tFita.insert(self.cabecote_fita - 1, self.delimiter[0])
            tFita.insert(self.cabecote_fita + 1, self.delimiter[1])

        tamanho_palavra = len(tFita)

        # Removendo do lado esquerdo e direito, a quantidade de caracteres conforme a metade da palavra.
        if (tamanho_palavra % 2) == 0:
            metadeEsquerda = metadeEsquerda - tamanho_palavra/2
            metadeDireita = metadeDireita - tamanho_palavra/2
        else:
            metadeEsquerda = metadeEsquerda - tamanho_palavra/2
            metadeDireita = metadeDireita - ((tamanho_palavra/2)+1)

        fitaFinal = (metadeEsquerda * "_") + ''.join(tFita) + (metadeDireita * "_")

        tamanho_palavra = len(nome_bloco) + 1 + len(estado_atual)

        total = 25

        qtd_restantes = total - tamanho_palavra

        caractere = "."

        bolinhas = caractere * qtd_restantes

        sys.stdout.write(bolinhas)
        sys.stdout.write(nome_bloco)
        sys.stdout.write(".")
        sys.stdout.write(estado_atual)
        sys.stdout.write(" : ")
        sys.stdout.write(fitaFinal)
        sys.stdout.write(" : ")
        sys.stdout.write(''.join(self.fita_segunda) + "\n")

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
                        elif linha[1] == "copiar":
                            linha.insert(0,"copi") #['copi','01', 'copiar', '10']
                        elif linha[1] == "colar":
                            linha.insert(0,"cola") #['cola','01', 'colar', '10']
                        else:
                            linha.insert(0,"func") #['func','01', 'nome_funcao', '10']

                        operacoes_atuais.append(linha)
        arq.close()

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
