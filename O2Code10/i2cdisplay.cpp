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

#include "i2cdisplay.h"
#include "constants.h"

#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(LCDAddr,LCDCols,LCDRows);  // set the LCD address to 0x27 for a 16 chars and 2 line display

//implementation

namespace i2cdisplay {

void display_init() {
  lcd.init();
  lcd.backlight();
}

void show_text(String s, int col, int row) {
  lcd.setCursor(row,col);
  lcd.print(s);
}

}
