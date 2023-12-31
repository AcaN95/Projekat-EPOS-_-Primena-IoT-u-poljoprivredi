#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>

const char *ssid = "Xiaomi 11 Lite 5G NE";
const char *password = "12345678";

ESP8266WebServer server(80);


#include <DHT.h>

#define DHTPIN 2 //d4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);


#define RELAY1_PIN  4  // Povežite prvi relej sa digitalnim pinom d1
#define RELAY2_PIN  5  // Povežite drugi relej sa digitalnim pinom d2


int relayState1 = 1;
int relayState2 = 1;

void setup() {
  Serial.begin(115200);


// Postavljanje pinova releja kao izlaz
  pinMode(RELAY1_PIN, OUTPUT);
  pinMode(RELAY2_PIN, OUTPUT);

  // Isključivanje oba releja na početku
  digitalWrite(RELAY1_PIN, HIGH);
  digitalWrite(RELAY2_PIN, HIGH);

  int relayState1 = digitalRead(RELAY1_PIN);
int relayState2 = digitalRead(RELAY2_PIN);

dht.begin();
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
  Serial.println(WiFi.localIP());

  // Define HTTP endpoints
  server.on("/sensor", HTTP_GET, handleGetSensor);
  server.on("/relay", HTTP_POST, handlePostRelay);
  server.on("/relayState", HTTP_GET, handleGetRelayState);

  server.begin();
}

float temperatura=0;
float vlaznost=0;
void loop() {
  server.handleClient();
  temperatura = dht.readTemperature();
  vlaznost = dht.readHumidity();

  // Provera da li su podaci validni
  if (isnan(temperatura) || isnan(vlaznost)) {
    Serial.println("Nemoguće pročitati podatke sa senzora DHT!");
    return;
  }
}

void handleGetSensor() {
  // Respond with JSON containing sensor data
  StaticJsonDocument<200> doc;
  doc["temperatura"] = temperatura;
   doc["vlaznost"] = vlaznost;

  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handleGetRelayState() {
  // Respond with JSON containing sensor data
  StaticJsonDocument<200> doc;
if(digitalRead(RELAY1_PIN)==0)
  doc["Relay1"] = "ukljucen";
  else doc["Relay1"] = "iskljucen";

  if(digitalRead(RELAY2_PIN)==0)
  doc["Relay2"] = "ukljucen";
  else doc["Relay2"] = "iskljucen";

  String response;
  serializeJson(doc, response);
  server.send(200, "application/json", response);
}

void handlePostRelay() {
  // Parse JSON and set relay state
  StaticJsonDocument<200> doc;
  deserializeJson(doc, server.arg("plain"));
  String jsonString;
serializeJson(doc, jsonString);
Serial.println(jsonString);
  if(doc["relay1"]==1 || doc["relay1"]==0)
  relayState1 = doc["relay1"];

  if(doc["relay2"]==1 || doc["relay2"]==0)
  relayState2 = doc["relay2"];
  if(relayState1==1)
  digitalWrite(RELAY1_PIN, HIGH);
   if(relayState1==0)
  digitalWrite(RELAY1_PIN, LOW);

  if(relayState2==1)
  digitalWrite(RELAY2_PIN, HIGH);
   if(relayState2==0)
  digitalWrite(RELAY2_PIN, LOW);
  Serial.println(String(relayState1)+String(relayState2));

server.send(200, "text/plain", "Relej1 je " + String(digitalRead(RELAY1_PIN)) + " Relej2 je " + String(digitalRead(RELAY2_PIN)));

}
