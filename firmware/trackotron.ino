// Leo Zhou
// leothemagnificent@gmail.com
#include <Wire.h> //I2C Arduino Library

void flash(int);

// arduino pin definitions
int ledPin     = 13; // LED connected to digital pin 13
int GPSoutput  = 2;  // GPS chip pin

// AzManOfst and ElManOfst Seem to be used if the initial position is not 0
int AzManOfst = 0;
int ElManOfst = 0;

void setup() // run once, when the sketch starts
{
    // define pin I/O status
    pinMode( ledPin,     OUTPUT ); // sets the digital pin as output
    pinMode( GPSoutput,  INPUT  ); // GPS data line
    
    Wire.begin();//Initialize I2C communications to compass
    Serial1.begin(600); // begin serial connection to roator at baud 600
    stopantenna(); // initialise contact with spid and stop it
    Serial.begin(115200); // begin serial connection computer at bps rate
    Serial.println("Initialised.");
}

void loop() // run over and over again
{
    String cmd = "";
    char incomming_char; // to store the incomming character from the computer

    flash(1); // turn on LED to show working

    //Don't do anything until we have a computer input command
    while( Serial.available() == 0 );
    delay(50); // wait for incomming message to be fully buffered.1s
         
    // read the incoming bytes and put in in a string
    while( Serial.available() )
    {
        incomming_char = Serial.read();
        if(incomming_char == ' ') break;
        cmd.concat( incomming_char );
        
    }

    int param1 = Serial.parseInt();
    int param2 = Serial.parseInt();
    
    // echo command
    //Serial.println( "Command Received: " + cmd );
    //Serial.print( param1 );
    //Serial.println( param2 );

    // switch case based on input command
    cmd.toLowerCase();
    if      ( cmd == "move_azel" ) moveantenna( int(param1), int(param2) ); // Move with Azimuth and Elevation tbc: test to see how the behaviour really is
    else if ( cmd == "move_stop" ) stopantenna();
    else if ( cmd == "rqst_azel" ) Serial.println( getantennapos() ); // get antenna position
    else if ( cmd == "comp_xyz"  ) Serial.println( compass_readxyz() ); // return compass reading
    else if ( cmd == "acc_xyz"   ); // Serial.println( acc_readxyz() ); // tbd: wrtie the functions
    else if ( cmd == "rqst_gps"  ); // Serial.println( gps_readxyz() ); // tbd: wrtie the functions
    else if ( cmd == "manu_ofst" ) {AzManOfst = param1; ElManOfst = param2;} // allow for manual offset definitions
    else if ( cmd == "rqst_ofst" ) Serial.print( String(AzManOfst) + " " + String(ElManOfst) ); //Reply with offsets
    else if ( cmd == "ping"      ) Serial.println( "pong" );
    else Serial.println("Error: COMMAND NOT RECOGNISED: " + cmd );
}

// the loop routine runs over and over again forever:
void flash(int n)
{
  for(int i=0;i<n;i++)
  {
    digitalWrite(ledPin, HIGH);   // turn the LED on (HIGH is the voltage level)
    delay(30);               // wait for a second
    digitalWrite(ledPin, LOW);    // turn the LED off by making the voltage LOW
    delay(20);               // wait for a second
  }
}


