import RPi.GPIO as GPIO
from sys import argv
import socket
import signal
from os import system
from os import getpid
from threading import Thread, Semaphore
from time import sleep
from datetime import datetime
import json

def trataPassagemPrincipal1a(sensor):
    tempo = datetime.now()
    global tempo1, passouPrincipal1
    tempo1 = tempo
    passouPrincipal1 = True

def trataPassagemPrincipal1b(sensor):
    tempo = datetime.now()
    global tempo1, qtdCarrosPrincipal1, qtdAvancoSinalVermelhoPrincipal1, somaVelocidades1, qtdAvancoAcimaVelocidade1, passouPrincipal1
    if passouPrincipal1 == True:
        velocidade = (1 / (tempo - tempo1).total_seconds()) * 3.6
        if(velocidade > 60):
            #system("cvlc example.mp3")
            print("Beep")
            qtdAvancoAcimaVelocidade1 += 1
        somaVelocidades1+=velocidade
        passouPrincipal1 = False
    if (estado != 2 and estado != 3 and estado < 7):
        #system("cvlc example.mp3")
        print("Beep")
        qtdAvancoSinalVermelhoPrincipal1 += 1
    qtdCarrosPrincipal1+=1

def trataPassagemPrincipal2a(sensor):
    tempo = datetime.now()
    global tempo2, passouPrincipal2
    tempo2 = tempo
    passouPrincipal2 = True

def trataPassagemPrincipal2b(sensor):
    tempo = datetime.now()
    global tempo2, qtdCarrosPrincipal2, qtdAvancoSinalVermelhoPrincipal2, somaVelocidades2, qtdAvancoAcimaVelocidade2, passouPrincipal2
    if passouPrincipal2 == True:
        velocidade = (1 / (tempo - tempo2).total_seconds()) * 3.6
        if(velocidade > 60):
            #system("cvlc example.mp3")
            print("Beep")
            qtdAvancoAcimaVelocidade2+=1
        somaVelocidades2+=velocidade
        passouPrincipal2 = False
    if (estado != 2 and estado != 3 and estado < 7):
        #system("cvlc example.mp3")
        print("Beep")
        qtdAvancoSinalVermelhoPrincipal2 += 1
    qtdCarrosPrincipal2+=1

def trataPassagemAux1(sensorPassagem):
    global contador, estado, diminuiTimer1, sensorPassagem1, qtdAvancoSinalVermelhoAux1, saiuSensor1, qtdCarrosAuxiliar1
    if(estado == 2 and diminuiTimer1 == 0):
        controlaContador.acquire()
        diminuiTimer1 = 1
        contador = contador - 10
        controlaContador.release()
    if saiuSensor1 == False: 
        if (estado < 5 or estado == 7):
            #system("cvlc example.mp3")
            print("Beep")
            qtdAvancoSinalVermelhoAux1 += 1
        saiuSensor1 = True  
        qtdCarrosAuxiliar1 += 1  
    else:
        saiuSensor1 = False
    
def trataPassagemAux2(sensorPassagem):
    global contador, estado, diminuiTimer1, sensorPassagem2, qtdAvancoSinalVermelhoAux2, saiuSensor2, qtdCarrosAuxiliar2
    if(estado == 2 and diminuiTimer1 == 0):
        controlaContador.acquire()
        diminuiTimer1 = 1
        contador = contador - 10
        controlaContador.release() 
    if saiuSensor2 == False:
        if estado < 5 or estado == 7:
            #system("cvlc example.mp3")
            print("Beep")
            qtdAvancoSinalVermelhoAux2 += 1
        saiuSensor2 = True
        qtdCarrosAuxiliar2 += 1
    else:
        saiuSensor2 = False

def trataBotao(botao):
    global estado, contador, diminuiTimer1, diminuiTimer2, botao1, botao2
    if(botao == botao1):
        if(estado == 2 and diminuiTimer1 == 0):
            controlaContador.acquire()
            diminuiTimer1 = 1
            contador = contador - 10
            controlaContador.release()
    else:
        if(estado == 5 and diminuiTimer2 == 0):
            controlaContador.acquire()
            diminuiTimer2 = 1
            contador = contador - 5
            controlaContador.release()

def estado_um():
    global estado, contador, diminuiTimer1
    estado = 2
    controlaContador.acquire()
    contador = 20
    diminuiTimer1 = 0
    controlaContador.release()
    GPIO.output(vermelho1, GPIO.LOW)
    GPIO.output(verde1, GPIO.HIGH)

def estado_dois():
    global estado, contador
    estado = 3
    controlaContador.acquire()
    contador = 3
    controlaContador.release()
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.HIGH)

def estado_tres():
    global estado, contador
    estado = 4
    controlaContador.acquire()
    contador = 1
    controlaContador.release()
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.HIGH)

def estado_quatro():
    global estado, contador, diminuiTimer2
    estado = 5
    controlaContador.acquire()
    contador = 10
    diminuiTimer2 = 0
    controlaContador.release()
    GPIO.output(vermelho2, GPIO.LOW)
    GPIO.output(verde2, GPIO.HIGH)

def estado_cinco():
    global estado, contador
    estado = 6
    controlaContador.acquire()
    contador = 3
    controlaContador.release()
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.HIGH)

def estado_seis():
    global estado, contador
    estado = 1
    controlaContador.acquire()
    contador = 1
    controlaContador.release()
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.HIGH)
    GPIO.output(vermelho2, GPIO.HIGH)

def estado_emergencia():
    GPIO.output(verde1, GPIO.HIGH)
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.LOW)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho2, GPIO.HIGH)  

def estado_noturno1():
    global estado, contador
    estado = 9
    controlaContador.acquire()
    contador = 1
    controlaContador.release()
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.LOW)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho2, GPIO.LOW)

def estado_noturno2():
    global estado, contador
    estado = 8
    controlaContador.acquire()
    contador = 1
    controlaContador.release()
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.HIGH)
    GPIO.output(vermelho1, GPIO.LOW)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.HIGH)
    GPIO.output(vermelho2, GPIO.LOW)

mudaEstado = {
    1: estado_um,
    2: estado_dois,
    3: estado_tres,
    4: estado_quatro,
    5: estado_cinco,
    6: estado_seis,
    7: estado_emergencia,
    8: estado_noturno1,
    9: estado_noturno2,
}

def muda_estado():
    global estado
    mudaEstado.get(estado)()

def estado_inicial1():
    # Inicialização de variáveis
    global tempoTotal, controlaContador, estado, verde1, amarelo1, vermelho1, verde2, amarelo2, vermelho2, botao1, botao2, diminuiTimer1, diminuiTimer2, sensorPassagem1, sensorPassagem2, qtdAvancoSinalVermelhoAux1, qtdAvancoSinalVermelhoAux2, tempo1, tempo2, qtdCarrosPrincipal1, qtdAvancoSinalVermelhoPrincipal1, qtdCarrosPrincipal2, qtdAvancoSinalVermelhoPrincipal2, somaVelocidades1, somaVelocidades2, qtdAvancoAcimaVelocidade1, qtdAvancoAcimaVelocidade2, encerramento, saiuSensor1, saiuSensor2, qtdCarrosAuxiliar1, qtdCarrosAuxiliar2, passouPrincipal1, passouPrincipal2
    passouPrincipal1 = False
    passouPrincipal2 = False
    qtdCarrosAuxiliar1 = 0
    qtdCarrosAuxiliar2 = 0
    encerramento = 0
    tempoTotal = 1
    qtdAvancoAcimaVelocidade1 = 0
    qtdAvancoAcimaVelocidade2 = 0
    somaVelocidades1 = 0
    somaVelocidades2 = 0
    qtdCarrosPrincipal1 = 0
    qtdAvancoSinalVermelhoPrincipal1 = 0
    qtdCarrosPrincipal2 = 0
    qtdAvancoSinalVermelhoPrincipal2 = 0
    qtdAvancoSinalVermelhoAux1 = 0
    qtdAvancoSinalVermelhoAux2 = 0
    controlaContador = Semaphore(1)
    estado = 6

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Saídas:
    verde1 = 20
    amarelo1 = 16
    vermelho1 = 12
    GPIO.setup(verde1, GPIO.OUT)
    GPIO.setup(amarelo1, GPIO.OUT)
    GPIO.setup(vermelho1, GPIO.OUT)
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.HIGH)
    
    verde2 = 1
    amarelo2 = 26
    vermelho2 = 21
    GPIO.setup(verde2, GPIO.OUT)
    GPIO.setup(amarelo2, GPIO.OUT)
    GPIO.setup(vermelho2, GPIO.OUT)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho2, GPIO.HIGH)
    
    # Entradas:
    botao1 = 8
    botao2 = 7
    diminuiTimer1 = 0
    diminuiTimer2 = 0
    GPIO.setup(botao1, GPIO.IN)
    GPIO.setup(botao2, GPIO.IN)
    GPIO.add_event_detect(botao1, GPIO.BOTH, callback = trataBotao)
    GPIO.add_event_detect(botao2, GPIO.BOTH, callback = trataBotao)
    
    sensorPassagem1 = 14
    sensorPassagem2 = 15
    saiuSensor1 = True
    saiuSensor2 = True
    GPIO.setup(sensorPassagem1, GPIO.IN)
    GPIO.setup(sensorPassagem2, GPIO.IN)
    GPIO.add_event_detect(sensorPassagem1, GPIO.BOTH, callback = trataPassagemAux1)
    GPIO.add_event_detect(sensorPassagem2, GPIO.BOTH, callback = trataPassagemAux2)

    tempo1 = 0 
    tempo2 = 0
    sensoresVelocidade1a = 23
    sensoresVelocidade1b = 18
    sensoresVelocidade2a = 25
    sensoresVelocidade2b = 24
    GPIO.setup(sensoresVelocidade1a, GPIO.IN)
    GPIO.setup(sensoresVelocidade1b, GPIO.IN)
    GPIO.setup(sensoresVelocidade2a, GPIO.IN)
    GPIO.setup(sensoresVelocidade2b, GPIO.IN)
    GPIO.add_event_detect(sensoresVelocidade1a, GPIO.FALLING, callback = trataPassagemPrincipal1a)
    GPIO.add_event_detect(sensoresVelocidade1b, GPIO.FALLING, callback = trataPassagemPrincipal1b)
    GPIO.add_event_detect(sensoresVelocidade2a, GPIO.FALLING, callback = trataPassagemPrincipal2a)
    GPIO.add_event_detect(sensoresVelocidade2b, GPIO.FALLING, callback = trataPassagemPrincipal2b)

def estado_inicial2():
    global tempoTotal, controlaContador, estado, verde1, amarelo1, vermelho1, verde2, amarelo2, vermelho2, botao1, botao2, diminuiTimer1, diminuiTimer2, sensorPassagem1, sensorPassagem2, qtdAvancoSinalVermelhoAux1, qtdAvancoSinalVermelhoAux2, tempo1, tempo2, qtdCarrosPrincipal1, qtdAvancoSinalVermelhoPrincipal1, qtdCarrosPrincipal2, qtdAvancoSinalVermelhoPrincipal2, somaVelocidades1, somaVelocidades2, qtdAvancoAcimaVelocidade1, qtdAvancoAcimaVelocidade2, encerramento, saiuSensor1, saiuSensor2, qtdCarrosAuxiliar1, qtdCarrosAuxiliar2, passouPrincipal1, passouPrincipal2
    passouPrincipal1 = False
    passouPrincipal2 = False
    qtdCarrosAuxiliar1 = 0
    qtdCarrosAuxiliar2 = 0
    encerramento = 0
    tempoTotal = 1
    qtdAvancoAcimaVelocidade1 = 0
    qtdAvancoAcimaVelocidade2 = 0
    somaVelocidades1 = 0
    somaVelocidades2 = 0
    qtdCarrosPrincipal1 = 0
    qtdAvancoSinalVermelhoPrincipal1 = 0
    qtdCarrosPrincipal2 = 0
    qtdAvancoSinalVermelhoPrincipal2 = 0
    qtdAvancoSinalVermelhoAux1 = 0
    qtdAvancoSinalVermelhoAux2 = 0
    controlaContador = Semaphore(1)
    estado = 6
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Saídas:
    verde1 = 0
    amarelo1 = 5
    vermelho1 = 6
    GPIO.setup(verde1, GPIO.OUT)
    GPIO.setup(amarelo1, GPIO.OUT)
    GPIO.setup(vermelho1, GPIO.OUT)
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.HIGH)
    
    verde2 = 2
    amarelo2 = 3
    vermelho2 = 11
    GPIO.setup(verde2, GPIO.OUT)
    GPIO.setup(amarelo2, GPIO.OUT)
    GPIO.setup(vermelho2, GPIO.OUT)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho2, GPIO.HIGH)
    
    # Entradas:
    botao1 = 10
    botao2 = 9
    diminuiTimer1 = 0
    diminuiTimer2 = 0
    GPIO.setup(botao1, GPIO.IN)
    GPIO.setup(botao2, GPIO.IN)
    GPIO.add_event_detect(botao1, GPIO.BOTH, callback = trataBotao)
    GPIO.add_event_detect(botao2, GPIO.BOTH, callback = trataBotao)
    
    sensorPassagem1 = 4
    sensorPassagem2 = 17
    saiuSensor1 = True
    saiuSensor2 = True
    GPIO.setup(sensorPassagem1, GPIO.IN)
    GPIO.setup(sensorPassagem2, GPIO.IN)
    GPIO.add_event_detect(sensorPassagem1, GPIO.BOTH, callback = trataPassagemAux1)
    GPIO.add_event_detect(sensorPassagem2, GPIO.BOTH, callback = trataPassagemAux2)

    tempo1 = 0 
    tempo2 = 0
    sensoresVelocidade1a = 22
    sensoresVelocidade1b = 27
    sensoresVelocidade2a = 13
    sensoresVelocidade2b = 19
    GPIO.setup(sensoresVelocidade1a, GPIO.IN)
    GPIO.setup(sensoresVelocidade1b, GPIO.IN)
    GPIO.setup(sensoresVelocidade2a, GPIO.IN)
    GPIO.setup(sensoresVelocidade2b, GPIO.IN)
    GPIO.add_event_detect(sensoresVelocidade1a, GPIO.FALLING, callback = trataPassagemPrincipal1a)
    GPIO.add_event_detect(sensoresVelocidade1b, GPIO.FALLING, callback = trataPassagemPrincipal1b)
    GPIO.add_event_detect(sensoresVelocidade2a, GPIO.FALLING, callback = trataPassagemPrincipal2a)
    GPIO.add_event_detect(sensoresVelocidade2b, GPIO.FALLING, callback = trataPassagemPrincipal2b)

def finalizaModoEspecial():
    global contador, estado, cruzamento
    if(estado >= 7):
        contador = 0
        estado = 6
        print("Estado especial desativado")
        
def modoEmergencia():
    global estado, contador
    estado = 7
    controlaContador.acquire()
    contador = 0
    controlaContador.release()
    print("Modo emergência ativado!")

def modoNoturno():
    global estado, contador
    estado = 9
    controlaContador.acquire()
    contador = 0
    controlaContador.release()
    print("Modo noturno ativado!")

def escutaServidor():
    global tcp, encerramento
    while encerramento == 0:
        try:
            msg = int(tcp.recv(60).decode())
        except:
            break
        else:
            if msg == 1:
                modoEmergencia()
            elif msg == 2:
                modoNoturno()
            elif msg == 3:
                finalizaModoEspecial()

def conexaoServidor():
    while encerramento == 0:
        global cruzamento, tcp
        if cruzamento == 1 or cruzamento == 2:
            HOST = '127.0.0.1'
        else:
            HOST = '192.168.1.103'
        PORT = 10000 + cruzamento
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (HOST, PORT)
        conectado = False
        while conectado == False and encerramento == 0:
            try:
                tcp.connect(dest)
                tcp.send(str(cruzamento).encode())
            except:
                sleep(1)
            else:
                conectado = True
                print("Servidor conectado!")
        if conectado == True:
            threadEscuta = Thread(target=escutaServidor)
            threadEscuta.start()
            while conectado == True and encerramento == 0:
                if(qtdCarrosPrincipal1 + qtdCarrosPrincipal2 == 0):
                    Velocidade_Media = 0
                    Infracoes_Velocidade = 0
                    if qtdCarrosAuxiliar1 + qtdCarrosAuxiliar2 == 0:
                        Fluxo_Carros = 0
                else:
                    Velocidade_Media = (somaVelocidades1 + somaVelocidades2)/(qtdCarrosPrincipal1 + qtdCarrosPrincipal2)
                    Fluxo_Carros = (qtdCarrosPrincipal1 + qtdCarrosPrincipal2+ qtdCarrosAuxiliar1 + qtdCarrosAuxiliar2)/(tempoTotal/60.0)
                Infracoes_Velocidade = qtdAvancoAcimaVelocidade1 + qtdAvancoAcimaVelocidade2
                Infracoes_Avanco_Sinal = qtdAvancoSinalVermelhoPrincipal1 + qtdAvancoSinalVermelhoPrincipal2 + qtdAvancoSinalVermelhoAux1 + qtdAvancoSinalVermelhoAux2
                dados = json.dumps({'Fluxo_Carros': Fluxo_Carros, 'Via_principal1':qtdCarrosPrincipal1, 'Via_principal2':qtdCarrosPrincipal2, 'Via_auxiliar1':qtdCarrosAuxiliar1, 'Via_auxiliar2':qtdCarrosAuxiliar2, 'Velocidade_Media':Velocidade_Media, 'Infracoes_Avanco_Sinal':Infracoes_Avanco_Sinal, 'Infracoes_Velocidade':Infracoes_Velocidade})
                try:
                    tcp.send(dados.encode())
                except:
                    print("Não foi possível enviar dados ao servidor!")
                    conectado = False
                else:
                    sleep(2)
        if(conectado == True):
            tcp.send("encerrado".encode())
        tcp.close()

def finalizaPrograma(signum, frame):
    global encerramento, contador, estado
    estado = 1
    encerramento = 1
    contador = 0


signal.signal(signal.SIGINT, finalizaPrograma)
global cruzamento, porta
cruzamento = int(argv[1])
if cruzamento == 1 or cruzamento == 3:
    estado_inicial1()
elif cruzamento == 2 or cruzamento == 4:
    estado_inicial2()
else:
    print("Cruzamento inválido!")
    exit(0)

threadComunicacao = Thread(target=conexaoServidor)
threadComunicacao.start()

while encerramento == 0:
    muda_estado()
    if(estado == 7):
        print("Estado de emergência ativado")
        while(estado == 7):
            estado_emergencia()
            tempoTotal+=1
            sleep(1)
    while(contador >= 1):
        sleep(1)
        #print(contador)
        controlaContador.acquire()
        contador -= 1
        controlaContador.release()
        tempoTotal+=1
threadComunicacao.join()