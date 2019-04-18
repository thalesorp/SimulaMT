#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

class Simulador(object):
    # Atributos

    # Construtor
    def __init__(self, opcao, n_steps, delimiter, arquivo):
        print "opcao =", opcao
        print "n_steps =", n_steps
        print "delimiter =", delimiter
        print "arquivo =", arquivo

    # Métodos


# 0        1         2                 3          4            5
#----------------------------------------------------------------------------------------------------
# simulaMT <opções>  <arquivo>                                              | opções = -r ou -v
# simulaMT -s        <n>               <arquivo>
# simulaMT -head     <delimitadores>   <opções>   <arquivo>                 | opções = -r ou -v
# simulaMT -head     <delimitadores>   -s         <n>         <arquivo>