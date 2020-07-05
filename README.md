# Concentration of CO2 conservation system

## Target :
Build a system that we can control the concentration of CO2 and temperature 
separately. By monitoring the data simultaneously, a feedback control algorithm 
can be applied to adjust the speed of fan. 
## Prerequisite :
Hardware: 
1. **arduino microcontroller**: implement the interface to access different types of sensor 
and periodically send data to computer by **Serial port**.
2. **CO2 sensor (MHZ14A)**:  With at least four sensors. (unit:ppm)
3. **ventilation fan**: find a controllable fan with less noise and  [volume flow rate](https://www.mitsubishielectric.co.jp/ldg/ja/air/guide/support/knowledge/detail_01.html)
    1. [San Ace 97W](https://www.mouser.jp/datasheet/2/471/San_Ace_97W1B33_E-1600555.pdf) :
    is the candidate fan.
    2. [FY-12ZH1](https://sumai.panasonic.jp/parts/upload/pdf_manual/12ZH14031H_M.pdf) : 30(m^3/h) / 31.5(dB). 
    The original fan we use in the room.
    3. [DC402012H2B-2Tx](https://www.mouser.tw/datasheet/2/433/DC_FANS_Wakefield_Vette_Data_Sheet_rev_A-1710305.pdf) 
    is the candidate fan.
4. [cover]() is used to avoid natural convection.
5. [acrylic knife](https://www.amazon.co.jp/%E3%82%AA%E3%83%AB%E3%83%95%E3%82%A1-OLFA-205B-P%E3%82%AB%E3%83%83%E3%82%BF%E3%83%BCL%E5%9E%8B/dp/B002RV9LGE/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%82%A2%E3%82%AF%E3%83%AA%E3%83%AB+%E3%83%8A%E3%82%A4%E3%83%95&qid=1593947547&sr=8-1) 
    is used to make a suitable shape to fit ventilation fan.
6. [MAX17079](https://datasheets.maximintegrated.com/en/ds/MAX17079.pdf) is the level shifter which is used to control the ventilation fan.


Software:
1. arduino IDE : integrate FreeRTOS and CO2 sensor code.
2. pycharm: Plotting real-time data, implementing data processing using python
3. git: all source code is maintained in the **gitlab**

## The physical phenomenon:
[Thermal conductivity](https://en.wikipedia.org/wiki/Thermal_conductivity):

Considering a situation that temperature varies with the fan is running. 
It means that a running fan will enhance the efficiency of heat transfer.

[Volume flow rate](https://www.mitsubishielectric.co.jp/ldg/ja/air/guide/support/knowledge/detail_02.html):


## System structure:
