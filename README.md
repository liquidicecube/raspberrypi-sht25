# raspberrypi-sht25
Interfacing sensirion sht25 temperature/humidity sensor with raspberry pi

SHT25 dataset:
http://www.sensirion.com/fileadmin/user_upload/customers/sensirion/Dokumente/Humidity/Sensirion_Humidity_SHT25_Datasheet_V3.pdf
(pages 7-10)


Initial testing:
pi@raspberrypi ~/raspberrypi-sht25 $ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
     00:          -- -- -- -- -- -- -- -- -- -- -- -- --
     10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
     70: -- -- -- -- -- -- -- --


Issues:

Synchronous measure/read interface ("hold master mode") doesn't work
reliably (sometimes i/o error on write, sometimes on read).
Didn't try this patch since switching to "no hold master" mode works:
https://github.com/raspberrypi/linux/issues/211

Chose conservative delays per dataset.
Might be able to poll at higher frequency and catch IO error.
