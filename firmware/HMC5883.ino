/*
An Arduino code example for interfacing with the HMC5883

by: Jordan McConnell
 SparkFun Electronics
 created on: 6/30/11
 license: OSHW 1.0, http://freedomdefined.org/OSHW

Analog input 4 I2C SDA
Analog input 5 I2C SCL

Modified by
Leo Zhou
leothemagnificent@gmail.com
*/

#define address 0x1E //0011110b, I2C 7bit address of HMC5883

String compass_readxyz(){
  int x,y,z;
  
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(address); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x01); //single measurement mode
  Wire.endTransmission();
  
  //Tell the HMC5883 where to begin reading data
  Wire.beginTransmission(address);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();

  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(address, 6);
  if(6<=Wire.available()){
    x = Wire.read()<<8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read()<<8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read()<<8; //Y msb
    y |= Wire.read(); //Y lsb
  }
  return String(x) + "," + String(y) + "," + String(z);
}
