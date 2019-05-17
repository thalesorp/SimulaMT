# SimulaMT

Um simulador da Máquina de Turing com duas fitas.


## Pré-requisitos

Será necessário apenas a versão 2.7 do Python para a compilação do código fonte.


## Como usar?

### Arquivo .mt

Um arquivo .mt é usado para definir um código fonte de algum algoritmo para a máquina de Turing. Existem dois algoritmos exemplos neste repositório: um reconhecedor de palíndromos e um algoritmo que troca vocais por números inteiros, sendo o segundo um exemplo da utilização da segunda fita.
Veja ``reconhecedor-palindromo.mt`` e ``troca-vogais-por-inteiros-2a-fita.mt`` para mais informações.
### Argumentos

Primeiramente será necessário informar o arquivo a ser simulado. Apois isso existem três opções de execução da máquina:

```
- "-r" ou "--resume": executa o programa até o fim em modo silencioso;
- "-v" ou "--verbose": executa até o fim mostrando o resultado passo a passo da execução;
- "-s N" ou "--steps N": mostra o resultado passo a passo de N computações, depois espera o usuário inserir uma nova opção para ser executada. O padrão é repetir a mesma opção fornecida anteriormente.
```

Um parâmetro optativo é a definição dos caracteres do cabeçote da máquina:

```
- "-head DELIMITADORES": modifica os dois caracteres delimitadores, esquerdo e direito, do cabeçote.
```


### Funções do simulador

Depois de instanciado um objeto do tipo ``Simulador.py``, usar a seguinte função:

```python
simulaMT.compila(palavra)
```

O argumento passado por parâmetro é a palavra a ser compilada pelo seu código de máquina de Turing.


## Autores

* **Thales Otávio** – @ThalesORP – *ThalesORP@gmail.com* – [ThalesORP](https://github.com/ThalesORP)
* **Pedro Costa** – *peducosta17@gmail.com* – [PeduCosta17](https://github.com/PeduCosta17)


## Licença

Distribuído sob a licença *GNU General Public License v3.0*. Veja ``LICENSE`` para mais informações.
