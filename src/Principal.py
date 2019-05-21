#!/usr/bin/env python
# -*- coding: utf-8 -*-

##########################################################################################
#                                                                                        #
#  Simulador da Máquina de Turing (com duas fitas)                                       #
#  Desenvolvido como trabalho prático para a disciplina de Teoria da Computação.         #
#  Instituto Federal de Minas Gerais - Campus Formiga, 2019.                             #
#  Autores:                                                                              #
#  Thales Otávio, @ThalesORP, ThalesORP@gmail.com                                        #
#  Pedro Costa, @PeduCosta17, peducosta17@gmail.com, +55 (37) 99829-1751                 #
#                                                                                        #
##########################################################################################

import sys
import argparse

from Simulador import *

def main():
    simulaMT = None
    arquivo = None
    opcao = None
    n_steps = 500
    delimitadores = "()"


    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', metavar='file', type=str, help='arquivo do algoritmo a ser simulado')
    parser.add_argument("-r", "--resume", action='store_true', help="executa o programa até o fim em modo silencioso")
    parser.add_argument("-v", "--verbose", action='store_true', help="executa até o fim mostrando o resultado passo a passo da execução")
    parser.add_argument("-s", "--steps", metavar='N', help="mostra o resultado passo a passo de N computações, depois reabre o prompt para aguardar nova opção (-r,-v,-s). Caso não seja fornecida nova opção (entrada em branco), o padrão é repetir a mesma opção fornecida anteriormente")
    parser.add_argument("-head", metavar='DELIMITADORES', help="modifica os dois caracteres delimitadores, esquerdo e direito, do cabeçote")
    args = vars(parser.parse_args())

    arquivo = args['file_path']

    if args['resume'] == True:
        opcao = "-r"

    if args['verbose'] == True:
        opcao = "-v"

    if args['steps'] != None:
        opcao = "-s"
        n_steps = args['steps']

    if opcao == None:
        sys.stdout.write("Erro: Opção de computação não inserida.\n")
        exit()

    if args['head'] != None:
        delimitadores = args['head']

    simulaMT = Simulador(arquivo, opcao, n_steps, delimitadores)

    print ""
    print "Simulador de Máquina de Turing v4.0"
    print "Desenvolvido como trabalho prático para a disciplina de Teoria da Computação."
    print "Thales Otávio e Pedro Costa, IFMG - Campus Formiga, 2019.\n"
    sys.stdout.write("Forneça a palavra inicial: ")
    palavra = raw_input()

    simulaMT.compila(palavra)

if __name__ == "__main__":
    main()
