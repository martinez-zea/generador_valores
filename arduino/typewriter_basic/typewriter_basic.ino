/*
 * Copyright © 2009 Scott Perry
 *
 * Permission is hereby granted, free of charge, to any person
 * obtaining a copy of this software and associapted documentation
 * files (the "Software"), to deal in the Software without
 * restriction, including without limitation the rights to use,
 * copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following
 * conditions:
 *
 * The above copyright notice and this permission notice shall be
 * included in all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
 * EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
 * OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
 * NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
 * HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
 * FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
 * OTHER DEALINGS IN THE SOFTWARE.
 */

/*
 * preprocessor macros
 */

//#define DUEMILANOVE
#define MEGA
//#define WIRING
/*
 * enabling debugging by defining DEBUG doesn't so much turn on extra debugging
 * facilities so much as turn off all normal usage of the STS lamp so it can be
 * used for debugging. this is what happens when you only have one pin free.
 */
//#define DEBUG

// disables use of Serial in the reading functions
//#define DEBUG_WRITES

/*
 * disables flooding the typewriter's lines to prevent passing keys when there
 * is nothing being actively written.
 */
//#define KEYBOARD_PASSTHROUGH

/*
 * TODO: though I'm tempted to throw the metapass idea out, it would still be
 * interesting to see why it's broken. it doesn't make a lot of sense.
 */
//#define METAPASS

// TODO: do a final review of plswrite, maybe even improve it

// pin definitions for the system status (LED) and activity status (STS)
#define LED 13

// measured in scans, more or less arbitrarily chosen.
#define KEYPRESS_DURATION 3
#define KEYPRESS_GAP 2
#define IDLE_WINDOW 10000

// measured in ms
 /* 
 4 funciona muy bien quitando tambien las funciones de lectura del teclado de la maquina,
 No estoy seguro de porque, pienso que es un desfase en la lectura de las seniales
 */
 
#define SCANLINE_INTERVAL 6

// measured in… baud
#define BAUD 115200

//#define PLSWRITE

// helper functions
#define LONIBBLE(x) ((x) & 0x0F)
#define HINIBBLE(x) (((x) >> 4) & 0x0F)
#define LOHINIBBLE(x) (((x) >> 8) & 0x0F)
#define BIT(x) (0x01 << (x))
#define MASK(x) (~(0x01 << (x)) & 0xFF)

/*
 * includes
 */

// functions for interacting with the scan/signal lines. no logic.
#include "signals.h"

// tables of key codes for reading and writing
#include "keycodes_gx9500.h"

// debouncer for tracking scanline state
#include "debounce.h"

//lcd
#include "LiquidCrystal.h"

//LiquidCrystal lcd(17,16,6,7,8,9);
//String message = " "; // mensaje para el lcd
/*
 * global state
 */

// loop-local persistant state
struct {
  // debouncer for catching scanline changes
 debounceState debouncer;

  // debouncer para shift
 debounceState shiftdebouncer;
  
  // the time of the last scanline transition, in ms
  uint32_t scanedge;
} loopstate;


boolean isPrinting;

// write-local persistant state
struct {
  // counts how long the current write cycle has been, or 0 when not writing
  uint8_t writing;

  // the character being written, 0 when not writing
  uint8_t character;

  // meta key(s) associated with character.  stale when character is 0
  uint8_t meta:4;

  // scan line associated with character.  stale when character is 0
  uint8_t scan:3;

  // signal line associated with character.  stale when character is 0
  uint8_t signal:3;
  
  //shift se almacena aparte
  uint8_t shift;

} writestate;

struct{
  //boton de la palanca
  uint8_t boton:1; 
  
  //sensor de entrada de papel
  uint8_t paperin:1; 
  
  //sensor de salida de papel
  uint8_t paperout:1;
  
  //conteo de palancazos
  uint8_t press:1; 
  
  uint32_t count; 
}sensors;



enum main_state_enum{
  WAITING = 0,
  INIT_PRINT = 1,  
  WRITING = 2,
  END_PRINT = 3,  
};


main_state_enum main_state;
uint32_t wait_window = 10000; 
boolean request_txt;
boolean newprint = false;
int count = 0;

/*
 * write_getcodes --
 *    looks up the writestate character's meta key requirements, signal, and
 *    scan. if the character is not supported by the typewriter, ? is used.
 *
 *    this is the only function that writes to the writestate's meta, signal,
 *    and scan members.
 */
void write_getcodes() {
    uint16_t *bank;
    uint16_t entry;
    uint8_t index;

    /*
     * not convinced this switch is necessary. we should just drop all
     * instructions to press meta keys.
     */
    switch(writestate.character) {
      case SHIFT:
        writestate.meta = 0;
        writestate.signal = 0;
        writestate.scan = 7;
        writestate.shift = 0;
        return;
      case 92:
        //Serial.println("shift detected");
        writestate.meta = 0;
        writestate.signal = 0;
        writestate.scan = 0;
        writestate.shift = 1;
        return;
      case SHIFT_LOCK:
        writestate.meta = 0;
        writestate.signal = 1;
        writestate.scan = 7;
        writestate.shift = 0;
        return;
      case CODE:
      case ALT:
        writestate.character = 0;
        writestate.writing = 0;
        writestate.meta = 0;
        writestate.shift = 0;
        return;
    }

    // get the lookup table and index for the char in question
    if(writestate.character < 0x80) {
      bank = (uint16_t *)ascii;
      index = writestate.character;
    }
    else if(writestate.character <= HALF && writestate.character >= CENT) {
      bank = (uint16_t *)extended;
      index = writestate.character - CENT;
    }
    else if(writestate.character <= OPERATE && writestate.character >= EXPR) {
      bank = (uint16_t *)control;
      index = writestate.character - EXPR;
    }

    // if not found, use ? instead!
    if (!bank || pgm_read_word_near(bank + index) == NC16) {
      writestate.character = '?';
      write_getcodes();
      return;
    }

    entry = pgm_read_word_near(bank + index);
    
    // for more detail on the lookup table's organization, see keycodes.h
    writestate.meta = LOHINIBBLE(entry);
    writestate.signal = HINIBBLE(entry);
    writestate.scan = LONIBBLE(entry);
    writestate.shift=LOHINIBBLE(entry);
    //Serial.print("signal: ");
    //Serial.println(writestate.signal, BIN);
    //Serial.print("scan: ");
    //Serial.println(writestate.scan, BIN);
    //Serial.println("sum: ");
    //Serial.println(writestate.signal + writestate.scan);
    //Serial.println(writestate.signal + writestate.scan, BIN);
    
    return;
}

/*
 * write_consume --
 *    consume input from the reading code or Serial, if available.
 *    set up state for writing—meta keys to hold, scan/signal lines,
 *    and write status.
 *
 *    write_consume DOES NOT BLOCK
 */
void write_consume(void) {

  if(Serial.available()) {
    writestate.character = Serial.read();  
  }

  if(writestate.character) {
    if(writestate.character == 0x03){ //ETX terminacion de impresion
      //Serial.println("end");
      writestate.character = 0;
      //isPrinting = false;
      Serial.flush();
      return;
    }
    // populate the writestate
    writestate.writing = 1;
    write_getcodes();

    // sanity check. if this condition is true there is a serious problem.
    if(writestate.meta > 0x07) {
      writestate.character = 0;
      writestate.writing = 0;
      //Serial.print(ERR);
    }
  }

  return;
}

/*
 * write_metagen --
 *    based on the desired meta key state and the current scanline state,
 *    return the signal state needed to hold the meta keys down.
 *
 * args:
 *    meta - the meta key state, either for an character we are printing, or
 *           the meta_key_state from the read logic.
 *    scans - the current state of the scanlines
 */
uint8_t write_metagen(uint8_t meta,uint8_t scans) {
  uint8_t signals = 0xFF;

  // only the lower three bits are valid
  if(meta & 0xF8) 
    return signals;

  // SHIFT
  if(meta & BIT(0) && scans == MASK(7)){
    //Serial.print("meta shift: ");
    //Serial.println(shift, BIN);
    signals &= MASK(0);
   }

  // CODE
  if(meta & BIT(1) && scans == MASK(6))
    signals &= MASK(7);

  // ALT
  if(meta & BIT(2) && scans == MASK(6))
    signals &= MASK(4);

  return signals;
}

/*
 * do_write --
 *    based upon the state of the scanlines, pulls down the appropriate
 *    signallines in order to type text read from Serial. this is called every
 *    time the scanlines change and settle into a new state.
 *
 * args:
 *    scans - the current state of the scanlines
 */
void do_write(uint8_t scans) {
  uint8_t signals = 0xFF;

  /*
   * the best time to consume input is when all the scanlines are high.
   * it happens often enough—every 16ms—and nothing much is happening on
   * our end: it's 2ms of totally free time in which to do our extra work.
   */
  if(scans == 0xFF ) {
    //Serial.println("FF");
    if(!writestate.writing){
        count++;
      if(request_txt){
        //Serial.flush();
        //Serial.print(0x05, HEX);
        Serial.println(0x05,HEX);
        request_txt = false;
      }
      write_consume();
    }else{
      writestate.writing++;
    }
    return;
  }

  if(writestate.character) {

    // hold down the appropriate meta key(s)
    if(writestate.meta){
      signals &= write_metagen(writestate.meta, scans);
      //Serial.print("meta signal : ");
      //Serial.println(signals, BIN); 
    }
    // after the meta key(s) (if applicable) have been held long enough, type the character
    if(writestate.writing > KEYPRESS_DURATION * !!writestate.meta)
      if(scans == MASK(writestate.scan))
        signals &= MASK(writestate.signal);
    // stop holding the keys, but continue blocking writes
    if(writestate.writing == KEYPRESS_DURATION * (1 + !!writestate.meta)) {

      writestate.character = 0;
    }
  }

  write_signs(signals);
  
  /*
   * wait long enough that the next keystroke, if the same, won't be
   * interpreted by the typewriter as a held key
   */
  if(writestate.writing == KEYPRESS_DURATION * (1 + !!writestate.meta) + KEYPRESS_GAP)
    writestate.writing = 0;

  return;
}

/*
*  init_machine()
*  inicaliza el estado de la maquina de escribir.  
*/

void init_machine(){

}

void update_machine(){

}

/*
*  send_command()
*
*envia comandos al generador, los comandos concuerdan con comandos de control ascii
*se integra con los comandos de la maquina;
*/

void send_command(uint8_t command){
  Serial.println(command);
}

/*
*  capture_data()
*  captura los datos de los sensores en tiempo de espera
*
*/
void update_input(){
  uint8_t port = read_shift(); // con el shift estan los sensores
  //Serial.println(port, BIN);  
  uint8_t b = port & (1 << 1); //obtiene el 2do bit, corresponde al pin del sensor 
  sensors.paperin = port >> 2;
  sensors.paperout = port >> 3;
  //Serial.println(sensors.paperout);
  if(sensors.boton && !b){
    
    // si no hay papel en la maquina
    //if(isPrinting){
      if(sensors.paperin | sensors.paperout){
        request_txt = true;
        //Serial.println("bang");
        //isPrinting = true;
        //lcd.clear();
        //lcd.print("PRINTING A");
      }
      //else{
        //lcd.clear();
        //lcd.print("INSERT PAPER");
      //}
      /*
    }
     else{
       if(!sensors.paperin && !sensors.paperout){
         lcd.clear();
         lcd.print("INSERT PAPER"); 
        }
       if(sensors.paperin && !sensors.paperout){
         isPrinting = true;
         request_txt = true;
         lcd.clear();
         lcd.print("PRINTING B");  
       }
       if(!sensors.paperin && sensors.paperout ){
          lcd.clear();
          lcd.print("RETIRE PAPER"); 
       }
     }
     */
  }
  sensors.boton = port >> 1; // update sensor reading
  //Serial.println(sensors.boton, BIN);
}


/*
 * setup --
 *    standard Arduino function.  initialize pins, ports, Serial.
 */
void setup(void) {

  Serial.begin(BAUD);
  digitalWrite(LED, HIGH);

  init_scans();
  init_read();
  init_shift();
  write_signs(0xFF);
  //isPrinting = false;

  digitalWrite(LED, LOW);
  sensors.boton = 0;
  //lcd.begin(16, 2);
  //lcd.setCursor(0,0);
  //lcd.print("init");
}

/*
 * loop --
 *    standard Arduino function.
 */
void loop(void) { 
  uint8_t scans = read_scans();
  //lee shift
  //Serial.println(scans, BIN);
  uint8_t changes = debounce(scans, &loopstate.debouncer);
  //uint8_t shiftchanges = debounce(shift, &loopstate.shiftdebouncer);
  if(changes) {
    loopstate.scanedge = millis();
    /*
     * ensure that only one (or zero!) scanline is down
     */
    if(~loopstate.debouncer.state & (~loopstate.debouncer.state - 1) & 0xFF)
      return;

    digitalWrite(LED, HIGH);
    //init_read();
    //write_signs(0xFF);
    init_write();
    do_write(scans); //escribe el estado a las lineas

    digitalWrite(LED, LOW);
  }
  update_input();
  
  /*
   * in normal operation, the scanlines change every 2ms, with a range reliably
   * between 1950 and 2050 µs. if we've waited much longer than that for a
   * change, it is safe to assume that the typewriter is resetting and has
   * pulled down the scanline the limit switch is on so it can respond as
   * quickly as possible when the carriage hits it.
   *
   * when this is happening we cannot be in write mode. driving the signal
   * lines will drown out the switch when it does trigger, causing the
   * typewriter to grind the gearing on the carriage motor.
   */   
   
  if(millis() - loopstate.scanedge >= SCANLINE_INTERVAL) {
    digitalWrite(LED, HIGH);
    init_read();
    write_signs(0xFF);

    while(loopstate.debouncer.state == read_scans());
    
    /*
     * sometimes there is a little bit of noise that could cause us to
     * mistakenly start polling in read/write mode. this 1ms delay should
     * be plenty to avoid the blips of noise that occur pretty rarely.
     */
    delay(1);
  }
}
