#!/usr/bin/env python 
# encoding: utf-8

import sys
from Simulador import *

def main():

    simulaMT = None
    opcao = None
    n_steps = 500
    delimiter = "()"
    arquivo = None

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

    simulaMT = Simulador(opcao, n_steps, delimiter, arquivo)

    print ""
    print "Simulador de Máquina de Turing ver 1.0"
    print "Desenvolvido como trabalho prático para a disciplina de Teoria da Computação"
    print "Thales Otávio e Pedro Costa, IFMG - Formiga , 2019.\n"
    sys.stdout.write("Forneça a palavra inicial: ")
    palavra = raw_input()

    simulaMT.computa(palavra)


# Erro: "python Principal.py -head {"
#       "python Principal.py -head { arq.mt"

# 0        1         2                 3          4            5
#----------------------------------------------------------------------------
# simulaMT <opções>  <arquivo>                                              | opções = -r ou -v
# simulaMT -s        <n>               <arquivo>
# simulaMT -head     <delimitadores>   <opções>   <arquivo>                 | opções = -r ou -v
# simulaMT -head     <delimitadores>   -s         <n>         <arquivo>


if __name__ == "__main__":
    main()

#Python argparser
