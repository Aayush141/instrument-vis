#include <iostream>
#include <string>
#include <vector>


char transmitBuffer[200];              // buffer to update with data values and send over serial

// This function executes exactly once at start up
void setup() {
  Serial.begin(9600);

  // Wait here until receiving serial communication
  do{
    Serial.println("INIT");
    delay(250);
  } while(!Serial.available());
  //Begin,1(Hz)
  //PARAMS,1,9,2000,0,0,0
  String beginMessage = Serial.readString();           // read begin command
  int fs = parseBegin(beginMessage);         // parse begin command
  sprintf(transmitBuffer, "BEGIN,%d(Hz)", fs);
  Serial.println(transmitBuffer);     

  do{
    delay(250);
  } while(!Serial.available());

  String paramMessage = Serial.readString();
  float* p = parseParams(paramMessage);
  sprintf(transmitBuffer, "PARAM,%f,%f,%f,%f,%f,%f", p[0], p[1], p[2], p[3], p[4], p[5]);
  Serial.println(transmitBuffer);
}

// This repeats as long as the device is powered on
void loop() {
  Serial.println("O," + String(random(1023)) + "," + String(random(1023)));
  delay(100);
}


int parseBegin(String s){
  std::string std_s = s.c_str();                      // convert s from primitive string to class string
  int ind1 = std_s.find(",");                         // find index of "," which occurs before sampling rate
  int ind2 = std_s.find("(");                         // find index of "(" which occurs after sampling rate
  int fs = std::stoi(std_s.substr(ind1+1, ind2-ind1));// pick out sampling rate and convert to int
  return fs;
}

float* parseParams(String s){
  std::string std_s = s.c_str();
  
  int ind = std_s.find(",");
  std_s = std_s.substr(ind+1);
  
  ind = std_s.find(",");
  int CH = std::stoi(std_s.substr(0,ind+1));
  std_s = std_s.substr(ind+1);
  
  ind = std_s.find(",");
  int RI = std::stoi(std_s.substr(0,ind+1));
  std_s = std_s.substr(ind+1);
  
  ind = std_s.find(",");
  int G = std::stoi(std_s.substr(0,ind+1));
  std_s = std_s.substr(ind+1);
  
  ind = std_s.find(",");
  
  float B = std::stof(std_s.substr(0,ind+1));
  std_s = std_s.substr(ind+1);
  
  ind = std_s.find(",");
  int EX_F = std::stoi(std_s.substr(0,ind+1));
  std_s = std_s.substr(ind+1);

  float EX_A = std::stof(std_s);

  static float a[6]; 
  a[0] = CH;
  a[1] = RI;
  a[2] = G;
  a[3] = B;
  a[4] = EX_F;
  a[5] = EX_A;

  return a; 

}

String extractParamMessage(String s){
  std::string std_s = s.c_str();
  int ind = std_s.find("PARAMS");
  std_s = std_s.substr(ind);
  return std_s.c_str();
}

