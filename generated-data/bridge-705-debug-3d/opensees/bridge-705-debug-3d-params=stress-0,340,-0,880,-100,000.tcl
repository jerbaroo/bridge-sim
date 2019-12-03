
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
node 105 34.95459 0 -16.6
node 106 42.175 0 -16.6
node 107 45.275 0 -16.6
node 108 51.375 0 -16.6
node 109 57.475 0 -16.6
node 110 60.575 0 -16.6
node 111 72.775 0 -16.6
node 112 75.875 0 -16.6
node 113 88.075 0 -16.6
node 114 91.175 0 -16.6
node 115 102.75 0 -16.6
node 200 0 0 -14.433
node 201 11.575 0 -14.433; # support node
node 202 14.675 0 -14.433; # support node
node 203 26.875 0 -14.433; # support node
node 204 29.975 0 -14.433; # support node
node 205 34.95459 0 -14.433
node 206 42.175 0 -14.433; # support node
node 207 45.275 0 -14.433; # support node
node 208 51.375 0 -14.433
node 209 57.475 0 -14.433; # support node
node 210 60.575 0 -14.433; # support node
node 211 72.775 0 -14.433; # support node
node 212 75.875 0 -14.433; # support node
node 213 88.075 0 -14.433; # support node
node 214 91.175 0 -14.433; # support node
node 215 102.75 0 -14.433
node 300 0 0 -12.6
node 301 11.575 0 -12.6; # support node
node 302 14.675 0 -12.6; # support node
node 303 26.875 0 -12.6; # support node
node 304 29.975 0 -12.6; # support node
node 305 34.95459 0 -12.6
node 306 42.175 0 -12.6; # support node
node 307 45.275 0 -12.6; # support node
node 308 51.375 0 -12.6
node 309 57.475 0 -12.6; # support node
node 310 60.575 0 -12.6; # support node
node 311 72.775 0 -12.6; # support node
node 312 75.875 0 -12.6; # support node
node 313 88.075 0 -12.6; # support node
node 314 91.175 0 -12.6; # support node
node 315 102.75 0 -12.6
node 400 0 0 -10.767
node 401 11.575 0 -10.767; # support node
node 402 14.675 0 -10.767; # support node
node 403 26.875 0 -10.767; # support node
node 404 29.975 0 -10.767; # support node
node 405 34.95459 0 -10.767
node 406 42.175 0 -10.767; # support node
node 407 45.275 0 -10.767; # support node
node 408 51.375 0 -10.767
node 409 57.475 0 -10.767; # support node
node 410 60.575 0 -10.767; # support node
node 411 72.775 0 -10.767; # support node
node 412 75.875 0 -10.767; # support node
node 413 88.075 0 -10.767; # support node
node 414 91.175 0 -10.767; # support node
node 415 102.75 0 -10.767
node 500 0 0 -6.033
node 501 11.575 0 -6.033; # support node
node 502 14.675 0 -6.033; # support node
node 503 26.875 0 -6.033; # support node
node 504 29.975 0 -6.033; # support node
node 505 34.95459 0 -6.033
node 506 42.175 0 -6.033; # support node
node 507 45.275 0 -6.033; # support node
node 508 51.375 0 -6.033
node 509 57.475 0 -6.033; # support node
node 510 60.575 0 -6.033; # support node
node 511 72.775 0 -6.033; # support node
node 512 75.875 0 -6.033; # support node
node 513 88.075 0 -6.033; # support node
node 514 91.175 0 -6.033; # support node
node 515 102.75 0 -6.033
node 600 0 0 -4.2
node 601 11.575 0 -4.2; # support node
node 602 14.675 0 -4.2; # support node
node 603 26.875 0 -4.2; # support node
node 604 29.975 0 -4.2; # support node
node 605 34.95459 0 -4.2
node 606 42.175 0 -4.2; # support node
node 607 45.275 0 -4.2; # support node
node 608 51.375 0 -4.2
node 609 57.475 0 -4.2; # support node
node 610 60.575 0 -4.2; # support node
node 611 72.775 0 -4.2; # support node
node 612 75.875 0 -4.2; # support node
node 613 88.075 0 -4.2; # support node
node 614 91.175 0 -4.2; # support node
node 615 102.75 0 -4.2
node 700 0 0 -2.367
node 701 11.575 0 -2.367; # support node
node 702 14.675 0 -2.367; # support node
node 703 26.875 0 -2.367; # support node
node 704 29.975 0 -2.367; # support node
node 705 34.95459 0 -2.367
node 706 42.175 0 -2.367; # support node
node 707 45.275 0 -2.367; # support node
node 708 51.375 0 -2.367
node 709 57.475 0 -2.367; # support node
node 710 60.575 0 -2.367; # support node
node 711 72.775 0 -2.367; # support node
node 712 75.875 0 -2.367; # support node
node 713 88.075 0 -2.367; # support node
node 714 91.175 0 -2.367; # support node
node 715 102.75 0 -2.367
node 800 0 0 0.0
node 801 11.575 0 0.0
node 802 14.675 0 0.0
node 803 26.875 0 0.0
node 804 29.975 0 0.0
node 805 34.95459 0 0.0
node 806 42.175 0 0.0
node 807 45.275 0 0.0
node 808 51.375 0 0.0
node 809 57.475 0 0.0
node 810 60.575 0 0.0
node 811 72.775 0 0.0
node 812 75.875 0 0.0
node 813 88.075 0 0.0
node 814 91.175 0 0.0
node 815 102.75 0 0.0
node 900 0 0 2.367
node 901 11.575 0 2.367; # support node
node 902 14.675 0 2.367; # support node
node 903 26.875 0 2.367; # support node
node 904 29.975 0 2.367; # support node
node 905 34.95459 0 2.367
node 906 42.175 0 2.367; # support node
node 907 45.275 0 2.367; # support node
node 908 51.375 0 2.367
node 909 57.475 0 2.367; # support node
node 910 60.575 0 2.367; # support node
node 911 72.775 0 2.367; # support node
node 912 75.875 0 2.367; # support node
node 913 88.075 0 2.367; # support node
node 914 91.175 0 2.367; # support node
node 915 102.75 0 2.367
node 1000 0 0 4.2
node 1001 11.575 0 4.2; # support node
node 1002 14.675 0 4.2; # support node
node 1003 26.875 0 4.2; # support node
node 1004 29.975 0 4.2; # support node
node 1005 34.95459 0 4.2
node 1006 42.175 0 4.2; # support node
node 1007 45.275 0 4.2; # support node
node 1008 51.375 0 4.2
node 1009 57.475 0 4.2; # support node
node 1010 60.575 0 4.2; # support node
node 1011 72.775 0 4.2; # support node
node 1012 75.875 0 4.2; # support node
node 1013 88.075 0 4.2; # support node
node 1014 91.175 0 4.2; # support node
node 1015 102.75 0 4.2
node 1100 0 0 6.033
node 1101 11.575 0 6.033; # support node
node 1102 14.675 0 6.033; # support node
node 1103 26.875 0 6.033; # support node
node 1104 29.975 0 6.033; # support node
node 1105 34.95459 0 6.033
node 1106 42.175 0 6.033; # support node
node 1107 45.275 0 6.033; # support node
node 1108 51.375 0 6.033
node 1109 57.475 0 6.033; # support node
node 1110 60.575 0 6.033; # support node
node 1111 72.775 0 6.033; # support node
node 1112 75.875 0 6.033; # support node
node 1113 88.075 0 6.033; # support node
node 1114 91.175 0 6.033; # support node
node 1115 102.75 0 6.033
node 1200 0 0 10.767
node 1201 11.575 0 10.767; # support node
node 1202 14.675 0 10.767; # support node
node 1203 26.875 0 10.767; # support node
node 1204 29.975 0 10.767; # support node
node 1205 34.95459 0 10.767
node 1206 42.175 0 10.767; # support node
node 1207 45.275 0 10.767; # support node
node 1208 51.375 0 10.767
node 1209 57.475 0 10.767; # support node
node 1210 60.575 0 10.767; # support node
node 1211 72.775 0 10.767; # support node
node 1212 75.875 0 10.767; # support node
node 1213 88.075 0 10.767; # support node
node 1214 91.175 0 10.767; # support node
node 1215 102.75 0 10.767
node 1300 0 0 12.6
node 1301 11.575 0 12.6; # support node
node 1302 14.675 0 12.6; # support node
node 1303 26.875 0 12.6; # support node
node 1304 29.975 0 12.6; # support node
node 1305 34.95459 0 12.6
node 1306 42.175 0 12.6; # support node
node 1307 45.275 0 12.6; # support node
node 1308 51.375 0 12.6
node 1309 57.475 0 12.6; # support node
node 1310 60.575 0 12.6; # support node
node 1311 72.775 0 12.6; # support node
node 1312 75.875 0 12.6; # support node
node 1313 88.075 0 12.6; # support node
node 1314 91.175 0 12.6; # support node
node 1315 102.75 0 12.6
node 1400 0 0 12.62606
node 1401 11.575 0 12.62606
node 1402 14.675 0 12.62606
node 1403 26.875 0 12.62606
node 1404 29.975 0 12.62606
node 1405 34.95459 0 12.62606
node 1406 42.175 0 12.62606
node 1407 45.275 0 12.62606
node 1408 51.375 0 12.62606
node 1409 57.475 0 12.62606
node 1410 60.575 0 12.62606
node 1411 72.775 0 12.62606
node 1412 75.875 0 12.62606
node 1413 88.075 0 12.62606
node 1414 91.175 0 12.62606
node 1415 102.75 0 12.62606
node 1500 0 0 14.433
node 1501 11.575 0 14.433; # support node
node 1502 14.675 0 14.433; # support node
node 1503 26.875 0 14.433; # support node
node 1504 29.975 0 14.433; # support node
node 1505 34.95459 0 14.433
node 1506 42.175 0 14.433; # support node
node 1507 45.275 0 14.433; # support node
node 1508 51.375 0 14.433
node 1509 57.475 0 14.433; # support node
node 1510 60.575 0 14.433; # support node
node 1511 72.775 0 14.433; # support node
node 1512 75.875 0 14.433; # support node
node 1513 88.075 0 14.433; # support node
node 1514 91.175 0 14.433; # support node
node 1515 102.75 0 14.433
node 1600 0 0 16.6
node 1601 11.575 0 16.6
node 1602 14.675 0 16.6
node 1603 26.875 0 16.6
node 1604 29.975 0 16.6
node 1605 34.95459 0 16.6
node 1606 42.175 0 16.6
node 1607 45.275 0 16.6
node 1608 51.375 0 16.6
node 1609 57.475 0 16.6
node 1610 60.575 0 16.6
node 1611 72.775 0 16.6
node 1612 75.875 0 16.6
node 1613 88.075 0 16.6
node 1614 91.175 0 16.6
node 1615 102.75 0 16.6
# End deck nodes

# node nodeTag x y z
# Begin support nodes
node 1700 12.35 -1.75 -13.9665; # support 1st wall 1st z 1 y 2nd
node 1701 13.125 -3.5 -13.5; # support 1st wall 1st z 1 y 3rd
node 1800 12.35 -1.75 -12.6; # support 1st wall 1st z 2 y 2nd
node 1801 13.125 -3.5 -12.6; # support 1st wall 1st z 2 y 3rd
node 1900 12.35 -1.75 -11.2335; # support 1st wall 1st z 3 y 2nd
node 1901 13.125 -3.5 -11.7; # support 1st wall 1st z 3 y 3rd
node 2000 13.9 -1.75 -13.9665; # support 1st wall 2nd z 1 y 2nd
node 2100 13.9 -1.75 -12.6; # support 1st wall 2nd z 2 y 2nd
node 2200 13.9 -1.75 -11.2335; # support 1st wall 2nd z 3 y 2nd
node 2300 12.35 -1.75 -5.5665; # support 2nd wall 1st z 1 y 2nd
node 2301 13.125 -3.5 -5.1; # support 2nd wall 1st z 1 y 3rd
node 2400 12.35 -1.75 -4.2; # support 2nd wall 1st z 2 y 2nd
node 2401 13.125 -3.5 -4.2; # support 2nd wall 1st z 2 y 3rd
node 2500 12.35 -1.75 -2.8335; # support 2nd wall 1st z 3 y 2nd
node 2501 13.125 -3.5 -3.3; # support 2nd wall 1st z 3 y 3rd
node 2600 13.9 -1.75 -5.5665; # support 2nd wall 2nd z 1 y 2nd
node 2700 13.9 -1.75 -4.2; # support 2nd wall 2nd z 2 y 2nd
node 2800 13.9 -1.75 -2.8335; # support 2nd wall 2nd z 3 y 2nd
node 2900 12.35 -1.75 2.8335; # support 3rd wall 1st z 1 y 2nd
node 2901 13.125 -3.5 3.3; # support 3rd wall 1st z 1 y 3rd
node 3000 12.35 -1.75 4.2; # support 3rd wall 1st z 2 y 2nd
node 3001 13.125 -3.5 4.2; # support 3rd wall 1st z 2 y 3rd
node 3100 12.35 -1.75 5.5665; # support 3rd wall 1st z 3 y 2nd
node 3101 13.125 -3.5 5.1; # support 3rd wall 1st z 3 y 3rd
node 3200 13.9 -1.75 2.8335; # support 3rd wall 2nd z 1 y 2nd
node 3300 13.9 -1.75 4.2; # support 3rd wall 2nd z 2 y 2nd
node 3400 13.9 -1.75 5.5665; # support 3rd wall 2nd z 3 y 2nd
node 3500 12.35 -1.75 11.2335; # support 4th wall 1st z 1 y 2nd
node 3501 13.125 -3.5 11.7; # support 4th wall 1st z 1 y 3rd
node 3600 12.35 -1.75 12.6; # support 4th wall 1st z 2 y 2nd
node 3601 13.125 -3.5 12.6; # support 4th wall 1st z 2 y 3rd
node 3700 12.35 -1.75 12.619428; # support 4th wall 1st z 3 y 2nd
node 3701 13.125 -3.5 12.612795; # support 4th wall 1st z 3 y 3rd
node 3800 12.35 -1.75 13.9665; # support 4th wall 1st z 4 y 2nd
node 3801 13.125 -3.5 13.5; # support 4th wall 1st z 4 y 3rd
node 3900 13.9 -1.75 11.2335; # support 4th wall 2nd z 1 y 2nd
node 4000 13.9 -1.75 12.6; # support 4th wall 2nd z 2 y 2nd
node 4100 13.9 -1.75 12.619428; # support 4th wall 2nd z 3 y 2nd
node 4200 13.9 -1.75 13.9665; # support 4th wall 2nd z 4 y 2nd
node 4300 27.65 -1.75 -13.9665; # support 5th wall 1st z 1 y 2nd
node 4301 28.425 -3.5 -13.5; # support 5th wall 1st z 1 y 3rd
node 4400 27.65 -1.75 -12.6; # support 5th wall 1st z 2 y 2nd
node 4401 28.425 -3.5 -12.6; # support 5th wall 1st z 2 y 3rd
node 4500 27.65 -1.75 -11.2335; # support 5th wall 1st z 3 y 2nd
node 4501 28.425 -3.5 -11.7; # support 5th wall 1st z 3 y 3rd
node 4600 29.2 -1.75 -13.9665; # support 5th wall 2nd z 1 y 2nd
node 4700 29.2 -1.75 -12.6; # support 5th wall 2nd z 2 y 2nd
node 4800 29.2 -1.75 -11.2335; # support 5th wall 2nd z 3 y 2nd
node 4900 27.65 -1.75 -5.5665; # support 6th wall 1st z 1 y 2nd
node 4901 28.425 -3.5 -5.1; # support 6th wall 1st z 1 y 3rd
node 5000 27.65 -1.75 -4.2; # support 6th wall 1st z 2 y 2nd
node 5001 28.425 -3.5 -4.2; # support 6th wall 1st z 2 y 3rd
node 5100 27.65 -1.75 -2.8335; # support 6th wall 1st z 3 y 2nd
node 5101 28.425 -3.5 -3.3; # support 6th wall 1st z 3 y 3rd
node 5200 29.2 -1.75 -5.5665; # support 6th wall 2nd z 1 y 2nd
node 5300 29.2 -1.75 -4.2; # support 6th wall 2nd z 2 y 2nd
node 5400 29.2 -1.75 -2.8335; # support 6th wall 2nd z 3 y 2nd
node 5500 27.65 -1.75 2.8335; # support 7th wall 1st z 1 y 2nd
node 5501 28.425 -3.5 3.3; # support 7th wall 1st z 1 y 3rd
node 5600 27.65 -1.75 4.2; # support 7th wall 1st z 2 y 2nd
node 5601 28.425 -3.5 4.2; # support 7th wall 1st z 2 y 3rd
node 5700 27.65 -1.75 5.5665; # support 7th wall 1st z 3 y 2nd
node 5701 28.425 -3.5 5.1; # support 7th wall 1st z 3 y 3rd
node 5800 29.2 -1.75 2.8335; # support 7th wall 2nd z 1 y 2nd
node 5900 29.2 -1.75 4.2; # support 7th wall 2nd z 2 y 2nd
node 6000 29.2 -1.75 5.5665; # support 7th wall 2nd z 3 y 2nd
node 6100 27.65 -1.75 11.2335; # support 8th wall 1st z 1 y 2nd
node 6101 28.425 -3.5 11.7; # support 8th wall 1st z 1 y 3rd
node 6200 27.65 -1.75 12.6; # support 8th wall 1st z 2 y 2nd
node 6201 28.425 -3.5 12.6; # support 8th wall 1st z 2 y 3rd
node 6300 27.65 -1.75 12.619428; # support 8th wall 1st z 3 y 2nd
node 6301 28.425 -3.5 12.612795; # support 8th wall 1st z 3 y 3rd
node 6400 27.65 -1.75 13.9665; # support 8th wall 1st z 4 y 2nd
node 6401 28.425 -3.5 13.5; # support 8th wall 1st z 4 y 3rd
node 6500 29.2 -1.75 11.2335; # support 8th wall 2nd z 1 y 2nd
node 6600 29.2 -1.75 12.6; # support 8th wall 2nd z 2 y 2nd
node 6700 29.2 -1.75 12.619428; # support 8th wall 2nd z 3 y 2nd
node 6800 29.2 -1.75 13.9665; # support 8th wall 2nd z 4 y 2nd
node 6900 42.95 -1.75 -13.9665; # support 9th wall 1st z 1 y 2nd
node 6901 43.725 -3.5 -13.5; # support 9th wall 1st z 1 y 3rd
node 7000 42.95 -1.75 -12.6; # support 9th wall 1st z 2 y 2nd
node 7001 43.725 -3.5 -12.6; # support 9th wall 1st z 2 y 3rd
node 7100 42.95 -1.75 -11.2335; # support 9th wall 1st z 3 y 2nd
node 7101 43.725 -3.5 -11.7; # support 9th wall 1st z 3 y 3rd
node 7200 44.5 -1.75 -13.9665; # support 9th wall 2nd z 1 y 2nd
node 7300 44.5 -1.75 -12.6; # support 9th wall 2nd z 2 y 2nd
node 7400 44.5 -1.75 -11.2335; # support 9th wall 2nd z 3 y 2nd
node 7500 42.95 -1.75 -5.5665; # support 10th wall 1st z 1 y 2nd
node 7501 43.725 -3.5 -5.1; # support 10th wall 1st z 1 y 3rd
node 7600 42.95 -1.75 -4.2; # support 10th wall 1st z 2 y 2nd
node 7601 43.725 -3.5 -4.2; # support 10th wall 1st z 2 y 3rd
node 7700 42.95 -1.75 -2.8335; # support 10th wall 1st z 3 y 2nd
node 7701 43.725 -3.5 -3.3; # support 10th wall 1st z 3 y 3rd
node 7800 44.5 -1.75 -5.5665; # support 10th wall 2nd z 1 y 2nd
node 7900 44.5 -1.75 -4.2; # support 10th wall 2nd z 2 y 2nd
node 8000 44.5 -1.75 -2.8335; # support 10th wall 2nd z 3 y 2nd
node 8100 42.95 -1.75 2.8335; # support 11th wall 1st z 1 y 2nd
node 8101 43.725 -3.5 3.3; # support 11th wall 1st z 1 y 3rd
node 8200 42.95 -1.75 4.2; # support 11th wall 1st z 2 y 2nd
node 8201 43.725 -3.5 4.2; # support 11th wall 1st z 2 y 3rd
node 8300 42.95 -1.75 5.5665; # support 11th wall 1st z 3 y 2nd
node 8301 43.725 -3.5 5.1; # support 11th wall 1st z 3 y 3rd
node 8400 44.5 -1.75 2.8335; # support 11th wall 2nd z 1 y 2nd
node 8500 44.5 -1.75 4.2; # support 11th wall 2nd z 2 y 2nd
node 8600 44.5 -1.75 5.5665; # support 11th wall 2nd z 3 y 2nd
node 8700 42.95 -1.75 11.2335; # support 12th wall 1st z 1 y 2nd
node 8701 43.725 -3.5 11.7; # support 12th wall 1st z 1 y 3rd
node 8800 42.95 -1.75 12.6; # support 12th wall 1st z 2 y 2nd
node 8801 43.725 -3.5 12.6; # support 12th wall 1st z 2 y 3rd
node 8900 42.95 -1.75 12.619428; # support 12th wall 1st z 3 y 2nd
node 8901 43.725 -3.5 12.612795; # support 12th wall 1st z 3 y 3rd
node 9000 42.95 -1.75 13.9665; # support 12th wall 1st z 4 y 2nd
node 9001 43.725 -3.5 13.5; # support 12th wall 1st z 4 y 3rd
node 9100 44.5 -1.75 11.2335; # support 12th wall 2nd z 1 y 2nd
node 9200 44.5 -1.75 12.6; # support 12th wall 2nd z 2 y 2nd
node 9300 44.5 -1.75 12.619428; # support 12th wall 2nd z 3 y 2nd
node 9400 44.5 -1.75 13.9665; # support 12th wall 2nd z 4 y 2nd
node 9500 58.25 -1.75 -13.9665; # support 13th wall 1st z 1 y 2nd
node 9501 59.025 -3.5 -13.5; # support 13th wall 1st z 1 y 3rd
node 9600 58.25 -1.75 -12.6; # support 13th wall 1st z 2 y 2nd
node 9601 59.025 -3.5 -12.6; # support 13th wall 1st z 2 y 3rd
node 9700 58.25 -1.75 -11.2335; # support 13th wall 1st z 3 y 2nd
node 9701 59.025 -3.5 -11.7; # support 13th wall 1st z 3 y 3rd
node 9800 59.8 -1.75 -13.9665; # support 13th wall 2nd z 1 y 2nd
node 9900 59.8 -1.75 -12.6; # support 13th wall 2nd z 2 y 2nd
node 10000 59.8 -1.75 -11.2335; # support 13th wall 2nd z 3 y 2nd
node 10100 58.25 -1.75 -5.5665; # support 14th wall 1st z 1 y 2nd
node 10101 59.025 -3.5 -5.1; # support 14th wall 1st z 1 y 3rd
node 10200 58.25 -1.75 -4.2; # support 14th wall 1st z 2 y 2nd
node 10201 59.025 -3.5 -4.2; # support 14th wall 1st z 2 y 3rd
node 10300 58.25 -1.75 -2.8335; # support 14th wall 1st z 3 y 2nd
node 10301 59.025 -3.5 -3.3; # support 14th wall 1st z 3 y 3rd
node 10400 59.8 -1.75 -5.5665; # support 14th wall 2nd z 1 y 2nd
node 10500 59.8 -1.75 -4.2; # support 14th wall 2nd z 2 y 2nd
node 10600 59.8 -1.75 -2.8335; # support 14th wall 2nd z 3 y 2nd
node 10700 58.25 -1.75 2.8335; # support 15th wall 1st z 1 y 2nd
node 10701 59.025 -3.5 3.3; # support 15th wall 1st z 1 y 3rd
node 10800 58.25 -1.75 4.2; # support 15th wall 1st z 2 y 2nd
node 10801 59.025 -3.5 4.2; # support 15th wall 1st z 2 y 3rd
node 10900 58.25 -1.75 5.5665; # support 15th wall 1st z 3 y 2nd
node 10901 59.025 -3.5 5.1; # support 15th wall 1st z 3 y 3rd
node 11000 59.8 -1.75 2.8335; # support 15th wall 2nd z 1 y 2nd
node 11100 59.8 -1.75 4.2; # support 15th wall 2nd z 2 y 2nd
node 11200 59.8 -1.75 5.5665; # support 15th wall 2nd z 3 y 2nd
node 11300 58.25 -1.75 11.2335; # support 16th wall 1st z 1 y 2nd
node 11301 59.025 -3.5 11.7; # support 16th wall 1st z 1 y 3rd
node 11400 58.25 -1.75 12.6; # support 16th wall 1st z 2 y 2nd
node 11401 59.025 -3.5 12.6; # support 16th wall 1st z 2 y 3rd
node 11500 58.25 -1.75 12.619428; # support 16th wall 1st z 3 y 2nd
node 11501 59.025 -3.5 12.612795; # support 16th wall 1st z 3 y 3rd
node 11600 58.25 -1.75 13.9665; # support 16th wall 1st z 4 y 2nd
node 11601 59.025 -3.5 13.5; # support 16th wall 1st z 4 y 3rd
node 11700 59.8 -1.75 11.2335; # support 16th wall 2nd z 1 y 2nd
node 11800 59.8 -1.75 12.6; # support 16th wall 2nd z 2 y 2nd
node 11900 59.8 -1.75 12.619428; # support 16th wall 2nd z 3 y 2nd
node 12000 59.8 -1.75 13.9665; # support 16th wall 2nd z 4 y 2nd
node 12100 73.55 -1.75 -13.9665; # support 17th wall 1st z 1 y 2nd
node 12101 74.325 -3.5 -13.5; # support 17th wall 1st z 1 y 3rd
node 12200 73.55 -1.75 -12.6; # support 17th wall 1st z 2 y 2nd
node 12201 74.325 -3.5 -12.6; # support 17th wall 1st z 2 y 3rd
node 12300 73.55 -1.75 -11.2335; # support 17th wall 1st z 3 y 2nd
node 12301 74.325 -3.5 -11.7; # support 17th wall 1st z 3 y 3rd
node 12400 75.1 -1.75 -13.9665; # support 17th wall 2nd z 1 y 2nd
node 12500 75.1 -1.75 -12.6; # support 17th wall 2nd z 2 y 2nd
node 12600 75.1 -1.75 -11.2335; # support 17th wall 2nd z 3 y 2nd
node 12700 73.55 -1.75 -5.5665; # support 18th wall 1st z 1 y 2nd
node 12701 74.325 -3.5 -5.1; # support 18th wall 1st z 1 y 3rd
node 12800 73.55 -1.75 -4.2; # support 18th wall 1st z 2 y 2nd
node 12801 74.325 -3.5 -4.2; # support 18th wall 1st z 2 y 3rd
node 12900 73.55 -1.75 -2.8335; # support 18th wall 1st z 3 y 2nd
node 12901 74.325 -3.5 -3.3; # support 18th wall 1st z 3 y 3rd
node 13000 75.1 -1.75 -5.5665; # support 18th wall 2nd z 1 y 2nd
node 13100 75.1 -1.75 -4.2; # support 18th wall 2nd z 2 y 2nd
node 13200 75.1 -1.75 -2.8335; # support 18th wall 2nd z 3 y 2nd
node 13300 73.55 -1.75 2.8335; # support 19th wall 1st z 1 y 2nd
node 13301 74.325 -3.5 3.3; # support 19th wall 1st z 1 y 3rd
node 13400 73.55 -1.75 4.2; # support 19th wall 1st z 2 y 2nd
node 13401 74.325 -3.5 4.2; # support 19th wall 1st z 2 y 3rd
node 13500 73.55 -1.75 5.5665; # support 19th wall 1st z 3 y 2nd
node 13501 74.325 -3.5 5.1; # support 19th wall 1st z 3 y 3rd
node 13600 75.1 -1.75 2.8335; # support 19th wall 2nd z 1 y 2nd
node 13700 75.1 -1.75 4.2; # support 19th wall 2nd z 2 y 2nd
node 13800 75.1 -1.75 5.5665; # support 19th wall 2nd z 3 y 2nd
node 13900 73.55 -1.75 11.2335; # support 20th wall 1st z 1 y 2nd
node 13901 74.325 -3.5 11.7; # support 20th wall 1st z 1 y 3rd
node 14000 73.55 -1.75 12.6; # support 20th wall 1st z 2 y 2nd
node 14001 74.325 -3.5 12.6; # support 20th wall 1st z 2 y 3rd
node 14100 73.55 -1.75 12.619428; # support 20th wall 1st z 3 y 2nd
node 14101 74.325 -3.5 12.612795; # support 20th wall 1st z 3 y 3rd
node 14200 73.55 -1.75 13.9665; # support 20th wall 1st z 4 y 2nd
node 14201 74.325 -3.5 13.5; # support 20th wall 1st z 4 y 3rd
node 14300 75.1 -1.75 11.2335; # support 20th wall 2nd z 1 y 2nd
node 14400 75.1 -1.75 12.6; # support 20th wall 2nd z 2 y 2nd
node 14500 75.1 -1.75 12.619428; # support 20th wall 2nd z 3 y 2nd
node 14600 75.1 -1.75 13.9665; # support 20th wall 2nd z 4 y 2nd
node 14700 88.85 -1.75 -13.9665; # support 21st wall 1st z 1 y 2nd
node 14701 89.625 -3.5 -13.5; # support 21st wall 1st z 1 y 3rd
node 14800 88.85 -1.75 -12.6; # support 21st wall 1st z 2 y 2nd
node 14801 89.625 -3.5 -12.6; # support 21st wall 1st z 2 y 3rd
node 14900 88.85 -1.75 -11.2335; # support 21st wall 1st z 3 y 2nd
node 14901 89.625 -3.5 -11.7; # support 21st wall 1st z 3 y 3rd
node 15000 90.4 -1.75 -13.9665; # support 21st wall 2nd z 1 y 2nd
node 15100 90.4 -1.75 -12.6; # support 21st wall 2nd z 2 y 2nd
node 15200 90.4 -1.75 -11.2335; # support 21st wall 2nd z 3 y 2nd
node 15300 88.85 -1.75 -5.5665; # support 22nd wall 1st z 1 y 2nd
node 15301 89.625 -3.5 -5.1; # support 22nd wall 1st z 1 y 3rd
node 15400 88.85 -1.75 -4.2; # support 22nd wall 1st z 2 y 2nd
node 15401 89.625 -3.5 -4.2; # support 22nd wall 1st z 2 y 3rd
node 15500 88.85 -1.75 -2.8335; # support 22nd wall 1st z 3 y 2nd
node 15501 89.625 -3.5 -3.3; # support 22nd wall 1st z 3 y 3rd
node 15600 90.4 -1.75 -5.5665; # support 22nd wall 2nd z 1 y 2nd
node 15700 90.4 -1.75 -4.2; # support 22nd wall 2nd z 2 y 2nd
node 15800 90.4 -1.75 -2.8335; # support 22nd wall 2nd z 3 y 2nd
node 15900 88.85 -1.75 2.8335; # support 23rd wall 1st z 1 y 2nd
node 15901 89.625 -3.5 3.3; # support 23rd wall 1st z 1 y 3rd
node 16000 88.85 -1.75 4.2; # support 23rd wall 1st z 2 y 2nd
node 16001 89.625 -3.5 4.2; # support 23rd wall 1st z 2 y 3rd
node 16100 88.85 -1.75 5.5665; # support 23rd wall 1st z 3 y 2nd
node 16101 89.625 -3.5 5.1; # support 23rd wall 1st z 3 y 3rd
node 16200 90.4 -1.75 2.8335; # support 23rd wall 2nd z 1 y 2nd
node 16300 90.4 -1.75 4.2; # support 23rd wall 2nd z 2 y 2nd
node 16400 90.4 -1.75 5.5665; # support 23rd wall 2nd z 3 y 2nd
node 16500 88.85 -1.75 11.2335; # support 24th wall 1st z 1 y 2nd
node 16501 89.625 -3.5 11.7; # support 24th wall 1st z 1 y 3rd
node 16600 88.85 -1.75 12.6; # support 24th wall 1st z 2 y 2nd
node 16601 89.625 -3.5 12.6; # support 24th wall 1st z 2 y 3rd
node 16700 88.85 -1.75 12.619428; # support 24th wall 1st z 3 y 2nd
node 16701 89.625 -3.5 12.612795; # support 24th wall 1st z 3 y 3rd
node 16800 88.85 -1.75 13.9665; # support 24th wall 1st z 4 y 2nd
node 16801 89.625 -3.5 13.5; # support 24th wall 1st z 4 y 3rd
node 16900 90.4 -1.75 11.2335; # support 24th wall 2nd z 1 y 2nd
node 17000 90.4 -1.75 12.6; # support 24th wall 2nd z 2 y 2nd
node 17100 90.4 -1.75 12.619428; # support 24th wall 2nd z 3 y 2nd
node 17200 90.4 -1.75 13.9665; # support 24th wall 2nd z 4 y 2nd
# End support nodes

# fix nodeTag x y z rx ry rz
# Begin fixed deck nodes
fix 100 1 1 1 0 0 0
fix 115 1 1 1 0 0 0
fix 200 1 1 1 0 0 0
fix 215 1 1 1 0 0 0
fix 300 1 1 1 0 0 0
fix 315 1 1 1 0 0 0
fix 400 1 1 1 0 0 0
fix 415 1 1 1 0 0 0
fix 500 1 1 1 0 0 0
fix 515 1 1 1 0 0 0
fix 600 1 1 1 0 0 0
fix 615 1 1 1 0 0 0
fix 700 1 1 1 0 0 0
fix 715 1 1 1 0 0 0
fix 800 1 1 1 0 0 0
fix 815 1 1 1 0 0 0
fix 900 1 1 1 0 0 0
fix 915 1 1 1 0 0 0
fix 1000 1 1 1 0 0 0
fix 1015 1 1 1 0 0 0
fix 1100 1 1 1 0 0 0
fix 1115 1 1 1 0 0 0
fix 1200 1 1 1 0 0 0
fix 1215 1 1 1 0 0 0
fix 1300 1 1 1 0 0 0
fix 1315 1 1 1 0 0 0
fix 1400 1 1 1 0 0 0
fix 1415 1 1 1 0 0 0
fix 1500 1 1 1 0 0 0
fix 1515 1 1 1 0 0 0
fix 1600 1 1 1 0 0 0
fix 1615 1 1 1 0 0 0
# End fixed deck nodes

# fix nodeTag x y z rx ry rz
# Begin fixed support nodes
fix 1701 0 1 1 1 1 0; # support 1 y 1
fix 1801 0 1 1 1 1 0; # support 1 y 2
fix 1901 0 1 1 1 1 0; # support 1 y 3
fix 2301 0 1 1 1 1 0; # support 2 y 1
fix 2401 0 1 1 1 1 0; # support 2 y 2
fix 2501 0 1 1 1 1 0; # support 2 y 3
fix 2901 0 1 1 1 1 0; # support 3 y 1
fix 3001 0 1 1 1 1 0; # support 3 y 2
fix 3101 0 1 1 1 1 0; # support 3 y 3
fix 3501 0 1 1 1 1 0; # support 4 y 1
fix 3601 0 1 1 1 1 0; # support 4 y 2
fix 3701 0 1 1 1 1 0; # support 4 y 3
fix 3801 0 1 1 1 1 0; # support 4 y 4
fix 4301 0 1 1 1 1 0; # support 5 y 1
fix 4401 0 1 1 1 1 0; # support 5 y 2
fix 4501 0 1 1 1 1 0; # support 5 y 3
fix 4901 0 1 1 1 1 0; # support 6 y 1
fix 5001 0 1 1 1 1 0; # support 6 y 2
fix 5101 0 1 1 1 1 0; # support 6 y 3
fix 5501 0 1 1 1 1 0; # support 7 y 1
fix 5601 0 1 1 1 1 0; # support 7 y 2
fix 5701 0 1 1 1 1 0; # support 7 y 3
fix 6101 0 1 1 1 1 0; # support 8 y 1
fix 6201 0 1 1 1 1 0; # support 8 y 2
fix 6301 0 1 1 1 1 0; # support 8 y 3
fix 6401 0 1 1 1 1 0; # support 8 y 4
fix 6901 1 1 1 1 1 0; # support 9 y 1
fix 7001 1 1 1 1 1 0; # support 9 y 2
fix 7101 1 1 1 1 1 0; # support 9 y 3
fix 7501 1 1 1 1 1 0; # support 10 y 1
fix 7601 1 1 1 1 1 0; # support 10 y 2
fix 7701 1 1 1 1 1 0; # support 10 y 3
fix 8101 1 1 1 1 1 0; # support 11 y 1
fix 8201 1 1 1 1 1 0; # support 11 y 2
fix 8301 1 1 1 1 1 0; # support 11 y 3
fix 8701 1 1 1 1 1 0; # support 12 y 1
fix 8801 1 1 1 1 1 0; # support 12 y 2
fix 8901 1 1 1 1 1 0; # support 12 y 3
fix 9001 1 1 1 1 1 0; # support 12 y 4
fix 9501 1 1 1 1 1 0; # support 13 y 1
fix 9601 1 1 1 1 1 0; # support 13 y 2
fix 9701 1 1 1 1 1 0; # support 13 y 3
fix 10101 1 1 1 1 1 0; # support 14 y 1
fix 10201 1 1 1 1 1 0; # support 14 y 2
fix 10301 1 1 1 1 1 0; # support 14 y 3
fix 10701 1 1 1 1 1 0; # support 15 y 1
fix 10801 1 1 1 1 1 0; # support 15 y 2
fix 10901 1 1 1 1 1 0; # support 15 y 3
fix 11301 1 1 1 1 1 0; # support 16 y 1
fix 11401 1 1 1 1 1 0; # support 16 y 2
fix 11501 1 1 1 1 1 0; # support 16 y 3
fix 11601 1 1 1 1 1 0; # support 16 y 4
fix 12101 0 1 1 1 1 0; # support 17 y 1
fix 12201 0 1 1 1 1 0; # support 17 y 2
fix 12301 0 1 1 1 1 0; # support 17 y 3
fix 12701 0 1 1 1 1 0; # support 18 y 1
fix 12801 0 1 1 1 1 0; # support 18 y 2
fix 12901 0 1 1 1 1 0; # support 18 y 3
fix 13301 0 1 1 1 1 0; # support 19 y 1
fix 13401 0 1 1 1 1 0; # support 19 y 2
fix 13501 0 1 1 1 1 0; # support 19 y 3
fix 13901 0 1 1 1 1 0; # support 20 y 1
fix 14001 0 1 1 1 1 0; # support 20 y 2
fix 14101 0 1 1 1 1 0; # support 20 y 3
fix 14201 0 1 1 1 1 0; # support 20 y 4
fix 14701 0 1 1 1 1 0; # support 21 y 1
fix 14801 0 1 1 1 1 0; # support 21 y 2
fix 14901 0 1 1 1 1 0; # support 21 y 3
fix 15301 0 1 1 1 1 0; # support 22 y 1
fix 15401 0 1 1 1 1 0; # support 22 y 2
fix 15501 0 1 1 1 1 0; # support 22 y 3
fix 15901 0 1 1 1 1 0; # support 23 y 1
fix 16001 0 1 1 1 1 0; # support 23 y 2
fix 16101 0 1 1 1 1 0; # support 23 y 3
fix 16501 0 1 1 1 1 0; # support 24 y 1
fix 16601 0 1 1 1 1 0; # support 24 y 2
fix 16701 0 1 1 1 1 0; # support 24 y 3
fix 16801 0 1 1 1 1 0; # support 24 y 4
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
section ElasticMembranePlateSection 36 38400000000.0 0.2 0.7902105263157895 0.0027240000000000003
section ElasticMembranePlateSection 27 38400000000.0 0.2 1.2184210526315788 0.0027240000000000003
section ElasticMembranePlateSection 26 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 28 38400000000.0 0.2 1.170842105263158 0.0027240000000000003
section ElasticMembranePlateSection 29 38400000000.0 0.2 1.123263157894737 0.0027240000000000003
section ElasticMembranePlateSection 30 38400000000.0 0.2 1.0756842105263158 0.0027240000000000003
section ElasticMembranePlateSection 35 38400000000.0 0.2 0.8377894736842105 0.0027240000000000003
section ElasticMembranePlateSection 31 38400000000.0 0.2 1.0281052631578946 0.0027240000000000003
section ElasticMembranePlateSection 32 38400000000.0 0.2 0.9805263157894737 0.0027240000000000003
section ElasticMembranePlateSection 33 38400000000.0 0.2 0.9329473684210526 0.0027240000000000003
section ElasticMembranePlateSection 34 38400000000.0 0.2 0.8853684210526316 0.0027240000000000003
section ElasticMembranePlateSection 37 38400000000.0 0.2 0.7426315789473684 0.0027240000000000003
section ElasticMembranePlateSection 38 38400000000.0 0.2 0.6950526315789474 0.0027240000000000003
section ElasticMembranePlateSection 39 38400000000.0 0.2 0.6474736842105264 0.0027240000000000003
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
element ShellMITC4 15 114 115 215 214 1; # Section3D   starts at (x_frac, z_frac) = (0, 0.0)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
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
element ShellMITC4 114 214 215 315 314 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
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
element ShellMITC4 214 314 315 415 414 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
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
element ShellMITC4 314 414 415 515 514 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
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
element ShellMITC4 414 514 515 615 614 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
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
element ShellMITC4 514 614 615 715 714 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
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
element ShellMITC4 614 714 715 815 814 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
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
element ShellMITC4 714 814 815 915 914 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
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
element ShellMITC4 814 914 915 1015 1014 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
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
element ShellMITC4 914 1014 1015 1115 1114 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
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
element ShellMITC4 1014 1114 1115 1215 1214 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
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
element ShellMITC4 1114 1214 1215 1315 1314 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
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
element ShellMITC4 1214 1314 1315 1415 1414 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1300 1400 1401 1501 1500 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1301 1401 1402 1502 1501 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1302 1402 1403 1503 1502 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1303 1403 1404 1504 1503 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1304 1404 1405 1505 1504 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1305 1405 1406 1506 1505 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1306 1406 1407 1507 1506 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1307 1407 1408 1508 1507 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1308 1408 1409 1509 1508 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1309 1409 1410 1510 1509 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1310 1410 1411 1511 1510 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1311 1411 1412 1512 1511 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1312 1412 1413 1513 1512 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1313 1413 1414 1514 1513 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1314 1414 1415 1515 1514 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1400 1500 1501 1601 1600 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1401 1501 1502 1602 1601 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1402 1502 1503 1603 1602 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1403 1503 1504 1604 1603 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1404 1504 1505 1605 1604 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1405 1505 1506 1606 1605 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1406 1506 1507 1607 1606 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1407 1507 1508 1608 1607 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1408 1508 1509 1609 1608 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1409 1509 1510 1610 1609 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1410 1510 1511 1611 1610 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1411 1511 1512 1612 1611 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1412 1512 1513 1613 1612 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1413 1513 1514 1614 1613 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1414 1514 1515 1615 1614 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
# End deck shell elements

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin pier shell elements
element ShellMITC4 1500 201 1700 1800 301 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1501 1700 1701 1801 1800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1600 301 1800 1900 401 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1601 1800 1801 1901 1900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1700 202 2000 2100 302 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1701 2000 1701 1801 2100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1800 302 2100 2200 402 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1801 2100 1801 1901 2200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1900 501 2300 2400 601 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1901 2300 2301 2401 2400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2000 601 2400 2500 701 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2001 2400 2401 2501 2500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2100 502 2600 2700 602 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2101 2600 2301 2401 2700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2200 602 2700 2800 702 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2201 2700 2401 2501 2800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2300 901 2900 3000 1001 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2301 2900 2901 3001 3000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2400 1001 3000 3100 1101 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2401 3000 3001 3101 3100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2500 902 3200 3300 1002 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2501 3200 2901 3001 3300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2600 1002 3300 3400 1102 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2601 3300 3001 3101 3400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2700 1201 3500 3600 1301 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2701 3500 3501 3601 3600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2800 1301 3600 3700 1401 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2801 3600 3601 3701 3700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2900 1401 3700 3800 1501 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2901 3700 3701 3801 3800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3000 1202 3900 4000 1302 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3001 3900 3501 3601 4000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3100 1302 4000 4100 1402 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3101 4000 3601 3701 4100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3200 1402 4100 4200 1502 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3201 4100 3701 3801 4200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3300 203 4300 4400 303 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3301 4300 4301 4401 4400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3400 303 4400 4500 403 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3401 4400 4401 4501 4500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3500 204 4600 4700 304 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3501 4600 4301 4401 4700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3600 304 4700 4800 404 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3601 4700 4401 4501 4800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3700 503 4900 5000 603 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3701 4900 4901 5001 5000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3800 603 5000 5100 703 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3801 5000 5001 5101 5100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3900 504 5200 5300 604 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3901 5200 4901 5001 5300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4000 604 5300 5400 704 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4001 5300 5001 5101 5400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4100 903 5500 5600 1003 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4101 5500 5501 5601 5600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4200 1003 5600 5700 1103 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4201 5600 5601 5701 5700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4300 904 5800 5900 1004 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4301 5800 5501 5601 5900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4400 1004 5900 6000 1104 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4401 5900 5601 5701 6000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4500 1203 6100 6200 1303 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4501 6100 6101 6201 6200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4600 1303 6200 6300 1403 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4601 6200 6201 6301 6300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4700 1403 6300 6400 1503 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4701 6300 6301 6401 6400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4800 1204 6500 6600 1304 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4801 6500 6101 6201 6600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4900 1304 6600 6700 1404 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 4901 6600 6201 6301 6700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5000 1404 6700 6800 1504 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5001 6700 6301 6401 6800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5100 206 6900 7000 306 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5101 6900 6901 7001 7000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5200 306 7000 7100 406 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5201 7000 7001 7101 7100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5300 207 7200 7300 307 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5301 7200 6901 7001 7300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5400 307 7300 7400 407 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5401 7300 7001 7101 7400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5500 506 7500 7600 606 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5501 7500 7501 7601 7600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5600 606 7600 7700 706 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5601 7600 7601 7701 7700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5700 507 7800 7900 607 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5701 7800 7501 7601 7900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5800 607 7900 8000 707 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5801 7900 7601 7701 8000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5900 906 8100 8200 1006 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 5901 8100 8101 8201 8200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6000 1006 8200 8300 1106 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6001 8200 8201 8301 8300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6100 907 8400 8500 1007 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6101 8400 8101 8201 8500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6200 1007 8500 8600 1107 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6201 8500 8201 8301 8600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6300 1206 8700 8800 1306 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6301 8700 8701 8801 8800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6400 1306 8800 8900 1406 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6401 8800 8801 8901 8900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6500 1406 8900 9000 1506 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6501 8900 8901 9001 9000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6600 1207 9100 9200 1307 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6601 9100 8701 8801 9200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6700 1307 9200 9300 1407 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6701 9200 8801 8901 9300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6800 1407 9300 9400 1507 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6801 9300 8901 9001 9400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6900 209 9500 9600 309 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 6901 9500 9501 9601 9600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7000 309 9600 9700 409 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7001 9600 9601 9701 9700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7100 210 9800 9900 310 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7101 9800 9501 9601 9900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7200 310 9900 10000 410 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7201 9900 9601 9701 10000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7300 509 10100 10200 609 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7301 10100 10101 10201 10200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7400 609 10200 10300 709 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7401 10200 10201 10301 10300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7500 510 10400 10500 610 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7501 10400 10101 10201 10500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7600 610 10500 10600 710 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7601 10500 10201 10301 10600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7700 909 10700 10800 1009 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7701 10700 10701 10801 10800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7800 1009 10800 10900 1109 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7801 10800 10801 10901 10900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7900 910 11000 11100 1010 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 7901 11000 10701 10801 11100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8000 1010 11100 11200 1110 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8001 11100 10801 10901 11200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8100 1209 11300 11400 1309 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8101 11300 11301 11401 11400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8200 1309 11400 11500 1409 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8201 11400 11401 11501 11500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8300 1409 11500 11600 1509 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8301 11500 11501 11601 11600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8400 1210 11700 11800 1310 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8401 11700 11301 11401 11800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8500 1310 11800 11900 1410 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8501 11800 11401 11501 11900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8600 1410 11900 12000 1510 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8601 11900 11501 11601 12000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8700 211 12100 12200 311 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8701 12100 12101 12201 12200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8800 311 12200 12300 411 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8801 12200 12201 12301 12300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8900 212 12400 12500 312 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 8901 12400 12101 12201 12500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9000 312 12500 12600 412 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9001 12500 12201 12301 12600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9100 511 12700 12800 611 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9101 12700 12701 12801 12800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9200 611 12800 12900 711 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9201 12800 12801 12901 12900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9300 512 13000 13100 612 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9301 13000 12701 12801 13100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9400 612 13100 13200 712 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9401 13100 12801 12901 13200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9500 911 13300 13400 1011 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9501 13300 13301 13401 13400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9600 1011 13400 13500 1111 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9601 13400 13401 13501 13500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9700 912 13600 13700 1012 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9701 13600 13301 13401 13700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9800 1012 13700 13800 1112 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9801 13700 13401 13501 13800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9900 1211 13900 14000 1311 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 9901 13900 13901 14001 14000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10000 1311 14000 14100 1411 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10001 14000 14001 14101 14100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10100 1411 14100 14200 1511 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10101 14100 14101 14201 14200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10200 1212 14300 14400 1312 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10201 14300 13901 14001 14400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10300 1312 14400 14500 1412 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10301 14400 14001 14101 14500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10400 1412 14500 14600 1512 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10401 14500 14101 14201 14600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10500 213 14700 14800 313 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10501 14700 14701 14801 14800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10600 313 14800 14900 413 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10601 14800 14801 14901 14900 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10700 214 15000 15100 314 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10701 15000 14701 14801 15100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10800 314 15100 15200 414 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10801 15100 14801 14901 15200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10900 513 15300 15400 613 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10901 15300 15301 15401 15400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11000 613 15400 15500 713 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11001 15400 15401 15501 15500 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11100 514 15600 15700 614 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11101 15600 15301 15401 15700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11200 614 15700 15800 714 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11201 15700 15401 15501 15800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11300 913 15900 16000 1013 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11301 15900 15901 16001 16000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11400 1013 16000 16100 1113 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11401 16000 16001 16101 16100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11500 914 16200 16300 1014 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11501 16200 15901 16001 16300 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11600 1014 16300 16400 1114 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11601 16300 16001 16101 16400 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11700 1213 16500 16600 1313 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11701 16500 16501 16601 16600 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11800 1313 16600 16700 1413 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11801 16600 16601 16701 16700 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11900 1413 16700 16800 1513 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 11901 16700 16701 16801 16800 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12000 1214 16900 17000 1314 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12001 16900 16501 16601 17000 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12100 1314 17000 17100 1414 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12101 17000 16601 16701 17100 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12200 1414 17100 17200 1514 26; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 12201 17100 16701 16801 17200 45; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
# End pier shell elements



timeSeries Linear 1

pattern Plain 1 1 {
# load nodeTag N_x N_y N_z N_rx N_ry N_rz
# Begin loads
load 1405 0 100000 0 0 0 0
# End loads
}

system BandGeneral
numberer RCM
constraints Transformation
integrator LoadControl 1
algorithm Linear

analysis Static

# recorder Node -file path -node nodeTags -dof direction disp
# Begin translation recorders

# End translation recorders

# Array of each element's ID.
set l [list 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1500 1501 1600 1601 1700 1701 1800 1801 1900 1901 2000 2001 2100 2101 2200 2201 2300 2301 2400 2401 2500 2501 2600 2601 2700 2701 2800 2801 2900 2901 3000 3001 3100 3101 3200 3201 3300 3301 3400 3401 3500 3501 3600 3601 3700 3701 3800 3801 3900 3901 4000 4001 4100 4101 4200 4201 4300 4301 4400 4401 4500 4501 4600 4601 4700 4701 4800 4801 4900 4901 5000 5001 5100 5101 5200 5201 5300 5301 5400 5401 5500 5501 5600 5601 5700 5701 5800 5801 5900 5901 6000 6001 6100 6101 6200 6201 6300 6301 6400 6401 6500 6501 6600 6601 6700 6701 6800 6801 6900 6901 7000 7001 7100 7101 7200 7201 7300 7301 7400 7401 7500 7501 7600 7601 7700 7701 7800 7801 7900 7901 8000 8001 8100 8101 8200 8201 8300 8301 8400 8401 8500 8501 8600 8601 8700 8701 8800 8801 8900 8901 9000 9001 9100 9101 9200 9201 9300 9301 9400 9401 9500 9501 9600 9601 9700 9701 9800 9801 9900 9901 10000 10001 10100 10101 10200 10201 10300 10301 10400 10401 10500 10501 10600 10601 10700 10701 10800 10801 10900 10901 11000 11001 11100 11101 11200 11201 11300 11301 11400 11401 11500 11501 11600 11601 11700 11701 11800 11801 11900 11901 12000 12001 12100 12101 12200 12201]
# Write internal forces to file.
set outfile [open "generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-0,340,-0,880,-100,000--elems.out" w]

foreach i $l {
	# https://opensees.berkeley.edu/community/viewtopic.php?f=2&t=64527&p=110182&hilit=shellMITC4#p110182
	# [Nxx, Nyy, Nxy, Mxx, Myy, Mxy, Vxz, Vyz]
	set internal_force [eleResponse $i stresses]
	puts $outfile $internal_force
}
close $outfile

analyze 1
