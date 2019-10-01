
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
node 103 20.55 0 -16.6
node 104 26.875 0 -16.6
node 105 29.975 0 -16.6
node 106 41.1 0 -16.6
node 107 42.175 0 -16.6
node 108 45.275 0 -16.6
node 109 57.475 0 -16.6
node 110 60.575 0 -16.6
node 111 61.65 0 -16.6
node 112 72.775 0 -16.6
node 113 75.875 0 -16.6
node 114 82.2 0 -16.6
node 115 88.075 0 -16.6
node 116 91.175 0 -16.6
node 117 102.75 0 -16.6
node 200 0 0 -14.433
node 201 11.575 0 -14.433; # support node
node 202 14.675 0 -14.433; # support node
node 203 20.55 0 -14.433
node 204 26.875 0 -14.433; # support node
node 205 29.975 0 -14.433; # support node
node 206 41.1 0 -14.433
node 207 42.175 0 -14.433; # support node
node 208 45.275 0 -14.433; # support node
node 209 57.475 0 -14.433; # support node
node 210 60.575 0 -14.433; # support node
node 211 61.65 0 -14.433
node 212 72.775 0 -14.433; # support node
node 213 75.875 0 -14.433; # support node
node 214 82.2 0 -14.433
node 215 88.075 0 -14.433; # support node
node 216 91.175 0 -14.433; # support node
node 217 102.75 0 -14.433
node 300 0 0 -13.211
node 301 11.575 0 -13.211; # support node
node 302 14.675 0 -13.211; # support node
node 303 20.55 0 -13.211
node 304 26.875 0 -13.211; # support node
node 305 29.975 0 -13.211; # support node
node 306 41.1 0 -13.211
node 307 42.175 0 -13.211; # support node
node 308 45.275 0 -13.211; # support node
node 309 57.475 0 -13.211; # support node
node 310 60.575 0 -13.211; # support node
node 311 61.65 0 -13.211
node 312 72.775 0 -13.211; # support node
node 313 75.875 0 -13.211; # support node
node 314 82.2 0 -13.211
node 315 88.075 0 -13.211; # support node
node 316 91.175 0 -13.211; # support node
node 317 102.75 0 -13.211
node 400 0 0 -11.989
node 401 11.575 0 -11.989; # support node
node 402 14.675 0 -11.989; # support node
node 403 20.55 0 -11.989
node 404 26.875 0 -11.989; # support node
node 405 29.975 0 -11.989; # support node
node 406 41.1 0 -11.989
node 407 42.175 0 -11.989; # support node
node 408 45.275 0 -11.989; # support node
node 409 57.475 0 -11.989; # support node
node 410 60.575 0 -11.989; # support node
node 411 61.65 0 -11.989
node 412 72.775 0 -11.989; # support node
node 413 75.875 0 -11.989; # support node
node 414 82.2 0 -11.989
node 415 88.075 0 -11.989; # support node
node 416 91.175 0 -11.989; # support node
node 417 102.75 0 -11.989
node 500 0 0 -10.767
node 501 11.575 0 -10.767; # support node
node 502 14.675 0 -10.767; # support node
node 503 20.55 0 -10.767
node 504 26.875 0 -10.767; # support node
node 505 29.975 0 -10.767; # support node
node 506 41.1 0 -10.767
node 507 42.175 0 -10.767; # support node
node 508 45.275 0 -10.767; # support node
node 509 57.475 0 -10.767; # support node
node 510 60.575 0 -10.767; # support node
node 511 61.65 0 -10.767
node 512 72.775 0 -10.767; # support node
node 513 75.875 0 -10.767; # support node
node 514 82.2 0 -10.767
node 515 88.075 0 -10.767; # support node
node 516 91.175 0 -10.767; # support node
node 517 102.75 0 -10.767
node 600 0 0 -9.96
node 601 11.575 0 -9.96
node 602 14.675 0 -9.96
node 603 20.55 0 -9.96
node 604 26.875 0 -9.96
node 605 29.975 0 -9.96
node 606 41.1 0 -9.96
node 607 42.175 0 -9.96
node 608 45.275 0 -9.96
node 609 57.475 0 -9.96
node 610 60.575 0 -9.96
node 611 61.65 0 -9.96
node 612 72.775 0 -9.96
node 613 75.875 0 -9.96
node 614 82.2 0 -9.96
node 615 88.075 0 -9.96
node 616 91.175 0 -9.96
node 617 102.75 0 -9.96
node 700 0 0 -6.033
node 701 11.575 0 -6.033; # support node
node 702 14.675 0 -6.033; # support node
node 703 20.55 0 -6.033
node 704 26.875 0 -6.033; # support node
node 705 29.975 0 -6.033; # support node
node 706 41.1 0 -6.033
node 707 42.175 0 -6.033; # support node
node 708 45.275 0 -6.033; # support node
node 709 57.475 0 -6.033; # support node
node 710 60.575 0 -6.033; # support node
node 711 61.65 0 -6.033
node 712 72.775 0 -6.033; # support node
node 713 75.875 0 -6.033; # support node
node 714 82.2 0 -6.033
node 715 88.075 0 -6.033; # support node
node 716 91.175 0 -6.033; # support node
node 717 102.75 0 -6.033
node 800 0 0 -4.811
node 801 11.575 0 -4.811; # support node
node 802 14.675 0 -4.811; # support node
node 803 20.55 0 -4.811
node 804 26.875 0 -4.811; # support node
node 805 29.975 0 -4.811; # support node
node 806 41.1 0 -4.811
node 807 42.175 0 -4.811; # support node
node 808 45.275 0 -4.811; # support node
node 809 57.475 0 -4.811; # support node
node 810 60.575 0 -4.811; # support node
node 811 61.65 0 -4.811
node 812 72.775 0 -4.811; # support node
node 813 75.875 0 -4.811; # support node
node 814 82.2 0 -4.811
node 815 88.075 0 -4.811; # support node
node 816 91.175 0 -4.811; # support node
node 817 102.75 0 -4.811
node 900 0 0 -3.589
node 901 11.575 0 -3.589; # support node
node 902 14.675 0 -3.589; # support node
node 903 20.55 0 -3.589
node 904 26.875 0 -3.589; # support node
node 905 29.975 0 -3.589; # support node
node 906 41.1 0 -3.589
node 907 42.175 0 -3.589; # support node
node 908 45.275 0 -3.589; # support node
node 909 57.475 0 -3.589; # support node
node 910 60.575 0 -3.589; # support node
node 911 61.65 0 -3.589
node 912 72.775 0 -3.589; # support node
node 913 75.875 0 -3.589; # support node
node 914 82.2 0 -3.589
node 915 88.075 0 -3.589; # support node
node 916 91.175 0 -3.589; # support node
node 917 102.75 0 -3.589
node 1000 0 0 -3.32
node 1001 11.575 0 -3.32
node 1002 14.675 0 -3.32
node 1003 20.55 0 -3.32
node 1004 26.875 0 -3.32
node 1005 29.975 0 -3.32
node 1006 41.1 0 -3.32
node 1007 42.175 0 -3.32
node 1008 45.275 0 -3.32
node 1009 57.475 0 -3.32
node 1010 60.575 0 -3.32
node 1011 61.65 0 -3.32
node 1012 72.775 0 -3.32
node 1013 75.875 0 -3.32
node 1014 82.2 0 -3.32
node 1015 88.075 0 -3.32
node 1016 91.175 0 -3.32
node 1017 102.75 0 -3.32
node 1100 0 0 -2.367
node 1101 11.575 0 -2.367; # support node
node 1102 14.675 0 -2.367; # support node
node 1103 20.55 0 -2.367
node 1104 26.875 0 -2.367; # support node
node 1105 29.975 0 -2.367; # support node
node 1106 41.1 0 -2.367
node 1107 42.175 0 -2.367; # support node
node 1108 45.275 0 -2.367; # support node
node 1109 57.475 0 -2.367; # support node
node 1110 60.575 0 -2.367; # support node
node 1111 61.65 0 -2.367
node 1112 72.775 0 -2.367; # support node
node 1113 75.875 0 -2.367; # support node
node 1114 82.2 0 -2.367
node 1115 88.075 0 -2.367; # support node
node 1116 91.175 0 -2.367; # support node
node 1117 102.75 0 -2.367
node 1200 0 0 2.367
node 1201 11.575 0 2.367; # support node
node 1202 14.675 0 2.367; # support node
node 1203 20.55 0 2.367
node 1204 26.875 0 2.367; # support node
node 1205 29.975 0 2.367; # support node
node 1206 41.1 0 2.367
node 1207 42.175 0 2.367; # support node
node 1208 45.275 0 2.367; # support node
node 1209 57.475 0 2.367; # support node
node 1210 60.575 0 2.367; # support node
node 1211 61.65 0 2.367
node 1212 72.775 0 2.367; # support node
node 1213 75.875 0 2.367; # support node
node 1214 82.2 0 2.367
node 1215 88.075 0 2.367; # support node
node 1216 91.175 0 2.367; # support node
node 1217 102.75 0 2.367
node 1300 0 0 3.32
node 1301 11.575 0 3.32
node 1302 14.675 0 3.32
node 1303 20.55 0 3.32
node 1304 26.875 0 3.32
node 1305 29.975 0 3.32
node 1306 41.1 0 3.32
node 1307 42.175 0 3.32
node 1308 45.275 0 3.32
node 1309 57.475 0 3.32
node 1310 60.575 0 3.32
node 1311 61.65 0 3.32
node 1312 72.775 0 3.32
node 1313 75.875 0 3.32
node 1314 82.2 0 3.32
node 1315 88.075 0 3.32
node 1316 91.175 0 3.32
node 1317 102.75 0 3.32
node 1400 0 0 3.589
node 1401 11.575 0 3.589; # support node
node 1402 14.675 0 3.589; # support node
node 1403 20.55 0 3.589
node 1404 26.875 0 3.589; # support node
node 1405 29.975 0 3.589; # support node
node 1406 41.1 0 3.589
node 1407 42.175 0 3.589; # support node
node 1408 45.275 0 3.589; # support node
node 1409 57.475 0 3.589; # support node
node 1410 60.575 0 3.589; # support node
node 1411 61.65 0 3.589
node 1412 72.775 0 3.589; # support node
node 1413 75.875 0 3.589; # support node
node 1414 82.2 0 3.589
node 1415 88.075 0 3.589; # support node
node 1416 91.175 0 3.589; # support node
node 1417 102.75 0 3.589
node 1500 0 0 4.811
node 1501 11.575 0 4.811; # support node
node 1502 14.675 0 4.811; # support node
node 1503 20.55 0 4.811
node 1504 26.875 0 4.811; # support node
node 1505 29.975 0 4.811; # support node
node 1506 41.1 0 4.811
node 1507 42.175 0 4.811; # support node
node 1508 45.275 0 4.811; # support node
node 1509 57.475 0 4.811; # support node
node 1510 60.575 0 4.811; # support node
node 1511 61.65 0 4.811
node 1512 72.775 0 4.811; # support node
node 1513 75.875 0 4.811; # support node
node 1514 82.2 0 4.811
node 1515 88.075 0 4.811; # support node
node 1516 91.175 0 4.811; # support node
node 1517 102.75 0 4.811
node 1600 0 0 6.033
node 1601 11.575 0 6.033; # support node
node 1602 14.675 0 6.033; # support node
node 1603 20.55 0 6.033
node 1604 26.875 0 6.033; # support node
node 1605 29.975 0 6.033; # support node
node 1606 41.1 0 6.033
node 1607 42.175 0 6.033; # support node
node 1608 45.275 0 6.033; # support node
node 1609 57.475 0 6.033; # support node
node 1610 60.575 0 6.033; # support node
node 1611 61.65 0 6.033
node 1612 72.775 0 6.033; # support node
node 1613 75.875 0 6.033; # support node
node 1614 82.2 0 6.033
node 1615 88.075 0 6.033; # support node
node 1616 91.175 0 6.033; # support node
node 1617 102.75 0 6.033
node 1700 0 0 9.96
node 1701 11.575 0 9.96
node 1702 14.675 0 9.96
node 1703 20.55 0 9.96
node 1704 26.875 0 9.96
node 1705 29.975 0 9.96
node 1706 41.1 0 9.96
node 1707 42.175 0 9.96
node 1708 45.275 0 9.96
node 1709 57.475 0 9.96
node 1710 60.575 0 9.96
node 1711 61.65 0 9.96
node 1712 72.775 0 9.96
node 1713 75.875 0 9.96
node 1714 82.2 0 9.96
node 1715 88.075 0 9.96
node 1716 91.175 0 9.96
node 1717 102.75 0 9.96
node 1800 0 0 10.767
node 1801 11.575 0 10.767; # support node
node 1802 14.675 0 10.767; # support node
node 1803 20.55 0 10.767
node 1804 26.875 0 10.767; # support node
node 1805 29.975 0 10.767; # support node
node 1806 41.1 0 10.767
node 1807 42.175 0 10.767; # support node
node 1808 45.275 0 10.767; # support node
node 1809 57.475 0 10.767; # support node
node 1810 60.575 0 10.767; # support node
node 1811 61.65 0 10.767
node 1812 72.775 0 10.767; # support node
node 1813 75.875 0 10.767; # support node
node 1814 82.2 0 10.767
node 1815 88.075 0 10.767; # support node
node 1816 91.175 0 10.767; # support node
node 1817 102.75 0 10.767
node 1900 0 0 11.989
node 1901 11.575 0 11.989; # support node
node 1902 14.675 0 11.989; # support node
node 1903 20.55 0 11.989
node 1904 26.875 0 11.989; # support node
node 1905 29.975 0 11.989; # support node
node 1906 41.1 0 11.989
node 1907 42.175 0 11.989; # support node
node 1908 45.275 0 11.989; # support node
node 1909 57.475 0 11.989; # support node
node 1910 60.575 0 11.989; # support node
node 1911 61.65 0 11.989
node 1912 72.775 0 11.989; # support node
node 1913 75.875 0 11.989; # support node
node 1914 82.2 0 11.989
node 1915 88.075 0 11.989; # support node
node 1916 91.175 0 11.989; # support node
node 1917 102.75 0 11.989
node 2000 0 0 13.211
node 2001 11.575 0 13.211; # support node
node 2002 14.675 0 13.211; # support node
node 2003 20.55 0 13.211
node 2004 26.875 0 13.211; # support node
node 2005 29.975 0 13.211; # support node
node 2006 41.1 0 13.211
node 2007 42.175 0 13.211; # support node
node 2008 45.275 0 13.211; # support node
node 2009 57.475 0 13.211; # support node
node 2010 60.575 0 13.211; # support node
node 2011 61.65 0 13.211
node 2012 72.775 0 13.211; # support node
node 2013 75.875 0 13.211; # support node
node 2014 82.2 0 13.211
node 2015 88.075 0 13.211; # support node
node 2016 91.175 0 13.211; # support node
node 2017 102.75 0 13.211
node 2100 0 0 14.433
node 2101 11.575 0 14.433; # support node
node 2102 14.675 0 14.433; # support node
node 2103 20.55 0 14.433
node 2104 26.875 0 14.433; # support node
node 2105 29.975 0 14.433; # support node
node 2106 41.1 0 14.433
node 2107 42.175 0 14.433; # support node
node 2108 45.275 0 14.433; # support node
node 2109 57.475 0 14.433; # support node
node 2110 60.575 0 14.433; # support node
node 2111 61.65 0 14.433
node 2112 72.775 0 14.433; # support node
node 2113 75.875 0 14.433; # support node
node 2114 82.2 0 14.433
node 2115 88.075 0 14.433; # support node
node 2116 91.175 0 14.433; # support node
node 2117 102.75 0 14.433
node 2200 0 0 16.6
node 2201 11.575 0 16.6
node 2202 14.675 0 16.6
node 2203 20.55 0 16.6
node 2204 26.875 0 16.6
node 2205 29.975 0 16.6
node 2206 41.1 0 16.6
node 2207 42.175 0 16.6
node 2208 45.275 0 16.6
node 2209 57.475 0 16.6
node 2210 60.575 0 16.6
node 2211 61.65 0 16.6
node 2212 72.775 0 16.6
node 2213 75.875 0 16.6
node 2214 82.2 0 16.6
node 2215 88.075 0 16.6
node 2216 91.175 0 16.6
node 2217 102.75 0 16.6
# End deck nodes

# node nodeTag x y z
# Begin support nodes
node 2300 12.091667 -1.166667 -14.122; # support 1 wall 1 z 1 y 1
node 2301 12.608333 -2.333333 -13.811; # support 1 wall 1 z 1 y 2
node 2302 13.125 -3.5 -13.5; # support 1 wall 1 z 1 y 3
node 2400 12.091667 -1.166667 -13.107333; # support 1 wall 1 z 2 y 1
node 2401 12.608333 -2.333333 -13.003667; # support 1 wall 1 z 2 y 2
node 2402 13.125 -3.5 -12.9; # support 1 wall 1 z 2 y 3
node 2500 12.091667 -1.166667 -12.092667; # support 1 wall 1 z 3 y 1
node 2501 12.608333 -2.333333 -12.196333; # support 1 wall 1 z 3 y 2
node 2502 13.125 -3.5 -12.3; # support 1 wall 1 z 3 y 3
node 2600 12.091667 -1.166667 -11.078; # support 1 wall 1 z 4 y 1
node 2601 12.608333 -2.333333 -11.389; # support 1 wall 1 z 4 y 2
node 2602 13.125 -3.5 -11.7; # support 1 wall 1 z 4 y 3
node 2700 14.158333 -1.166667 -14.122; # support 1 wall 2 z 1 y 1
node 2701 13.641667 -2.333333 -13.811; # support 1 wall 2 z 1 y 2
node 2800 14.158333 -1.166667 -13.107333; # support 1 wall 2 z 2 y 1
node 2801 13.641667 -2.333333 -13.003667; # support 1 wall 2 z 2 y 2
node 2900 14.158333 -1.166667 -12.092667; # support 1 wall 2 z 3 y 1
node 2901 13.641667 -2.333333 -12.196333; # support 1 wall 2 z 3 y 2
node 3000 14.158333 -1.166667 -11.078; # support 1 wall 2 z 4 y 1
node 3001 13.641667 -2.333333 -11.389; # support 1 wall 2 z 4 y 2
node 3100 12.091667 -1.166667 -5.722; # support 2 wall 1 z 1 y 1
node 3101 12.608333 -2.333333 -5.411; # support 2 wall 1 z 1 y 2
node 3102 13.125 -3.5 -5.1; # support 2 wall 1 z 1 y 3
node 3200 12.091667 -1.166667 -4.707333; # support 2 wall 1 z 2 y 1
node 3201 12.608333 -2.333333 -4.603667; # support 2 wall 1 z 2 y 2
node 3202 13.125 -3.5 -4.5; # support 2 wall 1 z 2 y 3
node 3300 12.091667 -1.166667 -3.692667; # support 2 wall 1 z 3 y 1
node 3301 12.608333 -2.333333 -3.796333; # support 2 wall 1 z 3 y 2
node 3302 13.125 -3.5 -3.9; # support 2 wall 1 z 3 y 3
node 3400 12.091667 -1.166667 -2.678; # support 2 wall 1 z 4 y 1
node 3401 12.608333 -2.333333 -2.989; # support 2 wall 1 z 4 y 2
node 3402 13.125 -3.5 -3.3; # support 2 wall 1 z 4 y 3
node 3500 14.158333 -1.166667 -5.722; # support 2 wall 2 z 1 y 1
node 3501 13.641667 -2.333333 -5.411; # support 2 wall 2 z 1 y 2
node 3600 14.158333 -1.166667 -4.707333; # support 2 wall 2 z 2 y 1
node 3601 13.641667 -2.333333 -4.603667; # support 2 wall 2 z 2 y 2
node 3700 14.158333 -1.166667 -3.692667; # support 2 wall 2 z 3 y 1
node 3701 13.641667 -2.333333 -3.796333; # support 2 wall 2 z 3 y 2
node 3800 14.158333 -1.166667 -2.678; # support 2 wall 2 z 4 y 1
node 3801 13.641667 -2.333333 -2.989; # support 2 wall 2 z 4 y 2
node 3900 12.091667 -1.166667 2.678; # support 3 wall 1 z 1 y 1
node 3901 12.608333 -2.333333 2.989; # support 3 wall 1 z 1 y 2
node 3902 13.125 -3.5 3.3; # support 3 wall 1 z 1 y 3
node 4000 12.091667 -1.166667 3.692667; # support 3 wall 1 z 2 y 1
node 4001 12.608333 -2.333333 3.796333; # support 3 wall 1 z 2 y 2
node 4002 13.125 -3.5 3.9; # support 3 wall 1 z 2 y 3
node 4100 12.091667 -1.166667 4.707333; # support 3 wall 1 z 3 y 1
node 4101 12.608333 -2.333333 4.603667; # support 3 wall 1 z 3 y 2
node 4102 13.125 -3.5 4.5; # support 3 wall 1 z 3 y 3
node 4200 12.091667 -1.166667 5.722; # support 3 wall 1 z 4 y 1
node 4201 12.608333 -2.333333 5.411; # support 3 wall 1 z 4 y 2
node 4202 13.125 -3.5 5.1; # support 3 wall 1 z 4 y 3
node 4300 14.158333 -1.166667 2.678; # support 3 wall 2 z 1 y 1
node 4301 13.641667 -2.333333 2.989; # support 3 wall 2 z 1 y 2
node 4400 14.158333 -1.166667 3.692667; # support 3 wall 2 z 2 y 1
node 4401 13.641667 -2.333333 3.796333; # support 3 wall 2 z 2 y 2
node 4500 14.158333 -1.166667 4.707333; # support 3 wall 2 z 3 y 1
node 4501 13.641667 -2.333333 4.603667; # support 3 wall 2 z 3 y 2
node 4600 14.158333 -1.166667 5.722; # support 3 wall 2 z 4 y 1
node 4601 13.641667 -2.333333 5.411; # support 3 wall 2 z 4 y 2
node 4700 12.091667 -1.166667 11.078; # support 4 wall 1 z 1 y 1
node 4701 12.608333 -2.333333 11.389; # support 4 wall 1 z 1 y 2
node 4702 13.125 -3.5 11.7; # support 4 wall 1 z 1 y 3
node 4800 12.091667 -1.166667 12.092667; # support 4 wall 1 z 2 y 1
node 4801 12.608333 -2.333333 12.196333; # support 4 wall 1 z 2 y 2
node 4802 13.125 -3.5 12.3; # support 4 wall 1 z 2 y 3
node 4900 12.091667 -1.166667 13.107333; # support 4 wall 1 z 3 y 1
node 4901 12.608333 -2.333333 13.003667; # support 4 wall 1 z 3 y 2
node 4902 13.125 -3.5 12.9; # support 4 wall 1 z 3 y 3
node 5000 12.091667 -1.166667 14.122; # support 4 wall 1 z 4 y 1
node 5001 12.608333 -2.333333 13.811; # support 4 wall 1 z 4 y 2
node 5002 13.125 -3.5 13.5; # support 4 wall 1 z 4 y 3
node 5100 14.158333 -1.166667 11.078; # support 4 wall 2 z 1 y 1
node 5101 13.641667 -2.333333 11.389; # support 4 wall 2 z 1 y 2
node 5200 14.158333 -1.166667 12.092667; # support 4 wall 2 z 2 y 1
node 5201 13.641667 -2.333333 12.196333; # support 4 wall 2 z 2 y 2
node 5300 14.158333 -1.166667 13.107333; # support 4 wall 2 z 3 y 1
node 5301 13.641667 -2.333333 13.003667; # support 4 wall 2 z 3 y 2
node 5400 14.158333 -1.166667 14.122; # support 4 wall 2 z 4 y 1
node 5401 13.641667 -2.333333 13.811; # support 4 wall 2 z 4 y 2
node 5500 27.391667 -1.166667 -14.122; # support 5 wall 1 z 1 y 1
node 5501 27.908333 -2.333333 -13.811; # support 5 wall 1 z 1 y 2
node 5502 28.425 -3.5 -13.5; # support 5 wall 1 z 1 y 3
node 5600 27.391667 -1.166667 -13.107333; # support 5 wall 1 z 2 y 1
node 5601 27.908333 -2.333333 -13.003667; # support 5 wall 1 z 2 y 2
node 5602 28.425 -3.5 -12.9; # support 5 wall 1 z 2 y 3
node 5700 27.391667 -1.166667 -12.092667; # support 5 wall 1 z 3 y 1
node 5701 27.908333 -2.333333 -12.196333; # support 5 wall 1 z 3 y 2
node 5702 28.425 -3.5 -12.3; # support 5 wall 1 z 3 y 3
node 5800 27.391667 -1.166667 -11.078; # support 5 wall 1 z 4 y 1
node 5801 27.908333 -2.333333 -11.389; # support 5 wall 1 z 4 y 2
node 5802 28.425 -3.5 -11.7; # support 5 wall 1 z 4 y 3
node 5900 29.458333 -1.166667 -14.122; # support 5 wall 2 z 1 y 1
node 5901 28.941667 -2.333333 -13.811; # support 5 wall 2 z 1 y 2
node 6000 29.458333 -1.166667 -13.107333; # support 5 wall 2 z 2 y 1
node 6001 28.941667 -2.333333 -13.003667; # support 5 wall 2 z 2 y 2
node 6100 29.458333 -1.166667 -12.092667; # support 5 wall 2 z 3 y 1
node 6101 28.941667 -2.333333 -12.196333; # support 5 wall 2 z 3 y 2
node 6200 29.458333 -1.166667 -11.078; # support 5 wall 2 z 4 y 1
node 6201 28.941667 -2.333333 -11.389; # support 5 wall 2 z 4 y 2
node 6300 27.391667 -1.166667 -5.722; # support 6 wall 1 z 1 y 1
node 6301 27.908333 -2.333333 -5.411; # support 6 wall 1 z 1 y 2
node 6302 28.425 -3.5 -5.1; # support 6 wall 1 z 1 y 3
node 6400 27.391667 -1.166667 -4.707333; # support 6 wall 1 z 2 y 1
node 6401 27.908333 -2.333333 -4.603667; # support 6 wall 1 z 2 y 2
node 6402 28.425 -3.5 -4.5; # support 6 wall 1 z 2 y 3
node 6500 27.391667 -1.166667 -3.692667; # support 6 wall 1 z 3 y 1
node 6501 27.908333 -2.333333 -3.796333; # support 6 wall 1 z 3 y 2
node 6502 28.425 -3.5 -3.9; # support 6 wall 1 z 3 y 3
node 6600 27.391667 -1.166667 -2.678; # support 6 wall 1 z 4 y 1
node 6601 27.908333 -2.333333 -2.989; # support 6 wall 1 z 4 y 2
node 6602 28.425 -3.5 -3.3; # support 6 wall 1 z 4 y 3
node 6700 29.458333 -1.166667 -5.722; # support 6 wall 2 z 1 y 1
node 6701 28.941667 -2.333333 -5.411; # support 6 wall 2 z 1 y 2
node 6800 29.458333 -1.166667 -4.707333; # support 6 wall 2 z 2 y 1
node 6801 28.941667 -2.333333 -4.603667; # support 6 wall 2 z 2 y 2
node 6900 29.458333 -1.166667 -3.692667; # support 6 wall 2 z 3 y 1
node 6901 28.941667 -2.333333 -3.796333; # support 6 wall 2 z 3 y 2
node 7000 29.458333 -1.166667 -2.678; # support 6 wall 2 z 4 y 1
node 7001 28.941667 -2.333333 -2.989; # support 6 wall 2 z 4 y 2
node 7100 27.391667 -1.166667 2.678; # support 7 wall 1 z 1 y 1
node 7101 27.908333 -2.333333 2.989; # support 7 wall 1 z 1 y 2
node 7102 28.425 -3.5 3.3; # support 7 wall 1 z 1 y 3
node 7200 27.391667 -1.166667 3.692667; # support 7 wall 1 z 2 y 1
node 7201 27.908333 -2.333333 3.796333; # support 7 wall 1 z 2 y 2
node 7202 28.425 -3.5 3.9; # support 7 wall 1 z 2 y 3
node 7300 27.391667 -1.166667 4.707333; # support 7 wall 1 z 3 y 1
node 7301 27.908333 -2.333333 4.603667; # support 7 wall 1 z 3 y 2
node 7302 28.425 -3.5 4.5; # support 7 wall 1 z 3 y 3
node 7400 27.391667 -1.166667 5.722; # support 7 wall 1 z 4 y 1
node 7401 27.908333 -2.333333 5.411; # support 7 wall 1 z 4 y 2
node 7402 28.425 -3.5 5.1; # support 7 wall 1 z 4 y 3
node 7500 29.458333 -1.166667 2.678; # support 7 wall 2 z 1 y 1
node 7501 28.941667 -2.333333 2.989; # support 7 wall 2 z 1 y 2
node 7600 29.458333 -1.166667 3.692667; # support 7 wall 2 z 2 y 1
node 7601 28.941667 -2.333333 3.796333; # support 7 wall 2 z 2 y 2
node 7700 29.458333 -1.166667 4.707333; # support 7 wall 2 z 3 y 1
node 7701 28.941667 -2.333333 4.603667; # support 7 wall 2 z 3 y 2
node 7800 29.458333 -1.166667 5.722; # support 7 wall 2 z 4 y 1
node 7801 28.941667 -2.333333 5.411; # support 7 wall 2 z 4 y 2
node 7900 27.391667 -1.166667 11.078; # support 8 wall 1 z 1 y 1
node 7901 27.908333 -2.333333 11.389; # support 8 wall 1 z 1 y 2
node 7902 28.425 -3.5 11.7; # support 8 wall 1 z 1 y 3
node 8000 27.391667 -1.166667 12.092667; # support 8 wall 1 z 2 y 1
node 8001 27.908333 -2.333333 12.196333; # support 8 wall 1 z 2 y 2
node 8002 28.425 -3.5 12.3; # support 8 wall 1 z 2 y 3
node 8100 27.391667 -1.166667 13.107333; # support 8 wall 1 z 3 y 1
node 8101 27.908333 -2.333333 13.003667; # support 8 wall 1 z 3 y 2
node 8102 28.425 -3.5 12.9; # support 8 wall 1 z 3 y 3
node 8200 27.391667 -1.166667 14.122; # support 8 wall 1 z 4 y 1
node 8201 27.908333 -2.333333 13.811; # support 8 wall 1 z 4 y 2
node 8202 28.425 -3.5 13.5; # support 8 wall 1 z 4 y 3
node 8300 29.458333 -1.166667 11.078; # support 8 wall 2 z 1 y 1
node 8301 28.941667 -2.333333 11.389; # support 8 wall 2 z 1 y 2
node 8400 29.458333 -1.166667 12.092667; # support 8 wall 2 z 2 y 1
node 8401 28.941667 -2.333333 12.196333; # support 8 wall 2 z 2 y 2
node 8500 29.458333 -1.166667 13.107333; # support 8 wall 2 z 3 y 1
node 8501 28.941667 -2.333333 13.003667; # support 8 wall 2 z 3 y 2
node 8600 29.458333 -1.166667 14.122; # support 8 wall 2 z 4 y 1
node 8601 28.941667 -2.333333 13.811; # support 8 wall 2 z 4 y 2
node 8700 42.691667 -1.166667 -14.122; # support 9 wall 1 z 1 y 1
node 8701 43.208333 -2.333333 -13.811; # support 9 wall 1 z 1 y 2
node 8702 43.725 -3.5 -13.5; # support 9 wall 1 z 1 y 3
node 8800 42.691667 -1.166667 -13.107333; # support 9 wall 1 z 2 y 1
node 8801 43.208333 -2.333333 -13.003667; # support 9 wall 1 z 2 y 2
node 8802 43.725 -3.5 -12.9; # support 9 wall 1 z 2 y 3
node 8900 42.691667 -1.166667 -12.092667; # support 9 wall 1 z 3 y 1
node 8901 43.208333 -2.333333 -12.196333; # support 9 wall 1 z 3 y 2
node 8902 43.725 -3.5 -12.3; # support 9 wall 1 z 3 y 3
node 9000 42.691667 -1.166667 -11.078; # support 9 wall 1 z 4 y 1
node 9001 43.208333 -2.333333 -11.389; # support 9 wall 1 z 4 y 2
node 9002 43.725 -3.5 -11.7; # support 9 wall 1 z 4 y 3
node 9100 44.758333 -1.166667 -14.122; # support 9 wall 2 z 1 y 1
node 9101 44.241667 -2.333333 -13.811; # support 9 wall 2 z 1 y 2
node 9200 44.758333 -1.166667 -13.107333; # support 9 wall 2 z 2 y 1
node 9201 44.241667 -2.333333 -13.003667; # support 9 wall 2 z 2 y 2
node 9300 44.758333 -1.166667 -12.092667; # support 9 wall 2 z 3 y 1
node 9301 44.241667 -2.333333 -12.196333; # support 9 wall 2 z 3 y 2
node 9400 44.758333 -1.166667 -11.078; # support 9 wall 2 z 4 y 1
node 9401 44.241667 -2.333333 -11.389; # support 9 wall 2 z 4 y 2
node 9500 42.691667 -1.166667 -5.722; # support 10 wall 1 z 1 y 1
node 9501 43.208333 -2.333333 -5.411; # support 10 wall 1 z 1 y 2
node 9502 43.725 -3.5 -5.1; # support 10 wall 1 z 1 y 3
node 9600 42.691667 -1.166667 -4.707333; # support 10 wall 1 z 2 y 1
node 9601 43.208333 -2.333333 -4.603667; # support 10 wall 1 z 2 y 2
node 9602 43.725 -3.5 -4.5; # support 10 wall 1 z 2 y 3
node 9700 42.691667 -1.166667 -3.692667; # support 10 wall 1 z 3 y 1
node 9701 43.208333 -2.333333 -3.796333; # support 10 wall 1 z 3 y 2
node 9702 43.725 -3.5 -3.9; # support 10 wall 1 z 3 y 3
node 9800 42.691667 -1.166667 -2.678; # support 10 wall 1 z 4 y 1
node 9801 43.208333 -2.333333 -2.989; # support 10 wall 1 z 4 y 2
node 9802 43.725 -3.5 -3.3; # support 10 wall 1 z 4 y 3
node 9900 44.758333 -1.166667 -5.722; # support 10 wall 2 z 1 y 1
node 9901 44.241667 -2.333333 -5.411; # support 10 wall 2 z 1 y 2
node 10000 44.758333 -1.166667 -4.707333; # support 10 wall 2 z 2 y 1
node 10001 44.241667 -2.333333 -4.603667; # support 10 wall 2 z 2 y 2
node 10100 44.758333 -1.166667 -3.692667; # support 10 wall 2 z 3 y 1
node 10101 44.241667 -2.333333 -3.796333; # support 10 wall 2 z 3 y 2
node 10200 44.758333 -1.166667 -2.678; # support 10 wall 2 z 4 y 1
node 10201 44.241667 -2.333333 -2.989; # support 10 wall 2 z 4 y 2
node 10300 42.691667 -1.166667 2.678; # support 11 wall 1 z 1 y 1
node 10301 43.208333 -2.333333 2.989; # support 11 wall 1 z 1 y 2
node 10302 43.725 -3.5 3.3; # support 11 wall 1 z 1 y 3
node 10400 42.691667 -1.166667 3.692667; # support 11 wall 1 z 2 y 1
node 10401 43.208333 -2.333333 3.796333; # support 11 wall 1 z 2 y 2
node 10402 43.725 -3.5 3.9; # support 11 wall 1 z 2 y 3
node 10500 42.691667 -1.166667 4.707333; # support 11 wall 1 z 3 y 1
node 10501 43.208333 -2.333333 4.603667; # support 11 wall 1 z 3 y 2
node 10502 43.725 -3.5 4.5; # support 11 wall 1 z 3 y 3
node 10600 42.691667 -1.166667 5.722; # support 11 wall 1 z 4 y 1
node 10601 43.208333 -2.333333 5.411; # support 11 wall 1 z 4 y 2
node 10602 43.725 -3.5 5.1; # support 11 wall 1 z 4 y 3
node 10700 44.758333 -1.166667 2.678; # support 11 wall 2 z 1 y 1
node 10701 44.241667 -2.333333 2.989; # support 11 wall 2 z 1 y 2
node 10800 44.758333 -1.166667 3.692667; # support 11 wall 2 z 2 y 1
node 10801 44.241667 -2.333333 3.796333; # support 11 wall 2 z 2 y 2
node 10900 44.758333 -1.166667 4.707333; # support 11 wall 2 z 3 y 1
node 10901 44.241667 -2.333333 4.603667; # support 11 wall 2 z 3 y 2
node 11000 44.758333 -1.166667 5.722; # support 11 wall 2 z 4 y 1
node 11001 44.241667 -2.333333 5.411; # support 11 wall 2 z 4 y 2
node 11100 42.691667 -1.166667 11.078; # support 12 wall 1 z 1 y 1
node 11101 43.208333 -2.333333 11.389; # support 12 wall 1 z 1 y 2
node 11102 43.725 -3.5 11.7; # support 12 wall 1 z 1 y 3
node 11200 42.691667 -1.166667 12.092667; # support 12 wall 1 z 2 y 1
node 11201 43.208333 -2.333333 12.196333; # support 12 wall 1 z 2 y 2
node 11202 43.725 -3.5 12.3; # support 12 wall 1 z 2 y 3
node 11300 42.691667 -1.166667 13.107333; # support 12 wall 1 z 3 y 1
node 11301 43.208333 -2.333333 13.003667; # support 12 wall 1 z 3 y 2
node 11302 43.725 -3.5 12.9; # support 12 wall 1 z 3 y 3
node 11400 42.691667 -1.166667 14.122; # support 12 wall 1 z 4 y 1
node 11401 43.208333 -2.333333 13.811; # support 12 wall 1 z 4 y 2
node 11402 43.725 -3.5 13.5; # support 12 wall 1 z 4 y 3
node 11500 44.758333 -1.166667 11.078; # support 12 wall 2 z 1 y 1
node 11501 44.241667 -2.333333 11.389; # support 12 wall 2 z 1 y 2
node 11600 44.758333 -1.166667 12.092667; # support 12 wall 2 z 2 y 1
node 11601 44.241667 -2.333333 12.196333; # support 12 wall 2 z 2 y 2
node 11700 44.758333 -1.166667 13.107333; # support 12 wall 2 z 3 y 1
node 11701 44.241667 -2.333333 13.003667; # support 12 wall 2 z 3 y 2
node 11800 44.758333 -1.166667 14.122; # support 12 wall 2 z 4 y 1
node 11801 44.241667 -2.333333 13.811; # support 12 wall 2 z 4 y 2
node 11900 57.991667 -1.166667 -14.122; # support 13 wall 1 z 1 y 1
node 11901 58.508333 -2.333333 -13.811; # support 13 wall 1 z 1 y 2
node 11902 59.025 -3.5 -13.5; # support 13 wall 1 z 1 y 3
node 12000 57.991667 -1.166667 -13.107333; # support 13 wall 1 z 2 y 1
node 12001 58.508333 -2.333333 -13.003667; # support 13 wall 1 z 2 y 2
node 12002 59.025 -3.5 -12.9; # support 13 wall 1 z 2 y 3
node 12100 57.991667 -1.166667 -12.092667; # support 13 wall 1 z 3 y 1
node 12101 58.508333 -2.333333 -12.196333; # support 13 wall 1 z 3 y 2
node 12102 59.025 -3.5 -12.3; # support 13 wall 1 z 3 y 3
node 12200 57.991667 -1.166667 -11.078; # support 13 wall 1 z 4 y 1
node 12201 58.508333 -2.333333 -11.389; # support 13 wall 1 z 4 y 2
node 12202 59.025 -3.5 -11.7; # support 13 wall 1 z 4 y 3
node 12300 60.058333 -1.166667 -14.122; # support 13 wall 2 z 1 y 1
node 12301 59.541667 -2.333333 -13.811; # support 13 wall 2 z 1 y 2
node 12400 60.058333 -1.166667 -13.107333; # support 13 wall 2 z 2 y 1
node 12401 59.541667 -2.333333 -13.003667; # support 13 wall 2 z 2 y 2
node 12500 60.058333 -1.166667 -12.092667; # support 13 wall 2 z 3 y 1
node 12501 59.541667 -2.333333 -12.196333; # support 13 wall 2 z 3 y 2
node 12600 60.058333 -1.166667 -11.078; # support 13 wall 2 z 4 y 1
node 12601 59.541667 -2.333333 -11.389; # support 13 wall 2 z 4 y 2
node 12700 57.991667 -1.166667 -5.722; # support 14 wall 1 z 1 y 1
node 12701 58.508333 -2.333333 -5.411; # support 14 wall 1 z 1 y 2
node 12702 59.025 -3.5 -5.1; # support 14 wall 1 z 1 y 3
node 12800 57.991667 -1.166667 -4.707333; # support 14 wall 1 z 2 y 1
node 12801 58.508333 -2.333333 -4.603667; # support 14 wall 1 z 2 y 2
node 12802 59.025 -3.5 -4.5; # support 14 wall 1 z 2 y 3
node 12900 57.991667 -1.166667 -3.692667; # support 14 wall 1 z 3 y 1
node 12901 58.508333 -2.333333 -3.796333; # support 14 wall 1 z 3 y 2
node 12902 59.025 -3.5 -3.9; # support 14 wall 1 z 3 y 3
node 13000 57.991667 -1.166667 -2.678; # support 14 wall 1 z 4 y 1
node 13001 58.508333 -2.333333 -2.989; # support 14 wall 1 z 4 y 2
node 13002 59.025 -3.5 -3.3; # support 14 wall 1 z 4 y 3
node 13100 60.058333 -1.166667 -5.722; # support 14 wall 2 z 1 y 1
node 13101 59.541667 -2.333333 -5.411; # support 14 wall 2 z 1 y 2
node 13200 60.058333 -1.166667 -4.707333; # support 14 wall 2 z 2 y 1
node 13201 59.541667 -2.333333 -4.603667; # support 14 wall 2 z 2 y 2
node 13300 60.058333 -1.166667 -3.692667; # support 14 wall 2 z 3 y 1
node 13301 59.541667 -2.333333 -3.796333; # support 14 wall 2 z 3 y 2
node 13400 60.058333 -1.166667 -2.678; # support 14 wall 2 z 4 y 1
node 13401 59.541667 -2.333333 -2.989; # support 14 wall 2 z 4 y 2
node 13500 57.991667 -1.166667 2.678; # support 15 wall 1 z 1 y 1
node 13501 58.508333 -2.333333 2.989; # support 15 wall 1 z 1 y 2
node 13502 59.025 -3.5 3.3; # support 15 wall 1 z 1 y 3
node 13600 57.991667 -1.166667 3.692667; # support 15 wall 1 z 2 y 1
node 13601 58.508333 -2.333333 3.796333; # support 15 wall 1 z 2 y 2
node 13602 59.025 -3.5 3.9; # support 15 wall 1 z 2 y 3
node 13700 57.991667 -1.166667 4.707333; # support 15 wall 1 z 3 y 1
node 13701 58.508333 -2.333333 4.603667; # support 15 wall 1 z 3 y 2
node 13702 59.025 -3.5 4.5; # support 15 wall 1 z 3 y 3
node 13800 57.991667 -1.166667 5.722; # support 15 wall 1 z 4 y 1
node 13801 58.508333 -2.333333 5.411; # support 15 wall 1 z 4 y 2
node 13802 59.025 -3.5 5.1; # support 15 wall 1 z 4 y 3
node 13900 60.058333 -1.166667 2.678; # support 15 wall 2 z 1 y 1
node 13901 59.541667 -2.333333 2.989; # support 15 wall 2 z 1 y 2
node 14000 60.058333 -1.166667 3.692667; # support 15 wall 2 z 2 y 1
node 14001 59.541667 -2.333333 3.796333; # support 15 wall 2 z 2 y 2
node 14100 60.058333 -1.166667 4.707333; # support 15 wall 2 z 3 y 1
node 14101 59.541667 -2.333333 4.603667; # support 15 wall 2 z 3 y 2
node 14200 60.058333 -1.166667 5.722; # support 15 wall 2 z 4 y 1
node 14201 59.541667 -2.333333 5.411; # support 15 wall 2 z 4 y 2
node 14300 57.991667 -1.166667 11.078; # support 16 wall 1 z 1 y 1
node 14301 58.508333 -2.333333 11.389; # support 16 wall 1 z 1 y 2
node 14302 59.025 -3.5 11.7; # support 16 wall 1 z 1 y 3
node 14400 57.991667 -1.166667 12.092667; # support 16 wall 1 z 2 y 1
node 14401 58.508333 -2.333333 12.196333; # support 16 wall 1 z 2 y 2
node 14402 59.025 -3.5 12.3; # support 16 wall 1 z 2 y 3
node 14500 57.991667 -1.166667 13.107333; # support 16 wall 1 z 3 y 1
node 14501 58.508333 -2.333333 13.003667; # support 16 wall 1 z 3 y 2
node 14502 59.025 -3.5 12.9; # support 16 wall 1 z 3 y 3
node 14600 57.991667 -1.166667 14.122; # support 16 wall 1 z 4 y 1
node 14601 58.508333 -2.333333 13.811; # support 16 wall 1 z 4 y 2
node 14602 59.025 -3.5 13.5; # support 16 wall 1 z 4 y 3
node 14700 60.058333 -1.166667 11.078; # support 16 wall 2 z 1 y 1
node 14701 59.541667 -2.333333 11.389; # support 16 wall 2 z 1 y 2
node 14800 60.058333 -1.166667 12.092667; # support 16 wall 2 z 2 y 1
node 14801 59.541667 -2.333333 12.196333; # support 16 wall 2 z 2 y 2
node 14900 60.058333 -1.166667 13.107333; # support 16 wall 2 z 3 y 1
node 14901 59.541667 -2.333333 13.003667; # support 16 wall 2 z 3 y 2
node 15000 60.058333 -1.166667 14.122; # support 16 wall 2 z 4 y 1
node 15001 59.541667 -2.333333 13.811; # support 16 wall 2 z 4 y 2
node 15100 73.291667 -1.166667 -14.122; # support 17 wall 1 z 1 y 1
node 15101 73.808333 -2.333333 -13.811; # support 17 wall 1 z 1 y 2
node 15102 74.325 -3.5 -13.5; # support 17 wall 1 z 1 y 3
node 15200 73.291667 -1.166667 -13.107333; # support 17 wall 1 z 2 y 1
node 15201 73.808333 -2.333333 -13.003667; # support 17 wall 1 z 2 y 2
node 15202 74.325 -3.5 -12.9; # support 17 wall 1 z 2 y 3
node 15300 73.291667 -1.166667 -12.092667; # support 17 wall 1 z 3 y 1
node 15301 73.808333 -2.333333 -12.196333; # support 17 wall 1 z 3 y 2
node 15302 74.325 -3.5 -12.3; # support 17 wall 1 z 3 y 3
node 15400 73.291667 -1.166667 -11.078; # support 17 wall 1 z 4 y 1
node 15401 73.808333 -2.333333 -11.389; # support 17 wall 1 z 4 y 2
node 15402 74.325 -3.5 -11.7; # support 17 wall 1 z 4 y 3
node 15500 75.358333 -1.166667 -14.122; # support 17 wall 2 z 1 y 1
node 15501 74.841667 -2.333333 -13.811; # support 17 wall 2 z 1 y 2
node 15600 75.358333 -1.166667 -13.107333; # support 17 wall 2 z 2 y 1
node 15601 74.841667 -2.333333 -13.003667; # support 17 wall 2 z 2 y 2
node 15700 75.358333 -1.166667 -12.092667; # support 17 wall 2 z 3 y 1
node 15701 74.841667 -2.333333 -12.196333; # support 17 wall 2 z 3 y 2
node 15800 75.358333 -1.166667 -11.078; # support 17 wall 2 z 4 y 1
node 15801 74.841667 -2.333333 -11.389; # support 17 wall 2 z 4 y 2
node 15900 73.291667 -1.166667 -5.722; # support 18 wall 1 z 1 y 1
node 15901 73.808333 -2.333333 -5.411; # support 18 wall 1 z 1 y 2
node 15902 74.325 -3.5 -5.1; # support 18 wall 1 z 1 y 3
node 16000 73.291667 -1.166667 -4.707333; # support 18 wall 1 z 2 y 1
node 16001 73.808333 -2.333333 -4.603667; # support 18 wall 1 z 2 y 2
node 16002 74.325 -3.5 -4.5; # support 18 wall 1 z 2 y 3
node 16100 73.291667 -1.166667 -3.692667; # support 18 wall 1 z 3 y 1
node 16101 73.808333 -2.333333 -3.796333; # support 18 wall 1 z 3 y 2
node 16102 74.325 -3.5 -3.9; # support 18 wall 1 z 3 y 3
node 16200 73.291667 -1.166667 -2.678; # support 18 wall 1 z 4 y 1
node 16201 73.808333 -2.333333 -2.989; # support 18 wall 1 z 4 y 2
node 16202 74.325 -3.5 -3.3; # support 18 wall 1 z 4 y 3
node 16300 75.358333 -1.166667 -5.722; # support 18 wall 2 z 1 y 1
node 16301 74.841667 -2.333333 -5.411; # support 18 wall 2 z 1 y 2
node 16400 75.358333 -1.166667 -4.707333; # support 18 wall 2 z 2 y 1
node 16401 74.841667 -2.333333 -4.603667; # support 18 wall 2 z 2 y 2
node 16500 75.358333 -1.166667 -3.692667; # support 18 wall 2 z 3 y 1
node 16501 74.841667 -2.333333 -3.796333; # support 18 wall 2 z 3 y 2
node 16600 75.358333 -1.166667 -2.678; # support 18 wall 2 z 4 y 1
node 16601 74.841667 -2.333333 -2.989; # support 18 wall 2 z 4 y 2
node 16700 73.291667 -1.166667 2.678; # support 19 wall 1 z 1 y 1
node 16701 73.808333 -2.333333 2.989; # support 19 wall 1 z 1 y 2
node 16702 74.325 -3.5 3.3; # support 19 wall 1 z 1 y 3
node 16800 73.291667 -1.166667 3.692667; # support 19 wall 1 z 2 y 1
node 16801 73.808333 -2.333333 3.796333; # support 19 wall 1 z 2 y 2
node 16802 74.325 -3.5 3.9; # support 19 wall 1 z 2 y 3
node 16900 73.291667 -1.166667 4.707333; # support 19 wall 1 z 3 y 1
node 16901 73.808333 -2.333333 4.603667; # support 19 wall 1 z 3 y 2
node 16902 74.325 -3.5 4.5; # support 19 wall 1 z 3 y 3
node 17000 73.291667 -1.166667 5.722; # support 19 wall 1 z 4 y 1
node 17001 73.808333 -2.333333 5.411; # support 19 wall 1 z 4 y 2
node 17002 74.325 -3.5 5.1; # support 19 wall 1 z 4 y 3
node 17100 75.358333 -1.166667 2.678; # support 19 wall 2 z 1 y 1
node 17101 74.841667 -2.333333 2.989; # support 19 wall 2 z 1 y 2
node 17200 75.358333 -1.166667 3.692667; # support 19 wall 2 z 2 y 1
node 17201 74.841667 -2.333333 3.796333; # support 19 wall 2 z 2 y 2
node 17300 75.358333 -1.166667 4.707333; # support 19 wall 2 z 3 y 1
node 17301 74.841667 -2.333333 4.603667; # support 19 wall 2 z 3 y 2
node 17400 75.358333 -1.166667 5.722; # support 19 wall 2 z 4 y 1
node 17401 74.841667 -2.333333 5.411; # support 19 wall 2 z 4 y 2
node 17500 73.291667 -1.166667 11.078; # support 20 wall 1 z 1 y 1
node 17501 73.808333 -2.333333 11.389; # support 20 wall 1 z 1 y 2
node 17502 74.325 -3.5 11.7; # support 20 wall 1 z 1 y 3
node 17600 73.291667 -1.166667 12.092667; # support 20 wall 1 z 2 y 1
node 17601 73.808333 -2.333333 12.196333; # support 20 wall 1 z 2 y 2
node 17602 74.325 -3.5 12.3; # support 20 wall 1 z 2 y 3
node 17700 73.291667 -1.166667 13.107333; # support 20 wall 1 z 3 y 1
node 17701 73.808333 -2.333333 13.003667; # support 20 wall 1 z 3 y 2
node 17702 74.325 -3.5 12.9; # support 20 wall 1 z 3 y 3
node 17800 73.291667 -1.166667 14.122; # support 20 wall 1 z 4 y 1
node 17801 73.808333 -2.333333 13.811; # support 20 wall 1 z 4 y 2
node 17802 74.325 -3.5 13.5; # support 20 wall 1 z 4 y 3
node 17900 75.358333 -1.166667 11.078; # support 20 wall 2 z 1 y 1
node 17901 74.841667 -2.333333 11.389; # support 20 wall 2 z 1 y 2
node 18000 75.358333 -1.166667 12.092667; # support 20 wall 2 z 2 y 1
node 18001 74.841667 -2.333333 12.196333; # support 20 wall 2 z 2 y 2
node 18100 75.358333 -1.166667 13.107333; # support 20 wall 2 z 3 y 1
node 18101 74.841667 -2.333333 13.003667; # support 20 wall 2 z 3 y 2
node 18200 75.358333 -1.166667 14.122; # support 20 wall 2 z 4 y 1
node 18201 74.841667 -2.333333 13.811; # support 20 wall 2 z 4 y 2
node 18300 88.591667 -1.166667 -14.122; # support 21 wall 1 z 1 y 1
node 18301 89.108333 -2.333333 -13.811; # support 21 wall 1 z 1 y 2
node 18302 89.625 -3.5 -13.5; # support 21 wall 1 z 1 y 3
node 18400 88.591667 -1.166667 -13.107333; # support 21 wall 1 z 2 y 1
node 18401 89.108333 -2.333333 -13.003667; # support 21 wall 1 z 2 y 2
node 18402 89.625 -3.5 -12.9; # support 21 wall 1 z 2 y 3
node 18500 88.591667 -1.166667 -12.092667; # support 21 wall 1 z 3 y 1
node 18501 89.108333 -2.333333 -12.196333; # support 21 wall 1 z 3 y 2
node 18502 89.625 -3.5 -12.3; # support 21 wall 1 z 3 y 3
node 18600 88.591667 -1.166667 -11.078; # support 21 wall 1 z 4 y 1
node 18601 89.108333 -2.333333 -11.389; # support 21 wall 1 z 4 y 2
node 18602 89.625 -3.5 -11.7; # support 21 wall 1 z 4 y 3
node 18700 90.658333 -1.166667 -14.122; # support 21 wall 2 z 1 y 1
node 18701 90.141667 -2.333333 -13.811; # support 21 wall 2 z 1 y 2
node 18800 90.658333 -1.166667 -13.107333; # support 21 wall 2 z 2 y 1
node 18801 90.141667 -2.333333 -13.003667; # support 21 wall 2 z 2 y 2
node 18900 90.658333 -1.166667 -12.092667; # support 21 wall 2 z 3 y 1
node 18901 90.141667 -2.333333 -12.196333; # support 21 wall 2 z 3 y 2
node 19000 90.658333 -1.166667 -11.078; # support 21 wall 2 z 4 y 1
node 19001 90.141667 -2.333333 -11.389; # support 21 wall 2 z 4 y 2
node 19100 88.591667 -1.166667 -5.722; # support 22 wall 1 z 1 y 1
node 19101 89.108333 -2.333333 -5.411; # support 22 wall 1 z 1 y 2
node 19102 89.625 -3.5 -5.1; # support 22 wall 1 z 1 y 3
node 19200 88.591667 -1.166667 -4.707333; # support 22 wall 1 z 2 y 1
node 19201 89.108333 -2.333333 -4.603667; # support 22 wall 1 z 2 y 2
node 19202 89.625 -3.5 -4.5; # support 22 wall 1 z 2 y 3
node 19300 88.591667 -1.166667 -3.692667; # support 22 wall 1 z 3 y 1
node 19301 89.108333 -2.333333 -3.796333; # support 22 wall 1 z 3 y 2
node 19302 89.625 -3.5 -3.9; # support 22 wall 1 z 3 y 3
node 19400 88.591667 -1.166667 -2.678; # support 22 wall 1 z 4 y 1
node 19401 89.108333 -2.333333 -2.989; # support 22 wall 1 z 4 y 2
node 19402 89.625 -3.5 -3.3; # support 22 wall 1 z 4 y 3
node 19500 90.658333 -1.166667 -5.722; # support 22 wall 2 z 1 y 1
node 19501 90.141667 -2.333333 -5.411; # support 22 wall 2 z 1 y 2
node 19600 90.658333 -1.166667 -4.707333; # support 22 wall 2 z 2 y 1
node 19601 90.141667 -2.333333 -4.603667; # support 22 wall 2 z 2 y 2
node 19700 90.658333 -1.166667 -3.692667; # support 22 wall 2 z 3 y 1
node 19701 90.141667 -2.333333 -3.796333; # support 22 wall 2 z 3 y 2
node 19800 90.658333 -1.166667 -2.678; # support 22 wall 2 z 4 y 1
node 19801 90.141667 -2.333333 -2.989; # support 22 wall 2 z 4 y 2
node 19900 88.591667 -1.166667 2.678; # support 23 wall 1 z 1 y 1
node 19901 89.108333 -2.333333 2.989; # support 23 wall 1 z 1 y 2
node 19902 89.625 -3.5 3.3; # support 23 wall 1 z 1 y 3
node 20000 88.591667 -1.166667 3.692667; # support 23 wall 1 z 2 y 1
node 20001 89.108333 -2.333333 3.796333; # support 23 wall 1 z 2 y 2
node 20002 89.625 -3.5 3.9; # support 23 wall 1 z 2 y 3
node 20100 88.591667 -1.166667 4.707333; # support 23 wall 1 z 3 y 1
node 20101 89.108333 -2.333333 4.603667; # support 23 wall 1 z 3 y 2
node 20102 89.625 -3.5 4.5; # support 23 wall 1 z 3 y 3
node 20200 88.591667 -1.166667 5.722; # support 23 wall 1 z 4 y 1
node 20201 89.108333 -2.333333 5.411; # support 23 wall 1 z 4 y 2
node 20202 89.625 -3.5 5.1; # support 23 wall 1 z 4 y 3
node 20300 90.658333 -1.166667 2.678; # support 23 wall 2 z 1 y 1
node 20301 90.141667 -2.333333 2.989; # support 23 wall 2 z 1 y 2
node 20400 90.658333 -1.166667 3.692667; # support 23 wall 2 z 2 y 1
node 20401 90.141667 -2.333333 3.796333; # support 23 wall 2 z 2 y 2
node 20500 90.658333 -1.166667 4.707333; # support 23 wall 2 z 3 y 1
node 20501 90.141667 -2.333333 4.603667; # support 23 wall 2 z 3 y 2
node 20600 90.658333 -1.166667 5.722; # support 23 wall 2 z 4 y 1
node 20601 90.141667 -2.333333 5.411; # support 23 wall 2 z 4 y 2
node 20700 88.591667 -1.166667 11.078; # support 24 wall 1 z 1 y 1
node 20701 89.108333 -2.333333 11.389; # support 24 wall 1 z 1 y 2
node 20702 89.625 -3.5 11.7; # support 24 wall 1 z 1 y 3
node 20800 88.591667 -1.166667 12.092667; # support 24 wall 1 z 2 y 1
node 20801 89.108333 -2.333333 12.196333; # support 24 wall 1 z 2 y 2
node 20802 89.625 -3.5 12.3; # support 24 wall 1 z 2 y 3
node 20900 88.591667 -1.166667 13.107333; # support 24 wall 1 z 3 y 1
node 20901 89.108333 -2.333333 13.003667; # support 24 wall 1 z 3 y 2
node 20902 89.625 -3.5 12.9; # support 24 wall 1 z 3 y 3
node 21000 88.591667 -1.166667 14.122; # support 24 wall 1 z 4 y 1
node 21001 89.108333 -2.333333 13.811; # support 24 wall 1 z 4 y 2
node 21002 89.625 -3.5 13.5; # support 24 wall 1 z 4 y 3
node 21100 90.658333 -1.166667 11.078; # support 24 wall 2 z 1 y 1
node 21101 90.141667 -2.333333 11.389; # support 24 wall 2 z 1 y 2
node 21200 90.658333 -1.166667 12.092667; # support 24 wall 2 z 2 y 1
node 21201 90.141667 -2.333333 12.196333; # support 24 wall 2 z 2 y 2
node 21300 90.658333 -1.166667 13.107333; # support 24 wall 2 z 3 y 1
node 21301 90.141667 -2.333333 13.003667; # support 24 wall 2 z 3 y 2
node 21400 90.658333 -1.166667 14.122; # support 24 wall 2 z 4 y 1
node 21401 90.141667 -2.333333 13.811; # support 24 wall 2 z 4 y 2
# End support nodes

# fix nodeTag x y z rx ry rz
# Begin fixed deck nodes
fix 100 1 1 1 0 0 0
fix 117 1 1 1 0 0 0
fix 200 1 1 1 0 0 0
fix 217 1 1 1 0 0 0
fix 300 1 1 1 0 0 0
fix 317 1 1 1 0 0 0
fix 400 1 1 1 0 0 0
fix 417 1 1 1 0 0 0
fix 500 1 1 1 0 0 0
fix 517 1 1 1 0 0 0
fix 600 1 1 1 0 0 0
fix 617 1 1 1 0 0 0
fix 700 1 1 1 0 0 0
fix 717 1 1 1 0 0 0
fix 800 1 1 1 0 0 0
fix 817 1 1 1 0 0 0
fix 900 1 1 1 0 0 0
fix 917 1 1 1 0 0 0
fix 1000 1 1 1 0 0 0
fix 1017 1 1 1 0 0 0
fix 1100 1 1 1 0 0 0
fix 1117 1 1 1 0 0 0
fix 1200 1 1 1 0 0 0
fix 1217 1 1 1 0 0 0
fix 1300 1 1 1 0 0 0
fix 1317 1 1 1 0 0 0
fix 1400 1 1 1 0 0 0
fix 1417 1 1 1 0 0 0
fix 1500 1 1 1 0 0 0
fix 1517 1 1 1 0 0 0
fix 1600 1 1 1 0 0 0
fix 1617 1 1 1 0 0 0
fix 1700 1 1 1 0 0 0
fix 1717 1 1 1 0 0 0
fix 1800 1 1 1 0 0 0
fix 1817 1 1 1 0 0 0
fix 1900 1 1 1 0 0 0
fix 1917 1 1 1 0 0 0
fix 2000 1 1 1 0 0 0
fix 2017 1 1 1 0 0 0
fix 2100 1 1 1 0 0 0
fix 2117 1 1 1 0 0 0
fix 2200 1 1 1 0 0 0
fix 2217 1 1 1 0 0 0
# End fixed deck nodes

# fix nodeTag x y z rx ry rz
# Begin fixed support nodes
fix 2302 1 1 1 0 0 0; # support 1 z 1
fix 2402 1 1 1 0 0 0; # support 1 z 2
fix 2502 1 1 1 0 0 0; # support 1 z 3
fix 2602 1 1 1 0 0 0; # support 1 z 4
fix 3102 1 1 1 0 0 0; # support 2 z 1
fix 3202 1 1 1 0 0 0; # support 2 z 2
fix 3302 1 1 1 0 0 0; # support 2 z 3
fix 3402 1 1 1 0 0 0; # support 2 z 4
fix 3902 1 1 1 0 0 0; # support 3 z 1
fix 4002 1 1 1 0 0 0; # support 3 z 2
fix 4102 1 1 1 0 0 0; # support 3 z 3
fix 4202 1 1 1 0 0 0; # support 3 z 4
fix 4702 1 1 1 0 0 0; # support 4 z 1
fix 4802 1 1 1 0 0 0; # support 4 z 2
fix 4902 1 1 1 0 0 0; # support 4 z 3
fix 5002 1 1 1 0 0 0; # support 4 z 4
fix 5502 1 1 1 0 0 0; # support 5 z 1
fix 5602 1 1 1 0 0 0; # support 5 z 2
fix 5702 1 1 1 0 0 0; # support 5 z 3
fix 5802 1 1 1 0 0 0; # support 5 z 4
fix 6302 1 1 1 0 0 0; # support 6 z 1
fix 6402 1 1 1 0 0 0; # support 6 z 2
fix 6502 1 1 1 0 0 0; # support 6 z 3
fix 6602 1 1 1 0 0 0; # support 6 z 4
fix 7102 1 1 1 0 0 0; # support 7 z 1
fix 7202 1 1 1 0 0 0; # support 7 z 2
fix 7302 1 1 1 0 0 0; # support 7 z 3
fix 7402 1 1 1 0 0 0; # support 7 z 4
fix 7902 1 1 1 0 0 0; # support 8 z 1
fix 8002 1 1 1 0 0 0; # support 8 z 2
fix 8102 1 1 1 0 0 0; # support 8 z 3
fix 8202 1 1 1 0 0 0; # support 8 z 4
fix 8702 1 1 1 0 0 0; # support 9 z 1
fix 8802 1 1 1 0 0 0; # support 9 z 2
fix 8902 1 1 1 0 0 0; # support 9 z 3
fix 9002 1 1 1 0 0 0; # support 9 z 4
fix 9502 1 1 1 0 0 0; # support 10 z 1
fix 9602 1 1 1 0 0 0; # support 10 z 2
fix 9702 1 1 1 0 0 0; # support 10 z 3
fix 9802 1 1 1 0 0 0; # support 10 z 4
fix 10302 1 1 1 0 0 0; # support 11 z 1
fix 10402 1 1 1 0 0 0; # support 11 z 2
fix 10502 1 1 1 0 0 0; # support 11 z 3
fix 10602 1 1 1 0 0 0; # support 11 z 4
fix 11102 1 1 1 0 0 0; # support 12 z 1
fix 11202 1 1 1 0 0 0; # support 12 z 2
fix 11302 1 1 1 0 0 0; # support 12 z 3
fix 11402 1 1 1 0 0 0; # support 12 z 4
fix 11902 1 1 1 0 0 0; # support 13 z 1
fix 12002 1 1 1 0 0 0; # support 13 z 2
fix 12102 1 1 1 0 0 0; # support 13 z 3
fix 12202 1 1 1 0 0 0; # support 13 z 4
fix 12702 1 1 1 0 0 0; # support 14 z 1
fix 12802 1 1 1 0 0 0; # support 14 z 2
fix 12902 1 1 1 0 0 0; # support 14 z 3
fix 13002 1 1 1 0 0 0; # support 14 z 4
fix 13502 1 1 1 0 0 0; # support 15 z 1
fix 13602 1 1 1 0 0 0; # support 15 z 2
fix 13702 1 1 1 0 0 0; # support 15 z 3
fix 13802 1 1 1 0 0 0; # support 15 z 4
fix 14302 1 1 1 0 0 0; # support 16 z 1
fix 14402 1 1 1 0 0 0; # support 16 z 2
fix 14502 1 1 1 0 0 0; # support 16 z 3
fix 14602 1 1 1 0 0 0; # support 16 z 4
fix 15102 1 1 1 0 0 0; # support 17 z 1
fix 15202 1 1 1 0 0 0; # support 17 z 2
fix 15302 1 1 1 0 0 0; # support 17 z 3
fix 15402 1 1 1 0 0 0; # support 17 z 4
fix 15902 1 1 1 0 0 0; # support 18 z 1
fix 16002 1 1 1 0 0 0; # support 18 z 2
fix 16102 1 1 1 0 0 0; # support 18 z 3
fix 16202 1 1 1 0 0 0; # support 18 z 4
fix 16702 1 1 1 0 0 0; # support 19 z 1
fix 16802 1 1 1 0 0 0; # support 19 z 2
fix 16902 1 1 1 0 0 0; # support 19 z 3
fix 17002 1 1 1 0 0 0; # support 19 z 4
fix 17502 1 1 1 0 0 0; # support 20 z 1
fix 17602 1 1 1 0 0 0; # support 20 z 2
fix 17702 1 1 1 0 0 0; # support 20 z 3
fix 17802 1 1 1 0 0 0; # support 20 z 4
fix 18302 1 1 1 0 0 0; # support 21 z 1
fix 18402 1 1 1 0 0 0; # support 21 z 2
fix 18502 1 1 1 0 0 0; # support 21 z 3
fix 18602 1 1 1 0 0 0; # support 21 z 4
fix 19102 1 1 1 0 0 0; # support 22 z 1
fix 19202 1 1 1 0 0 0; # support 22 z 2
fix 19302 1 1 1 0 0 0; # support 22 z 3
fix 19402 1 1 1 0 0 0; # support 22 z 4
fix 19902 1 1 1 0 0 0; # support 23 z 1
fix 20002 1 1 1 0 0 0; # support 23 z 2
fix 20102 1 1 1 0 0 0; # support 23 z 3
fix 20202 1 1 1 0 0 0; # support 23 z 4
fix 20702 1 1 1 0 0 0; # support 24 z 1
fix 20802 1 1 1 0 0 0; # support 24 z 2
fix 20902 1 1 1 0 0 0; # support 24 z 3
fix 21002 1 1 1 0 0 0; # support 24 z 4
# End fixed support nodes

# section ElasticMembranePlateSection secTag youngs_modulus poisson_ratio depth mass_density
# Begin sections
section ElasticMembranePlateSection 0 38400 0.2 0.75 0.002724
# End sections

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin deck elements
element ShellMITC4 1 100 101 201 200 0
element ShellMITC4 2 101 102 202 201 0
element ShellMITC4 3 102 103 203 202 0
element ShellMITC4 4 103 104 204 203 0
element ShellMITC4 5 104 105 205 204 0
element ShellMITC4 6 105 106 206 205 0
element ShellMITC4 7 106 107 207 206 0
element ShellMITC4 8 107 108 208 207 0
element ShellMITC4 9 108 109 209 208 0
element ShellMITC4 10 109 110 210 209 0
element ShellMITC4 11 110 111 211 210 0
element ShellMITC4 12 111 112 212 211 0
element ShellMITC4 13 112 113 213 212 0
element ShellMITC4 14 113 114 214 213 0
element ShellMITC4 15 114 115 215 214 0
element ShellMITC4 16 115 116 216 215 0
element ShellMITC4 17 116 117 217 216 0
element ShellMITC4 100 200 201 301 300 0
element ShellMITC4 101 201 202 302 301 0
element ShellMITC4 102 202 203 303 302 0
element ShellMITC4 103 203 204 304 303 0
element ShellMITC4 104 204 205 305 304 0
element ShellMITC4 105 205 206 306 305 0
element ShellMITC4 106 206 207 307 306 0
element ShellMITC4 107 207 208 308 307 0
element ShellMITC4 108 208 209 309 308 0
element ShellMITC4 109 209 210 310 309 0
element ShellMITC4 110 210 211 311 310 0
element ShellMITC4 111 211 212 312 311 0
element ShellMITC4 112 212 213 313 312 0
element ShellMITC4 113 213 214 314 313 0
element ShellMITC4 114 214 215 315 314 0
element ShellMITC4 115 215 216 316 315 0
element ShellMITC4 116 216 217 317 316 0
element ShellMITC4 200 300 301 401 400 0
element ShellMITC4 201 301 302 402 401 0
element ShellMITC4 202 302 303 403 402 0
element ShellMITC4 203 303 304 404 403 0
element ShellMITC4 204 304 305 405 404 0
element ShellMITC4 205 305 306 406 405 0
element ShellMITC4 206 306 307 407 406 0
element ShellMITC4 207 307 308 408 407 0
element ShellMITC4 208 308 309 409 408 0
element ShellMITC4 209 309 310 410 409 0
element ShellMITC4 210 310 311 411 410 0
element ShellMITC4 211 311 312 412 411 0
element ShellMITC4 212 312 313 413 412 0
element ShellMITC4 213 313 314 414 413 0
element ShellMITC4 214 314 315 415 414 0
element ShellMITC4 215 315 316 416 415 0
element ShellMITC4 216 316 317 417 416 0
element ShellMITC4 300 400 401 501 500 0
element ShellMITC4 301 401 402 502 501 0
element ShellMITC4 302 402 403 503 502 0
element ShellMITC4 303 403 404 504 503 0
element ShellMITC4 304 404 405 505 504 0
element ShellMITC4 305 405 406 506 505 0
element ShellMITC4 306 406 407 507 506 0
element ShellMITC4 307 407 408 508 507 0
element ShellMITC4 308 408 409 509 508 0
element ShellMITC4 309 409 410 510 509 0
element ShellMITC4 310 410 411 511 510 0
element ShellMITC4 311 411 412 512 511 0
element ShellMITC4 312 412 413 513 512 0
element ShellMITC4 313 413 414 514 513 0
element ShellMITC4 314 414 415 515 514 0
element ShellMITC4 315 415 416 516 515 0
element ShellMITC4 316 416 417 517 516 0
element ShellMITC4 400 500 501 601 600 0
element ShellMITC4 401 501 502 602 601 0
element ShellMITC4 402 502 503 603 602 0
element ShellMITC4 403 503 504 604 603 0
element ShellMITC4 404 504 505 605 604 0
element ShellMITC4 405 505 506 606 605 0
element ShellMITC4 406 506 507 607 606 0
element ShellMITC4 407 507 508 608 607 0
element ShellMITC4 408 508 509 609 608 0
element ShellMITC4 409 509 510 610 609 0
element ShellMITC4 410 510 511 611 610 0
element ShellMITC4 411 511 512 612 611 0
element ShellMITC4 412 512 513 613 612 0
element ShellMITC4 413 513 514 614 613 0
element ShellMITC4 414 514 515 615 614 0
element ShellMITC4 415 515 516 616 615 0
element ShellMITC4 416 516 517 617 616 0
element ShellMITC4 500 600 601 701 700 0
element ShellMITC4 501 601 602 702 701 0
element ShellMITC4 502 602 603 703 702 0
element ShellMITC4 503 603 604 704 703 0
element ShellMITC4 504 604 605 705 704 0
element ShellMITC4 505 605 606 706 705 0
element ShellMITC4 506 606 607 707 706 0
element ShellMITC4 507 607 608 708 707 0
element ShellMITC4 508 608 609 709 708 0
element ShellMITC4 509 609 610 710 709 0
element ShellMITC4 510 610 611 711 710 0
element ShellMITC4 511 611 612 712 711 0
element ShellMITC4 512 612 613 713 712 0
element ShellMITC4 513 613 614 714 713 0
element ShellMITC4 514 614 615 715 714 0
element ShellMITC4 515 615 616 716 715 0
element ShellMITC4 516 616 617 717 716 0
element ShellMITC4 600 700 701 801 800 0
element ShellMITC4 601 701 702 802 801 0
element ShellMITC4 602 702 703 803 802 0
element ShellMITC4 603 703 704 804 803 0
element ShellMITC4 604 704 705 805 804 0
element ShellMITC4 605 705 706 806 805 0
element ShellMITC4 606 706 707 807 806 0
element ShellMITC4 607 707 708 808 807 0
element ShellMITC4 608 708 709 809 808 0
element ShellMITC4 609 709 710 810 809 0
element ShellMITC4 610 710 711 811 810 0
element ShellMITC4 611 711 712 812 811 0
element ShellMITC4 612 712 713 813 812 0
element ShellMITC4 613 713 714 814 813 0
element ShellMITC4 614 714 715 815 814 0
element ShellMITC4 615 715 716 816 815 0
element ShellMITC4 616 716 717 817 816 0
element ShellMITC4 700 800 801 901 900 0
element ShellMITC4 701 801 802 902 901 0
element ShellMITC4 702 802 803 903 902 0
element ShellMITC4 703 803 804 904 903 0
element ShellMITC4 704 804 805 905 904 0
element ShellMITC4 705 805 806 906 905 0
element ShellMITC4 706 806 807 907 906 0
element ShellMITC4 707 807 808 908 907 0
element ShellMITC4 708 808 809 909 908 0
element ShellMITC4 709 809 810 910 909 0
element ShellMITC4 710 810 811 911 910 0
element ShellMITC4 711 811 812 912 911 0
element ShellMITC4 712 812 813 913 912 0
element ShellMITC4 713 813 814 914 913 0
element ShellMITC4 714 814 815 915 914 0
element ShellMITC4 715 815 816 916 915 0
element ShellMITC4 716 816 817 917 916 0
element ShellMITC4 800 900 901 1001 1000 0
element ShellMITC4 801 901 902 1002 1001 0
element ShellMITC4 802 902 903 1003 1002 0
element ShellMITC4 803 903 904 1004 1003 0
element ShellMITC4 804 904 905 1005 1004 0
element ShellMITC4 805 905 906 1006 1005 0
element ShellMITC4 806 906 907 1007 1006 0
element ShellMITC4 807 907 908 1008 1007 0
element ShellMITC4 808 908 909 1009 1008 0
element ShellMITC4 809 909 910 1010 1009 0
element ShellMITC4 810 910 911 1011 1010 0
element ShellMITC4 811 911 912 1012 1011 0
element ShellMITC4 812 912 913 1013 1012 0
element ShellMITC4 813 913 914 1014 1013 0
element ShellMITC4 814 914 915 1015 1014 0
element ShellMITC4 815 915 916 1016 1015 0
element ShellMITC4 816 916 917 1017 1016 0
element ShellMITC4 900 1000 1001 1101 1100 0
element ShellMITC4 901 1001 1002 1102 1101 0
element ShellMITC4 902 1002 1003 1103 1102 0
element ShellMITC4 903 1003 1004 1104 1103 0
element ShellMITC4 904 1004 1005 1105 1104 0
element ShellMITC4 905 1005 1006 1106 1105 0
element ShellMITC4 906 1006 1007 1107 1106 0
element ShellMITC4 907 1007 1008 1108 1107 0
element ShellMITC4 908 1008 1009 1109 1108 0
element ShellMITC4 909 1009 1010 1110 1109 0
element ShellMITC4 910 1010 1011 1111 1110 0
element ShellMITC4 911 1011 1012 1112 1111 0
element ShellMITC4 912 1012 1013 1113 1112 0
element ShellMITC4 913 1013 1014 1114 1113 0
element ShellMITC4 914 1014 1015 1115 1114 0
element ShellMITC4 915 1015 1016 1116 1115 0
element ShellMITC4 916 1016 1017 1117 1116 0
element ShellMITC4 1000 1100 1101 1201 1200 0
element ShellMITC4 1001 1101 1102 1202 1201 0
element ShellMITC4 1002 1102 1103 1203 1202 0
element ShellMITC4 1003 1103 1104 1204 1203 0
element ShellMITC4 1004 1104 1105 1205 1204 0
element ShellMITC4 1005 1105 1106 1206 1205 0
element ShellMITC4 1006 1106 1107 1207 1206 0
element ShellMITC4 1007 1107 1108 1208 1207 0
element ShellMITC4 1008 1108 1109 1209 1208 0
element ShellMITC4 1009 1109 1110 1210 1209 0
element ShellMITC4 1010 1110 1111 1211 1210 0
element ShellMITC4 1011 1111 1112 1212 1211 0
element ShellMITC4 1012 1112 1113 1213 1212 0
element ShellMITC4 1013 1113 1114 1214 1213 0
element ShellMITC4 1014 1114 1115 1215 1214 0
element ShellMITC4 1015 1115 1116 1216 1215 0
element ShellMITC4 1016 1116 1117 1217 1216 0
element ShellMITC4 1100 1200 1201 1301 1300 0
element ShellMITC4 1101 1201 1202 1302 1301 0
element ShellMITC4 1102 1202 1203 1303 1302 0
element ShellMITC4 1103 1203 1204 1304 1303 0
element ShellMITC4 1104 1204 1205 1305 1304 0
element ShellMITC4 1105 1205 1206 1306 1305 0
element ShellMITC4 1106 1206 1207 1307 1306 0
element ShellMITC4 1107 1207 1208 1308 1307 0
element ShellMITC4 1108 1208 1209 1309 1308 0
element ShellMITC4 1109 1209 1210 1310 1309 0
element ShellMITC4 1110 1210 1211 1311 1310 0
element ShellMITC4 1111 1211 1212 1312 1311 0
element ShellMITC4 1112 1212 1213 1313 1312 0
element ShellMITC4 1113 1213 1214 1314 1313 0
element ShellMITC4 1114 1214 1215 1315 1314 0
element ShellMITC4 1115 1215 1216 1316 1315 0
element ShellMITC4 1116 1216 1217 1317 1316 0
element ShellMITC4 1200 1300 1301 1401 1400 0
element ShellMITC4 1201 1301 1302 1402 1401 0
element ShellMITC4 1202 1302 1303 1403 1402 0
element ShellMITC4 1203 1303 1304 1404 1403 0
element ShellMITC4 1204 1304 1305 1405 1404 0
element ShellMITC4 1205 1305 1306 1406 1405 0
element ShellMITC4 1206 1306 1307 1407 1406 0
element ShellMITC4 1207 1307 1308 1408 1407 0
element ShellMITC4 1208 1308 1309 1409 1408 0
element ShellMITC4 1209 1309 1310 1410 1409 0
element ShellMITC4 1210 1310 1311 1411 1410 0
element ShellMITC4 1211 1311 1312 1412 1411 0
element ShellMITC4 1212 1312 1313 1413 1412 0
element ShellMITC4 1213 1313 1314 1414 1413 0
element ShellMITC4 1214 1314 1315 1415 1414 0
element ShellMITC4 1215 1315 1316 1416 1415 0
element ShellMITC4 1216 1316 1317 1417 1416 0
element ShellMITC4 1300 1400 1401 1501 1500 0
element ShellMITC4 1301 1401 1402 1502 1501 0
element ShellMITC4 1302 1402 1403 1503 1502 0
element ShellMITC4 1303 1403 1404 1504 1503 0
element ShellMITC4 1304 1404 1405 1505 1504 0
element ShellMITC4 1305 1405 1406 1506 1505 0
element ShellMITC4 1306 1406 1407 1507 1506 0
element ShellMITC4 1307 1407 1408 1508 1507 0
element ShellMITC4 1308 1408 1409 1509 1508 0
element ShellMITC4 1309 1409 1410 1510 1509 0
element ShellMITC4 1310 1410 1411 1511 1510 0
element ShellMITC4 1311 1411 1412 1512 1511 0
element ShellMITC4 1312 1412 1413 1513 1512 0
element ShellMITC4 1313 1413 1414 1514 1513 0
element ShellMITC4 1314 1414 1415 1515 1514 0
element ShellMITC4 1315 1415 1416 1516 1515 0
element ShellMITC4 1316 1416 1417 1517 1516 0
element ShellMITC4 1400 1500 1501 1601 1600 0
element ShellMITC4 1401 1501 1502 1602 1601 0
element ShellMITC4 1402 1502 1503 1603 1602 0
element ShellMITC4 1403 1503 1504 1604 1603 0
element ShellMITC4 1404 1504 1505 1605 1604 0
element ShellMITC4 1405 1505 1506 1606 1605 0
element ShellMITC4 1406 1506 1507 1607 1606 0
element ShellMITC4 1407 1507 1508 1608 1607 0
element ShellMITC4 1408 1508 1509 1609 1608 0
element ShellMITC4 1409 1509 1510 1610 1609 0
element ShellMITC4 1410 1510 1511 1611 1610 0
element ShellMITC4 1411 1511 1512 1612 1611 0
element ShellMITC4 1412 1512 1513 1613 1612 0
element ShellMITC4 1413 1513 1514 1614 1613 0
element ShellMITC4 1414 1514 1515 1615 1614 0
element ShellMITC4 1415 1515 1516 1616 1615 0
element ShellMITC4 1416 1516 1517 1617 1616 0
element ShellMITC4 1500 1600 1601 1701 1700 0
element ShellMITC4 1501 1601 1602 1702 1701 0
element ShellMITC4 1502 1602 1603 1703 1702 0
element ShellMITC4 1503 1603 1604 1704 1703 0
element ShellMITC4 1504 1604 1605 1705 1704 0
element ShellMITC4 1505 1605 1606 1706 1705 0
element ShellMITC4 1506 1606 1607 1707 1706 0
element ShellMITC4 1507 1607 1608 1708 1707 0
element ShellMITC4 1508 1608 1609 1709 1708 0
element ShellMITC4 1509 1609 1610 1710 1709 0
element ShellMITC4 1510 1610 1611 1711 1710 0
element ShellMITC4 1511 1611 1612 1712 1711 0
element ShellMITC4 1512 1612 1613 1713 1712 0
element ShellMITC4 1513 1613 1614 1714 1713 0
element ShellMITC4 1514 1614 1615 1715 1714 0
element ShellMITC4 1515 1615 1616 1716 1715 0
element ShellMITC4 1516 1616 1617 1717 1716 0
element ShellMITC4 1600 1700 1701 1801 1800 0
element ShellMITC4 1601 1701 1702 1802 1801 0
element ShellMITC4 1602 1702 1703 1803 1802 0
element ShellMITC4 1603 1703 1704 1804 1803 0
element ShellMITC4 1604 1704 1705 1805 1804 0
element ShellMITC4 1605 1705 1706 1806 1805 0
element ShellMITC4 1606 1706 1707 1807 1806 0
element ShellMITC4 1607 1707 1708 1808 1807 0
element ShellMITC4 1608 1708 1709 1809 1808 0
element ShellMITC4 1609 1709 1710 1810 1809 0
element ShellMITC4 1610 1710 1711 1811 1810 0
element ShellMITC4 1611 1711 1712 1812 1811 0
element ShellMITC4 1612 1712 1713 1813 1812 0
element ShellMITC4 1613 1713 1714 1814 1813 0
element ShellMITC4 1614 1714 1715 1815 1814 0
element ShellMITC4 1615 1715 1716 1816 1815 0
element ShellMITC4 1616 1716 1717 1817 1816 0
element ShellMITC4 1700 1800 1801 1901 1900 0
element ShellMITC4 1701 1801 1802 1902 1901 0
element ShellMITC4 1702 1802 1803 1903 1902 0
element ShellMITC4 1703 1803 1804 1904 1903 0
element ShellMITC4 1704 1804 1805 1905 1904 0
element ShellMITC4 1705 1805 1806 1906 1905 0
element ShellMITC4 1706 1806 1807 1907 1906 0
element ShellMITC4 1707 1807 1808 1908 1907 0
element ShellMITC4 1708 1808 1809 1909 1908 0
element ShellMITC4 1709 1809 1810 1910 1909 0
element ShellMITC4 1710 1810 1811 1911 1910 0
element ShellMITC4 1711 1811 1812 1912 1911 0
element ShellMITC4 1712 1812 1813 1913 1912 0
element ShellMITC4 1713 1813 1814 1914 1913 0
element ShellMITC4 1714 1814 1815 1915 1914 0
element ShellMITC4 1715 1815 1816 1916 1915 0
element ShellMITC4 1716 1816 1817 1917 1916 0
element ShellMITC4 1800 1900 1901 2001 2000 0
element ShellMITC4 1801 1901 1902 2002 2001 0
element ShellMITC4 1802 1902 1903 2003 2002 0
element ShellMITC4 1803 1903 1904 2004 2003 0
element ShellMITC4 1804 1904 1905 2005 2004 0
element ShellMITC4 1805 1905 1906 2006 2005 0
element ShellMITC4 1806 1906 1907 2007 2006 0
element ShellMITC4 1807 1907 1908 2008 2007 0
element ShellMITC4 1808 1908 1909 2009 2008 0
element ShellMITC4 1809 1909 1910 2010 2009 0
element ShellMITC4 1810 1910 1911 2011 2010 0
element ShellMITC4 1811 1911 1912 2012 2011 0
element ShellMITC4 1812 1912 1913 2013 2012 0
element ShellMITC4 1813 1913 1914 2014 2013 0
element ShellMITC4 1814 1914 1915 2015 2014 0
element ShellMITC4 1815 1915 1916 2016 2015 0
element ShellMITC4 1816 1916 1917 2017 2016 0
element ShellMITC4 1900 2000 2001 2101 2100 0
element ShellMITC4 1901 2001 2002 2102 2101 0
element ShellMITC4 1902 2002 2003 2103 2102 0
element ShellMITC4 1903 2003 2004 2104 2103 0
element ShellMITC4 1904 2004 2005 2105 2104 0
element ShellMITC4 1905 2005 2006 2106 2105 0
element ShellMITC4 1906 2006 2007 2107 2106 0
element ShellMITC4 1907 2007 2008 2108 2107 0
element ShellMITC4 1908 2008 2009 2109 2108 0
element ShellMITC4 1909 2009 2010 2110 2109 0
element ShellMITC4 1910 2010 2011 2111 2110 0
element ShellMITC4 1911 2011 2012 2112 2111 0
element ShellMITC4 1912 2012 2013 2113 2112 0
element ShellMITC4 1913 2013 2014 2114 2113 0
element ShellMITC4 1914 2014 2015 2115 2114 0
element ShellMITC4 1915 2015 2016 2116 2115 0
element ShellMITC4 1916 2016 2017 2117 2116 0
element ShellMITC4 2000 2100 2101 2201 2200 0
element ShellMITC4 2001 2101 2102 2202 2201 0
element ShellMITC4 2002 2102 2103 2203 2202 0
element ShellMITC4 2003 2103 2104 2204 2203 0
element ShellMITC4 2004 2104 2105 2205 2204 0
element ShellMITC4 2005 2105 2106 2206 2205 0
element ShellMITC4 2006 2106 2107 2207 2206 0
element ShellMITC4 2007 2107 2108 2208 2207 0
element ShellMITC4 2008 2108 2109 2209 2208 0
element ShellMITC4 2009 2109 2110 2210 2209 0
element ShellMITC4 2010 2110 2111 2211 2210 0
element ShellMITC4 2011 2111 2112 2212 2211 0
element ShellMITC4 2012 2112 2113 2213 2212 0
element ShellMITC4 2013 2113 2114 2214 2213 0
element ShellMITC4 2014 2114 2115 2215 2214 0
element ShellMITC4 2015 2115 2116 2216 2215 0
element ShellMITC4 2016 2116 2117 2217 2216 0
# End deck elements

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin support elements
element ShellMITC4 2100 201 2300 2400 301 0; # support 1, wall 1, z 1, y 1 below deck
element ShellMITC4 2101 2300 2301 2401 2400 0; # support 1, wall 1, z 1, y 2 below deck
element ShellMITC4 2102 2301 2302 2402 2401 0; # support 1, wall 1, z 1, y 3 below deck
element ShellMITC4 2200 301 2400 2500 401 0; # support 1, wall 1, z 2, y 1 below deck
element ShellMITC4 2201 2400 2401 2501 2500 0; # support 1, wall 1, z 2, y 2 below deck
element ShellMITC4 2202 2401 2402 2502 2501 0; # support 1, wall 1, z 2, y 3 below deck
element ShellMITC4 2300 401 2500 2600 501 0; # support 1, wall 1, z 3, y 1 below deck
element ShellMITC4 2301 2500 2501 2601 2600 0; # support 1, wall 1, z 3, y 2 below deck
element ShellMITC4 2302 2501 2502 2602 2601 0; # support 1, wall 1, z 3, y 3 below deck
element ShellMITC4 2400 202 2700 2800 302 0; # support 1, wall 2, z 1, y 1 below deck
element ShellMITC4 2401 2700 2701 2801 2800 0; # support 1, wall 2, z 1, y 2 below deck
element ShellMITC4 2402 2701 2302 2402 2801 0; # support 1, wall 2, z 1, y 3 below deck
element ShellMITC4 2500 302 2800 2900 402 0; # support 1, wall 2, z 2, y 1 below deck
element ShellMITC4 2501 2800 2801 2901 2900 0; # support 1, wall 2, z 2, y 2 below deck
element ShellMITC4 2502 2801 2402 2502 2901 0; # support 1, wall 2, z 2, y 3 below deck
element ShellMITC4 2600 402 2900 3000 502 0; # support 1, wall 2, z 3, y 1 below deck
element ShellMITC4 2601 2900 2901 3001 3000 0; # support 1, wall 2, z 3, y 2 below deck
element ShellMITC4 2602 2901 2502 2602 3001 0; # support 1, wall 2, z 3, y 3 below deck
element ShellMITC4 2700 701 3100 3200 801 0; # support 2, wall 1, z 1, y 1 below deck
element ShellMITC4 2701 3100 3101 3201 3200 0; # support 2, wall 1, z 1, y 2 below deck
element ShellMITC4 2702 3101 3102 3202 3201 0; # support 2, wall 1, z 1, y 3 below deck
element ShellMITC4 2800 801 3200 3300 901 0; # support 2, wall 1, z 2, y 1 below deck
element ShellMITC4 2801 3200 3201 3301 3300 0; # support 2, wall 1, z 2, y 2 below deck
element ShellMITC4 2802 3201 3202 3302 3301 0; # support 2, wall 1, z 2, y 3 below deck
element ShellMITC4 2900 901 3300 3400 1101 0; # support 2, wall 1, z 3, y 1 below deck
element ShellMITC4 2901 3300 3301 3401 3400 0; # support 2, wall 1, z 3, y 2 below deck
element ShellMITC4 2902 3301 3302 3402 3401 0; # support 2, wall 1, z 3, y 3 below deck
element ShellMITC4 3000 702 3500 3600 802 0; # support 2, wall 2, z 1, y 1 below deck
element ShellMITC4 3001 3500 3501 3601 3600 0; # support 2, wall 2, z 1, y 2 below deck
element ShellMITC4 3002 3501 3102 3202 3601 0; # support 2, wall 2, z 1, y 3 below deck
element ShellMITC4 3100 802 3600 3700 902 0; # support 2, wall 2, z 2, y 1 below deck
element ShellMITC4 3101 3600 3601 3701 3700 0; # support 2, wall 2, z 2, y 2 below deck
element ShellMITC4 3102 3601 3202 3302 3701 0; # support 2, wall 2, z 2, y 3 below deck
element ShellMITC4 3200 902 3700 3800 1102 0; # support 2, wall 2, z 3, y 1 below deck
element ShellMITC4 3201 3700 3701 3801 3800 0; # support 2, wall 2, z 3, y 2 below deck
element ShellMITC4 3202 3701 3302 3402 3801 0; # support 2, wall 2, z 3, y 3 below deck
element ShellMITC4 3300 1201 3900 4000 1401 0; # support 3, wall 1, z 1, y 1 below deck
element ShellMITC4 3301 3900 3901 4001 4000 0; # support 3, wall 1, z 1, y 2 below deck
element ShellMITC4 3302 3901 3902 4002 4001 0; # support 3, wall 1, z 1, y 3 below deck
element ShellMITC4 3400 1401 4000 4100 1501 0; # support 3, wall 1, z 2, y 1 below deck
element ShellMITC4 3401 4000 4001 4101 4100 0; # support 3, wall 1, z 2, y 2 below deck
element ShellMITC4 3402 4001 4002 4102 4101 0; # support 3, wall 1, z 2, y 3 below deck
element ShellMITC4 3500 1501 4100 4200 1601 0; # support 3, wall 1, z 3, y 1 below deck
element ShellMITC4 3501 4100 4101 4201 4200 0; # support 3, wall 1, z 3, y 2 below deck
element ShellMITC4 3502 4101 4102 4202 4201 0; # support 3, wall 1, z 3, y 3 below deck
element ShellMITC4 3600 1202 4300 4400 1402 0; # support 3, wall 2, z 1, y 1 below deck
element ShellMITC4 3601 4300 4301 4401 4400 0; # support 3, wall 2, z 1, y 2 below deck
element ShellMITC4 3602 4301 3902 4002 4401 0; # support 3, wall 2, z 1, y 3 below deck
element ShellMITC4 3700 1402 4400 4500 1502 0; # support 3, wall 2, z 2, y 1 below deck
element ShellMITC4 3701 4400 4401 4501 4500 0; # support 3, wall 2, z 2, y 2 below deck
element ShellMITC4 3702 4401 4002 4102 4501 0; # support 3, wall 2, z 2, y 3 below deck
element ShellMITC4 3800 1502 4500 4600 1602 0; # support 3, wall 2, z 3, y 1 below deck
element ShellMITC4 3801 4500 4501 4601 4600 0; # support 3, wall 2, z 3, y 2 below deck
element ShellMITC4 3802 4501 4102 4202 4601 0; # support 3, wall 2, z 3, y 3 below deck
element ShellMITC4 3900 1801 4700 4800 1901 0; # support 4, wall 1, z 1, y 1 below deck
element ShellMITC4 3901 4700 4701 4801 4800 0; # support 4, wall 1, z 1, y 2 below deck
element ShellMITC4 3902 4701 4702 4802 4801 0; # support 4, wall 1, z 1, y 3 below deck
element ShellMITC4 4000 1901 4800 4900 2001 0; # support 4, wall 1, z 2, y 1 below deck
element ShellMITC4 4001 4800 4801 4901 4900 0; # support 4, wall 1, z 2, y 2 below deck
element ShellMITC4 4002 4801 4802 4902 4901 0; # support 4, wall 1, z 2, y 3 below deck
element ShellMITC4 4100 2001 4900 5000 2101 0; # support 4, wall 1, z 3, y 1 below deck
element ShellMITC4 4101 4900 4901 5001 5000 0; # support 4, wall 1, z 3, y 2 below deck
element ShellMITC4 4102 4901 4902 5002 5001 0; # support 4, wall 1, z 3, y 3 below deck
element ShellMITC4 4200 1802 5100 5200 1902 0; # support 4, wall 2, z 1, y 1 below deck
element ShellMITC4 4201 5100 5101 5201 5200 0; # support 4, wall 2, z 1, y 2 below deck
element ShellMITC4 4202 5101 4702 4802 5201 0; # support 4, wall 2, z 1, y 3 below deck
element ShellMITC4 4300 1902 5200 5300 2002 0; # support 4, wall 2, z 2, y 1 below deck
element ShellMITC4 4301 5200 5201 5301 5300 0; # support 4, wall 2, z 2, y 2 below deck
element ShellMITC4 4302 5201 4802 4902 5301 0; # support 4, wall 2, z 2, y 3 below deck
element ShellMITC4 4400 2002 5300 5400 2102 0; # support 4, wall 2, z 3, y 1 below deck
element ShellMITC4 4401 5300 5301 5401 5400 0; # support 4, wall 2, z 3, y 2 below deck
element ShellMITC4 4402 5301 4902 5002 5401 0; # support 4, wall 2, z 3, y 3 below deck
element ShellMITC4 4500 204 5500 5600 304 0; # support 5, wall 1, z 1, y 1 below deck
element ShellMITC4 4501 5500 5501 5601 5600 0; # support 5, wall 1, z 1, y 2 below deck
element ShellMITC4 4502 5501 5502 5602 5601 0; # support 5, wall 1, z 1, y 3 below deck
element ShellMITC4 4600 304 5600 5700 404 0; # support 5, wall 1, z 2, y 1 below deck
element ShellMITC4 4601 5600 5601 5701 5700 0; # support 5, wall 1, z 2, y 2 below deck
element ShellMITC4 4602 5601 5602 5702 5701 0; # support 5, wall 1, z 2, y 3 below deck
element ShellMITC4 4700 404 5700 5800 504 0; # support 5, wall 1, z 3, y 1 below deck
element ShellMITC4 4701 5700 5701 5801 5800 0; # support 5, wall 1, z 3, y 2 below deck
element ShellMITC4 4702 5701 5702 5802 5801 0; # support 5, wall 1, z 3, y 3 below deck
element ShellMITC4 4800 205 5900 6000 305 0; # support 5, wall 2, z 1, y 1 below deck
element ShellMITC4 4801 5900 5901 6001 6000 0; # support 5, wall 2, z 1, y 2 below deck
element ShellMITC4 4802 5901 5502 5602 6001 0; # support 5, wall 2, z 1, y 3 below deck
element ShellMITC4 4900 305 6000 6100 405 0; # support 5, wall 2, z 2, y 1 below deck
element ShellMITC4 4901 6000 6001 6101 6100 0; # support 5, wall 2, z 2, y 2 below deck
element ShellMITC4 4902 6001 5602 5702 6101 0; # support 5, wall 2, z 2, y 3 below deck
element ShellMITC4 5000 405 6100 6200 505 0; # support 5, wall 2, z 3, y 1 below deck
element ShellMITC4 5001 6100 6101 6201 6200 0; # support 5, wall 2, z 3, y 2 below deck
element ShellMITC4 5002 6101 5702 5802 6201 0; # support 5, wall 2, z 3, y 3 below deck
element ShellMITC4 5100 704 6300 6400 804 0; # support 6, wall 1, z 1, y 1 below deck
element ShellMITC4 5101 6300 6301 6401 6400 0; # support 6, wall 1, z 1, y 2 below deck
element ShellMITC4 5102 6301 6302 6402 6401 0; # support 6, wall 1, z 1, y 3 below deck
element ShellMITC4 5200 804 6400 6500 904 0; # support 6, wall 1, z 2, y 1 below deck
element ShellMITC4 5201 6400 6401 6501 6500 0; # support 6, wall 1, z 2, y 2 below deck
element ShellMITC4 5202 6401 6402 6502 6501 0; # support 6, wall 1, z 2, y 3 below deck
element ShellMITC4 5300 904 6500 6600 1104 0; # support 6, wall 1, z 3, y 1 below deck
element ShellMITC4 5301 6500 6501 6601 6600 0; # support 6, wall 1, z 3, y 2 below deck
element ShellMITC4 5302 6501 6502 6602 6601 0; # support 6, wall 1, z 3, y 3 below deck
element ShellMITC4 5400 705 6700 6800 805 0; # support 6, wall 2, z 1, y 1 below deck
element ShellMITC4 5401 6700 6701 6801 6800 0; # support 6, wall 2, z 1, y 2 below deck
element ShellMITC4 5402 6701 6302 6402 6801 0; # support 6, wall 2, z 1, y 3 below deck
element ShellMITC4 5500 805 6800 6900 905 0; # support 6, wall 2, z 2, y 1 below deck
element ShellMITC4 5501 6800 6801 6901 6900 0; # support 6, wall 2, z 2, y 2 below deck
element ShellMITC4 5502 6801 6402 6502 6901 0; # support 6, wall 2, z 2, y 3 below deck
element ShellMITC4 5600 905 6900 7000 1105 0; # support 6, wall 2, z 3, y 1 below deck
element ShellMITC4 5601 6900 6901 7001 7000 0; # support 6, wall 2, z 3, y 2 below deck
element ShellMITC4 5602 6901 6502 6602 7001 0; # support 6, wall 2, z 3, y 3 below deck
element ShellMITC4 5700 1204 7100 7200 1404 0; # support 7, wall 1, z 1, y 1 below deck
element ShellMITC4 5701 7100 7101 7201 7200 0; # support 7, wall 1, z 1, y 2 below deck
element ShellMITC4 5702 7101 7102 7202 7201 0; # support 7, wall 1, z 1, y 3 below deck
element ShellMITC4 5800 1404 7200 7300 1504 0; # support 7, wall 1, z 2, y 1 below deck
element ShellMITC4 5801 7200 7201 7301 7300 0; # support 7, wall 1, z 2, y 2 below deck
element ShellMITC4 5802 7201 7202 7302 7301 0; # support 7, wall 1, z 2, y 3 below deck
element ShellMITC4 5900 1504 7300 7400 1604 0; # support 7, wall 1, z 3, y 1 below deck
element ShellMITC4 5901 7300 7301 7401 7400 0; # support 7, wall 1, z 3, y 2 below deck
element ShellMITC4 5902 7301 7302 7402 7401 0; # support 7, wall 1, z 3, y 3 below deck
element ShellMITC4 6000 1205 7500 7600 1405 0; # support 7, wall 2, z 1, y 1 below deck
element ShellMITC4 6001 7500 7501 7601 7600 0; # support 7, wall 2, z 1, y 2 below deck
element ShellMITC4 6002 7501 7102 7202 7601 0; # support 7, wall 2, z 1, y 3 below deck
element ShellMITC4 6100 1405 7600 7700 1505 0; # support 7, wall 2, z 2, y 1 below deck
element ShellMITC4 6101 7600 7601 7701 7700 0; # support 7, wall 2, z 2, y 2 below deck
element ShellMITC4 6102 7601 7202 7302 7701 0; # support 7, wall 2, z 2, y 3 below deck
element ShellMITC4 6200 1505 7700 7800 1605 0; # support 7, wall 2, z 3, y 1 below deck
element ShellMITC4 6201 7700 7701 7801 7800 0; # support 7, wall 2, z 3, y 2 below deck
element ShellMITC4 6202 7701 7302 7402 7801 0; # support 7, wall 2, z 3, y 3 below deck
element ShellMITC4 6300 1804 7900 8000 1904 0; # support 8, wall 1, z 1, y 1 below deck
element ShellMITC4 6301 7900 7901 8001 8000 0; # support 8, wall 1, z 1, y 2 below deck
element ShellMITC4 6302 7901 7902 8002 8001 0; # support 8, wall 1, z 1, y 3 below deck
element ShellMITC4 6400 1904 8000 8100 2004 0; # support 8, wall 1, z 2, y 1 below deck
element ShellMITC4 6401 8000 8001 8101 8100 0; # support 8, wall 1, z 2, y 2 below deck
element ShellMITC4 6402 8001 8002 8102 8101 0; # support 8, wall 1, z 2, y 3 below deck
element ShellMITC4 6500 2004 8100 8200 2104 0; # support 8, wall 1, z 3, y 1 below deck
element ShellMITC4 6501 8100 8101 8201 8200 0; # support 8, wall 1, z 3, y 2 below deck
element ShellMITC4 6502 8101 8102 8202 8201 0; # support 8, wall 1, z 3, y 3 below deck
element ShellMITC4 6600 1805 8300 8400 1905 0; # support 8, wall 2, z 1, y 1 below deck
element ShellMITC4 6601 8300 8301 8401 8400 0; # support 8, wall 2, z 1, y 2 below deck
element ShellMITC4 6602 8301 7902 8002 8401 0; # support 8, wall 2, z 1, y 3 below deck
element ShellMITC4 6700 1905 8400 8500 2005 0; # support 8, wall 2, z 2, y 1 below deck
element ShellMITC4 6701 8400 8401 8501 8500 0; # support 8, wall 2, z 2, y 2 below deck
element ShellMITC4 6702 8401 8002 8102 8501 0; # support 8, wall 2, z 2, y 3 below deck
element ShellMITC4 6800 2005 8500 8600 2105 0; # support 8, wall 2, z 3, y 1 below deck
element ShellMITC4 6801 8500 8501 8601 8600 0; # support 8, wall 2, z 3, y 2 below deck
element ShellMITC4 6802 8501 8102 8202 8601 0; # support 8, wall 2, z 3, y 3 below deck
element ShellMITC4 6900 207 8700 8800 307 0; # support 9, wall 1, z 1, y 1 below deck
element ShellMITC4 6901 8700 8701 8801 8800 0; # support 9, wall 1, z 1, y 2 below deck
element ShellMITC4 6902 8701 8702 8802 8801 0; # support 9, wall 1, z 1, y 3 below deck
element ShellMITC4 7000 307 8800 8900 407 0; # support 9, wall 1, z 2, y 1 below deck
element ShellMITC4 7001 8800 8801 8901 8900 0; # support 9, wall 1, z 2, y 2 below deck
element ShellMITC4 7002 8801 8802 8902 8901 0; # support 9, wall 1, z 2, y 3 below deck
element ShellMITC4 7100 407 8900 9000 507 0; # support 9, wall 1, z 3, y 1 below deck
element ShellMITC4 7101 8900 8901 9001 9000 0; # support 9, wall 1, z 3, y 2 below deck
element ShellMITC4 7102 8901 8902 9002 9001 0; # support 9, wall 1, z 3, y 3 below deck
element ShellMITC4 7200 208 9100 9200 308 0; # support 9, wall 2, z 1, y 1 below deck
element ShellMITC4 7201 9100 9101 9201 9200 0; # support 9, wall 2, z 1, y 2 below deck
element ShellMITC4 7202 9101 8702 8802 9201 0; # support 9, wall 2, z 1, y 3 below deck
element ShellMITC4 7300 308 9200 9300 408 0; # support 9, wall 2, z 2, y 1 below deck
element ShellMITC4 7301 9200 9201 9301 9300 0; # support 9, wall 2, z 2, y 2 below deck
element ShellMITC4 7302 9201 8802 8902 9301 0; # support 9, wall 2, z 2, y 3 below deck
element ShellMITC4 7400 408 9300 9400 508 0; # support 9, wall 2, z 3, y 1 below deck
element ShellMITC4 7401 9300 9301 9401 9400 0; # support 9, wall 2, z 3, y 2 below deck
element ShellMITC4 7402 9301 8902 9002 9401 0; # support 9, wall 2, z 3, y 3 below deck
element ShellMITC4 7500 707 9500 9600 807 0; # support 10, wall 1, z 1, y 1 below deck
element ShellMITC4 7501 9500 9501 9601 9600 0; # support 10, wall 1, z 1, y 2 below deck
element ShellMITC4 7502 9501 9502 9602 9601 0; # support 10, wall 1, z 1, y 3 below deck
element ShellMITC4 7600 807 9600 9700 907 0; # support 10, wall 1, z 2, y 1 below deck
element ShellMITC4 7601 9600 9601 9701 9700 0; # support 10, wall 1, z 2, y 2 below deck
element ShellMITC4 7602 9601 9602 9702 9701 0; # support 10, wall 1, z 2, y 3 below deck
element ShellMITC4 7700 907 9700 9800 1107 0; # support 10, wall 1, z 3, y 1 below deck
element ShellMITC4 7701 9700 9701 9801 9800 0; # support 10, wall 1, z 3, y 2 below deck
element ShellMITC4 7702 9701 9702 9802 9801 0; # support 10, wall 1, z 3, y 3 below deck
element ShellMITC4 7800 708 9900 10000 808 0; # support 10, wall 2, z 1, y 1 below deck
element ShellMITC4 7801 9900 9901 10001 10000 0; # support 10, wall 2, z 1, y 2 below deck
element ShellMITC4 7802 9901 9502 9602 10001 0; # support 10, wall 2, z 1, y 3 below deck
element ShellMITC4 7900 808 10000 10100 908 0; # support 10, wall 2, z 2, y 1 below deck
element ShellMITC4 7901 10000 10001 10101 10100 0; # support 10, wall 2, z 2, y 2 below deck
element ShellMITC4 7902 10001 9602 9702 10101 0; # support 10, wall 2, z 2, y 3 below deck
element ShellMITC4 8000 908 10100 10200 1108 0; # support 10, wall 2, z 3, y 1 below deck
element ShellMITC4 8001 10100 10101 10201 10200 0; # support 10, wall 2, z 3, y 2 below deck
element ShellMITC4 8002 10101 9702 9802 10201 0; # support 10, wall 2, z 3, y 3 below deck
element ShellMITC4 8100 1207 10300 10400 1407 0; # support 11, wall 1, z 1, y 1 below deck
element ShellMITC4 8101 10300 10301 10401 10400 0; # support 11, wall 1, z 1, y 2 below deck
element ShellMITC4 8102 10301 10302 10402 10401 0; # support 11, wall 1, z 1, y 3 below deck
element ShellMITC4 8200 1407 10400 10500 1507 0; # support 11, wall 1, z 2, y 1 below deck
element ShellMITC4 8201 10400 10401 10501 10500 0; # support 11, wall 1, z 2, y 2 below deck
element ShellMITC4 8202 10401 10402 10502 10501 0; # support 11, wall 1, z 2, y 3 below deck
element ShellMITC4 8300 1507 10500 10600 1607 0; # support 11, wall 1, z 3, y 1 below deck
element ShellMITC4 8301 10500 10501 10601 10600 0; # support 11, wall 1, z 3, y 2 below deck
element ShellMITC4 8302 10501 10502 10602 10601 0; # support 11, wall 1, z 3, y 3 below deck
element ShellMITC4 8400 1208 10700 10800 1408 0; # support 11, wall 2, z 1, y 1 below deck
element ShellMITC4 8401 10700 10701 10801 10800 0; # support 11, wall 2, z 1, y 2 below deck
element ShellMITC4 8402 10701 10302 10402 10801 0; # support 11, wall 2, z 1, y 3 below deck
element ShellMITC4 8500 1408 10800 10900 1508 0; # support 11, wall 2, z 2, y 1 below deck
element ShellMITC4 8501 10800 10801 10901 10900 0; # support 11, wall 2, z 2, y 2 below deck
element ShellMITC4 8502 10801 10402 10502 10901 0; # support 11, wall 2, z 2, y 3 below deck
element ShellMITC4 8600 1508 10900 11000 1608 0; # support 11, wall 2, z 3, y 1 below deck
element ShellMITC4 8601 10900 10901 11001 11000 0; # support 11, wall 2, z 3, y 2 below deck
element ShellMITC4 8602 10901 10502 10602 11001 0; # support 11, wall 2, z 3, y 3 below deck
element ShellMITC4 8700 1807 11100 11200 1907 0; # support 12, wall 1, z 1, y 1 below deck
element ShellMITC4 8701 11100 11101 11201 11200 0; # support 12, wall 1, z 1, y 2 below deck
element ShellMITC4 8702 11101 11102 11202 11201 0; # support 12, wall 1, z 1, y 3 below deck
element ShellMITC4 8800 1907 11200 11300 2007 0; # support 12, wall 1, z 2, y 1 below deck
element ShellMITC4 8801 11200 11201 11301 11300 0; # support 12, wall 1, z 2, y 2 below deck
element ShellMITC4 8802 11201 11202 11302 11301 0; # support 12, wall 1, z 2, y 3 below deck
element ShellMITC4 8900 2007 11300 11400 2107 0; # support 12, wall 1, z 3, y 1 below deck
element ShellMITC4 8901 11300 11301 11401 11400 0; # support 12, wall 1, z 3, y 2 below deck
element ShellMITC4 8902 11301 11302 11402 11401 0; # support 12, wall 1, z 3, y 3 below deck
element ShellMITC4 9000 1808 11500 11600 1908 0; # support 12, wall 2, z 1, y 1 below deck
element ShellMITC4 9001 11500 11501 11601 11600 0; # support 12, wall 2, z 1, y 2 below deck
element ShellMITC4 9002 11501 11102 11202 11601 0; # support 12, wall 2, z 1, y 3 below deck
element ShellMITC4 9100 1908 11600 11700 2008 0; # support 12, wall 2, z 2, y 1 below deck
element ShellMITC4 9101 11600 11601 11701 11700 0; # support 12, wall 2, z 2, y 2 below deck
element ShellMITC4 9102 11601 11202 11302 11701 0; # support 12, wall 2, z 2, y 3 below deck
element ShellMITC4 9200 2008 11700 11800 2108 0; # support 12, wall 2, z 3, y 1 below deck
element ShellMITC4 9201 11700 11701 11801 11800 0; # support 12, wall 2, z 3, y 2 below deck
element ShellMITC4 9202 11701 11302 11402 11801 0; # support 12, wall 2, z 3, y 3 below deck
element ShellMITC4 9300 209 11900 12000 309 0; # support 13, wall 1, z 1, y 1 below deck
element ShellMITC4 9301 11900 11901 12001 12000 0; # support 13, wall 1, z 1, y 2 below deck
element ShellMITC4 9302 11901 11902 12002 12001 0; # support 13, wall 1, z 1, y 3 below deck
element ShellMITC4 9400 309 12000 12100 409 0; # support 13, wall 1, z 2, y 1 below deck
element ShellMITC4 9401 12000 12001 12101 12100 0; # support 13, wall 1, z 2, y 2 below deck
element ShellMITC4 9402 12001 12002 12102 12101 0; # support 13, wall 1, z 2, y 3 below deck
element ShellMITC4 9500 409 12100 12200 509 0; # support 13, wall 1, z 3, y 1 below deck
element ShellMITC4 9501 12100 12101 12201 12200 0; # support 13, wall 1, z 3, y 2 below deck
element ShellMITC4 9502 12101 12102 12202 12201 0; # support 13, wall 1, z 3, y 3 below deck
element ShellMITC4 9600 210 12300 12400 310 0; # support 13, wall 2, z 1, y 1 below deck
element ShellMITC4 9601 12300 12301 12401 12400 0; # support 13, wall 2, z 1, y 2 below deck
element ShellMITC4 9602 12301 11902 12002 12401 0; # support 13, wall 2, z 1, y 3 below deck
element ShellMITC4 9700 310 12400 12500 410 0; # support 13, wall 2, z 2, y 1 below deck
element ShellMITC4 9701 12400 12401 12501 12500 0; # support 13, wall 2, z 2, y 2 below deck
element ShellMITC4 9702 12401 12002 12102 12501 0; # support 13, wall 2, z 2, y 3 below deck
element ShellMITC4 9800 410 12500 12600 510 0; # support 13, wall 2, z 3, y 1 below deck
element ShellMITC4 9801 12500 12501 12601 12600 0; # support 13, wall 2, z 3, y 2 below deck
element ShellMITC4 9802 12501 12102 12202 12601 0; # support 13, wall 2, z 3, y 3 below deck
element ShellMITC4 9900 709 12700 12800 809 0; # support 14, wall 1, z 1, y 1 below deck
element ShellMITC4 9901 12700 12701 12801 12800 0; # support 14, wall 1, z 1, y 2 below deck
element ShellMITC4 9902 12701 12702 12802 12801 0; # support 14, wall 1, z 1, y 3 below deck
element ShellMITC4 10000 809 12800 12900 909 0; # support 14, wall 1, z 2, y 1 below deck
element ShellMITC4 10001 12800 12801 12901 12900 0; # support 14, wall 1, z 2, y 2 below deck
element ShellMITC4 10002 12801 12802 12902 12901 0; # support 14, wall 1, z 2, y 3 below deck
element ShellMITC4 10100 909 12900 13000 1109 0; # support 14, wall 1, z 3, y 1 below deck
element ShellMITC4 10101 12900 12901 13001 13000 0; # support 14, wall 1, z 3, y 2 below deck
element ShellMITC4 10102 12901 12902 13002 13001 0; # support 14, wall 1, z 3, y 3 below deck
element ShellMITC4 10200 710 13100 13200 810 0; # support 14, wall 2, z 1, y 1 below deck
element ShellMITC4 10201 13100 13101 13201 13200 0; # support 14, wall 2, z 1, y 2 below deck
element ShellMITC4 10202 13101 12702 12802 13201 0; # support 14, wall 2, z 1, y 3 below deck
element ShellMITC4 10300 810 13200 13300 910 0; # support 14, wall 2, z 2, y 1 below deck
element ShellMITC4 10301 13200 13201 13301 13300 0; # support 14, wall 2, z 2, y 2 below deck
element ShellMITC4 10302 13201 12802 12902 13301 0; # support 14, wall 2, z 2, y 3 below deck
element ShellMITC4 10400 910 13300 13400 1110 0; # support 14, wall 2, z 3, y 1 below deck
element ShellMITC4 10401 13300 13301 13401 13400 0; # support 14, wall 2, z 3, y 2 below deck
element ShellMITC4 10402 13301 12902 13002 13401 0; # support 14, wall 2, z 3, y 3 below deck
element ShellMITC4 10500 1209 13500 13600 1409 0; # support 15, wall 1, z 1, y 1 below deck
element ShellMITC4 10501 13500 13501 13601 13600 0; # support 15, wall 1, z 1, y 2 below deck
element ShellMITC4 10502 13501 13502 13602 13601 0; # support 15, wall 1, z 1, y 3 below deck
element ShellMITC4 10600 1409 13600 13700 1509 0; # support 15, wall 1, z 2, y 1 below deck
element ShellMITC4 10601 13600 13601 13701 13700 0; # support 15, wall 1, z 2, y 2 below deck
element ShellMITC4 10602 13601 13602 13702 13701 0; # support 15, wall 1, z 2, y 3 below deck
element ShellMITC4 10700 1509 13700 13800 1609 0; # support 15, wall 1, z 3, y 1 below deck
element ShellMITC4 10701 13700 13701 13801 13800 0; # support 15, wall 1, z 3, y 2 below deck
element ShellMITC4 10702 13701 13702 13802 13801 0; # support 15, wall 1, z 3, y 3 below deck
element ShellMITC4 10800 1210 13900 14000 1410 0; # support 15, wall 2, z 1, y 1 below deck
element ShellMITC4 10801 13900 13901 14001 14000 0; # support 15, wall 2, z 1, y 2 below deck
element ShellMITC4 10802 13901 13502 13602 14001 0; # support 15, wall 2, z 1, y 3 below deck
element ShellMITC4 10900 1410 14000 14100 1510 0; # support 15, wall 2, z 2, y 1 below deck
element ShellMITC4 10901 14000 14001 14101 14100 0; # support 15, wall 2, z 2, y 2 below deck
element ShellMITC4 10902 14001 13602 13702 14101 0; # support 15, wall 2, z 2, y 3 below deck
element ShellMITC4 11000 1510 14100 14200 1610 0; # support 15, wall 2, z 3, y 1 below deck
element ShellMITC4 11001 14100 14101 14201 14200 0; # support 15, wall 2, z 3, y 2 below deck
element ShellMITC4 11002 14101 13702 13802 14201 0; # support 15, wall 2, z 3, y 3 below deck
element ShellMITC4 11100 1809 14300 14400 1909 0; # support 16, wall 1, z 1, y 1 below deck
element ShellMITC4 11101 14300 14301 14401 14400 0; # support 16, wall 1, z 1, y 2 below deck
element ShellMITC4 11102 14301 14302 14402 14401 0; # support 16, wall 1, z 1, y 3 below deck
element ShellMITC4 11200 1909 14400 14500 2009 0; # support 16, wall 1, z 2, y 1 below deck
element ShellMITC4 11201 14400 14401 14501 14500 0; # support 16, wall 1, z 2, y 2 below deck
element ShellMITC4 11202 14401 14402 14502 14501 0; # support 16, wall 1, z 2, y 3 below deck
element ShellMITC4 11300 2009 14500 14600 2109 0; # support 16, wall 1, z 3, y 1 below deck
element ShellMITC4 11301 14500 14501 14601 14600 0; # support 16, wall 1, z 3, y 2 below deck
element ShellMITC4 11302 14501 14502 14602 14601 0; # support 16, wall 1, z 3, y 3 below deck
element ShellMITC4 11400 1810 14700 14800 1910 0; # support 16, wall 2, z 1, y 1 below deck
element ShellMITC4 11401 14700 14701 14801 14800 0; # support 16, wall 2, z 1, y 2 below deck
element ShellMITC4 11402 14701 14302 14402 14801 0; # support 16, wall 2, z 1, y 3 below deck
element ShellMITC4 11500 1910 14800 14900 2010 0; # support 16, wall 2, z 2, y 1 below deck
element ShellMITC4 11501 14800 14801 14901 14900 0; # support 16, wall 2, z 2, y 2 below deck
element ShellMITC4 11502 14801 14402 14502 14901 0; # support 16, wall 2, z 2, y 3 below deck
element ShellMITC4 11600 2010 14900 15000 2110 0; # support 16, wall 2, z 3, y 1 below deck
element ShellMITC4 11601 14900 14901 15001 15000 0; # support 16, wall 2, z 3, y 2 below deck
element ShellMITC4 11602 14901 14502 14602 15001 0; # support 16, wall 2, z 3, y 3 below deck
element ShellMITC4 11700 212 15100 15200 312 0; # support 17, wall 1, z 1, y 1 below deck
element ShellMITC4 11701 15100 15101 15201 15200 0; # support 17, wall 1, z 1, y 2 below deck
element ShellMITC4 11702 15101 15102 15202 15201 0; # support 17, wall 1, z 1, y 3 below deck
element ShellMITC4 11800 312 15200 15300 412 0; # support 17, wall 1, z 2, y 1 below deck
element ShellMITC4 11801 15200 15201 15301 15300 0; # support 17, wall 1, z 2, y 2 below deck
element ShellMITC4 11802 15201 15202 15302 15301 0; # support 17, wall 1, z 2, y 3 below deck
element ShellMITC4 11900 412 15300 15400 512 0; # support 17, wall 1, z 3, y 1 below deck
element ShellMITC4 11901 15300 15301 15401 15400 0; # support 17, wall 1, z 3, y 2 below deck
element ShellMITC4 11902 15301 15302 15402 15401 0; # support 17, wall 1, z 3, y 3 below deck
element ShellMITC4 12000 213 15500 15600 313 0; # support 17, wall 2, z 1, y 1 below deck
element ShellMITC4 12001 15500 15501 15601 15600 0; # support 17, wall 2, z 1, y 2 below deck
element ShellMITC4 12002 15501 15102 15202 15601 0; # support 17, wall 2, z 1, y 3 below deck
element ShellMITC4 12100 313 15600 15700 413 0; # support 17, wall 2, z 2, y 1 below deck
element ShellMITC4 12101 15600 15601 15701 15700 0; # support 17, wall 2, z 2, y 2 below deck
element ShellMITC4 12102 15601 15202 15302 15701 0; # support 17, wall 2, z 2, y 3 below deck
element ShellMITC4 12200 413 15700 15800 513 0; # support 17, wall 2, z 3, y 1 below deck
element ShellMITC4 12201 15700 15701 15801 15800 0; # support 17, wall 2, z 3, y 2 below deck
element ShellMITC4 12202 15701 15302 15402 15801 0; # support 17, wall 2, z 3, y 3 below deck
element ShellMITC4 12300 712 15900 16000 812 0; # support 18, wall 1, z 1, y 1 below deck
element ShellMITC4 12301 15900 15901 16001 16000 0; # support 18, wall 1, z 1, y 2 below deck
element ShellMITC4 12302 15901 15902 16002 16001 0; # support 18, wall 1, z 1, y 3 below deck
element ShellMITC4 12400 812 16000 16100 912 0; # support 18, wall 1, z 2, y 1 below deck
element ShellMITC4 12401 16000 16001 16101 16100 0; # support 18, wall 1, z 2, y 2 below deck
element ShellMITC4 12402 16001 16002 16102 16101 0; # support 18, wall 1, z 2, y 3 below deck
element ShellMITC4 12500 912 16100 16200 1112 0; # support 18, wall 1, z 3, y 1 below deck
element ShellMITC4 12501 16100 16101 16201 16200 0; # support 18, wall 1, z 3, y 2 below deck
element ShellMITC4 12502 16101 16102 16202 16201 0; # support 18, wall 1, z 3, y 3 below deck
element ShellMITC4 12600 713 16300 16400 813 0; # support 18, wall 2, z 1, y 1 below deck
element ShellMITC4 12601 16300 16301 16401 16400 0; # support 18, wall 2, z 1, y 2 below deck
element ShellMITC4 12602 16301 15902 16002 16401 0; # support 18, wall 2, z 1, y 3 below deck
element ShellMITC4 12700 813 16400 16500 913 0; # support 18, wall 2, z 2, y 1 below deck
element ShellMITC4 12701 16400 16401 16501 16500 0; # support 18, wall 2, z 2, y 2 below deck
element ShellMITC4 12702 16401 16002 16102 16501 0; # support 18, wall 2, z 2, y 3 below deck
element ShellMITC4 12800 913 16500 16600 1113 0; # support 18, wall 2, z 3, y 1 below deck
element ShellMITC4 12801 16500 16501 16601 16600 0; # support 18, wall 2, z 3, y 2 below deck
element ShellMITC4 12802 16501 16102 16202 16601 0; # support 18, wall 2, z 3, y 3 below deck
element ShellMITC4 12900 1212 16700 16800 1412 0; # support 19, wall 1, z 1, y 1 below deck
element ShellMITC4 12901 16700 16701 16801 16800 0; # support 19, wall 1, z 1, y 2 below deck
element ShellMITC4 12902 16701 16702 16802 16801 0; # support 19, wall 1, z 1, y 3 below deck
element ShellMITC4 13000 1412 16800 16900 1512 0; # support 19, wall 1, z 2, y 1 below deck
element ShellMITC4 13001 16800 16801 16901 16900 0; # support 19, wall 1, z 2, y 2 below deck
element ShellMITC4 13002 16801 16802 16902 16901 0; # support 19, wall 1, z 2, y 3 below deck
element ShellMITC4 13100 1512 16900 17000 1612 0; # support 19, wall 1, z 3, y 1 below deck
element ShellMITC4 13101 16900 16901 17001 17000 0; # support 19, wall 1, z 3, y 2 below deck
element ShellMITC4 13102 16901 16902 17002 17001 0; # support 19, wall 1, z 3, y 3 below deck
element ShellMITC4 13200 1213 17100 17200 1413 0; # support 19, wall 2, z 1, y 1 below deck
element ShellMITC4 13201 17100 17101 17201 17200 0; # support 19, wall 2, z 1, y 2 below deck
element ShellMITC4 13202 17101 16702 16802 17201 0; # support 19, wall 2, z 1, y 3 below deck
element ShellMITC4 13300 1413 17200 17300 1513 0; # support 19, wall 2, z 2, y 1 below deck
element ShellMITC4 13301 17200 17201 17301 17300 0; # support 19, wall 2, z 2, y 2 below deck
element ShellMITC4 13302 17201 16802 16902 17301 0; # support 19, wall 2, z 2, y 3 below deck
element ShellMITC4 13400 1513 17300 17400 1613 0; # support 19, wall 2, z 3, y 1 below deck
element ShellMITC4 13401 17300 17301 17401 17400 0; # support 19, wall 2, z 3, y 2 below deck
element ShellMITC4 13402 17301 16902 17002 17401 0; # support 19, wall 2, z 3, y 3 below deck
element ShellMITC4 13500 1812 17500 17600 1912 0; # support 20, wall 1, z 1, y 1 below deck
element ShellMITC4 13501 17500 17501 17601 17600 0; # support 20, wall 1, z 1, y 2 below deck
element ShellMITC4 13502 17501 17502 17602 17601 0; # support 20, wall 1, z 1, y 3 below deck
element ShellMITC4 13600 1912 17600 17700 2012 0; # support 20, wall 1, z 2, y 1 below deck
element ShellMITC4 13601 17600 17601 17701 17700 0; # support 20, wall 1, z 2, y 2 below deck
element ShellMITC4 13602 17601 17602 17702 17701 0; # support 20, wall 1, z 2, y 3 below deck
element ShellMITC4 13700 2012 17700 17800 2112 0; # support 20, wall 1, z 3, y 1 below deck
element ShellMITC4 13701 17700 17701 17801 17800 0; # support 20, wall 1, z 3, y 2 below deck
element ShellMITC4 13702 17701 17702 17802 17801 0; # support 20, wall 1, z 3, y 3 below deck
element ShellMITC4 13800 1813 17900 18000 1913 0; # support 20, wall 2, z 1, y 1 below deck
element ShellMITC4 13801 17900 17901 18001 18000 0; # support 20, wall 2, z 1, y 2 below deck
element ShellMITC4 13802 17901 17502 17602 18001 0; # support 20, wall 2, z 1, y 3 below deck
element ShellMITC4 13900 1913 18000 18100 2013 0; # support 20, wall 2, z 2, y 1 below deck
element ShellMITC4 13901 18000 18001 18101 18100 0; # support 20, wall 2, z 2, y 2 below deck
element ShellMITC4 13902 18001 17602 17702 18101 0; # support 20, wall 2, z 2, y 3 below deck
element ShellMITC4 14000 2013 18100 18200 2113 0; # support 20, wall 2, z 3, y 1 below deck
element ShellMITC4 14001 18100 18101 18201 18200 0; # support 20, wall 2, z 3, y 2 below deck
element ShellMITC4 14002 18101 17702 17802 18201 0; # support 20, wall 2, z 3, y 3 below deck
element ShellMITC4 14100 215 18300 18400 315 0; # support 21, wall 1, z 1, y 1 below deck
element ShellMITC4 14101 18300 18301 18401 18400 0; # support 21, wall 1, z 1, y 2 below deck
element ShellMITC4 14102 18301 18302 18402 18401 0; # support 21, wall 1, z 1, y 3 below deck
element ShellMITC4 14200 315 18400 18500 415 0; # support 21, wall 1, z 2, y 1 below deck
element ShellMITC4 14201 18400 18401 18501 18500 0; # support 21, wall 1, z 2, y 2 below deck
element ShellMITC4 14202 18401 18402 18502 18501 0; # support 21, wall 1, z 2, y 3 below deck
element ShellMITC4 14300 415 18500 18600 515 0; # support 21, wall 1, z 3, y 1 below deck
element ShellMITC4 14301 18500 18501 18601 18600 0; # support 21, wall 1, z 3, y 2 below deck
element ShellMITC4 14302 18501 18502 18602 18601 0; # support 21, wall 1, z 3, y 3 below deck
element ShellMITC4 14400 216 18700 18800 316 0; # support 21, wall 2, z 1, y 1 below deck
element ShellMITC4 14401 18700 18701 18801 18800 0; # support 21, wall 2, z 1, y 2 below deck
element ShellMITC4 14402 18701 18302 18402 18801 0; # support 21, wall 2, z 1, y 3 below deck
element ShellMITC4 14500 316 18800 18900 416 0; # support 21, wall 2, z 2, y 1 below deck
element ShellMITC4 14501 18800 18801 18901 18900 0; # support 21, wall 2, z 2, y 2 below deck
element ShellMITC4 14502 18801 18402 18502 18901 0; # support 21, wall 2, z 2, y 3 below deck
element ShellMITC4 14600 416 18900 19000 516 0; # support 21, wall 2, z 3, y 1 below deck
element ShellMITC4 14601 18900 18901 19001 19000 0; # support 21, wall 2, z 3, y 2 below deck
element ShellMITC4 14602 18901 18502 18602 19001 0; # support 21, wall 2, z 3, y 3 below deck
element ShellMITC4 14700 715 19100 19200 815 0; # support 22, wall 1, z 1, y 1 below deck
element ShellMITC4 14701 19100 19101 19201 19200 0; # support 22, wall 1, z 1, y 2 below deck
element ShellMITC4 14702 19101 19102 19202 19201 0; # support 22, wall 1, z 1, y 3 below deck
element ShellMITC4 14800 815 19200 19300 915 0; # support 22, wall 1, z 2, y 1 below deck
element ShellMITC4 14801 19200 19201 19301 19300 0; # support 22, wall 1, z 2, y 2 below deck
element ShellMITC4 14802 19201 19202 19302 19301 0; # support 22, wall 1, z 2, y 3 below deck
element ShellMITC4 14900 915 19300 19400 1115 0; # support 22, wall 1, z 3, y 1 below deck
element ShellMITC4 14901 19300 19301 19401 19400 0; # support 22, wall 1, z 3, y 2 below deck
element ShellMITC4 14902 19301 19302 19402 19401 0; # support 22, wall 1, z 3, y 3 below deck
element ShellMITC4 15000 716 19500 19600 816 0; # support 22, wall 2, z 1, y 1 below deck
element ShellMITC4 15001 19500 19501 19601 19600 0; # support 22, wall 2, z 1, y 2 below deck
element ShellMITC4 15002 19501 19102 19202 19601 0; # support 22, wall 2, z 1, y 3 below deck
element ShellMITC4 15100 816 19600 19700 916 0; # support 22, wall 2, z 2, y 1 below deck
element ShellMITC4 15101 19600 19601 19701 19700 0; # support 22, wall 2, z 2, y 2 below deck
element ShellMITC4 15102 19601 19202 19302 19701 0; # support 22, wall 2, z 2, y 3 below deck
element ShellMITC4 15200 916 19700 19800 1116 0; # support 22, wall 2, z 3, y 1 below deck
element ShellMITC4 15201 19700 19701 19801 19800 0; # support 22, wall 2, z 3, y 2 below deck
element ShellMITC4 15202 19701 19302 19402 19801 0; # support 22, wall 2, z 3, y 3 below deck
element ShellMITC4 15300 1215 19900 20000 1415 0; # support 23, wall 1, z 1, y 1 below deck
element ShellMITC4 15301 19900 19901 20001 20000 0; # support 23, wall 1, z 1, y 2 below deck
element ShellMITC4 15302 19901 19902 20002 20001 0; # support 23, wall 1, z 1, y 3 below deck
element ShellMITC4 15400 1415 20000 20100 1515 0; # support 23, wall 1, z 2, y 1 below deck
element ShellMITC4 15401 20000 20001 20101 20100 0; # support 23, wall 1, z 2, y 2 below deck
element ShellMITC4 15402 20001 20002 20102 20101 0; # support 23, wall 1, z 2, y 3 below deck
element ShellMITC4 15500 1515 20100 20200 1615 0; # support 23, wall 1, z 3, y 1 below deck
element ShellMITC4 15501 20100 20101 20201 20200 0; # support 23, wall 1, z 3, y 2 below deck
element ShellMITC4 15502 20101 20102 20202 20201 0; # support 23, wall 1, z 3, y 3 below deck
element ShellMITC4 15600 1216 20300 20400 1416 0; # support 23, wall 2, z 1, y 1 below deck
element ShellMITC4 15601 20300 20301 20401 20400 0; # support 23, wall 2, z 1, y 2 below deck
element ShellMITC4 15602 20301 19902 20002 20401 0; # support 23, wall 2, z 1, y 3 below deck
element ShellMITC4 15700 1416 20400 20500 1516 0; # support 23, wall 2, z 2, y 1 below deck
element ShellMITC4 15701 20400 20401 20501 20500 0; # support 23, wall 2, z 2, y 2 below deck
element ShellMITC4 15702 20401 20002 20102 20501 0; # support 23, wall 2, z 2, y 3 below deck
element ShellMITC4 15800 1516 20500 20600 1616 0; # support 23, wall 2, z 3, y 1 below deck
element ShellMITC4 15801 20500 20501 20601 20600 0; # support 23, wall 2, z 3, y 2 below deck
element ShellMITC4 15802 20501 20102 20202 20601 0; # support 23, wall 2, z 3, y 3 below deck
element ShellMITC4 15900 1815 20700 20800 1915 0; # support 24, wall 1, z 1, y 1 below deck
element ShellMITC4 15901 20700 20701 20801 20800 0; # support 24, wall 1, z 1, y 2 below deck
element ShellMITC4 15902 20701 20702 20802 20801 0; # support 24, wall 1, z 1, y 3 below deck
element ShellMITC4 16000 1915 20800 20900 2015 0; # support 24, wall 1, z 2, y 1 below deck
element ShellMITC4 16001 20800 20801 20901 20900 0; # support 24, wall 1, z 2, y 2 below deck
element ShellMITC4 16002 20801 20802 20902 20901 0; # support 24, wall 1, z 2, y 3 below deck
element ShellMITC4 16100 2015 20900 21000 2115 0; # support 24, wall 1, z 3, y 1 below deck
element ShellMITC4 16101 20900 20901 21001 21000 0; # support 24, wall 1, z 3, y 2 below deck
element ShellMITC4 16102 20901 20902 21002 21001 0; # support 24, wall 1, z 3, y 3 below deck
element ShellMITC4 16200 1816 21100 21200 1916 0; # support 24, wall 2, z 1, y 1 below deck
element ShellMITC4 16201 21100 21101 21201 21200 0; # support 24, wall 2, z 1, y 2 below deck
element ShellMITC4 16202 21101 20702 20802 21201 0; # support 24, wall 2, z 1, y 3 below deck
element ShellMITC4 16300 1916 21200 21300 2016 0; # support 24, wall 2, z 2, y 1 below deck
element ShellMITC4 16301 21200 21201 21301 21300 0; # support 24, wall 2, z 2, y 2 below deck
element ShellMITC4 16302 21201 20802 20902 21301 0; # support 24, wall 2, z 2, y 3 below deck
element ShellMITC4 16400 2016 21300 21400 2116 0; # support 24, wall 2, z 3, y 1 below deck
element ShellMITC4 16401 21300 21301 21401 21400 0; # support 24, wall 2, z 3, y 2 below deck
element ShellMITC4 16402 21301 20902 21002 21401 0; # support 24, wall 2, z 3, y 3 below deck
# End support elements



timeSeries Linear 1

pattern Plain 1 1 {
# load nodeTag N_x N_y N_z N_rx N_ry N_rz
# Begin loads
load 1705 0 100000 0 0 0 0
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
recorder Node -file generated-data-test/opensees/bridge705-3d-response-params=034,10000-node-y.out -node 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 115 116 117 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 215 216 217 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 315 316 317 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 415 416 417 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 515 516 517 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 615 616 617 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 715 716 717 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 815 816 817 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 915 916 917 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1015 1016 1017 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1115 1116 1117 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1215 1216 1217 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1315 1316 1317 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1415 1416 1417 1500 1501 1502 1503 1504 1505 1506 1507 1508 1509 1510 1511 1512 1513 1514 1515 1516 1517 1600 1601 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1615 1616 1617 1700 1701 1702 1703 1704 1705 1706 1707 1708 1709 1710 1711 1712 1713 1714 1715 1716 1717 1800 1801 1802 1803 1804 1805 1806 1807 1808 1809 1810 1811 1812 1813 1814 1815 1816 1817 1900 1901 1902 1903 1904 1905 1906 1907 1908 1909 1910 1911 1912 1913 1914 1915 1916 1917 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2015 2016 2017 2100 2101 2102 2103 2104 2105 2106 2107 2108 2109 2110 2111 2112 2113 2114 2115 2116 2117 2200 2201 2202 2203 2204 2205 2206 2207 2208 2209 2210 2211 2212 2213 2214 2215 2216 2217 -dof 2 disp
# End translation recorders

analyze 1
