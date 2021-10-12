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
   - LiquidCrystal
 *
 *=============================================================================*/
 
 #include <Arduino.h>

 namespace i2cdisplay {

  void display_init();

  void show_text(String s, int col, int row);
  
 }
