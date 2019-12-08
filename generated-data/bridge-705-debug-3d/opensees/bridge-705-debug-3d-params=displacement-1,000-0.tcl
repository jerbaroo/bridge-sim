
# Programatically generated file.
#
# Units:
# - dimension: metre
# - force: newton
#
# Dimension order is
# - x: longitudinal
# - y: vertical
# - z: transverse

wipe

model basic -ndm 3 -ndf 6

# node nodeTag x y z
# Begin deck nodes
node 100 0 0 -16.6
node 101 11.575 0 -16.6
node 102 14.675 0 -16.6
node 103 26.875 0 -16.6
node 104 29.975 0 -16.6
node 105 42.175 0 -16.6
node 106 45.275 0 -16.6
node 107 51.375 0 -16.6
node 108 57.475 0 -16.6
node 109 60.575 0 -16.6
node 110 72.775 0 -16.6
node 111 75.875 0 -16.6
node 112 88.075 0 -16.6
node 113 91.175 0 -16.6
node 114 102.75 0 -16.6
node 200 0 0 -14.433
node 201 11.575 0 -14.433; # support node
node 202 14.675 0 -14.433; # support node
node 203 26.875 0 -14.433; # support node
node 204 29.975 0 -14.433; # support node
node 205 42.175 0 -14.433; # support node
node 206 45.275 0 -14.433; # support node
node 207 51.375 0 -14.433
node 208 57.475 0 -14.433; # support node
node 209 60.575 0 -14.433; # support node
node 210 72.775 0 -14.433; # support node
node 211 75.875 0 -14.433; # support node
node 212 88.075 0 -14.433; # support node
node 213 91.175 0 -14.433; # support node
node 214 102.75 0 -14.433
node 300 0 0 -12.6
node 301 11.575 0 -12.6; # support node
node 302 14.675 0 -12.6; # support node
node 303 26.875 0 -12.6; # support node
node 304 29.975 0 -12.6; # support node
node 305 42.175 0 -12.6; # support node
node 306 45.275 0 -12.6; # support node
node 307 51.375 0 -12.6
node 308 57.475 0 -12.6; # support node
node 309 60.575 0 -12.6; # support node
node 310 72.775 0 -12.6; # support node
node 311 75.875 0 -12.6; # support node
node 312 88.075 0 -12.6; # support node
node 313 91.175 0 -12.6; # support node
node 314 102.75 0 -12.6
node 400 0 0 -10.767
node 401 11.575 0 -10.767; # support node
node 402 14.675 0 -10.767; # support node
node 403 26.875 0 -10.767; # support node
node 404 29.975 0 -10.767; # support node
node 405 42.175 0 -10.767; # support node
node 406 45.275 0 -10.767; # support node
node 407 51.375 0 -10.767
node 408 57.475 0 -10.767; # support node
node 409 60.575 0 -10.767; # support node
node 410 72.775 0 -10.767; # support node
node 411 75.875 0 -10.767; # support node
node 412 88.075 0 -10.767; # support node
node 413 91.175 0 -10.767; # support node
node 414 102.75 0 -10.767
node 500 0 0 -6.033
node 501 11.575 0 -6.033; # support node
node 502 14.675 0 -6.033; # support node
node 503 26.875 0 -6.033; # support node
node 504 29.975 0 -6.033; # support node
node 505 42.175 0 -6.033; # support node
node 506 45.275 0 -6.033; # support node
node 507 51.375 0 -6.033
node 508 57.475 0 -6.033; # support node
node 509 60.575 0 -6.033; # support node
node 510 72.775 0 -6.033; # support node
node 511 75.875 0 -6.033; # support node
node 512 88.075 0 -6.033; # support node
node 513 91.175 0 -6.033; # support node
node 514 102.75 0 -6.033
node 600 0 0 -4.2
node 601 11.575 0 -4.2; # support node
node 602 14.675 0 -4.2; # support node
node 603 26.875 0 -4.2; # support node
node 604 29.975 0 -4.2; # support node
node 605 42.175 0 -4.2; # support node
node 606 45.275 0 -4.2; # support node
node 607 51.375 0 -4.2
node 608 57.475 0 -4.2; # support node
node 609 60.575 0 -4.2; # support node
node 610 72.775 0 -4.2; # support node
node 611 75.875 0 -4.2; # support node
node 612 88.075 0 -4.2; # support node
node 613 91.175 0 -4.2; # support node
node 614 102.75 0 -4.2
node 700 0 0 -2.367
node 701 11.575 0 -2.367; # support node
node 702 14.675 0 -2.367; # support node
node 703 26.875 0 -2.367; # support node
node 704 29.975 0 -2.367; # support node
node 705 42.175 0 -2.367; # support node
node 706 45.275 0 -2.367; # support node
node 707 51.375 0 -2.367
node 708 57.475 0 -2.367; # support node
node 709 60.575 0 -2.367; # support node
node 710 72.775 0 -2.367; # support node
node 711 75.875 0 -2.367; # support node
node 712 88.075 0 -2.367; # support node
node 713 91.175 0 -2.367; # support node
node 714 102.75 0 -2.367
node 800 0 0 0.0
node 801 11.575 0 0.0
node 802 14.675 0 0.0
node 803 26.875 0 0.0
node 804 29.975 0 0.0
node 805 42.175 0 0.0
node 806 45.275 0 0.0
node 807 51.375 0 0.0
node 808 57.475 0 0.0
node 809 60.575 0 0.0
node 810 72.775 0 0.0
node 811 75.875 0 0.0
node 812 88.075 0 0.0
node 813 91.175 0 0.0
node 814 102.75 0 0.0
node 900 0 0 2.367
node 901 11.575 0 2.367; # support node
node 902 14.675 0 2.367; # support node
node 903 26.875 0 2.367; # support node
node 904 29.975 0 2.367; # support node
node 905 42.175 0 2.367; # support node
node 906 45.275 0 2.367; # support node
node 907 51.375 0 2.367
node 908 57.475 0 2.367; # support node
node 909 60.575 0 2.367; # support node
node 910 72.775 0 2.367; # support node
node 911 75.875 0 2.367; # support node
node 912 88.075 0 2.367; # support node
node 913 91.175 0 2.367; # support node
node 914 102.75 0 2.367
node 1000 0 0 4.2
node 1001 11.575 0 4.2; # support node
node 1002 14.675 0 4.2; # support node
node 1003 26.875 0 4.2; # support node
node 1004 29.975 0 4.2; # support node
node 1005 42.175 0 4.2; # support node
node 1006 45.275 0 4.2; # support node
node 1007 51.375 0 4.2
node 1008 57.475 0 4.2; # support node
node 1009 60.575 0 4.2; # support node
node 1010 72.775 0 4.2; # support node
node 1011 75.875 0 4.2; # support node
node 1012 88.075 0 4.2; # support node
node 1013 91.175 0 4.2; # support node
node 1014 102.75 0 4.2
node 1100 0 0 6.033
node 1101 11.575 0 6.033; # support node
node 1102 14.675 0 6.033; # support node
node 1103 26.875 0 6.033; # support node
node 1104 29.975 0 6.033; # support node
node 1105 42.175 0 6.033; # support node
node 1106 45.275 0 6.033; # support node
node 1107 51.375 0 6.033
node 1108 57.475 0 6.033; # support node
node 1109 60.575 0 6.033; # support node
node 1110 72.775 0 6.033; # support node
node 1111 75.875 0 6.033; # support node
node 1112 88.075 0 6.033; # support node
node 1113 91.175 0 6.033; # support node
node 1114 102.75 0 6.033
node 1200 0 0 10.767
node 1201 11.575 0 10.767; # support node
node 1202 14.675 0 10.767; # support node
node 1203 26.875 0 10.767; # support node
node 1204 29.975 0 10.767; # support node
node 1205 42.175 0 10.767; # support node
node 1206 45.275 0 10.767; # support node
node 1207 51.375 0 10.767
node 1208 57.475 0 10.767; # support node
node 1209 60.575 0 10.767; # support node
node 1210 72.775 0 10.767; # support node
node 1211 75.875 0 10.767; # support node
node 1212 88.075 0 10.767; # support node
node 1213 91.175 0 10.767; # support node
node 1214 102.75 0 10.767
node 1300 0 0 12.6
node 1301 11.575 0 12.6; # support node
node 1302 14.675 0 12.6; # support node
node 1303 26.875 0 12.6; # support node
node 1304 29.975 0 12.6; # support node
node 1305 42.175 0 12.6; # support node
node 1306 45.275 0 12.6; # support node
node 1307 51.375 0 12.6
node 1308 57.475 0 12.6; # support node
node 1309 60.575 0 12.6; # support node
node 1310 72.775 0 12.6; # support node
node 1311 75.875 0 12.6; # support node
node 1312 88.075 0 12.6; # support node
node 1313 91.175 0 12.6; # support node
node 1314 102.75 0 12.6
node 1400 0 0 14.433
node 1401 11.575 0 14.433; # support node
node 1402 14.675 0 14.433; # support node
node 1403 26.875 0 14.433; # support node
node 1404 29.975 0 14.433; # support node
node 1405 42.175 0 14.433; # support node
node 1406 45.275 0 14.433; # support node
node 1407 51.375 0 14.433
node 1408 57.475 0 14.433; # support node
node 1409 60.575 0 14.433; # support node
node 1410 72.775 0 14.433; # support node
node 1411 75.875 0 14.433; # support node
node 1412 88.075 0 14.433; # support node
node 1413 91.175 0 14.433; # support node
node 1414 102.75 0 14.433
node 1500 0 0 16.6
node 1501 11.575 0 16.6
node 1502 14.675 0 16.6
node 1503 26.875 0 16.6
node 1504 29.975 0 16.6
node 1505 42.175 0 16.6
node 1506 45.275 0 16.6
node 1507 51.375 0 16.6
node 1508 57.475 0 16.6
node 1509 60.575 0 16.6
node 1510 72.775 0 16.6
node 1511 75.875 0 16.6
node 1512 88.075 0 16.6
node 1513 91.175 0 16.6
node 1514 102.75 0 16.6
# End deck nodes

# node nodeTag x y z
# Begin support nodes
node 1600 12.35 -1.75 -13.9665; # support 1st wall 1st z 1 y 2nd
node 1601 13.125 -3.5 -13.5; # support 1st wall 1st z 1 y 3rd
node 1700 12.35 -1.75 -12.6; # support 1st wall 1st z 2 y 2nd
node 1701 13.125 -3.5 -12.6; # support 1st wall 1st z 2 y 3rd
node 1800 12.35 -1.75 -11.2335; # support 1st wall 1st z 3 y 2nd
node 1801 13.125 -3.5 -11.7; # support 1st wall 1st z 3 y 3rd
node 1900 13.9 -1.75 -13.9665; # support 1st wall 2nd z 1 y 2nd
node 2000 13.9 -1.75 -12.6; # support 1st wall 2nd z 2 y 2nd
node 2100 13.9 -1.75 -11.2335; # support 1st wall 2nd z 3 y 2nd
node 2200 12.35 -1.75 -5.5665; # support 2nd wall 1st z 1 y 2nd
node 2201 13.125 -3.5 -5.1; # support 2nd wall 1st z 1 y 3rd
node 2300 12.35 -1.75 -4.2; # support 2nd wall 1st z 2 y 2nd
node 2301 13.125 -3.5 -4.2; # support 2nd wall 1st z 2 y 3rd
node 2400 12.35 -1.75 -2.8335; # support 2nd wall 1st z 3 y 2nd
node 2401 13.125 -3.5 -3.3; # support 2nd wall 1st z 3 y 3rd
node 2500 13.9 -1.75 -5.5665; # support 2nd wall 2nd z 1 y 2nd
node 2600 13.9 -1.75 -4.2; # support 2nd wall 2nd z 2 y 2nd
node 2700 13.9 -1.75 -2.8335; # support 2nd wall 2nd z 3 y 2nd
node 2800 12.35 -1.75 2.8335; # support 3rd wall 1st z 1 y 2nd
node 2801 13.125 -3.5 3.3; # support 3rd wall 1st z 1 y 3rd
node 2900 12.35 -1.75 4.2; # support 3rd wall 1st z 2 y 2nd
node 2901 13.125 -3.5 4.2; # support 3rd wall 1st z 2 y 3rd
node 3000 12.35 -1.75 5.5665; # support 3rd wall 1st z 3 y 2nd
node 3001 13.125 -3.5 5.1; # support 3rd wall 1st z 3 y 3rd
node 3100 13.9 -1.75 2.8335; # support 3rd wall 2nd z 1 y 2nd
node 3200 13.9 -1.75 4.2; # support 3rd wall 2nd z 2 y 2nd
node 3300 13.9 -1.75 5.5665; # support 3rd wall 2nd z 3 y 2nd
node 3400 12.35 -1.75 11.2335; # support 4th wall 1st z 1 y 2nd
node 3401 13.125 -3.5 11.7; # support 4th wall 1st z 1 y 3rd
node 3500 12.35 -1.75 12.6; # support 4th wall 1st z 2 y 2nd
node 3501 13.125 -3.5 12.6; # support 4th wall 1st z 2 y 3rd
node 3600 12.35 -1.75 13.9665; # support 4th wall 1st z 3 y 2nd
node 3601 13.125 -3.5 13.5; # support 4th wall 1st z 3 y 3rd
node 3700 13.9 -1.75 11.2335; # support 4th wall 2nd z 1 y 2nd
node 3800 13.9 -1.75 12.6; # support 4th wall 2nd z 2 y 2nd
node 3900 13.9 -1.75 13.9665; # support 4th wall 2nd z 3 y 2nd
node 4000 27.65 -1.75 -13.9665; # support 5th wall 1st z 1 y 2nd
node 4001 28.425 -3.5 -13.5; # support 5th wall 1st z 1 y 3rd
node 4100 27.65 -1.75 -12.6; # support 5th wall 1st z 2 y 2nd
node 4101 28.425 -3.5 -12.6; # support 5th wall 1st z 2 y 3rd
node 4200 27.65 -1.75 -11.2335; # support 5th wall 1st z 3 y 2nd
node 4201 28.425 -3.5 -11.7; # support 5th wall 1st z 3 y 3rd
node 4300 29.2 -1.75 -13.9665; # support 5th wall 2nd z 1 y 2nd
node 4400 29.2 -1.75 -12.6; # support 5th wall 2nd z 2 y 2nd
node 4500 29.2 -1.75 -11.2335; # support 5th wall 2nd z 3 y 2nd
node 4600 27.65 -1.75 -5.5665; # support 6th wall 1st z 1 y 2nd
node 4601 28.425 -3.5 -5.1; # support 6th wall 1st z 1 y 3rd
node 4700 27.65 -1.75 -4.2; # support 6th wall 1st z 2 y 2nd
node 4701 28.425 -3.5 -4.2; # support 6th wall 1st z 2 y 3rd
node 4800 27.65 -1.75 -2.8335; # support 6th wall 1st z 3 y 2nd
node 4801 28.425 -3.5 -3.3; # support 6th wall 1st z 3 y 3rd
node 4900 29.2 -1.75 -5.5665; # support 6th wall 2nd z 1 y 2nd
node 5000 29.2 -1.75 -4.2; # support 6th wall 2nd z 2 y 2nd
node 5100 29.2 -1.75 -2.8335; # support 6th wall 2nd z 3 y 2nd
node 5200 27.65 -1.75 2.8335; # support 7th wall 1st z 1 y 2nd
node 5201 28.425 -3.5 3.3; # support 7th wall 1st z 1 y 3rd
node 5300 27.65 -1.75 4.2; # support 7th wall 1st z 2 y 2nd
node 5301 28.425 -3.5 4.2; # support 7th wall 1st z 2 y 3rd
node 5400 27.65 -1.75 5.5665; # support 7th wall 1st z 3 y 2nd
node 5401 28.425 -3.5 5.1; # support 7th wall 1st z 3 y 3rd
node 5500 29.2 -1.75 2.8335; # support 7th wall 2nd z 1 y 2nd
node 5600 29.2 -1.75 4.2; # support 7th wall 2nd z 2 y 2nd
node 5700 29.2 -1.75 5.5665; # support 7th wall 2nd z 3 y 2nd
node 5800 27.65 -1.75 11.2335; # support 8th wall 1st z 1 y 2nd
node 5801 28.425 -3.5 11.7; # support 8th wall 1st z 1 y 3rd
node 5900 27.65 -1.75 12.6; # support 8th wall 1st z 2 y 2nd
node 5901 28.425 -3.5 12.6; # support 8th wall 1st z 2 y 3rd
node 6000 27.65 -1.75 13.9665; # support 8th wall 1st z 3 y 2nd
node 6001 28.425 -3.5 13.5; # support 8th wall 1st z 3 y 3rd
node 6100 29.2 -1.75 11.2335; # support 8th wall 2nd z 1 y 2nd
node 6200 29.2 -1.75 12.6; # support 8th wall 2nd z 2 y 2nd
node 6300 29.2 -1.75 13.9665; # support 8th wall 2nd z 3 y 2nd
node 6400 42.95 -1.75 -13.9665; # support 9th wall 1st z 1 y 2nd
node 6401 43.725 -3.5 -13.5; # support 9th wall 1st z 1 y 3rd
node 6500 42.95 -1.75 -12.6; # support 9th wall 1st z 2 y 2nd
node 6501 43.725 -3.5 -12.6; # support 9th wall 1st z 2 y 3rd
node 6600 42.95 -1.75 -11.2335; # support 9th wall 1st z 3 y 2nd
node 6601 43.725 -3.5 -11.7; # support 9th wall 1st z 3 y 3rd
node 6700 44.5 -1.75 -13.9665; # support 9th wall 2nd z 1 y 2nd
node 6800 44.5 -1.75 -12.6; # support 9th wall 2nd z 2 y 2nd
node 6900 44.5 -1.75 -11.2335; # support 9th wall 2nd z 3 y 2nd
node 7000 42.95 -1.75 -5.5665; # support 10th wall 1st z 1 y 2nd
node 7001 43.725 -3.5 -5.1; # support 10th wall 1st z 1 y 3rd
node 7100 42.95 -1.75 -4.2; # support 10th wall 1st z 2 y 2nd
node 7101 43.725 -3.5 -4.2; # support 10th wall 1st z 2 y 3rd
node 7200 42.95 -1.75 -2.8335; # support 10th wall 1st z 3 y 2nd
node 7201 43.725 -3.5 -3.3; # support 10th wall 1st z 3 y 3rd
node 7300 44.5 -1.75 -5.5665; # support 10th wall 2nd z 1 y 2nd
node 7400 44.5 -1.75 -4.2; # support 10th wall 2nd z 2 y 2nd
node 7500 44.5 -1.75 -2.8335; # support 10th wall 2nd z 3 y 2nd
node 7600 42.95 -1.75 2.8335; # support 11th wall 1st z 1 y 2nd
node 7601 43.725 -3.5 3.3; # support 11th wall 1st z 1 y 3rd
node 7700 42.95 -1.75 4.2; # support 11th wall 1st z 2 y 2nd
node 7701 43.725 -3.5 4.2; # support 11th wall 1st z 2 y 3rd
node 7800 42.95 -1.75 5.5665; # support 11th wall 1st z 3 y 2nd
node 7801 43.725 -3.5 5.1; # support 11th wall 1st z 3 y 3rd
node 7900 44.5 -1.75 2.8335; # support 11th wall 2nd z 1 y 2nd
node 8000 44.5 -1.75 4.2; # support 11th wall 2nd z 2 y 2nd
node 8100 44.5 -1.75 5.5665; # support 11th wall 2nd z 3 y 2nd
node 8200 42.95 -1.75 11.2335; # support 12th wall 1st z 1 y 2nd
node 8201 43.725 -3.5 11.7; # support 12th wall 1st z 1 y 3rd
node 8300 42.95 -1.75 12.6; # support 12th wall 1st z 2 y 2nd
node 8301 43.725 -3.5 12.6; # support 12th wall 1st z 2 y 3rd
node 8400 42.95 -1.75 13.9665; # support 12th wall 1st z 3 y 2nd
node 8401 43.725 -3.5 13.5; # support 12th wall 1st z 3 y 3rd
node 8500 44.5 -1.75 11.2335; # support 12th wall 2nd z 1 y 2nd
node 8600 44.5 -1.75 12.6; # support 12th wall 2nd z 2 y 2nd
node 8700 44.5 -1.75 13.9665; # support 12th wall 2nd z 3 y 2nd
node 8800 58.25 -1.75 -13.9665; # support 13th wall 1st z 1 y 2nd
node 8801 59.025 -3.5 -13.5; # support 13th wall 1st z 1 y 3rd
node 8900 58.25 -1.75 -12.6; # support 13th wall 1st z 2 y 2nd
node 8901 59.025 -3.5 -12.6; # support 13th wall 1st z 2 y 3rd
node 9000 58.25 -1.75 -11.2335; # support 13th wall 1st z 3 y 2nd
node 9001 59.025 -3.5 -11.7; # support 13th wall 1st z 3 y 3rd
node 9100 59.8 -1.75 -13.9665; # support 13th wall 2nd z 1 y 2nd
node 9200 59.8 -1.75 -12.6; # support 13th wall 2nd z 2 y 2nd
node 9300 59.8 -1.75 -11.2335; # support 13th wall 2nd z 3 y 2nd
node 9400 58.25 -1.75 -5.5665; # support 14th wall 1st z 1 y 2nd
node 9401 59.025 -3.5 -5.1; # support 14th wall 1st z 1 y 3rd
node 9500 58.25 -1.75 -4.2; # support 14th wall 1st z 2 y 2nd
node 9501 59.025 -3.5 -4.2; # support 14th wall 1st z 2 y 3rd
node 9600 58.25 -1.75 -2.8335; # support 14th wall 1st z 3 y 2nd
node 9601 59.025 -3.5 -3.3; # support 14th wall 1st z 3 y 3rd
node 9700 59.8 -1.75 -5.5665; # support 14th wall 2nd z 1 y 2nd
node 9800 59.8 -1.75 -4.2; # support 14th wall 2nd z 2 y 2nd
node 9900 59.8 -1.75 -2.8335; # support 14th wall 2nd z 3 y 2nd
node 10000 58.25 -1.75 2.8335; # support 15th wall 1st z 1 y 2nd
node 10001 59.025 -3.5 3.3; # support 15th wall 1st z 1 y 3rd
node 10100 58.25 -1.75 4.2; # support 15th wall 1st z 2 y 2nd
node 10101 59.025 -3.5 4.2; # support 15th wall 1st z 2 y 3rd
node 10200 58.25 -1.75 5.5665; # support 15th wall 1st z 3 y 2nd
node 10201 59.025 -3.5 5.1; # support 15th wall 1st z 3 y 3rd
node 10300 59.8 -1.75 2.8335; # support 15th wall 2nd z 1 y 2nd
node 10400 59.8 -1.75 4.2; # support 15th wall 2nd z 2 y 2nd
node 10500 59.8 -1.75 5.5665; # support 15th wall 2nd z 3 y 2nd
node 10600 58.25 -1.75 11.2335; # support 16th wall 1st z 1 y 2nd
node 10601 59.025 -3.5 11.7; # support 16th wall 1st z 1 y 3rd
node 10700 58.25 -1.75 12.6; # support 16th wall 1st z 2 y 2nd
node 10701 59.025 -3.5 12.6; # support 16th wall 1st z 2 y 3rd
node 10800 58.25 -1.75 13.9665; # support 16th wall 1st z 3 y 2nd
node 10801 59.025 -3.5 13.5; # support 16th wall 1st z 3 y 3rd
node 10900 59.8 -1.75 11.2335; # support 16th wall 2nd z 1 y 2nd
node 11000 59.8 -1.75 12.6; # support 16th wall 2nd z 2 y 2nd
node 11100 59.8 -1.75 13.9665; # support 16th wall 2nd z 3 y 2nd
node 11200 73.55 -1.75 -13.9665; # support 17th wall 1st z 1 y 2nd
node 11201 74.325 -3.5 -13.5; # support 17th wall 1st z 1 y 3rd
node 11300 73.55 -1.75 -12.6; # support 17th wall 1st z 2 y 2nd
node 11301 74.325 -3.5 -12.6; # support 17th wall 1st z 2 y 3rd
node 11400 73.55 -1.75 -11.2335; # support 17th wall 1st z 3 y 2nd
node 11401 74.325 -3.5 -11.7; # support 17th wall 1st z 3 y 3rd
node 11500 75.1 -1.75 -13.9665; # support 17th wall 2nd z 1 y 2nd
node 11600 75.1 -1.75 -12.6; # support 17th wall 2nd z 2 y 2nd
node 11700 75.1 -1.75 -11.2335; # support 17th wall 2nd z 3 y 2nd
node 11800 73.55 -1.75 -5.5665; # support 18th wall 1st z 1 y 2nd
node 11801 74.325 -3.5 -5.1; # support 18th wall 1st z 1 y 3rd
node 11900 73.55 -1.75 -4.2; # support 18th wall 1st z 2 y 2nd
node 11901 74.325 -3.5 -4.2; # support 18th wall 1st z 2 y 3rd
node 12000 73.55 -1.75 -2.8335; # support 18th wall 1st z 3 y 2nd
node 12001 74.325 -3.5 -3.3; # support 18th wall 1st z 3 y 3rd
node 12100 75.1 -1.75 -5.5665; # support 18th wall 2nd z 1 y 2nd
node 12200 75.1 -1.75 -4.2; # support 18th wall 2nd z 2 y 2nd
node 12300 75.1 -1.75 -2.8335; # support 18th wall 2nd z 3 y 2nd
node 12400 73.55 -1.75 2.8335; # support 19th wall 1st z 1 y 2nd
node 12401 74.325 -3.5 3.3; # support 19th wall 1st z 1 y 3rd
node 12500 73.55 -1.75 4.2; # support 19th wall 1st z 2 y 2nd
node 12501 74.325 -3.5 4.2; # support 19th wall 1st z 2 y 3rd
node 12600 73.55 -1.75 5.5665; # support 19th wall 1st z 3 y 2nd
node 12601 74.325 -3.5 5.1; # support 19th wall 1st z 3 y 3rd
node 12700 75.1 -1.75 2.8335; # support 19th wall 2nd z 1 y 2nd
node 12800 75.1 -1.75 4.2; # support 19th wall 2nd z 2 y 2nd
node 12900 75.1 -1.75 5.5665; # support 19th wall 2nd z 3 y 2nd
node 13000 73.55 -1.75 11.2335; # support 20th wall 1st z 1 y 2nd
node 13001 74.325 -3.5 11.7; # support 20th wall 1st z 1 y 3rd
node 13100 73.55 -1.75 12.6; # support 20th wall 1st z 2 y 2nd
node 13101 74.325 -3.5 12.6; # support 20th wall 1st z 2 y 3rd
node 13200 73.55 -1.75 13.9665; # support 20th wall 1st z 3 y 2nd
node 13201 74.325 -3.5 13.5; # support 20th wall 1st z 3 y 3rd
node 13300 75.1 -1.75 11.2335; # support 20th wall 2nd z 1 y 2nd
node 13400 75.1 -1.75 12.6; # support 20th wall 2nd z 2 y 2nd
node 13500 75.1 -1.75 13.9665; # support 20th wall 2nd z 3 y 2nd
node 13600 88.85 -1.75 -13.9665; # support 21st wall 1st z 1 y 2nd
node 13601 89.625 -3.5 -13.5; # support 21st wall 1st z 1 y 3rd
node 13700 88.85 -1.75 -12.6; # support 21st wall 1st z 2 y 2nd
node 13701 89.625 -3.5 -12.6; # support 21st wall 1st z 2 y 3rd
node 13800 88.85 -1.75 -11.2335; # support 21st wall 1st z 3 y 2nd
node 13801 89.625 -3.5 -11.7; # support 21st wall 1st z 3 y 3rd
node 13900 90.4 -1.75 -13.9665; # support 21st wall 2nd z 1 y 2nd
node 14000 90.4 -1.75 -12.6; # support 21st wall 2nd z 2 y 2nd
node 14100 90.4 -1.75 -11.2335; # support 21st wall 2nd z 3 y 2nd
node 14200 88.85 -1.75 -5.5665; # support 22nd wall 1st z 1 y 2nd
node 14201 89.625 -3.5 -5.1; # support 22nd wall 1st z 1 y 3rd
node 14300 88.85 -1.75 -4.2; # support 22nd wall 1st z 2 y 2nd
node 14301 89.625 -3.5 -4.2; # support 22nd wall 1st z 2 y 3rd
node 14400 88.85 -1.75 -2.8335; # support 22nd wall 1st z 3 y 2nd
node 14401 89.625 -3.5 -3.3; # support 22nd wall 1st z 3 y 3rd
node 14500 90.4 -1.75 -5.5665; # support 22nd wall 2nd z 1 y 2nd
node 14600 90.4 -1.75 -4.2; # support 22nd wall 2nd z 2 y 2nd
node 14700 90.4 -1.75 -2.8335; # support 22nd wall 2nd z 3 y 2nd
node 14800 88.85 -1.75 2.8335; # support 23rd wall 1st z 1 y 2nd
node 14801 89.625 -3.5 3.3; # support 23rd wall 1st z 1 y 3rd
node 14900 88.85 -1.75 4.2; # support 23rd wall 1st z 2 y 2nd
node 14901 89.625 -3.5 4.2; # support 23rd wall 1st z 2 y 3rd
node 15000 88.85 -1.75 5.5665; # support 23rd wall 1st z 3 y 2nd
node 15001 89.625 -3.5 5.1; # support 23rd wall 1st z 3 y 3rd
node 15100 90.4 -1.75 2.8335; # support 23rd wall 2nd z 1 y 2nd
node 15200 90.4 -1.75 4.2; # support 23rd wall 2nd z 2 y 2nd
node 15300 90.4 -1.75 5.5665; # support 23rd wall 2nd z 3 y 2nd
node 15400 88.85 -1.75 11.2335; # support 24th wall 1st z 1 y 2nd
node 15401 89.625 -3.5 11.7; # support 24th wall 1st z 1 y 3rd
node 15500 88.85 -1.75 12.6; # support 24th wall 1st z 2 y 2nd
node 15501 89.625 -3.5 12.6; # support 24th wall 1st z 2 y 3rd
node 15600 88.85 -1.75 13.9665; # support 24th wall 1st z 3 y 2nd
node 15601 89.625 -3.5 13.5; # support 24th wall 1st z 3 y 3rd
node 15700 90.4 -1.75 11.2335; # support 24th wall 2nd z 1 y 2nd
node 15800 90.4 -1.75 12.6; # support 24th wall 2nd z 2 y 2nd
node 15900 90.4 -1.75 13.9665; # support 24th wall 2nd z 3 y 2nd
# End support nodes

# fix nodeTag x y z rx ry rz
# Begin fixed deck nodes
fix 100 1 1 1 0 0 0
fix 114 1 1 1 0 0 0
fix 200 1 1 1 0 0 0
fix 214 1 1 1 0 0 0
fix 300 1 1 1 0 0 0
fix 314 1 1 1 0 0 0
fix 400 1 1 1 0 0 0
fix 414 1 1 1 0 0 0
fix 500 1 1 1 0 0 0
fix 514 1 1 1 0 0 0
fix 600 1 1 1 0 0 0
fix 614 1 1 1 0 0 0
fix 700 1 1 1 0 0 0
fix 714 1 1 1 0 0 0
fix 800 1 1 1 0 0 0
fix 814 1 1 1 0 0 0
fix 900 1 1 1 0 0 0
fix 914 1 1 1 0 0 0
fix 1000 1 1 1 0 0 0
fix 1014 1 1 1 0 0 0
fix 1100 1 1 1 0 0 0
fix 1114 1 1 1 0 0 0
fix 1200 1 1 1 0 0 0
fix 1214 1 1 1 0 0 0
fix 1300 1 1 1 0 0 0
fix 1314 1 1 1 0 0 0
fix 1400 1 1 1 0 0 0
fix 1414 1 1 1 0 0 0
fix 1500 1 1 1 0 0 0
fix 1514 1 1 1 0 0 0
# End fixed deck nodes

# fix nodeTag x y z rx ry rz
# Begin fixed support nodes
fix 1601 0 0 1 1 1 0; # support 1 y 1
fix 1701 0 0 1 1 1 0; # support 1 y 2
fix 1801 0 0 1 1 1 0; # support 1 y 3
fix 2201 0 1 1 1 1 0; # support 2 y 1
fix 2301 0 1 1 1 1 0; # support 2 y 2
fix 2401 0 1 1 1 1 0; # support 2 y 3
fix 2801 0 1 1 1 1 0; # support 3 y 1
fix 2901 0 1 1 1 1 0; # support 3 y 2
fix 3001 0 1 1 1 1 0; # support 3 y 3
fix 3401 0 1 1 1 1 0; # support 4 y 1
fix 3501 0 1 1 1 1 0; # support 4 y 2
fix 3601 0 1 1 1 1 0; # support 4 y 3
fix 4001 0 1 1 1 1 0; # support 5 y 1
fix 4101 0 1 1 1 1 0; # support 5 y 2
fix 4201 0 1 1 1 1 0; # support 5 y 3
fix 4601 0 1 1 1 1 0; # support 6 y 1
fix 4701 0 1 1 1 1 0; # support 6 y 2
fix 4801 0 1 1 1 1 0; # support 6 y 3
fix 5201 0 1 1 1 1 0; # support 7 y 1
fix 5301 0 1 1 1 1 0; # support 7 y 2
fix 5401 0 1 1 1 1 0; # support 7 y 3
fix 5801 0 1 1 1 1 0; # support 8 y 1
fix 5901 0 1 1 1 1 0; # support 8 y 2
fix 6001 0 1 1 1 1 0; # support 8 y 3
fix 6401 1 1 1 1 1 0; # support 9 y 1
fix 6501 1 1 1 1 1 0; # support 9 y 2
fix 6601 1 1 1 1 1 0; # support 9 y 3
fix 7001 1 1 1 1 1 0; # support 10 y 1
fix 7101 1 1 1 1 1 0; # support 10 y 2
fix 7201 1 1 1 1 1 0; # support 10 y 3
fix 7601 1 1 1 1 1 0; # support 11 y 1
fix 7701 1 1 1 1 1 0; # support 11 y 2
fix 7801 1 1 1 1 1 0; # support 11 y 3
fix 8201 1 1 1 1 1 0; # support 12 y 1
fix 8301 1 1 1 1 1 0; # support 12 y 2
fix 8401 1 1 1 1 1 0; # support 12 y 3
fix 8801 1 1 1 1 1 0; # support 13 y 1
fix 8901 1 1 1 1 1 0; # support 13 y 2
fix 9001 1 1 1 1 1 0; # support 13 y 3
fix 9401 1 1 1 1 1 0; # support 14 y 1
fix 9501 1 1 1 1 1 0; # support 14 y 2
fix 9601 1 1 1 1 1 0; # support 14 y 3
fix 10001 1 1 1 1 1 0; # support 15 y 1
fix 10101 1 1 1 1 1 0; # support 15 y 2
fix 10201 1 1 1 1 1 0; # support 15 y 3
fix 10601 1 1 1 1 1 0; # support 16 y 1
fix 10701 1 1 1 1 1 0; # support 16 y 2
fix 10801 1 1 1 1 1 0; # support 16 y 3
fix 11201 0 1 1 1 1 0; # support 17 y 1
fix 11301 0 1 1 1 1 0; # support 17 y 2
fix 11401 0 1 1 1 1 0; # support 17 y 3
fix 11801 0 1 1 1 1 0; # support 18 y 1
fix 11901 0 1 1 1 1 0; # support 18 y 2
fix 12001 0 1 1 1 1 0; # support 18 y 3
fix 12401 0 1 1 1 1 0; # support 19 y 1
fix 12501 0 1 1 1 1 0; # support 19 y 2
fix 12601 0 1 1 1 1 0; # support 19 y 3
fix 13001 0 1 1 1 1 0; # support 20 y 1
fix 13101 0 1 1 1 1 0; # support 20 y 2
fix 13201 0 1 1 1 1 0; # support 20 y 3
fix 13601 0 1 1 1 1 0; # support 21 y 1
fix 13701 0 1 1 1 1 0; # support 21 y 2
fix 13801 0 1 1 1 1 0; # support 21 y 3
fix 14201 0 1 1 1 1 0; # support 22 y 1
fix 14301 0 1 1 1 1 0; # support 22 y 2
fix 14401 0 1 1 1 1 0; # support 22 y 3
fix 14801 0 1 1 1 1 0; # support 23 y 1
fix 14901 0 1 1 1 1 0; # support 23 y 2
fix 15001 0 1 1 1 1 0; # support 23 y 3
fix 15401 0 1 1 1 1 0; # support 24 y 1
fix 15501 0 1 1 1 1 0; # support 24 y 2
fix 15601 0 1 1 1 1 0; # support 24 y 3
# End fixed support nodes

# section ElasticMembranePlateSection secTag youngs_modulus poisson_ratio depth mass_density
# Begin deck sections
section ElasticMembranePlateSection 1 38400000000.0 0.2 0.75 0.0027240000000000003
section ElasticMembranePlateSection 2 38400000000.0 0.2 0.74 0.0027240000000000003
section ElasticMembranePlateSection 3 38400000000.0 0.2 0.655 0.002637
section ElasticMembranePlateSection 4 38400000000.0 0.2 0.589 0.0026639999999999997
section ElasticMembranePlateSection 5 38400000000.0 0.2 0.5 0.003143
section ElasticMembranePlateSection 6 38400000000.0 0.2 0.5 0.003124
section ElasticMembranePlateSection 7 41291000000.0 0.2 0.5 0.002845
section ElasticMembranePlateSection 8 41291000000.0 0.2 0.65 0.002765
section ElasticMembranePlateSection 9 38400000000.0 0.2 0.65 0.00298
section ElasticMembranePlateSection 10 38400000000.0 0.2 0.65 0.0029950000000000003
section ElasticMembranePlateSection 11 38400000000.0 0.2 0.739 0.0026309999999999997
section ElasticMembranePlateSection 12 38400000000.0 0.2 0.787 0.002617
section ElasticMembranePlateSection 13 47277000000.0 0.2 0.65 0.0029070000000000003
section ElasticMembranePlateSection 14 38400000000.0 0.2 0.787 0.002617
section ElasticMembranePlateSection 15 38400000000.0 0.2 0.739 0.0026309999999999997
section ElasticMembranePlateSection 16 38400000000.0 0.2 0.65 0.0029950000000000003
section ElasticMembranePlateSection 17 38400000000.0 0.2 0.65 0.00298
section ElasticMembranePlateSection 18 41291000000.0 0.2 0.65 0.002765
section ElasticMembranePlateSection 19 41291000000.0 0.2 0.5 0.002845
section ElasticMembranePlateSection 20 38400000000.0 0.2 0.5 0.003124
section ElasticMembranePlateSection 21 38400000000.0 0.2 0.5 0.003143
section ElasticMembranePlateSection 22 38400000000.0 0.2 0.589 0.0026639999999999997
section ElasticMembranePlateSection 23 38400000000.0 0.2 0.655 0.002637
section ElasticMembranePlateSection 24 38400000000.0 0.2 0.74 0.0027240000000000003
section ElasticMembranePlateSection 25 38400000000.0 0.2 0.75 0.0027240000000000003
# End deck sections

# section ElasticMembranePlateSection secTag youngs_modulus poisson_ratio depth mass_density
# Begin pier sections
section ElasticMembranePlateSection 26 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 27 38400000000.0 0.2 1.2184210526315788 0.0027240000000000003
section ElasticMembranePlateSection 28 38400000000.0 0.2 1.170842105263158 0.0027240000000000003
section ElasticMembranePlateSection 29 38400000000.0 0.2 1.123263157894737 0.0027240000000000003
section ElasticMembranePlateSection 30 38400000000.0 0.2 1.0756842105263158 0.0027240000000000003
section ElasticMembranePlateSection 31 38400000000.0 0.2 1.0281052631578946 0.0027240000000000003
section ElasticMembranePlateSection 32 38400000000.0 0.2 0.9805263157894737 0.0027240000000000003
section ElasticMembranePlateSection 34 38400000000.0 0.2 0.8853684210526316 0.0027240000000000003
section ElasticMembranePlateSection 35 38400000000.0 0.2 0.8377894736842105 0.0027240000000000003
section ElasticMembranePlateSection 36 38400000000.0 0.2 0.7902105263157895 0.0027240000000000003
section ElasticMembranePlateSection 37 38400000000.0 0.2 0.7426315789473684 0.0027240000000000003
section ElasticMembranePlateSection 38 38400000000.0 0.2 0.6950526315789474 0.0027240000000000003
section ElasticMembranePlateSection 39 38400000000.0 0.2 0.6474736842105264 0.0027240000000000003
section ElasticMembranePlateSection 33 38400000000.0 0.2 0.9329473684210526 0.0027240000000000003
section ElasticMembranePlateSection 40 38400000000.0 0.2 0.5998947368421053 0.0027240000000000003
section ElasticMembranePlateSection 41 38400000000.0 0.2 0.5523157894736842 0.0027240000000000003
section ElasticMembranePlateSection 42 38400000000.0 0.2 0.5047368421052632 0.0027240000000000003
section ElasticMembranePlateSection 43 38400000000.0 0.2 0.4571578947368422 0.0027240000000000003
section ElasticMembranePlateSection 44 38400000000.0 0.2 0.40957894736842104 0.0027240000000000003
section ElasticMembranePlateSection 45 38400000000.0 0.2 0.362 0.0027240000000000003
# End pier sections

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin deck shell elements
element ShellMITC4 1 100 101 201 200 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2 101 102 202 201 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3 102 103 203 202 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 4 103 104 204 203 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 5 104 105 205 204 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 6 105 106 206 205 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 7 106 107 207 206 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 8 107 108 208 207 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 9 108 109 209 208 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 10 109 110 210 209 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 11 110 111 211 210 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 12 111 112 212 211 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 13 112 113 213 212 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 14 113 114 214 213 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 100 200 201 301 300 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 101 201 202 302 301 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 102 202 203 303 302 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 103 203 204 304 303 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 104 204 205 305 304 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 105 205 206 306 305 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 106 206 207 307 306 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 107 207 208 308 307 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 108 208 209 309 308 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 109 209 210 310 309 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 110 210 211 311 310 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 111 211 212 312 311 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 112 212 213 313 312 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 113 213 214 314 313 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 200 300 301 401 400 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 201 301 302 402 401 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 202 302 303 403 402 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 203 303 304 404 403 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 204 304 305 405 404 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 205 305 306 406 405 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 206 306 307 407 406 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 207 307 308 408 407 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 208 308 309 409 408 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 209 309 310 410 409 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 210 310 311 411 410 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 211 311 312 412 411 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 212 312 313 413 412 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 213 313 314 414 413 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 300 400 401 501 500 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 301 401 402 502 501 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 302 402 403 503 502 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 303 403 404 504 503 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 304 404 405 505 504 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 305 405 406 506 505 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 306 406 407 507 506 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 307 407 408 508 507 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 308 408 409 509 508 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 309 409 410 510 509 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 310 410 411 511 510 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 311 411 412 512 511 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 312 412 413 513 512 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 313 413 414 514 513 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 400 500 501 601 600 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 401 501 502 602 601 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 402 502 503 603 602 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 403 503 504 604 603 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 404 504 505 605 604 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 405 505 506 606 605 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 406 506 507 607 606 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 407 507 508 608 607 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 408 508 509 609 608 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 409 509 510 610 609 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 410 510 511 611 610 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 411 511 512 612 611 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 412 512 513 613 612 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 413 513 514 614 613 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 500 600 601 701 700 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 501 601 602 702 701 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 502 602 603 703 702 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 503 603 604 704 703 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 504 604 605 705 704 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 505 605 606 706 705 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 506 606 607 707 706 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 507 607 608 708 707 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 508 608 609 709 708 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 509 609 610 710 709 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 510 610 611 711 710 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 511 611 612 712 711 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 512 612 613 713 712 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 513 613 614 714 713 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 600 700 701 801 800 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 601 701 702 802 801 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 602 702 703 803 802 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 603 703 704 804 803 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 604 704 705 805 804 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 605 705 706 806 805 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 606 706 707 807 806 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 607 707 708 808 807 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 608 708 709 809 808 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 609 709 710 810 809 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 610 710 711 811 810 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 611 711 712 812 811 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 612 712 713 813 812 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 613 713 714 814 813 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 700 800 801 901 900 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 701 801 802 902 901 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 702 802 803 903 902 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 703 803 804 904 903 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 704 804 805 905 904 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 705 805 806 906 905 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 706 806 807 907 906 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 707 807 808 908 907 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 708 808 809 909 908 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 709 809 810 910 909 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 710 810 811 911 910 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 711 811 812 912 911 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 712 812 813 913 912 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 713 813 814 914 913 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 800 900 901 1001 1000 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 801 901 902 1002 1001 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 802 902 903 1003 1002 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 803 903 904 1004 1003 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 804 904 905 1005 1004 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 805 905 906 1006 1005 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 806 906 907 1007 1006 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 807 907 908 1008 1007 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 808 908 909 1009 1008 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 809 909 910 1010 1009 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 810 910 911 1011 1010 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 811 911 912 1012 1011 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 812 912 913 1013 1012 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 813 913 914 1014 1013 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 900 1000 1001 1101 1100 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 901 1001 1002 1102 1101 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 902 1002 1003 1103 1102 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 903 1003 1004 1104 1103 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 904 1004 1005 1105 1104 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 905 1005 1006 1106 1105 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 906 1006 1007 1107 1106 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 907 1007 1008 1108 1107 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 908 1008 1009 1109 1108 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 909 1009 1010 1110 1109 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 910 1010 1011 1111 1110 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 911 1011 1012 1112 1111 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 912 1012 1013 1113 1112 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 913 1013 1014 1114 1113 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1000 1100 1101 1201 1200 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1001 1101 1102 1202 1201 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1002 1102 1103 1203 1202 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1003 1103 1104 1204 1203 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1004 1104 1105 1205 1204 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1005 1105 1106 1206 1205 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1006 1106 1107 1207 1206 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1007 1107 1108 1208 1207 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1008 1108 1109 1209 1208 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1009 1109 1110 1210 1209 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1010 1110 1111 1211 1210 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1011 1111 1112 1212 1211 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1012 1112 1113 1213 1212 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1013 1113 1114 1214 1213 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1100 1200 1201 1301 1300 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1101 1201 1202 1302 1301 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1102 1202 1203 1303 1302 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1103 1203 1204 1304 1303 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1104 1204 1205 1305 1304 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1105 1205 1206 1306 1305 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1106 1206 1207 1307 1306 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1107 1207 1208 1308 1307 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1108 1208 1209 1309 1308 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1109 1209 1210 1310 1309 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1110 1210 1211 1311 1310 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1111 1211 1212 1312 1311 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1112 1212 1213 1313 1312 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1113 1213 1214 1314 1313 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1200 1300 1301 1401 1400 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1201 1301 1302 1402 1401 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1202 1302 1303 1403 1402 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1203 1303 1304 1404 1403 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1204 1304 1305 1405 1404 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1205 1305 1306 1406 1405 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1206 1306 1307 1407 1406 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1207 1307 1308 1408 1407 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1208 1308 1309 1409 1408 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1209 1309 1310 1410 1409 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1210 1310 1311 1411 1410 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1211 1311 1312 1412 1411 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1212 1312 1313 1413 1412 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1213 1313 1314 1414 1413 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1300 1400 1401 1501 1500 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1301 1401 1402 1502 1501 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1302 1402 1403 1503 1502 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1303 1403 1404 1504 1503 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1304 1404 1405 1505 1504 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1305 1405 1406 1506 1505 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1306 1406 1407 1507 1506 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1307 1407 1408 1508 1507 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1308 1408 1409 1509 1508 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1309 1409 1410 1510 1509 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1310 1410 1411 1511 1510 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1311 1411 1412 1512 1511 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1312 1412 1413 1513 1512 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1313 1413 1414 1514 1513 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
# End deck shell elements

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin pier shell elements
element ShellMITC4 1400 201 1600 1700 301 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1401 1600 1601 1701 1700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1500 301 1700 1800 401 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1501 1700 1701 1801 1800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1600 202 1900 2000 302 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1601 1900 1601 1701 2000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1700 302 2000 2100 402 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1701 2000 1701 1801 2100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1800 501 2200 2300 601 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1801 2200 2201 2301 2300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1900 601 2300 2400 701 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1901 2300 2301 2401 2400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2000 502 2500 2600 602 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2001 2500 2201 2301 2600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2100 602 2600 2700 702 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2101 2600 2301 2401 2700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2200 901 2800 2900 1001 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2201 2800 2801 2901 2900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2300 1001 2900 3000 1101 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2301 2900 2901 3001 3000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2400 902 3100 3200 1002 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2401 3100 2801 2901 3200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2500 1002 3200 3300 1102 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2501 3200 2901 3001 3300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2600 1201 3400 3500 1301 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2601 3400 3401 3501 3500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2700 1301 3500 3600 1401 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2701 3500 3501 3601 3600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2800 1202 3700 3800 1302 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2801 3700 3401 3501 3800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2900 1302 3800 3900 1402 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2901 3800 3501 3601 3900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3000 203 4000 4100 303 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3001 4000 4001 4101 4100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3100 303 4100 4200 403 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3101 4100 4101 4201 4200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3200 204 4300 4400 304 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3201 4300 4001 4101 4400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3300 304 4400 4500 404 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3301 4400 4101 4201 4500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3400 503 4600 4700 603 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3401 4600 4601 4701 4700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3500 603 4700 4800 703 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3501 4700 4701 4801 4800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3600 504 4900 5000 604 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3601 4900 4601 4701 5000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3700 604 5000 5100 704 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3701 5000 4701 4801 5100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3800 903 5200 5300 1003 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3801 5200 5201 5301 5300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3900 1003 5300 5400 1103 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3901 5300 5301 5401 5400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4000 904 5500 5600 1004 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4001 5500 5201 5301 5600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4100 1004 5600 5700 1104 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4101 5600 5301 5401 5700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4200 1203 5800 5900 1303 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4201 5800 5801 5901 5900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4300 1303 5900 6000 1403 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4301 5900 5901 6001 6000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4400 1204 6100 6200 1304 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4401 6100 5801 5901 6200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4500 1304 6200 6300 1404 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4501 6200 5901 6001 6300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4600 205 6400 6500 305 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4601 6400 6401 6501 6500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4700 305 6500 6600 405 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4701 6500 6501 6601 6600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4800 206 6700 6800 306 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4801 6700 6401 6501 6800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4900 306 6800 6900 406 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4901 6800 6501 6601 6900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5000 505 7000 7100 605 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5001 7000 7001 7101 7100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5100 605 7100 7200 705 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5101 7100 7101 7201 7200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5200 506 7300 7400 606 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5201 7300 7001 7101 7400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5300 606 7400 7500 706 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5301 7400 7101 7201 7500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5400 905 7600 7700 1005 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5401 7600 7601 7701 7700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5500 1005 7700 7800 1105 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5501 7700 7701 7801 7800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5600 906 7900 8000 1006 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5601 7900 7601 7701 8000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5700 1006 8000 8100 1106 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5701 8000 7701 7801 8100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5800 1205 8200 8300 1305 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5801 8200 8201 8301 8300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5900 1305 8300 8400 1405 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5901 8300 8301 8401 8400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6000 1206 8500 8600 1306 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6001 8500 8201 8301 8600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6100 1306 8600 8700 1406 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6101 8600 8301 8401 8700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6200 208 8800 8900 308 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6201 8800 8801 8901 8900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6300 308 8900 9000 408 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6301 8900 8901 9001 9000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6400 209 9100 9200 309 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6401 9100 8801 8901 9200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6500 309 9200 9300 409 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6501 9200 8901 9001 9300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6600 508 9400 9500 608 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6601 9400 9401 9501 9500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6700 608 9500 9600 708 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6701 9500 9501 9601 9600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6800 509 9700 9800 609 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6801 9700 9401 9501 9800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6900 609 9800 9900 709 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6901 9800 9501 9601 9900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7000 908 10000 10100 1008 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7001 10000 10001 10101 10100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7100 1008 10100 10200 1108 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7101 10100 10101 10201 10200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7200 909 10300 10400 1009 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7201 10300 10001 10101 10400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7300 1009 10400 10500 1109 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7301 10400 10101 10201 10500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7400 1208 10600 10700 1308 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7401 10600 10601 10701 10700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7500 1308 10700 10800 1408 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7501 10700 10701 10801 10800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7600 1209 10900 11000 1309 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7601 10900 10601 10701 11000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7700 1309 11000 11100 1409 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7701 11000 10701 10801 11100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7800 210 11200 11300 310 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7801 11200 11201 11301 11300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7900 310 11300 11400 410 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7901 11300 11301 11401 11400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8000 211 11500 11600 311 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8001 11500 11201 11301 11600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8100 311 11600 11700 411 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8101 11600 11301 11401 11700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8200 510 11800 11900 610 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8201 11800 11801 11901 11900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8300 610 11900 12000 710 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8301 11900 11901 12001 12000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8400 511 12100 12200 611 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8401 12100 11801 11901 12200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8500 611 12200 12300 711 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8501 12200 11901 12001 12300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8600 910 12400 12500 1010 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8601 12400 12401 12501 12500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8700 1010 12500 12600 1110 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8701 12500 12501 12601 12600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8800 911 12700 12800 1011 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8801 12700 12401 12501 12800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8900 1011 12800 12900 1111 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8901 12800 12501 12601 12900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9000 1210 13000 13100 1310 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9001 13000 13001 13101 13100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9100 1310 13100 13200 1410 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9101 13100 13101 13201 13200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9200 1211 13300 13400 1311 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9201 13300 13001 13101 13400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9300 1311 13400 13500 1411 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9301 13400 13101 13201 13500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9400 212 13600 13700 312 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9401 13600 13601 13701 13700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9500 312 13700 13800 412 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9501 13700 13701 13801 13800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9600 213 13900 14000 313 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9601 13900 13601 13701 14000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9700 313 14000 14100 413 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9701 14000 13701 13801 14100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9800 512 14200 14300 612 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9801 14200 14201 14301 14300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9900 612 14300 14400 712 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9901 14300 14301 14401 14400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10000 513 14500 14600 613 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10001 14500 14201 14301 14600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10100 613 14600 14700 713 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10101 14600 14301 14401 14700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10200 912 14800 14900 1012 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10201 14800 14801 14901 14900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10300 1012 14900 15000 1112 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10301 14900 14901 15001 15000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10400 913 15100 15200 1013 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10401 15100 14801 14901 15200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10500 1013 15200 15300 1113 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10501 15200 14901 15001 15300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10600 1212 15400 15500 1312 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10601 15400 15401 15501 15500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10700 1312 15500 15600 1412 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10701 15500 15501 15601 15600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10800 1213 15700 15800 1313 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10801 15700 15401 15501 15800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10900 1313 15800 15900 1413 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10901 15800 15501 15601 15900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
# End pier shell elements



timeSeries Linear 1

pattern Plain 1 1 {
# load nodeTag N_x N_y N_z N_rx N_ry N_rz
# Begin loads
load 1701 0 10000 0 0 0 0
# End loads
}

recorder Element -file generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-1,000-0--forces.out -ele 1 400 forces

# recorder Node -file path -node nodeTags -dof direction disp
# Begin translation recorders
recorder Node -file generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-1,000-0-node-y.out -node 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1500 1501 1502 1503 1504 1505 1506 1507 1508 1509 1510 1511 1512 1513 1514 201 1600 1601 301 1700 1701 401 1800 1801 202 1900 1601 302 2000 1701 402 2100 1801 501 2200 2201 601 2300 2301 701 2400 2401 502 2500 2201 602 2600 2301 702 2700 2401 901 2800 2801 1001 2900 2901 1101 3000 3001 902 3100 2801 1002 3200 2901 1102 3300 3001 1201 3400 3401 1301 3500 3501 1401 3600 3601 1202 3700 3401 1302 3800 3501 1402 3900 3601 203 4000 4001 303 4100 4101 403 4200 4201 204 4300 4001 304 4400 4101 404 4500 4201 503 4600 4601 603 4700 4701 703 4800 4801 504 4900 4601 604 5000 4701 704 5100 4801 903 5200 5201 1003 5300 5301 1103 5400 5401 904 5500 5201 1004 5600 5301 1104 5700 5401 1203 5800 5801 1303 5900 5901 1403 6000 6001 1204 6100 5801 1304 6200 5901 1404 6300 6001 205 6400 6401 305 6500 6501 405 6600 6601 206 6700 6401 306 6800 6501 406 6900 6601 505 7000 7001 605 7100 7101 705 7200 7201 506 7300 7001 606 7400 7101 706 7500 7201 905 7600 7601 1005 7700 7701 1105 7800 7801 906 7900 7601 1006 8000 7701 1106 8100 7801 1205 8200 8201 1305 8300 8301 1405 8400 8401 1206 8500 8201 1306 8600 8301 1406 8700 8401 208 8800 8801 308 8900 8901 408 9000 9001 209 9100 8801 309 9200 8901 409 9300 9001 508 9400 9401 608 9500 9501 708 9600 9601 509 9700 9401 609 9800 9501 709 9900 9601 908 10000 10001 1008 10100 10101 1108 10200 10201 909 10300 10001 1009 10400 10101 1109 10500 10201 1208 10600 10601 1308 10700 10701 1408 10800 10801 1209 10900 10601 1309 11000 10701 1409 11100 10801 210 11200 11201 310 11300 11301 410 11400 11401 211 11500 11201 311 11600 11301 411 11700 11401 510 11800 11801 610 11900 11901 710 12000 12001 511 12100 11801 611 12200 11901 711 12300 12001 910 12400 12401 1010 12500 12501 1110 12600 12601 911 12700 12401 1011 12800 12501 1111 12900 12601 1210 13000 13001 1310 13100 13101 1410 13200 13201 1211 13300 13001 1311 13400 13101 1411 13500 13201 212 13600 13601 312 13700 13701 412 13800 13801 213 13900 13601 313 14000 13701 413 14100 13801 512 14200 14201 612 14300 14301 712 14400 14401 513 14500 14201 613 14600 14301 713 14700 14401 912 14800 14801 1012 14900 14901 1112 15000 15001 913 15100 14801 1013 15200 14901 1113 15300 15001 1212 15400 15401 1312 15500 15501 1412 15600 15601 1213 15700 15401 1313 15800 15501 1413 15900 15601 -dof 2 disp
# End translation recorders



system BandGeneral
numberer RCM
constraints Plain
integrator DisplacementControl 1701 2 1.0
algorithm Newton
test NormDispIncr 1.0e-12 1000
analysis Static

analyze 1

# Array of each element's ID.
set l [list ]
# Write internal forces to file.
set outfile [open "generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-1,000-0--stress.out" w]

foreach i $l {
	# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64527&p=110182&hilit=shellMITC4#p110182
	# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]
	set internal_force [eleResponse $i stresses]
	puts $outfile $internal_force
}
close $outfile
