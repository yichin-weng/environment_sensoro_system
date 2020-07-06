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
    1. **axial fan**: find a controllable fan with less noise and  [volume flow rate](https://www.mitsubishielectric.co.jp/ldg/ja/air/guide/support/knowledge/detail_01.html)
        1. [109R0605H402](https://www.amazon.co.jp/SANYO-DENKI-SANACE-109R0605H402-AXIAL/dp/B00DJY6CVK/ref=sr_1_82?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=axial+fans&qid=1594027788&sr=8-82) is the candidate axial fan.
    2. [voltage regulator](https://www.amazon.co.jp/dp/B08CDHZHX5/ref=sr_1_28?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=5volt+power+supply&qid=1594028534&sr=8-28) USB-type voltage regulator for axial fan
    3. [cover(not found yet)]() is used to avoid natural convection.
    4. [plastic box](https://www.amazon.co.jp/%E3%82%A2%E3%82%A4%E3%83%AA%E3%82%B9%E3%82%AA%E3%83%BC%E3%83%A4%E3%83%9E-%E3%82%AD%E3%83%A3%E3%83%AA%E3%83%BC%E3%82%B9%E3%83%88%E3%83%83%E3%82%AB%E3%83%BC-%E5%B9%8540%C3%97%E5%A5%A5%E8%A1%8C74%C3%97%E9%AB%98%E3%81%9531cm-4%E5%80%8B%E3%82%BB%E3%83%83%E3%83%88-AA-740E/dp/B001UQWSYO/ref=sr_1_5?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=plastic+box&qid=1594029543&sr=8-5) for installing a new axial fan
    5. [acrylic knife](https://www.amazon.co.jp/%E3%82%AA%E3%83%AB%E3%83%95%E3%82%A1-OLFA-205B-P%E3%82%AB%E3%83%83%E3%82%BF%E3%83%BCL%E5%9E%8B/dp/B002RV9LGE/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E3%82%A2%E3%82%AF%E3%83%AA%E3%83%AB+%E3%83%8A%E3%82%A4%E3%83%95&qid=1593947547&sr=8-1) is the candidate axial fan
        is used to make a suitable shape to fit axial fan.
    6. [saw](https://www.amazon.co.jp/dp/B07B7CYW3K/ref=sspa_dk_detail_2?psc=1&pd_rd_i=B07B7CYW3K&pd_rd_w=cFOti&pf_rd_p=6413bd85-d494-49e7-9f81-0e63e79171a9&pd_rd_wg=wHhY7&pf_rd_r=10VQFANVXCCDA2KEEK90&pd_rd_r=0bae6020-57f4-4421-88d0-370ff34c258b&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUExTTZCNE5DSkxFOUE5JmVuY3J5cHRlZElkPUEwODIwOTU4SDlQRlBUTDZSUUxNJmVuY3J5cHRlZEFkSWQ9QUpKMDFLMThZMU8zRiZ3aWRnZXROYW1lPXNwX2RldGFpbCZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=)
        cut the plastic box
4. **ask how to buy**:    
    1. [MAX17079](https://datasheets.maximintegrated.com/en/ds/MAX17079.pdf) is the level shifter which is used to control multiple fans.

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
