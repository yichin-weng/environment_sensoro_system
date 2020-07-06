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
3. **list to buy**:
    3. **axial fan**: find a controllable fan with less noise and  [volume flow rate](https://www.mitsubishielectric.co.jp/ldg/ja/air/guide/support/knowledge/detail_01.html)
        1. [109R0605H402](https://www.amazon.co.jp/SANYO-DENKI-SANACE-109R0605H402-AXIAL/dp/B00DJY6CVK/ref=sr_1_82?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=axial+fans&qid=1594027788&sr=8-82) is the candidate axial fan.
    4. [voltage regulator](https://www.amazon.co.jp/dp/B08CDHZHX5/ref=sr_1_28?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=5volt+power+supply&qid=1594028534&sr=8-28) USB-type voltage regulator for axial fan
    5. [cover(not found yet)]() is used to avoid natural convection.
    5. [plastic box](https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%AD%E3%83%A3%E3%83%AA%E3%83%BC%E3%82%B9%E3%83%88%E3%83%83%E3%82%AB%E3%83%BC-%E5%B9%8540%C3%97%E5%A5%A5%E8%A1%8C74%C3%97%E9%AB%98%E3%81%9531cm-4%E5%80%8B%E3%82%BB%E3%83%83%E3%83%88-AA-740E/dp/B001UQWSYO/ref=sr_1_5?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=plastic+box&qid=1594029543&sr=8-5) for installing a new axial fan
    6. [acrylic knife](https://www.amazon.co.jp/%E3%82%AA%E3%83%AB%E3%83%95%E3%82%A1-OLFA-205B-P%E3%82%AB%E3%83%83%E3%82%BF%E3%83%BCL%E5%9E%8B/dp/B002RV9LGE/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%82%A2%E3%82%AF%E3%83%AA%E3%83%AB+%E3%83%8A%E3%82%A4%E3%83%95&qid=1593947547&sr=8-1) is the candidate axial fan
        is used to make a suitable shape to fit axial fan.
    8. [saw](https://www.amazon.co.jp/FLORA-GUARD-%E6%8A%98%E8%BE%BC%E9%8B%B8-%E6%9B%BF%E5%88%83%E5%BC%8F%E5%89%AA%E5%AE%9A%E9%8B%B8%E3%80%81%E9%A0%91%E4%B8%88%E3%81%AA195mm%E3%83%96%E3%83%AC%E3%83%BC%E3%83%89%E3%81%A7%E3%81%AE%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%97-%E3%83%97%E3%83%AB%E3%83%BC%E3%83%8B%E3%83%B3%E3%82%B0%E3%82%BD%E3%83%BC%E3%80%81%E3%83%8E%E3%82%B3%E3%82%AE%E3%83%AA%E4%B8%87%E8%83%BD/dp/B06XSFMVRV/ref=sr_1_4_sspa?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&crid=1SP6Z29RLDU9C&dchild=1&keywords=%E3%83%8E%E3%82%B3%E3%82%AE%E3%83%AA+%E3%83%97%E3%83%A9%E3%82%B9%E3%83%81%E3%83%83%E3%82%AF&qid=1594024859&sprefix=%E3%81%AE%E3%81%93%E3%81%8E%E3%82%8A%E3%80%80%E3%81%B7%E3%82%89%2Cundefined%2C226&sr=8-4-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzMkdPQTU2RVZWTVJCJmVuY3J5cHRlZElkPUEwODU2NDgzSTVFTVM4OTI3TEgzJmVuY3J5cHRlZEFkSWQ9QVlNVVZKQkJNVVdQRCZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)
        cut the plastic box
4. **ask how to buy**:    
    7. [MAX17079](https://datasheets.maximintegrated.com/en/ds/MAX17079.pdf) is the level shifter which is used to control multiple fans.

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
