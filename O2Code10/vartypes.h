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

//#include <Arduino.h>

//Global struct
struct tParams {
  int BPM;
  int Tidal;
  int IE;
  int Assist;
};

struct tsetParams {
  int BPM;
  int Tidal;
  int IE;
  int Assist;
};

struct tRespiration {
  float Tdur, Tin, Tex, Vin, Vex;
};

struct tMotor {
  int posStop, pwmIn, pwmEx;
};

extern unsigned long startRunning;
extern struct tParams Params;
extern struct tRespiration Resp;
extern struct tMotor Motor;
extern struct tsetParams setParams;
