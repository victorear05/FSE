#include "bib.h"
#include <stdio.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "freertos/semphr.h"

#include "dht11.h"

extern int temperaturaAtual;
extern float mediaTemperatura;

extern int umidadeAtual;
extern float mediaUmidade;

extern xSemaphoreHandle temDadosTemp;
extern xSemaphoreHandle temDadosUmidade;

float temperaturas[10];
float umidades[10];

int cont = 0;

void temp() {
    float somaTemperaturas = 0;
    temperaturas[cont%10] = temperaturaAtual;
    int aux = 10;
    for(int i=0;i<=9;i++) {
        if(i<=cont)
            somaTemperaturas += temperaturas[i];
        else {
            aux = i;
            break;
        }
    }
    mediaTemperatura = somaTemperaturas/aux;
    xSemaphoreGive(temDadosTemp);
}

void umidade() {
    float somaUmidades = 0;
    umidades[cont%10] = umidadeAtual;
    int aux = 10;
    for(int i=0;i<=9;i++) {
        if(i<=cont)
            somaUmidades += umidades[i];
        else {
            aux = i;
            break;
        }
    }
    mediaUmidade = somaUmidades/aux;
    xSemaphoreGive(temDadosUmidade);
}
void sensorMain() {
    DHT11_init(4);
    while(true) {
        struct dht11_reading leitura = DHT11_read();
        while(leitura.status != 0) {
            leitura = DHT11_read();
        }
        temperaturaAtual = leitura.temperature;
        umidadeAtual = leitura.humidity;
        temp();
        umidade();
        cont++;
        vTaskDelay(1000 / portTICK_PERIOD_MS);
    }
}

