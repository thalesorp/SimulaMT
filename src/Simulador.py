#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
#                                                                                        #
#  Simulador da Máquina de Turing (com duas fitas)                                       #
#  Desenvolvido como trabalho prático para a disciplina de Teoria da Computação.         #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019.                             #
#  Autores:                                                                              #
#  Thales Otávio, @ThalesORP, ThalesORP@gmail.com                                        #
#  Pedro Costa, @PeduCosta, peducosta17@gmail.com, +55 (37) 99829-1751                   #
#                                                                                        #
##########################################################################################

import sys

class Simulador(object):

    # Construtor
    def __init__(self, arquivo, opcao, qtd_passos, delimitadores):
        self.arquivo = arquivo
        self.opcao = opcao[1] # "-r", "-v", "-s N".
        self.qtd_passos = int(qtd_passos)
        self.delimitadores = delimitadores

        self.blocos = list()
        self.pilha_blocos = list()

        self.fita = list()
        self.fita_segunda = ["_"]
        self.cabecote_fita = 0

        self.nome_bloco_atual = None
        self.estado_atual = None

        self.__armazena_codigo_fonte__()


    # Métodos
    def compila(self, palavra):
        self.__guarda_na_fita__(palavra)

        self.nome_bloco_atual = "main"
        self.estado_atual = self.get_estado_inicial_bloco(self.nome_bloco_atual)

        if self.estado_atual == "erro":
            self.UI_mostra_resultado("erro")
            return

        self.UI_mostra_divisoria()

        resultado = self.computa()
    
        while (resultado == None):
            self.UI_solicita_nova_opcao()
            resultado = self.computa()

        self.UI_mostra_resultado(resultado)

    def computa(self):
        operacao = [None]
        computacoes_decorridas = 0

        while (computacoes_decorridas < self.qtd_passos):

            if self.opcao != "r":
                self.UI_mostra_computacao(self.nome_bloco_atual, self.estado_atual)

            # Caso a computação atual tiver um "!" (breakpoint).
            if operacao[len(operacao)-1] == "!":
                return None

            computacoes_decorridas = computacoes_decorridas + 1

            if self.estado_atual == "pare_aceita":
                return True
            if self.estado_atual == "pare_rejeita":
                return False

            operacao = self.get_operacao(self.nome_bloco_atual, self.estado_atual)

            if operacao == "erro":
                return "erro"

            if operacao[0] == "op": # ['op', estado, caractere_atual, caractere_a_escrever, movimento, estado_destino ]
                self.set_letra_cabecote_fita(operacao[3])
                self.__move_cabecote__(operacao[4])
                self.__atualiza_estado_atual__(operacao[5])

            elif operacao[0] == "func": # ['func', estado_atual, nome_funcao, estado_destino]
                self.pilha_blocos.append([self.nome_bloco_atual, operacao[3]])
                self.__atualiza_bloco_atual__(operacao[2])
                self.__atualiza_estado_atual__(self.get_estado_inicial_bloco(self.nome_bloco_atual))
                if self.estado_atual == "erro":
                    return "erro"

            elif operacao[0] == "copi": # ['copi', estado_atual, copiar, estado_destino]
                self.set_letra_cabecote_fita_segunda(self.get_letra_atual_cabecote())
                self.__atualiza_estado_atual__(operacao[3])

            elif operacao[0] == "cola": # ['cola', estado_atual, colar, estado_destino]
                self.set_letra_cabecote_fita(self.get_letra_fita_segunda())
                self.__atualiza_estado_atual__(operacao[3])

            if self.estado_atual == "retorne": # Desempilha da pilha de blocos.
                [self.nome_bloco_atual, self.estado_atual] = self.pilha_blocos.pop()

        return None


    # Getters e setters.
    def get_estado_inicial_bloco(self, nome_bloco):
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                return bloco[1]
        return "erro"

    def get_operacao(self, nome_bloco, estado):
        for bloco in self.blocos:
            if bloco[0] == nome_bloco:
                for operacao in bloco[2]:
                    if operacao[1] == estado:
                        
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


    # Interface com o usuário.
    def UI_mostra_computacao(self, nome_bloco, estado):
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
            tFita.insert(self.cabecote_fita, self.delimitadores[0])
            tFita.insert(self.cabecote_fita + 2, self.delimitadores[1])
        else:
            tFita.insert(self.cabecote_fita - 1, self.delimitadores[0])
            tFita.insert(self.cabecote_fita + 1, self.delimitadores[1])

        tamanho_palavra = len(tFita)

        # Removendo do lado esquerdo e direito, a quantidade de caracteres conforme a metade da palavra.
        if (tamanho_palavra % 2) == 0:
            metadeEsquerda = metadeEsquerda - tamanho_palavra/2
            metadeDireita = metadeDireita - tamanho_palavra/2
        else:
            metadeEsquerda = metadeEsquerda - tamanho_palavra/2
            metadeDireita = metadeDireita - ((tamanho_palavra/2)+1)

        fitaFinal = (metadeEsquerda * "_") + ''.join(tFita) + (metadeDireita * "_")

        tamanho_palavra = len(nome_bloco) + 1 + len(estado)

        total = 25

        qtd_restantes = total - tamanho_palavra

        caractere = "."

        bolinhas = caractere * qtd_restantes

        sys.stdout.write(bolinhas)
        sys.stdout.write(nome_bloco)
        sys.stdout.write(".")
        sys.stdout.write(estado)
        sys.stdout.write(" : ")
        sys.stdout.write(fitaFinal)
        sys.stdout.write(" : ")
        sys.stdout.write(''.join(self.fita_segunda) + "\n")

    def UI_solicita_nova_opcao(self):
        self.UI_mostra_divisoria()
        sys.stdout.write("Forneça nova opção (−r, −v, −s): ")
        nova_opcao = raw_input()
        
        if len(nova_opcao) == 0:
            return

        if len(nova_opcao) > 2: # "-s N"
            nova_opcao = nova_opcao.split(" ")
            self.opcao = nova_opcao[0][1]
            self.qtd_passos = int(nova_opcao[1])
        
        else: # "-r" ou "-v"
            self.opcao = nova_opcao[1]

    def UI_mostra_divisoria(self):
        #
        print "__________________________________________________________________________________"

    def UI_mostra_resultado(self, resultado):
        self.UI_mostra_divisoria()
        if resultado == True:
            print "ACEITOU."
        elif resultado == False:
            print "REJEITOU."
        else:
            print "ERRO."


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

    def __guarda_na_fita__(self, palavra):
        # Guarda na fita a palavra a ser computada.
        for letra in palavra:
            self.fita.append(letra)

    def __move_cabecote__(self, direcao):
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

    def __atualiza_estado_atual__(self, novo_estado):
        #
        self.estado_atual = novo_estado

    def __atualiza_bloco_atual__(self, nome_novo_bloco):
        #
        self.nome_bloco_atual = nome_novo_bloco
