/*======================================================================
 * 
   Calvin Institute of Technology
   Proof of Concept
   21 July 2021
   Revision 0.01
   
   Copyright @2020 Calvin Institute of Technology - Jakarta, Indonesia

   All code usage and distribution must have prior written permission from 
   Calvin Institute of Technology
 *
 *=============================================================================*/

#include <Adafruit_ADS1X15.h>

#include "constants.h"
#include "vartypes.h"
#include "valves.h"
#include "tools.h"
#include "sensors.h"

using namespace valves;
using namespace sensors;

void setup() {
  // put your setup code here, to run once:
  Serial.println("Init Start"); 
  Serial.begin(9600);
  sensors_init();
  valves_init();
  Serial.println("Init End");
  Serial.println("Loop Start"); 
}

float o2;
float o2max = 0.0;
float o2min = 100.0;
int nskip;
int nskipfew = 25;

void printsensors(){
  o2 = chreadO2(o2_pin, 6);
  delay(20);
//  
//  flow_lpm = measureflow();
//  delay(20);
//  
//  pressure1 = chreadpressure1(pressure1_pin, 6);
//  delay(2);
//  
//  pressure2 = chreadpressure2(pressure2_pin, 6);
//  delay(2);

//  int blank = chreadint(blankpin, 6);
//  delay(2);

  if (nskip > nskipfew) {
    if (o2>o2max) {o2max = o2;}
    if (o2<o2min) {o2min = 02;}
  } else { nskip++; }
  
  Serial.print("O2: "); Serial.print(o2);Serial.print(" :: highest = ");Serial.print(o2max);
                                         Serial.print(" :: lowest = ");Serial.println(o2min);

//  Serial.print("Flow (OK): "); Serial.print(flow_lpm);Serial.println(" LPM");
//  Serial.print("P1 (OK): "); Serial.print(pressure1);Serial.println(" kPa");
  // Serial.print("P2 (NO SENSOR): "); Serial.print(pressure2);Serial.println(" kPa");
}

uint16_t starttime = millis();
int phase1 = 1000;
int phase2 = 1500;  
int phase3 = 6000;
int phase4 = 7000;
bool bphase1 = false;
bool bphase2 = false;
bool bphase3 = false;
bool bphase4 = false;
uint16_t countV1, countV2;

bool isvalve01close;
bool isvalve02close;
bool isvalve03close;
bool isvalve04close;


void loop() {
//  printsensors();
 
  countV1 = millis() - starttime;
  countV2 = countV1;
// 
  if (countV1 <= phase1) { 
    if (!bphase1) { 
      Serial.println("valve04_close(); "); 
      bphase1 = true; 
      if (!isvalve04close) { valve04_close(); isvalve04close=true; }
      if (!isvalve03close) { valve03_close(); isvalve03close=true; }
    }
  }
    
  if ((countV1 > phase1) && (countV1 <= phase2)) { 
    if (!bphase2) { 
      Serial.println("valve04_open(); "); 
      bphase2 = true; 
      if (isvalve04close) { valve04_open(); isvalve04close=false; }
      if (!isvalve03close) { valve03_close(); isvalve03close=true; }
    }
  }
    
  if ((countV1 > phase2) && (countV1 <= phase3)) { 
    if (!bphase3) { 
      Serial.println("valve04_open(); "); 
      bphase3 = true; 
      if (!isvalve04close) { valve04_close(); isvalve04close=true; }
      if (!isvalve03close) { valve03_close(); isvalve03close=true; }
    }
   } 
  
  if ((countV1 > phase3) && (countV1 <= phase4)) { 
    if (!bphase4) { 
      Serial.println("valve04_open(); "); 
      bphase4 = true; valve04_open();
      if (isvalve04close) { valve04_open(); isvalve04close=false; }
      if (isvalve03close) { valve03_open(); isvalve03close=false; }
    }
  }

  if (countV1 > phase4) { 
      Serial.println("End cycle"); 
      starttime = millis();
      bphase1 = false; 
      bphase2 = false;
      bphase3 = false;
      bphase4 = false;
    }
}
