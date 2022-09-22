# Trabalho1_FSE
Repositório do Trabalho 1 da disciplina Fundamentos de Sistemas Embarcados da Universidade de Brasília. Tem o objetivo de por em prática os conhecimentos acerca de comunicação TCP/IP usando sockets. O projeto foi feito em Python 3.

## Sobre o Projeto
O projeto tem finalidade de simular o controle de cruzamentos de trânsito, com o uso de duas raspberrys conectadas a leds, botões e sensores conectados nas portas GPIO de cada rasp. Além de controlar os semáforos, é enviado ao servidor a cada 2 segundos, dados coletados em cada cruzamento. Além disso, pode-se mandar os comandos de ligar modo noturno, ligar modo de emergência ou sair voltar ao modo normal para cada cruzamento via terminal do servidor para cada cruzamento. Toda comunicação entre os cruzamentos e o servidore é feita com o uso de sockets com o protocolo TCP/IP.

## Executando 
Para subir e executar um cruzamento, basta executar o arquivo semaforo.py passando o cruzamento desejado:  
`python3 semaforo.py cruzamento` (o projeto só aceita cruzamentos no intervalo de 1 a 4)  
Para subir e executar um servidor, basta executar o arquivo servidor.py:  
`python3 servidor.py`

**O único item que pode variar é o ip da função de conexão com servidor, que depende de qual raspberry terá o servidor rodando.  
**Como não consegui executar os comandos de soltar o som para cada infração, quando ele emitiria um som, é mostrado no terminal do cruzamento "beep".

[Enunciado do trabalho](https://gitlab.com/fse_fga/trabalhos-2022_1/trabalho-1-2022-1)
