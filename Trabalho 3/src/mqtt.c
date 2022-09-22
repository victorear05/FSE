#include "bib.h"

#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>
#include "esp_system.h"
#include "esp_event.h"
#include "esp_netif.h"

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"

#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"

#include "esp_log.h"
#include "mqtt_client.h"
#include "cJSON.h"

#define TAG "MQTT"

#define ACESS_TOKEN CONFIG_ESP_ACESS_TOKEN

extern xSemaphoreHandle conexaoMQTTSemaphore;
esp_mqtt_client_handle_t client;

void trata_dados(char * dado) {
    char mensagem[200];
    cJSON *json = cJSON_Parse(dado);
    cJSON *method = cJSON_GetObjectItem(json, "method");
    char method_value[20];
    strcpy(method_value, method->valuestring);
    ESP_LOGI(TAG, "method: %s", method_value);
    cJSON *params = cJSON_GetObjectItem(json, "params");
    int params_value = params->valueint;
    ESP_LOGI(TAG, "params: %d", params_value);
    if(strcmp(method_value, "ligaDesliga") == 0) {
        sprintf(mensagem, "{\"estadoLed\":%d}", params_value);
        mqtt_envia_mensagem("v1/devices/me/telemetry", mensagem);
    }
    else {
        altera_led(params_value);
    }
}

static esp_err_t mqtt_event_handler_cb(esp_mqtt_event_handle_t event)
{
    esp_mqtt_client_handle_t client = event->client;

    switch (event->event_id) {
        case MQTT_EVENT_CONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_CONNECTED");
            xSemaphoreGive(conexaoMQTTSemaphore);
            esp_mqtt_client_subscribe(client, "v1/devices/me/rpc/request/+", 0);
            break;
        case MQTT_EVENT_DISCONNECTED:
            ESP_LOGI(TAG, "MQTT_EVENT_DISCONNECTED");
            break;
        case MQTT_EVENT_SUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_SUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_UNSUBSCRIBED:
            ESP_LOGI(TAG, "MQTT_EVENT_UNSUBSCRIBED, msg_id=%d", event->msg_id);
            break;
        case MQTT_EVENT_PUBLISHED:
            break;
        case MQTT_EVENT_DATA:
            ESP_LOGI(TAG, "MQTT_EVENT_DATA");
            trata_dados(event->data);
            break;
        case MQTT_EVENT_ERROR:
            ESP_LOGI(TAG, "MQTT_EVENT_ERROR");
            break;
        default:
            ESP_LOGI(TAG, "Other event id:%d", event->event_id);
            break;  
    }
    return ESP_OK;
} 

static void mqtt_event_handler(void *handler_args, esp_event_base_t base, int32_t event_id, void *event_data) {
    ESP_LOGD(TAG, "Event dispatched from event loop base=%s, event_id=%d", base, event_id);
    mqtt_event_handler_cb(event_data);
}


void mqtt_start() 
{
    esp_mqtt_client_config_t mqtt_config = {
        .uri = "mqtt://164.41.98.25",
        .username = ACESS_TOKEN
    };
    client = esp_mqtt_client_init(&mqtt_config);
    esp_mqtt_client_register_event(client, ESP_EVENT_ANY_ID, mqtt_event_handler, client);
    esp_mqtt_client_start(client);
}

void mqtt_envia_mensagem(char * topico, char * mensagem)
{
    esp_mqtt_client_publish(client, topico, mensagem, 0, 1, 0);
}
