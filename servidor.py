import threading
import socket
from time import sleep
import json
import signal
from os import kill

def trataDados(msg):
    print(f'   Fluxo de carros: {int(msg["Fluxo_Carros"])} carros por minuto')
    print(f'   Carros na via principal 1: {msg["Via_principal1"]}')
    print(f'   Carros na via principal 2: {msg["Via_principal2"]}')
    print(f'   Carros na via auxiliar 1: {msg["Via_auxiliar1"]}')
    print(f'   Carros na via auxiliar 2: {msg["Via_auxiliar2"]}')
    print(f'   Velocidade média: {round(msg["Velocidade_Media"], 2)} km/h')
    print(f'   Infrações por avanço de sinal: {msg["Infracoes_Avanco_Sinal"]}')
    print(f'   Infrações por velocidade: {msg["Infracoes_Velocidade"]}')

def trataMensagens(client, cruzamento):
    while True:
        try:
            msg = client.recv(1024).decode()
            if(msg == "encerrado" or msg == ''):
                break
        except:
            del cruzamentos[cruzamento]
            break
        print(f'Cruzamento {cruzamento}:')
        trataDados(json.loads(msg))
    print(f'\nCruzamento {cruzamento} desligado\n')

def recebeInput():
    while True:
        acao = int(input("Digite 1 para acionar estado de emergência, 2 para acionar estado noturno ou 3 para resetar (estado normal)"))
        if(acao == 1):
            cruzamento = input("Digite 'a' para os cruzamentos 1 e 2 ou 'b' para os cruzamentos 3 e 4")
            if(cruzamento == 'a'):
                if(1 in cruzamentos):
                    kill(cruzamentos[1].get("pid"), signal.SIGUSR1)
                if(2 in cruzamentos):
                    kill(cruzamentos[2].get("pid"), signal.SIGUSR1)
            elif(cruzamento == 'b'):
                if(3 in cruzamentos):
                    kill(cruzamentos[3].get("pid"), signal.SIGUSR1)
                if(4 in cruzamentos):
                    kill(cruzamentos[4].get("pid"), signal.SIGUSR1)
        elif(acao == 2):
            if(1 in cruzamentos):
                kill(cruzamentos[1].get("pid"), signal.SIGUSR2)
            if(2 in cruzamentos):
                kill(cruzamentos[2].get("pid"), signal.SIGUSR2)
            if(3 in cruzamentos):
                kill(cruzamentos[3].get("pid"), signal.SIGUSR2)
            if(4 in cruzamentos):
                kill(cruzamentos[4].get("pid"), signal.SIGUSR2)
        elif(acao == 3):
                cruzamento = int(input("Digite o cruzamento desejado ou 0 para resetar todos os cruzamentos"))
                if cruzamento == 0:
                    if(1 in cruzamentos):
                        kill(cruzamentos[1].get("pid"), signal.SIGTSTP)
                    if(2 in cruzamentos):
                        kill(cruzamentos[2].get("pid"), signal.SIGTSTP)
                    if(3 in cruzamentos):
                        kill(cruzamentos[3].get("pid"), signal.SIGTSTP)
                    if(4 in cruzamentos):
                        kill(cruzamentos[4].get("pid"), signal.SIGTSTP)
                else:
                    if(cruzamento in cruzamentos):
                        kill(cruzamentos[cruzamento].get("pid"), signal.SIGTSTP)
        else:
            print("Opção Inválida!")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global cruzamentos
    cruzamentos = {}
    try:
        server.bind(('localhost', 10000))
        server.listen(4)
    except:
        print('\nNão foi possível iniciar o servidor!\n')
        return
    threadAcao = threading.Thread(target=recebeInput)
    threadAcao.start()
    while True:
        client, endereco = server.accept()
        dados = json.loads(client.recv(1024).decode())
        cruzamento = dados["cruzamento"] 
        pid = dados["pid"]
        cruzamentos[cruzamento] = {"client":client, "pid":pid}
        print(f'Cruzamento {cruzamento} conectado!')
        thread = threading.Thread(target=trataMensagens, args=(client, cruzamento))
        thread.start()
main()

"""
import threading
import socket
from time import sleep
import json
import signal
from os import kill

def trataDados(msg):
    print(f'   Fluxo de carros: {int(msg["Fluxo_Carros"])} carros por minuto')
    print(f'   Carros na via principal 1: {msg["Via_principal1"]}')
    print(f'   Carros na via principal 2: {msg["Via_principal2"]}')
    print(f'   Carros na via auxiliar 1: {msg["Via_auxiliar1"]}')
    print(f'   Carros na via auxiliar 2: {msg["Via_auxiliar2"]}')
    print(f'   Velocidade média: {round(msg["Velocidade_Media"], 2)} km/h')
    print(f'   Infrações por avanço de sinal: {msg["Infracoes_Avanco_Sinal"]}')
    print(f'   Infrações por velocidade: {msg["Infracoes_Velocidade"]}')

def trataMensagens(client, cruzamento):
    global encerramento
    while encerramento == 0:
        try:
            msg = client.recv(250).decode()
            if(msg == "encerrado" or msg == ''):
                break
        except:
            del cruzamentos[cruzamento]
            break
        print(f'Cruzamento {cruzamento}:')
        trataDados(json.loads(msg))
    print(f'\nCruzamento {cruzamento} desligado\n')

def recebeInput():
    global encerramento
    while encerramento == 0:
        acao = int(input("Digite 1 para acionar estado de emergência, 2 para acionar estado noturno ou 3 para resetar (estado normal)"))
        if(acao == 1):
            cruzamento = input("Digite 'a' para os cruzamentos 1 e 2 ou 'b' para os cruzamentos 3 e 4")
            if(cruzamento == 'a'):
                if(1 in cruzamentos):
                    kill(cruzamentos[1].get("pid"), signal.SIGUSR1)
                if(2 in cruzamentos):
                    kill(cruzamentos[2].get("pid"), signal.SIGUSR1)
            elif(cruzamento == 'b'):
                if(3 in cruzamentos):
                    kill(cruzamentos[3].get("pid"), signal.SIGUSR1)
                if(4 in cruzamentos):
                    kill(cruzamentos[4].get("pid"), signal.SIGUSR1)
        elif(acao == 2):
            if(1 in cruzamentos):
                kill(cruzamentos[1].get("pid"), signal.SIGUSR2)
            if(2 in cruzamentos):
                kill(cruzamentos[2].get("pid"), signal.SIGUSR2)
            if(3 in cruzamentos):
                kill(cruzamentos[3].get("pid"), signal.SIGUSR2)
            if(4 in cruzamentos):
                kill(cruzamentos[4].get("pid"), signal.SIGUSR2)
        elif(acao == 3):
                cruzamento = int(input("Digite o cruzamento desejado ou 0 para resetar todos os cruzamentos"))
                if cruzamento == 0:
                    if(1 in cruzamentos):
                        kill(cruzamentos[1].get("pid"), signal.SIGTSTP)
                    if(2 in cruzamentos):
                        kill(cruzamentos[2].get("pid"), signal.SIGTSTP)
                    if(3 in cruzamentos):
                        kill(cruzamentos[3].get("pid"), signal.SIGTSTP)
                    if(4 in cruzamentos):
                        kill(cruzamentos[4].get("pid"), signal.SIGTSTP)
                else:
                    if(cruzamento in cruzamentos):
                        kill(cruzamentos[cruzamento].get("pid"), signal.SIGTSTP)
        elif(acao == 0):
            encerramento = 1
            print("Encerrando Servidor!")
            break
        else:
            print("Opção Inválida!")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    global cruzamentos, encerramento
    encerramento = 0
    cruzamentos = {}
    try:
        server.bind(('localhost', 10000))
        server.listen(4)
    except:
        print('\nNão foi possível iniciar o servidor!\n')
        return
    
    threadAcao = threading.Thread(target=recebeInput)
    threadAcao.start()
    while encerramento == 0:
        client, endereco = server.accept()
        dados = json.loads(client.recv(60).decode())
        cruzamento = dados["cruzamento"] 
        pid = dados["pid"]
        cruzamentos[cruzamento] = {"client":client, "pid":pid}
        print(f'Cruzamento {cruzamento} conectado!\n')
        thread = threading.Thread(target=trataMensagens, args=(client, cruzamento))
        thread.start()
main()
"""
