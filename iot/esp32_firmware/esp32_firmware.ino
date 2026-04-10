#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiManager.h> // https://github.com/tzapu/WiFiManager

// --- CONFIGURATION ---
// No hardcoded credentials needed anymore!
// WiFiManager will handle the connection.

// Replace with your PC IP address
const char* serverUrl = "http://192.168.137.99:5000/api/data";

WiFiClient wifiClient;

void setup() {
  Serial.begin(115200);
  delay(100);

  // WiFiManager
  // Local intialization. Once its business is done, there is no need to keep it around
  WiFiManager wm;

  // Reset settings - wipe stored credentials for testing
  // wm.resetSettings();

  // Automatically connect using saved credentials,
  // if connection fails, it starts an access point with the specified name
  // "AutoConnectAP", with password "password"
  // If you want to use a specific AP name/password, use:
  // wm.autoConnect("ESP32_Config_AP", "password123");
  
  bool res;
  res = wm.autoConnect("ESP32_Config_AP"); // anonymous ap

  if(!res) {
      Serial.println("Failed to connect");
      // ESP.restart();
  } 
  else {
      //if you get here you have connected to the WiFi    
      Serial.println("connected...yeey :)");
  }

  Serial.println("\nConnected!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {

    HTTPClient http;

    // Begin HTTP connection
    http.begin(wifiClient, serverUrl);
    http.addHeader("Content-Type", "application/json");

    // Simulated Sensor Data
    int temp = random(20, 40);
    int humidity = random(40, 90);

    // JSON Payload
    String jsonPayload =
      "{\"temp\": " + String(temp) +
      ", \"humidity\": " + String(humidity) +
      ", \"device\": \"ESP32_Device\"}";

    Serial.print("Sending: ");
    Serial.println(jsonPayload);

    int httpResponseCode = http.POST(jsonPayload);

    if (httpResponseCode > 0) {
      Serial.print("HTTP Response Code: ");
      Serial.println(httpResponseCode);

      String response = http.getString();
      Serial.println("Server Response:");
      Serial.println(response);
    } else {
      Serial.print("POST Failed, Error: ");
      Serial.println(httpResponseCode);
    }

    http.end();
  } else {
    Serial.println("WiFi Disconnected");
  }

  // Send every 5 seconds
  delay(5000);
}
