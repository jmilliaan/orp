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

namespace tools {

void p(String s);

String fullRight(String s,int l);

String fullLeft(String s,int l);

int getHour(unsigned long d);

int getMinute(unsigned long d);

int getSecond(unsigned long d);

}
