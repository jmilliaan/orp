/*======================================================================
 * 
   Calvin Institute of Technology
   Proof of Concept
   21 July 2021
   Revision 0.01
   
   Copyright @2020 Calvin Institute of Technology - Jakarta, Indonesia

   All code usage and distribution must have prior written permission from 
   Calvin Institute of Technology

   Display Library
   - Sensors
 *
 *=============================================================================*/

#include <Wire.h>
#include <Adafruit_ADS1X15.h>
#include "constants.h"

Adafruit_ADS1115 ads;  /* Use this for the 16-bit version */

 namespace sensors {

  void sensors_init() {
    if (!ads.begin()) {
      Serial.println("Failed to initialize ADS!");
      Serial.println("Program halt");
      while(1);
    }
    Serial.println("ADS successfully initialized");
    
    // Intialize flow sensor
    Wire.begin();
    Wire.beginTransmission(FlowAddr);
    Wire.write(0x10);
    Wire.write(0x00);
    Wire.endTransmission();
  }

  adsGain_t convertgain(int igain) {
    adsGain_t dgain;
    switch (igain) {
      case 6: dgain = GAIN_TWOTHIRDS; break;
      case 4: dgain = GAIN_ONE; break;
      case 2: dgain = GAIN_TWO; break; 
      case 1: dgain = GAIN_FOUR; break;
      case 0: dgain = GAIN_EIGHT; break;
      case 16: dgain = GAIN_SIXTEEN; break;
    }  
    return dgain;
  }

  int16_t chreadint(int chnum, int dgain) {
    int16_t readval;    
    ads.setGain(convertgain(dgain));
    readval = ads.readADC_SingleEnded(chnum);
    return readval;
  }

  float chreadvolt(int chnum, int dgain) {
    float readval;
    ads.setGain(convertgain(dgain));
    readval = ads.computeVolts(chreadint(chnum, GAIN_TWOTHIRDS));
    return readval;
  }

  float chreadO2(int chnum, int dgain) {
    float readval;
    ads.setGain(convertgain(dgain));
    readval = ads.readADC_SingleEnded(chnum);
    readval = (readval * 0.1875)/1000;
    readval =  0.61051865721074 + 1965.68158984*readval;
    return readval;
  }

  float chreadpressure1(int chnum, int dgain){
    float readval;
    ads.setGain(convertgain(dgain));
    // ads.setGain(GAIN_TWOTHIRDS);

    readval = ads.readADC_SingleEnded(chnum);
    readval = ads.computeVolts(readval);
    // readval =  ((readval/5.0) - 0.04)/0.0012858;
    // readval = ((readval/4.63) - 0.04)/0.0012858;
    
    // New transfer function:
    readval = readval/(5.0 * 0.00163829);
    return readval;
    }
  float chreadpressure(int chnum){
    float readval;
    float readvoltage;
    float readpressure;
    readval = analogRead(chnum);
    readval = readval * 5.0 / 1023;
    readval = (readvoltage / 5.0)/0.00163829;
    return readval;
    }  
  float chreadpressure2(int chnum, int dgain){
    float readval;
    ads.setGain(convertgain(dgain));
    readval = ads.readADC_SingleEnded(chnum);
    readval = ads.computeVolts(readval);
    readval =  ((readval/5.0) - 0.04)/0.0012858;
    return readval;
    }
    
  float measureflow(){
    if(2==Wire.requestFrom(FlowAddr, 2)){
      uint16_t a = Wire.read();
      uint8_t b = Wire.read();
      a = (a<<8) | b;
      float flow = ((float)a - 32768) / 120;
      return flow;
    }
  }
}
