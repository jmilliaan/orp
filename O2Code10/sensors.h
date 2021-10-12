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

#include <Adafruit_ADS1X15.h>

namespace sensors {

  void sensors_init();

  int16_t chreadint(int chnum, int dgain);

  float chreadvolt(int chnum, int dgain);

  float chreadO2(int chnum, int dgain);

  float measureflow();

  float chreadpressure1(int chnum, int dgain);

  float chreadpressure2(int chnum, int dgain);

  float chreadpressure (int chnum);
}
