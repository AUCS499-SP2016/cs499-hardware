#include <Wire.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

#define SOUND_SENSOR                  A1
#define WATER_SENSOR                  7
#define SMOKE_SENSOR                  A2
#define THRESHOLD_VALUE_SOUND         400

#define RL_VALUE                      5
#define RO_CLEAN_AIR_FACTOR           9.83

#define CALIBRATION_SAMPLE_TIMES      50
#define CALIBRATION_SAMPLE_INTERVAL   500

#define READ_SAMPLE_INTERVAL          50
#define READ_SAMPLE_TIMES             5

//For SPI wiring
//#define BME_SCK 13
//#define BME_MISO 12
//#define BME_MOSI 11
//#define BME_CS 10

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C
//Adafruit_BME280 bme(BME_CS); // hardware SPI
//Adafruit_BME280 bme(BME_CS, BME_MOSI, BME_MISO,  BME_SCK);

float   Ro = 10;
float   SmokeCurve[3] = {2.3,0.53,-0.44};//sandbox electronics

void setup()
{
    Serial.begin(9600);
    Ro = MQCalibration();         //Calibrating the sensor. Please make sure the sensor is in clean air 
                                  //when you perform the calibration                    
    pins_init();
    if (!bme.begin()) 
    {
      Serial.println("error, Could not find a valid BME280 sensor, check wiring!");
      while (1);
    }
}
 
void loop()
{
    bme280_fn();
    sound_fn();
    water_fn();
    smoke_fn();
    delay(30000);
}

void bme280_fn()
{
    Serial.println("Temperature");
    Serial.println((bme.readTemperature() * (9.0/5.0)) + 32.0);
    //Serial.println(" F");

    Serial.println("Pressure");
    Serial.println(bme.readPressure() / 100.0F);
    //Serial.println(" mb");

    Serial.println("Humidity");
    Serial.println(bme.readHumidity());
    //Serial.println(" %");
}

void sound_fn()
{
    Serial.println("Sound");
    int sensorValue = analogRead(SOUND_SENSOR);
    Serial.println(sensorValue);
    /*if(sensorValue > THRESHOLD_VALUE_SOUND)
    {
        Serial.println(",TRUE");
    }
    else
    {
        Serial.println(",FALSE");
    }*/
}

void water_fn()
{
    Serial.println("Water");
    Serial.println(digitalRead(WATER_SENSOR));
    /*
    if(digitalRead(WATER_SENSOR) == LOW)//exposed to water
    {
      Serial.println(",TRUE");
    }
    else
    {
      Serial.println(",FALSE");
    }*/
}


void smoke_fn()
{
    Serial.println("Smoke");
    int i;
    float rs=0;
    float ratio;
 
    for (i=0;i<READ_SAMPLE_TIMES;i++) {
      rs += MQResistanceCalculation(analogRead(SMOKE_SENSOR));
      delay(READ_SAMPLE_INTERVAL);
    }
 
    rs = rs/READ_SAMPLE_TIMES;
    ratio = rs/Ro;  // ratio = RS/R0 | R0 from calibration
    
    Serial.println(MQGetPercentage(ratio, SmokeCurve));
    //Serial.print(" ppm");

    /*if(MQGetPercentage(ratio, SmokeCurve) > 100) //need to determine threshold
    {
      Serial.println(",TRUE");
    }
    else
    {
      Serial.println(",FALSE");
    }*/
}

//linear formula | approximate | from sandbox electronics demo
int  MQGetPercentage(float rs_ro_ratio, float *pcurve)
{
  return (pow(10,( ((log(rs_ro_ratio)-pcurve[1])/pcurve[2]) + pcurve[0])));
}

float MQResistanceCalculation(int raw_adc)
{
  return ( ((float)RL_VALUE*(1023-raw_adc)/raw_adc));
}

float MQCalibration()
{
  int i;
  float val=0;
 
  for (i=0;i<CALIBRATION_SAMPLE_TIMES;i++) {            //take multiple samples
    val += MQResistanceCalculation(analogRead(SMOKE_SENSOR));
    delay(CALIBRATION_SAMPLE_INTERVAL);
  }
  val = val/CALIBRATION_SAMPLE_TIMES;                   //calculate the average value
 
  val = val/RO_CLEAN_AIR_FACTOR;                        //divided by RO_CLEAN_AIR_FACTOR yields the Ro 
                                                        //according to the chart in the datasheet 
 
  return val; 
}

void pins_init()
{
    pinMode(WATER_SENSOR, INPUT);
}
