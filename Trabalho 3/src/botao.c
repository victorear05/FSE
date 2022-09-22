#include "bib.h"
#include <stdio.h>
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#define ESP_INTR_FLAG_DEFAULT 14
#define CONFIG_BUTTON_PIN 14

#define LED_1 2

TaskHandle_t ISR = NULL;
extern int estado_led;

void IRAM_ATTR button_isr_handler(void* arg) {
    xTaskResumeFromISR(ISR);
}

void button_task(void *arg)
{
    char mensagem[200];
    while(1){
        vTaskSuspend(NULL);
        vTaskDelay(200 / portTICK_PERIOD_MS);
        estado_led = !estado_led;
        gpio_set_level(LED_1, estado_led);
        sprintf(mensagem, "{\"estadoLed\":%d}", estado_led);
        mqtt_envia_mensagem("v1/devices/me/telemetry", mensagem);
    }
}

void inicializa_botao()
{
    gpio_pad_select_gpio(CONFIG_BUTTON_PIN);
    gpio_set_direction(CONFIG_BUTTON_PIN, GPIO_MODE_INPUT);
    gpio_set_intr_type(CONFIG_BUTTON_PIN, GPIO_INTR_NEGEDGE);
    gpio_install_isr_service(ESP_INTR_FLAG_DEFAULT);
    gpio_isr_handler_add(CONFIG_BUTTON_PIN, button_isr_handler, NULL);
    xTaskCreate( button_task, "button_task", 2048, NULL , 10,&ISR );
}
