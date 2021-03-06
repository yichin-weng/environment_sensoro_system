# Concentration of CO2 conservation system

## Target :
Build a system that we can control the concentration of CO2 and temperature 
separately. By monitoring the data simultaneously, a feedback control algorithm 
can be applied to adjust the speed of fan. 

[FY-12ZH1](https://sumai.panasonic.jp/parts/upload/pdf_manual/12ZH14031H_M.pdf) specification: 30(m^3/h) / 31.5(dB). 
The fan is equipped in the CO2 room. 
## Prerequisite :
Hardware: 
1. **arduino microcontroller**: implement the interface to access different types of sensor 
and periodically send data to computer by **Serial port**.
2. **CO2 sensor (MHZ14A)**:  With at least four sensors. (unit:ppm)
3. **TR-76Ui**: control model.
4. **lists to buy**:

5. **CO2 sensor (SGP30)**: equivalent carbon dioxide and volatile organic compounds 
6. **multiple sensor(BME680)**: moisture, barometric pressure, temperature, humidity and 
volatile compounds by this sensed
[reference site](https://www.adafruit.com/product/3660)

|item|price|numbers|description|
|----|-----|-------|-----------|
|[PWMGELID FAN](https://www.amazon.co.jp/%E9%9D%99%E9%9F%B3PWM%E3%83%95%E3%82%A1%E3%83%B3-PWM-%E3%83%8F%E3%82%A4%E3%83%89%E3%83%AD%E3%83%80%E3%82%A4%E3%83%8A%E3%83%9F%E3%83%83%E3%82%AF%E3%83%99%E3%82%A2%E3%83%AA%E3%83%B3%E3%82%B0%E6%8E%A1%E7%94%A8%E9%9D%99%E9%9F%B3FAN-Silent8-PWMGELID/dp/B002BVUNEE/ref=sr_1_3?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E9%9D%99%E9%9F%B3+pwm&qid=1594096697&refinements=p_76%3A2227292051&rnid=2227291051&rps=1&s=computers&sr=1-3)|980yen/1|4|candidate axial fan|
|[voltage regulator](https://www.amazon.co.jp/DiyStudio-DC-DC%E6%98%87%E9%99%8D%E5%9C%A7%E3%82%B3%E3%83%B3%E3%83%90%E3%83%BC%E3%82%BF-5V-1-2V-5V-24V%E6%98%87%E5%9C%A7%E9%99%8D%E5%9C%A7%E9%9B%BB%E5%9C%A7%E3%83%AC%E3%82%AE%E3%83%A5%E3%83%AC%E3%83%BC%E3%82%BF%E9%9B%BB%E6%BA%90%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%ABLED%E9%9B%BB%E5%9C%A7%E8%A8%88%E3%83%87%E3%82%A3%E3%82%B9%E3%83%97%E3%83%AC%E3%82%A4%E4%BB%98%E3%81%8D5V-USB%E5%85%85%E9%9B%BB%E5%99%A8/dp/B07MVV78FH/ref=sr_1_4?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=usb+%E9%9B%BB%E5%9C%A7+%E3%83%A2%E3%82%B8%E3%83%A5%E3%83%BC%E3%83%AB&qid=1594031675&s=industrial&sr=1-4)|659yen/1|4|USB-type voltage regulator for axial fan.|
|[USB cable](https://www.amazon.co.jp/Amazon%E3%83%99%E3%83%BC%E3%82%B7%E3%83%83%E3%82%AF-AmazonBasics-FDBU-USB3-0%E5%BB%B6%E9%95%B7%E3%82%B1%E3%83%BC%E3%83%96%E3%83%AB-A%E3%82%AA%E3%82%B9-A%E3%83%A1%E3%82%B9/dp/B00NH134L6/ref=sr_1_11?dchild=1&keywords=USBA%2B%E5%BB%B6%E9%95%B7&qid=1594031948&sr=8-11&th=1)| 798yen/1| 4|power line|
|[cover(not found yet)]()| ?| 4|is used to avoid natural convection|
|[plastic box](https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%AD%E3%83%A3%E3%83%AA%E3%83%BC%E3%82%B9%E3%83%88%E3%83%83%E3%82%AB%E3%83%BC-%E5%B9%8540%C3%97%E5%A5%A5%E8%A1%8C74%C3%97%E9%AB%98%E3%81%9531cm-4%E5%80%8B%E3%82%BB%E3%83%83%E3%83%88-AA-740E/dp/B001UQWSYO/ref=sr_1_5?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=plastic+box&qid=1594029543&sr=8-5)| 4404yen/4| 4| They are used for installing a new axial fan|
|[acrylic knife](https://www.amazon.co.jp/%E3%82%AA%E3%83%AB%E3%83%95%E3%82%A1-OLFA-204B-P%E3%82%AB%E3%83%83%E3%82%BF%E3%83%BCS%E5%9E%8B/dp/B002RVEYGG/ref=sr_1_30?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=UHDUU6MJ99RK&dchild=1&keywords=%E3%83%97%E3%83%A9%E3%82%B9%E3%83%81%E3%83%83%E3%82%AF+%E3%82%AB%E3%83%83%E3%82%BF%E3%83%BC&qid=1594031029&s=diy&sprefix=%E3%81%B7%E3%82%89%E3%81%99%E3%81%A3%E3%81%A1%2Cdiy%2C244&sr=1-30)|394yen/1|1|is used to make a suitable shape to fit axial fan|
|[saw](https://www.amazon.co.jp/dp/B07B7CYW3K/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B07B7CYW3K&pd_rd_w=cFOti&pf_rd_p=6413bd85-d494-49e7-9f81-0e63e79171a9&pd_rd_wg=wHhY7&pf_rd_r=10VQFANVXCCDA2KEEK90&pd_rd_r=0bae6020-57f4-4421-88d0-370ff34c258b&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTTZCNE5DSkxFOUE5JmVuY3J5cHRlZElkPUEwODIwOTU4SDlQRlBUTDZSUUxNJmVuY3J5cHRlZEFkSWQ9QUpKMDFLMThZMU8zRiZ3aWRnZXROYW1lPXNwX2RldGFpbCZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)|1780yen/1|1|cut the plastic box|

**ask how to buy**:    

|item|price|numbers|description|
|----|-----|-------|-----------|
|[MAX17079](https://www.digikey.jp/products/en/development-boards-kits-programmers/evaluation-and-demonstration-boards-and-kits/787?k=MAX17079)|8420yen/1|1|is the level shifter which is used to control multiple fans.|
|[automatic screw](https://reurl.cc/Q3n260)|
|[4pin 2510](https://reurl.cc/KjKqAy)|
    
Software:
1. arduino IDE : integrate FreeRTOS and CO2 sensor code.
2. pycharm: Plotting real-time data, implementing data processing using python
3. git: all source code is maintained in the **gitlab**

[espressif project for bluetooth mesh](https://github.com/espressif/esp-idf/tree/8bc19ba893e5544d571a753d82b44a84799b94b1/examples/bluetooth/esp_ble_mesh/ble_mesh_sensor_model/sensor_client)

## The physical phenomenon:
[Thermal conductivity](https://en.wikipedia.org/wiki/Thermal_conductivity):

Considering a situation that temperature varies with the fan is running. 
It means that a running fan will enhance the efficiency of heat transfer.

[Volume flow rate](https://www.mitsubishielectric.co.jp/ldg/ja/air/guide/support/knowledge/detail_02.html):


## System structure:

## design pattern:
1.  abstract factory: In this type design pattern, it creates an interface to extend and customize components.
2.  adapter: It is used to support legacy code. (It will not be used in this project)
3.  builder: It is used to build an object with a lot of configurations.
4.  factory method: It can provide high level flexibility.
5.  command: It is used for queueing task, callbacks, tracking operation.
6.  iterator: It is used for traversing the collections
7.  observer: It provides a way to react to an event happening in other objects.
8.  strategy: It provides the flexibility that users define their own strategy to change the operation of the object.



iterator for creating device we have.

###
In order to build a system like the following figure, A multitask real-time OS need.

```plantuml
node pc1
node sensor1
node sensor2
node sensor3
node sensor4
pc1 <--> sensor1 : SoftwareSerial
pc1 <--> sensor2 : SoftwareSerial
pc1 <--> sensor3 : SoftwareSerial
pc1 <--> sensor4 : SoftwareSerial
```

### basic concepts:
    
    1. python:
        1. control multi-sensors
            define instruction:
                1. set up CO2 sensor parameter.
                2. If needed, interrupt individual device.
        2. plot a live graph
        3. (optional) analyze data real-time
        
```plantuml

start
:instantiate a GUI
:access 'COM3'
:instantiate all the devices;
:check connection with different devices;
:check whether we need to calibrate or not;
if (iscalibration?) then (true)
    :calibrate all devices by the instruction defined by sensor;
else(false)
endif
while ()
    :read CO2 UART;
    :read CO2 PWM;
    :get temperature;
endwhile

stop
```
        
    2. arduino:
        real-time operating system
            1. initialize every sensor.
            2. sample data from different sensors.
            3. react with Personal Computer(python)
        
