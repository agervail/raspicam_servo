#include <Wire.h>
#include <Servo.h> 


#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0; // 0 for waiting, 1 for tilt, 1 for pan
Servo pan;
Servo tilt;
 
int pos = 90;


void setup()
{
	pinMode(13, OUTPUT);
	Serial.begin(9600); // start serial for output
// initialize i2c as slave
	Wire.begin(SLAVE_ADDRESS);

// define callbacks for i2c communication
	Wire.onReceive(receiveData);
	Wire.onRequest(sendData);
	pan.attach(9);
    tilt.attach(10);
    pan.write(pos);
    tilt.write(pos);
	Serial.println("Ready!");
}

void loop()
{
	delay(100);
}

// callback for received data
void receiveData(int byteCount)
{

	while(Wire.available())
	{
		number = Wire.read();
		Serial.print("data received: ");
		Serial.println(number);
		if (state == 0 and number == 200){
			state = 1;
		} else if (state == 0 and number == 210){
			state = 2;
		} else if (state == 1 and number >= 10 and number <= 170){
			pan.write(number);
			state = 0;
		} else if (state == 2 and number >= 10 and number <= 170){
			tilt.write(number);
			state = 0;
		}
		
		
	}
}

// callback for sending data
void sendData()
{
	Wire.write(number);
}
