#!/usr/bin/env python 
# encoding: utf-8

import sys

class Simulador(object):
    # Atributos
    opcao = None
    n_steps = None
    delimiter = None
    arquivo = None

    blocos = None

    fita = None
    fita2 = None

    cabecote_fita = None

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
        
        self.__armazena_codigo_fonte__()
        self.debug()
        '''print "opcao =", opcao
        print "n_steps =", n_steps
        print "delimiter =", delimiter
        print "arquivo =", arquivo'''

    # Métodos
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
                    sys.stdout.write("LINHA: \"" + linha + "\"\n")

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
                        operacoes_atuais.append(linha) #['01', 'a', '--', 'A', 'i', '10']

        arq.close()


    def computa(self, palavra):
        self.__guarda_na_fita__(palavra)


    def __guarda_na_fita__(self, palavra):
        for letra in palavra:
            self.fita.append(letra)

        print self.fita


    def debug(self):

        '''print self.blocos           # Todos os blocos.
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



# 0        1         2                 3          4            5
#----------------------------------------------------------------------------------------------------
# simulaMT <opções>  <arquivo>                                              | opções = -r ou -v
# simulaMT -s        <n>               <arquivo>
# simulaMT -head     <delimitadores>   <opções>   <arquivo>                 | opções = -r ou -v
# simulaMT -head     <delimitadores>   -s         <n>         <arquivo>