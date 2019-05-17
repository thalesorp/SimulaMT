#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import argparse

from Simulador import *

def main():
    simulaMT = None
    arquivo = None
    opcao = None
    n_steps = 500
    delimiter = "()"

    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('file_path', metavar='file', type=str, help='arquivo do algoritmo a ser simulado')
    parser.add_argument("-r", "--resume", action='store_true', help="executa o programa até o fim em modo silencioso")
    parser.add_argument("-v", "--verbose", action='store_true', help="executa até o fim mostrando o resultado passo a passo da execução")
    parser.add_argument("-s", "--steps", metavar='N', help="mostra o resultado passo a passo de N computações, depois reabre o prompt para aguardar nova opção (-r,-v,-s). Caso não seja fornecida nova opção (entrada em branco), o padrão é repetir a mesma opção fornecida anteriormente")
    parser.add_argument("-head", metavar='DELIMITADORES', help="modifica os dois caracteres delimitadores, esquerdo e direito, do cabeçote")
    args = vars(parser.parse_args())

    arquivo = args['file_path']
    print "arquivo:", arquivo

    opcao = "?"
    opcao = args['']

    n_steps = args['steps']
    print "n_steps:", n_steps

    if not args['head']:
        print "not args"
        delimiter = args['head']

    print "delimiter:", delimiter
    raw_input()
    '''

    if len(sys.argv) < 3:
        print 'Parametros incorretos!'
        quit()
    elif (len(sys.argv) == 3) and (sys.argv[1] == "-r" or sys.argv[1] == "-v"):
        opcao = sys.argv[1]
        arquivo = sys.argv[2]
    elif (len(sys.argv) == 4) and (sys.argv[1] == "-s"):
        opcao = sys.argv[1]
        arquivo = sys.argv[3]
        if not sys.argv[2].isdigit():
            print "Número de steps inválido!"
            quit()
        n_steps = sys.argv[2]
    elif (len(sys.argv) >= 5) and (sys.argv[1] == "-head"):
        opcao = sys.argv[3]
        
        if len(sys.argv[2]) != 2:
            print "Erro nos delimitadores!"
            quit()
        delimiter = sys.argv[2]
        if (opcao != "-r") and (opcao != "-v") and (opcao != "-s"):
            print "Opção invalida!"
            quit()
        elif opcao == "-s":
            if not sys.argv[4].isdigit():
                print "Número de steps inválido!"
                quit()
            n_steps = sys.argv[4]
            arquivo = sys.argv[5]
        else:
            arquivo = sys.argv[4]


    simulaMT = Simulador(arquivo, opcao, n_steps, delimiter)

    print ""
    print "Simulador de Máquina de Turing v4.0"
    print "Desenvolvido como trabalho prático para a disciplina de Teoria da Computação."
    print "Thales Otávio e Pedro Costa, IFMG - Campus Formiga, 2019.\n"
    sys.stdout.write("Forneça a palavra inicial: ")
    palavra = raw_input()

    simulaMT.compila(palavra)

if __name__ == "__main__":
    main()
