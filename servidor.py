import threading
import socket
from time import sleep
import json

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

def recebeCruzamento(server, cruzamento):
    server.bind(('', 10000+cruzamento))
    server.listen(1)
    while encerramento == 0:
        client, endereco = server.accept()
        cruzamento = int(client.recv(60).decode())
        cruzamentos[cruzamento] = client
        print(f'Cruzamento {cruzamento} conectado!\n')
        thread = threading.Thread(target=trataMensagens, args=(client, cruzamento))
        thread.start()


def main():
    global cruzamentos, encerramento
    encerramento = 0

    server1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cruzamentos = {}
    cruzamento1 = threading.Thread(target=recebeCruzamento, args=(server1, 1))
    cruzamento1.start()

    server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cruzamento2 = threading.Thread(target=recebeCruzamento, args=(server2, 2))
    cruzamento2.start()

    server3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cruzamento3 = threading.Thread(target=recebeCruzamento, args=(server3, 3))
    cruzamento3.start()

    server4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cruzamento4 = threading.Thread(target=recebeCruzamento, args=(server4, 4))
    cruzamento4.start()
    
    while encerramento == 0:
        acao = int(input("Digite 1 para acionar estado de emergência, 2 para acionar estado noturno ou 3 para resetar (estado normal)"))
        if(acao == 1):
            cruzamento = input("Digite 'a' para os cruzamentos 1 e 2 ou 'b' para os cruzamentos 3 e 4")
            if(cruzamento == 'a'):
                if(1 in cruzamentos):
                    cruzamentos[1].send(str(1).encode())
                if(2 in cruzamentos):
                    cruzamentos[2].send(str(1).encode())
            elif(cruzamento == 'b'):
                if(3 in cruzamentos):
                    cruzamentos[3].send(str(1).encode())
                if(4 in cruzamentos):
                    cruzamentos[4].send(str(1).encode())
        elif(acao == 2):
            if(1 in cruzamentos):
                cruzamentos[1].send(str(2).encode())
            if(2 in cruzamentos):
                cruzamentos[2].send(str(2).encode())
            if(3 in cruzamentos):
                cruzamentos[1].send(str(2).encode())
            if(4 in cruzamentos):
                cruzamentos[1].send(str(2).encode())
        elif(acao == 3):
                cruzamento = int(input("Digite o cruzamento desejado ou 0 para resetar todos os cruzamentos"))
                if cruzamento == 0:
                    if(1 in cruzamentos):
                        cruzamentos[1].send(str(3).encode())
                    if(2 in cruzamentos):
                        cruzamentos[2].send(str(3).encode())
                    if(3 in cruzamentos):
                        cruzamentos[3].send(str(3).encode())
                    if(4 in cruzamentos):
                        cruzamentos[4].send(str(3).encode())
                else:
                    if(cruzamento in cruzamentos):
                        cruzamentos[cruzamento].send(str(3).encode())
        elif(acao == 0):
            encerramento = 1
            print("Encerrando Servidor!")
            break
        else:
            print("Opção Inválida!")
main()