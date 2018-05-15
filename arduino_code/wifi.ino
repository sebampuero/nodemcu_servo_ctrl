#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <WiFiUdp.h>
#include <Wire.h>

#define MPU 0x68
#define A_R 16384.0 // 32768/2
#define G_R 131.0 // 32768/250
#define RAD_TO_DEG 57.295779
#define builtInLED D4
int16_t AcX, AcY, AcZ, GyX, GyY, GyZ;
float Acc[2];
float Gy[3];
float Angle[2]; // contains angle values for pitch and roll
long tiempo_prev;
float dt;

WiFiUDP udp;

void setup()
{
  pinMode(builtInLED, OUTPUT);
  Serial.begin(115200);
  wiFiSetup();
  mpuSetup();
}

void loop() {
  readValues();
  udp.beginPacket("192.168.2.3", 8088);
  for(int i = 0; i < 2; i++){ // loop through angles array
   uint8_t *f_array;
   f_array = reinterpret_cast<uint8_t*>(&Angle[i]);
    for(int i = 0; i<4; i++){ // for every byte in the float
      udp.write(f_array[i]);  
    }  
  }
  udp.endPacket();
}

void wiFiSetup(){
  IPAddress ip(192, 168, 2, 25); 
  IPAddress gateway(192, 168, 2, 1); 
  IPAddress subnet(255, 255, 255, 0); 
  WiFi.config(ip, gateway, subnet);
  WiFi.begin("", "");
  while (WiFi.status() != WL_CONNECTED) { 
    delay(500);
    Serial.print(".");
  }
  digitalWrite(builtInLED, HIGH);
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());
}

void mpuSetup(){
  Wire.begin(4,5); // D1=SDA / D2=SCL
  Wire.beginTransmission(MPU);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);;
}

void readValues(){
   Wire.beginTransmission(MPU);
   Wire.write(0x3B); 
   Wire.endTransmission(false);
   Wire.requestFrom(MPU,6,true);   
   AcX=Wire.read()<<8|Wire.read(); 
   AcY=Wire.read()<<8|Wire.read();
   AcZ=Wire.read()<<8|Wire.read();
 
   Acc[1] = atan(-1*(AcX/A_R)/sqrt(pow((AcY/A_R),2) + pow((AcZ/A_R),2)))*RAD_TO_DEG;
   Acc[0] = atan((AcY/A_R)/sqrt(pow((AcX/A_R),2) + pow((AcZ/A_R),2)))*RAD_TO_DEG;
 
   Wire.beginTransmission(MPU);
   Wire.write(0x43);
   Wire.endTransmission(false);
   Wire.requestFrom(MPU,6,true);   
   GyX=Wire.read()<<8|Wire.read(); 
   GyY=Wire.read()<<8|Wire.read();
   GyZ=Wire.read()<<8|Wire.read();
 
   
   Gy[0] = GyX/G_R;
   Gy[1] = GyY/G_R;
   Gy[2] = GyZ/G_R;

   dt = (millis() - tiempo_prev) / 1000.0;
   tiempo_prev = millis();
   // Apply complementary filter
   Angle[0] = 0.98 *(Angle[0]+Gy[0]*dt) + 0.02*Acc[0];
   Angle[1] = 0.98 *(Angle[1]+Gy[1]*dt) + 0.02*Acc[1];
   delay(2);
}

