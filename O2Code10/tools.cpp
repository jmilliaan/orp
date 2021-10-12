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
#include "tools.h"

namespace tools {

#define SECS_PER_MIN  (60UL)
#define SECS_PER_HOUR (3600UL)
#define SECS_PER_DAY  (SECS_PER_HOUR * 24L)

/* Useful Macros for getting elapsed time */
#define numberOfSeconds(_time_) (_time_ % SECS_PER_MIN)  
#define numberOfMinutes(_time_) ((_time_ / SECS_PER_MIN) % SECS_PER_MIN)
#define numberOfHours(_time_) (( _time_% SECS_PER_DAY) / SECS_PER_HOUR)
#define elapsedDays(_time_) ( _time_ / SECS_PER_DAY)  


#include "constants.h"
  
void p(String s1) {
  Serial.println(s1);
}

String fullRight(String s,int l) {
  String sresult;
  while (s.length()<l) s += " "; 
  sresult = s;
  return sresult;
}

String fullLeft(String s,int l) {
  String sresult;
  while (s.length()<l) s =+ " "; 
  sresult = s;
  return sresult;
}

int getHour(unsigned long d) {
  long dd = d / 1000;
  int h = numberOfHours(dd);
  return h;
}

int getMinute(unsigned long d){
  long dd = d / 1000;
  int m = numberOfMinutes(dd);
  return m;
}

int getSecond(unsigned long d){
  long dd = d / 1000;
  int s = numberOfSeconds(dd);
  return s;
}

}
