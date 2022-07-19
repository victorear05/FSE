import RPi.GPIO as GPIO
from time import sleep

def funcSemaforo(verde1, amarelo1, vermelho1, verde2, amarelo2, vermelho2):
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(verde1, GPIO.OUT)
    GPIO.setup(amarelo1, GPIO.OUT)
    GPIO.setup(vermelho1, GPIO.OUT)
    GPIO.setup(verde2, GPIO.OUT)
    GPIO.setup(amarelo2, GPIO.OUT)
    GPIO.setup(vermelho2, GPIO.OUT)
    
    GPIO.output(verde1, GPIO.LOW)
    GPIO.output(amarelo1, GPIO.LOW)
    GPIO.output(vermelho1, GPIO.HIGH)
    GPIO.output(verde2, GPIO.LOW)
    GPIO.output(amarelo2, GPIO.LOW)
    GPIO.output(vermelho2, GPIO.HIGH)
    sleep(1)
    while 1:
        GPIO.output(vermelho1, GPIO.LOW)
        GPIO.output(verde1, GPIO.HIGH)
        sleep(5)
        GPIO.output(verde1, GPIO.LOW)
        GPIO.output(amarelo1, GPIO.HIGH)
        sleep(0.75)
        GPIO.output(amarelo1, GPIO.LOW)
        GPIO.output(vermelho1, GPIO.HIGH) 
        sleep(0.5)
        GPIO.output(vermelho2, GPIO.LOW)
        GPIO.output(verde2, GPIO.HIGH)
        sleep(2.5)
        GPIO.output(verde2, GPIO.LOW)
        GPIO.output(amarelo2, GPIO.HIGH)
        sleep(0.75)
        GPIO.output(amarelo2, GPIO.LOW)
        GPIO.output(vermelho2, GPIO.HIGH)
        sleep(5)

semaforo1 = [20, 16, 12, 1, 26, 21]

funcSemaforo(semaforo1[0], semaforo1[1], semaforo1[2], semaforo1[3], semaforo1[4], semaforo1[5])
"""
GPIO.setmode(GPIO.BCM)
GPIO.setup(8, GPIO.IN)
GPIO.setup(7, GPIO.IN)
while(1):
    if GPIO.input(8) == True:
        print("ola")
"""