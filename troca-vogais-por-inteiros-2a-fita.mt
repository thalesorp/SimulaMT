;--------------------------------------------------------------
;  Teste do simulador de MT
;
;  Objetivo: copia uma frase substituindo vogais por inteiros.
;            a=1, e=2, i=3, o=4, u=5
;
;  Entrada: uma frase no alfabeto [a-zA-Z] terminada com .
;  Cabeçote inicia no 1o caractere não-branco
;
;  Saida: a frase clonada, com vogais substituidas
;
;  ATENCAO: o programa nao trata entradas invalidas!!
;
;  Exemplo:
;      ENTRADA: Este exemplo funciona.
;      SAIDA:   Este exemplo funciona. 2st2 2x2mpl4 f5nc34n1.
;--------------------------------------------------------------

bloco main 1   
   1 copiar 5      ; acha a letra de referencia
   5 * -- # i 10   ; marca o local da referencia
   10 clonaCar 15  ; vai para o local da cópia, copia e volta
   15 colar 20     ; restaura a letra de referencia
   20 . -- . i 30  ; o loop termina no .
   20 * -- * d 1   ; passa para a letra seguinte
   30 * -- * i pare_aceita
fim ; main


; INICIA com cabecote no # e o caractere na 2a fita
; move ate o branco onde deve copiar o caractere da 2a fita
; (move ate o . e depois ate o branco)
; copia o caractere
; volta ate o #
; TERMINA com cabecote no #
bloco clonaCar 1
   1 [.] -- * d 5 ; procura o branco
   1 [*] -- * i 3 ; precisa o . antes
   ; procura o .
   3 . -- * d 5    
   3 * -- * d 3
   ; procura o branco depois do .
   5 _ -- * i 10
   5 * -- * d 5
   ; chegou no local da copia
   10 fazCopia 15
   15 voltaRef 20
   20 # -- # i retorne
fim ; clonaCar

; INICIA com cabecote no branco onde faz a copia e o caractere na 2a fita
; copia fazendo as alteracoes com as vogais
; TERMINA com cabecote no caractere que foi copiado
bloco fazCopia 1
   1 [a] -- 1 i 10
   1 [e] -- 2 i 10
   1 [i] -- 3 i 10
   1 [o] -- 4 i 10
   1 [u] -- 5 i 10
   1 [A] -- 1 i 10
   1 [E] -- 2 i 10
   1 [I] -- 3 i 10
   1 [O] -- 4 i 10
   1 [U] -- 5 i 10
   1 colar 10
   10 * -- * i retorne
fim ; fazCopia

; INICIA com cabecote no caractere clonado e o caractere de referencia na 2a fita
; volta ate o #
; TERMINA com cabecote no #
bloco voltaRef 1
   1 # -- * i retorne
   1 * -- * e 1
fim ; voltaRef



