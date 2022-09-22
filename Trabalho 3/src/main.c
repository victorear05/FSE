#include "bib.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"    
#include "freertos/semphr.h"
#include "nvs_flash.h"
#include "driver/gpio.h"

float mediaTemperatura;
int temperaturaAtual;

float mediaUmidade;
int umidadeAtual;

int estado_led = 0;

xSemaphoreHandle temDadosTemp;
xSemaphoreHandle temDadosUmidade;
xSemaphoreHandle conexaoWifiSemaphore;
xSemaphoreHandle conexaoMQTTSemaphore;

void trataComunicacaoComServidor(void * params) { 
    char mensagem[200];
    if(xSemaphoreTake(conexaoMQTTSemaphore, portMAX_DELAY)) {
        while(true) {
            if(xSemaphoreTake(temDadosTemp, portMAX_DELAY) && xSemaphoreTake(temDadosUmidade, portMAX_DELAY)) {
                sprintf(mensagem, "{\"temperatura\":%d,\"temperaturaMedia\":%f,\"umidade\":%d,\"umidadeMedia\":%f}", temperaturaAtual, mediaTemperatura, umidadeAtual, mediaUmidade);
                mqtt_envia_mensagem("v1/devices/me/telemetry", mensagem);
                sprintf(mensagem, "{\"temperatura\":%d,\"temperaturaMedia\":%f,\"umidade\":%d,\"umidadeMedia\":%f}", temperaturaAtual, mediaTemperatura, umidadeAtual, mediaUmidade);
                mqtt_envia_mensagem("v1/devices/me/attributes", mensagem);
                vTaskDelay(1000 / portTICK_PERIOD_MS);
            }
        }
    }
}

void conectadoWifi(void * params)
{
    while(true)
        if(xSemaphoreTake(conexaoWifiSemaphore, portMAX_DELAY))
            mqtt_start();
}

void controla_sensor() {
    temDadosTemp = xSemaphoreCreateBinary();
    temDadosUmidade = xSemaphoreCreateBinary();
    sensorMain();
}

void app_main() {
    xTaskCreate(&controla_sensor, "Inicia sensores", 2048, NULL, 1, NULL);
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND)
    {
      ESP_ERROR_CHECK(nvs_flash_erase());
      ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
    conexaoWifiSemaphore = xSemaphoreCreateBinary();
    conexaoMQTTSemaphore = xSemaphoreCreateBinary();
    wifi_start();

    xTaskCreate(&conectadoWifi,  "Conexão ao MQTT", 4096, NULL, 1, NULL);
    xTaskCreate(&trataComunicacaoComServidor,  "Comunicação com o Broker", 4096, NULL, 1, NULL);
    configura_led();
    inicializa_botao();
}
