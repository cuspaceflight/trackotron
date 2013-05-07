// Leo Zhou
// leothemagnificent@gmail.com

char Stopstring[14]   = {0x57,0x30,0x30,0x30,0x30,0x01,0x30,0x38,0x37,0x36,0x01,0x0F,0x20,0};
char Movestring[14]   = {0x57,0x30,0x30,0x30,0x30,0x01,0x30,0x38,0x37,0x36,0x01,0x2F,0x20,0};
char Statusstring[14] = {0x57,0x30,0x30,0x30,0x30,0x01,0x30,0x38,0x37,0x36,0x01,0x1F,0x20,0};


// function to correctly format the Alpha Spid serial protocol
// and move the roator by sending the command to the serial port.
// azheading & horizheading allow local az & el to be converted into 
// Earth az and el
void moveantenna( int Az, int El ){

    int tempAz,tempEl;

    // Bit of error checking
    if ( !( Az > -540 && Az < 540 ) ) {
        Serial.println( "Error: Azimuth not entered within limits"   );
        return; }

    if ( !( El > -40  && El < 200 ) ) {
        Serial.println( "Error: Elevation not entered within limits" );
        return; }

    // Format for SPID protocol begins with 0x57 then 0x30 + thousands, tens .... of az+360,
    // then 0x01 for 1 degree accuracy then 0x30 + thousands, tens .... of el+360 then 0x01 0x2F and 0x20 to finish
    tempAz = (int)( Az+360 + AzManOfst );
    tempEl = (int)( El+360 + ElManOfst );

    Movestring[1] = ( tempAz/1000 ) + 0x30; tempAz %=1000;
    Movestring[2] = ( tempAz/100  ) + 0x30; tempAz %=100;
    Movestring[3] = ( tempAz/10   ) + 0x30; tempAz %=10;
    Movestring[4] = ( tempAz      ) + 0x30;

    Movestring[6] = ( tempEl/1000 ) + 0x30; tempEl %=1000;
    Movestring[7] = ( tempEl/100  ) + 0x30; tempEl %=100;
    Movestring[8] = ( tempEl/10   ) + 0x30; tempEl %=10;
    Movestring[9] = ( tempEl      ) + 0x30;

    // Move the antenna, send movestring via serial
    Serial1.write( Movestring );
}

// function to stop the rotator
void stopantenna(){ Serial1.write( Stopstring );}

//function to return current position of the antenna mount
String getantennapos()
{
    char Status[13];
    
    // send status request and receive input string
    Serial1.write( Statusstring );
    Serial.readBytesUntil( 0x20, Status, 13 );
    // the string ends with 0x20 seem to be an hard coded value

    // decode az & el
    float AzPos = (Status[1]*100+Status[2]*10+Status[3]+Status[4]/10)%360;
    float ElPos = (Status[6]*100+Status[7]*10+Status[8]+Status[9]/10)%360;
    
    return String( int(AzPos) )+"."+String(int((AzPos-int(AzPos))*1000))+","+String(int(ElPos))+"."+String(int((ElPos-int(ElPos))*1000));
}



























