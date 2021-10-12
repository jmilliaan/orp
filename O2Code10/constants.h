/*=====================================================
   Calvin Institute of Technology
   Simple Ventilator Project for COVID-19 Patient
   21 April 2020
   Revision 0.09
   Made by IEE and IBDA Team
   
   Based on MIT Open Project (https://e-vent.mit.edu/)
   Copyright @2020 Calvin Institute of Technology - Jakarta, Indonesia
   Based on Open Design - MIT

   Please provide link to CIT for reproduction
*/

#include <Arduino.h>

/*
 * Constants
 */

//Pin for Valves through relays
#define pinValve01 6           //Pin for Valve01
#define pinValve02 7           //Pin for Valve02
#define pinValve03 8           //Pin for Valve03
#define pinValve04 9           //Pin for Valve04

//Pin for LCD
#define LCDAddr 0x27      //LCD I2C Address
#define LCDCols 20
#define LCDRows 4


// Pin for Flow Sensor
#define FlowAddr 0x40

// Pin for O2 Sensor
#define o2_pin 0

// Pin for Pressure Sensor 1
#define pressure1_pin 1

// Pin for Pressure Sensor 2
#define pressure2_pin 2

#define blankpin 3

// Timing
#define timeA 1000
#define timeB 1000
#define timeC 5000
#define timeD 3000  
