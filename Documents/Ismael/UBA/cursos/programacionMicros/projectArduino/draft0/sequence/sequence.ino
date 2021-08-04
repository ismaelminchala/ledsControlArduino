const int16_t LED1 = 50;            // Port address of LEDx
const int16_t LED2 = 51;
const int16_t LED3 = 52;
const int16_t LED4 = 53;
const int16_t KEY1 = 48;            // Por address of KEYx
const int16_t KEY2 = 49;

/****************** + Variables declaration + ******************/
enum  dir {ascending, descending};  // Enum variable for sequence
      dir orientation = ascending;  // orientation

      int16_t leds[] = {LED1, LED2, LED3, LED4}; // Array of leds
      int16_t len = sizeof(leds) / sizeof(int);
const int16_t t_base = 10;          // Time base for delay           

typedef struct{                     // Struct definition for 
  const int16_t* ptr;               // functions arguments
  const int16_t len;
  enum  dir orientation;
} sequenceControl;
/***************************************************************/

/****************** + Functions prototypes + *******************/
bool turnOffLeds(sequenceControl *controller);
bool ledSequence(sequenceControl *controller);
bool sequenceSpeed(int t_base, int t_delay);
bool toogleState();
/***************************************************************/

/*********************** + Setup loop + ************************/
void setup() {
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(KEY1, INPUT);
  pinMode(KEY2, INPUT);
  Serial.begin(9600);
}
/***************************************************************/

/************************ + Main loop + ************************/
void loop() {
  int16_t fast = 250;
  int16_t slow = 750;
  int16_t t_delay = fast;
  sequenceControl ledsControl = {leds, len, ascending};
/*  
  if ( !digitalRead(KEY1) == LOW ){
    ledsControl.orientation = ascending;
  } else{
    ledsControl.orientation = descending;
  }*/
  if ( !digitalRead(KEY1) == LOW ){
    if(toogleState()){
      ledsControl.orientation = ascending;;
    } else{
      ledsControl.orientation = descending;
    }
  }

  if ( !digitalRead(KEY2) == LOW ){
    t_delay = fast;
  } else{
    t_delay = slow;
  }
  
  if (sequenceSpeed(t_base, t_delay)){
    ledSequence(ledsControl); 
  }  
}
/***************************************************************/

bool turnOffLeds(sequenceControl controller){
  for (int i = 0; i < controller.len; ++i){
    digitalWrite(controller.ptr[i], LOW);
  }
  return 0;
}

bool ledSequence(sequenceControl controller){
  static int pos = 0;
  //int16_t var = ledsControl.ptr[0];
  turnOffLeds(controller);
  digitalWrite(controller.ptr[pos], HIGH);
  if (controller.orientation == ascending){
    if (pos < len - 1){
      ++pos;
    } else{
      pos = 0;
    }  
  } else{
    if (pos > 0){
      --pos;
    } else{
      pos = len - 1;
    }
  }
  return 0;
}


bool sequenceSpeed(int t_base, int t_delay){
  static int cont = 0;
  delay(t_base);
  int n_base = t_delay / t_base;
  if (cont < n_base){
    ++cont;
    return false;
  } else{
    cont = 0;
    return true;
  }
}

bool toogleState(){
  static bool var = false;
  delay(100);
  var = !var;
  return var;
}
