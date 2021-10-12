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
   - Valves
 *
 *=============================================================================*/

#include "valves.h"
#include <Arduino.h>
#include "constants.h"

namespace valves {

  void valves_init() {
    pinMode(pinValve01, OUTPUT);
    pinMode(pinValve02, OUTPUT);
    pinMode(pinValve03, OUTPUT);
    pinMode(pinValve04, OUTPUT);
  }

  bool valve01_close() {
    digitalWrite(pinValve01, LOW);
//    isvalve01close=true;
//    isvalve01open=false;
    return true;
  }
  
  bool valve01_open() {
    digitalWrite(pinValve01, HIGH);
//    isvalve01close=false;
//    isvalve01open=true;
    return true;
  }
  
  bool valve02_close() {
    digitalWrite(pinValve02, LOW);
//    isvalve02close=true;
//    isvalve02open=false;
    return true;
  }
  
  bool valve02_open() {
    digitalWrite(pinValve02, HIGH);
//    isvalve02close=false;
//    isvalve02open=true;
    return true;
  }

  bool valve03_close() {
    digitalWrite(pinValve03, LOW);
//    isvalve03close=true;
//    isvalve03open=false;
    return true;
  }
  
  bool valve03_open() {
    digitalWrite(pinValve03, HIGH);
//    isvalve03close=true;
//    isvalve03open=false;
    return true;
  }

  bool valve04_close() {
    digitalWrite(pinValve04, LOW);
//    isvalve04close=true;
//    isvalve04open=false;
    return true;
  }
  
  bool valve04_open() {
    digitalWrite(pinValve04, HIGH);
//    isvalve04close=false;
//    isvalve04open=true;
    return true;
  }

  
}

 
