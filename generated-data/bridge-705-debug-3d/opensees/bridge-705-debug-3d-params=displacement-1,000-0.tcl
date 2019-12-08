
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
node 200 0 0 -16.0
node 201 11.575 0 -16.0
node 202 14.675 0 -16.0
node 203 26.875 0 -16.0
node 204 29.975 0 -16.0
node 205 42.175 0 -16.0
node 206 45.275 0 -16.0
node 207 51.375 0 -16.0
node 208 57.475 0 -16.0
node 209 60.575 0 -16.0
node 210 72.775 0 -16.0
node 211 75.875 0 -16.0
node 212 88.075 0 -16.0
node 213 91.175 0 -16.0
node 214 102.75 0 -16.0
node 300 0 0 -15.999
node 301 11.575 0 -15.999
node 302 14.675 0 -15.999
node 303 26.875 0 -15.999
node 304 29.975 0 -15.999
node 305 42.175 0 -15.999
node 306 45.275 0 -15.999
node 307 51.375 0 -15.999
node 308 57.475 0 -15.999
node 309 60.575 0 -15.999
node 310 72.775 0 -15.999
node 311 75.875 0 -15.999
node 312 88.075 0 -15.999
node 313 91.175 0 -15.999
node 314 102.75 0 -15.999
node 400 0 0 -14.433
node 401 11.575 0 -14.433; # support node
node 402 14.675 0 -14.433; # support node
node 403 26.875 0 -14.433; # support node
node 404 29.975 0 -14.433; # support node
node 405 42.175 0 -14.433; # support node
node 406 45.275 0 -14.433; # support node
node 407 51.375 0 -14.433
node 408 57.475 0 -14.433; # support node
node 409 60.575 0 -14.433; # support node
node 410 72.775 0 -14.433; # support node
node 411 75.875 0 -14.433; # support node
node 412 88.075 0 -14.433; # support node
node 413 91.175 0 -14.433; # support node
node 414 102.75 0 -14.433
node 500 0 0 -12.95
node 501 11.575 0 -12.95
node 502 14.675 0 -12.95
node 503 26.875 0 -12.95
node 504 29.975 0 -12.95
node 505 42.175 0 -12.95
node 506 45.275 0 -12.95
node 507 51.375 0 -12.95
node 508 57.475 0 -12.95
node 509 60.575 0 -12.95
node 510 72.775 0 -12.95
node 511 75.875 0 -12.95
node 512 88.075 0 -12.95
node 513 91.175 0 -12.95
node 514 102.75 0 -12.95
node 600 0 0 -12.949
node 601 11.575 0 -12.949
node 602 14.675 0 -12.949
node 603 26.875 0 -12.949
node 604 29.975 0 -12.949
node 605 42.175 0 -12.949
node 606 45.275 0 -12.949
node 607 51.375 0 -12.949
node 608 57.475 0 -12.949
node 609 60.575 0 -12.949
node 610 72.775 0 -12.949
node 611 75.875 0 -12.949
node 612 88.075 0 -12.949
node 613 91.175 0 -12.949
node 614 102.75 0 -12.949
node 700 0 0 -12.75
node 701 11.575 0 -12.75
node 702 14.675 0 -12.75
node 703 26.875 0 -12.75
node 704 29.975 0 -12.75
node 705 42.175 0 -12.75
node 706 45.275 0 -12.75
node 707 51.375 0 -12.75
node 708 57.475 0 -12.75
node 709 60.575 0 -12.75
node 710 72.775 0 -12.75
node 711 75.875 0 -12.75
node 712 88.075 0 -12.75
node 713 91.175 0 -12.75
node 714 102.75 0 -12.75
node 800 0 0 -12.749
node 801 11.575 0 -12.749
node 802 14.675 0 -12.749
node 803 26.875 0 -12.749
node 804 29.975 0 -12.749
node 805 42.175 0 -12.749
node 806 45.275 0 -12.749
node 807 51.375 0 -12.749
node 808 57.475 0 -12.749
node 809 60.575 0 -12.749
node 810 72.775 0 -12.749
node 811 75.875 0 -12.749
node 812 88.075 0 -12.749
node 813 91.175 0 -12.749
node 814 102.75 0 -12.749
node 900 0 0 -12.6
node 901 11.575 0 -12.6; # support node
node 902 14.675 0 -12.6; # support node
node 903 26.875 0 -12.6; # support node
node 904 29.975 0 -12.6; # support node
node 905 42.175 0 -12.6; # support node
node 906 45.275 0 -12.6; # support node
node 907 51.375 0 -12.6
node 908 57.475 0 -12.6; # support node
node 909 60.575 0 -12.6; # support node
node 910 72.775 0 -12.6; # support node
node 911 75.875 0 -12.6; # support node
node 912 88.075 0 -12.6; # support node
node 913 91.175 0 -12.6; # support node
node 914 102.75 0 -12.6
node 1000 0 0 -10.767
node 1001 11.575 0 -10.767; # support node
node 1002 14.675 0 -10.767; # support node
node 1003 26.875 0 -10.767; # support node
node 1004 29.975 0 -10.767; # support node
node 1005 42.175 0 -10.767; # support node
node 1006 45.275 0 -10.767; # support node
node 1007 51.375 0 -10.767
node 1008 57.475 0 -10.767; # support node
node 1009 60.575 0 -10.767; # support node
node 1010 72.775 0 -10.767; # support node
node 1011 75.875 0 -10.767; # support node
node 1012 88.075 0 -10.767; # support node
node 1013 91.175 0 -10.767; # support node
node 1014 102.75 0 -10.767
node 1100 0 0 -6.033
node 1101 11.575 0 -6.033; # support node
node 1102 14.675 0 -6.033; # support node
node 1103 26.875 0 -6.033; # support node
node 1104 29.975 0 -6.033; # support node
node 1105 42.175 0 -6.033; # support node
node 1106 45.275 0 -6.033; # support node
node 1107 51.375 0 -6.033
node 1108 57.475 0 -6.033; # support node
node 1109 60.575 0 -6.033; # support node
node 1110 72.775 0 -6.033; # support node
node 1111 75.875 0 -6.033; # support node
node 1112 88.075 0 -6.033; # support node
node 1113 91.175 0 -6.033; # support node
node 1114 102.75 0 -6.033
node 1200 0 0 -5.5
node 1201 11.575 0 -5.5
node 1202 14.675 0 -5.5
node 1203 26.875 0 -5.5
node 1204 29.975 0 -5.5
node 1205 42.175 0 -5.5
node 1206 45.275 0 -5.5
node 1207 51.375 0 -5.5
node 1208 57.475 0 -5.5
node 1209 60.575 0 -5.5
node 1210 72.775 0 -5.5
node 1211 75.875 0 -5.5
node 1212 88.075 0 -5.5
node 1213 91.175 0 -5.5
node 1214 102.75 0 -5.5
node 1300 0 0 -5.499
node 1301 11.575 0 -5.499
node 1302 14.675 0 -5.499
node 1303 26.875 0 -5.499
node 1304 29.975 0 -5.499
node 1305 42.175 0 -5.499
node 1306 45.275 0 -5.499
node 1307 51.375 0 -5.499
node 1308 57.475 0 -5.499
node 1309 60.575 0 -5.499
node 1310 72.775 0 -5.499
node 1311 75.875 0 -5.499
node 1312 88.075 0 -5.499
node 1313 91.175 0 -5.499
node 1314 102.75 0 -5.499
node 1400 0 0 -5.3
node 1401 11.575 0 -5.3
node 1402 14.675 0 -5.3
node 1403 26.875 0 -5.3
node 1404 29.975 0 -5.3
node 1405 42.175 0 -5.3
node 1406 45.275 0 -5.3
node 1407 51.375 0 -5.3
node 1408 57.475 0 -5.3
node 1409 60.575 0 -5.3
node 1410 72.775 0 -5.3
node 1411 75.875 0 -5.3
node 1412 88.075 0 -5.3
node 1413 91.175 0 -5.3
node 1414 102.75 0 -5.3
node 1500 0 0 -5.299
node 1501 11.575 0 -5.299
node 1502 14.675 0 -5.299
node 1503 26.875 0 -5.299
node 1504 29.975 0 -5.299
node 1505 42.175 0 -5.299
node 1506 45.275 0 -5.299
node 1507 51.375 0 -5.299
node 1508 57.475 0 -5.299
node 1509 60.575 0 -5.299
node 1510 72.775 0 -5.299
node 1511 75.875 0 -5.299
node 1512 88.075 0 -5.299
node 1513 91.175 0 -5.299
node 1514 102.75 0 -5.299
node 1600 0 0 -4.2
node 1601 11.575 0 -4.2; # support node
node 1602 14.675 0 -4.2; # support node
node 1603 26.875 0 -4.2; # support node
node 1604 29.975 0 -4.2; # support node
node 1605 42.175 0 -4.2; # support node
node 1606 45.275 0 -4.2; # support node
node 1607 51.375 0 -4.2
node 1608 57.475 0 -4.2; # support node
node 1609 60.575 0 -4.2; # support node
node 1610 72.775 0 -4.2; # support node
node 1611 75.875 0 -4.2; # support node
node 1612 88.075 0 -4.2; # support node
node 1613 91.175 0 -4.2; # support node
node 1614 102.75 0 -4.2
node 1700 0 0 -2.89
node 1701 11.575 0 -2.89
node 1702 14.675 0 -2.89
node 1703 26.875 0 -2.89
node 1704 29.975 0 -2.89
node 1705 42.175 0 -2.89
node 1706 45.275 0 -2.89
node 1707 51.375 0 -2.89
node 1708 57.475 0 -2.89
node 1709 60.575 0 -2.89
node 1710 72.775 0 -2.89
node 1711 75.875 0 -2.89
node 1712 88.075 0 -2.89
node 1713 91.175 0 -2.89
node 1714 102.75 0 -2.89
node 1800 0 0 -2.889
node 1801 11.575 0 -2.889
node 1802 14.675 0 -2.889
node 1803 26.875 0 -2.889
node 1804 29.975 0 -2.889
node 1805 42.175 0 -2.889
node 1806 45.275 0 -2.889
node 1807 51.375 0 -2.889
node 1808 57.475 0 -2.889
node 1809 60.575 0 -2.889
node 1810 72.775 0 -2.889
node 1811 75.875 0 -2.889
node 1812 88.075 0 -2.889
node 1813 91.175 0 -2.889
node 1814 102.75 0 -2.889
node 1900 0 0 -2.367
node 1901 11.575 0 -2.367; # support node
node 1902 14.675 0 -2.367; # support node
node 1903 26.875 0 -2.367; # support node
node 1904 29.975 0 -2.367; # support node
node 1905 42.175 0 -2.367; # support node
node 1906 45.275 0 -2.367; # support node
node 1907 51.375 0 -2.367
node 1908 57.475 0 -2.367; # support node
node 1909 60.575 0 -2.367; # support node
node 1910 72.775 0 -2.367; # support node
node 1911 75.875 0 -2.367; # support node
node 1912 88.075 0 -2.367; # support node
node 1913 91.175 0 -2.367; # support node
node 1914 102.75 0 -2.367
node 2000 0 0 0.0
node 2001 11.575 0 0.0
node 2002 14.675 0 0.0
node 2003 26.875 0 0.0
node 2004 29.975 0 0.0
node 2005 42.175 0 0.0
node 2006 45.275 0 0.0
node 2007 51.375 0 0.0
node 2008 57.475 0 0.0
node 2009 60.575 0 0.0
node 2010 72.775 0 0.0
node 2011 75.875 0 0.0
node 2012 88.075 0 0.0
node 2013 91.175 0 0.0
node 2014 102.75 0 0.0
node 2100 0 0 2.367
node 2101 11.575 0 2.367; # support node
node 2102 14.675 0 2.367; # support node
node 2103 26.875 0 2.367; # support node
node 2104 29.975 0 2.367; # support node
node 2105 42.175 0 2.367; # support node
node 2106 45.275 0 2.367; # support node
node 2107 51.375 0 2.367
node 2108 57.475 0 2.367; # support node
node 2109 60.575 0 2.367; # support node
node 2110 72.775 0 2.367; # support node
node 2111 75.875 0 2.367; # support node
node 2112 88.075 0 2.367; # support node
node 2113 91.175 0 2.367; # support node
node 2114 102.75 0 2.367
node 2200 0 0 2.889
node 2201 11.575 0 2.889
node 2202 14.675 0 2.889
node 2203 26.875 0 2.889
node 2204 29.975 0 2.889
node 2205 42.175 0 2.889
node 2206 45.275 0 2.889
node 2207 51.375 0 2.889
node 2208 57.475 0 2.889
node 2209 60.575 0 2.889
node 2210 72.775 0 2.889
node 2211 75.875 0 2.889
node 2212 88.075 0 2.889
node 2213 91.175 0 2.889
node 2214 102.75 0 2.889
node 2300 0 0 2.89
node 2301 11.575 0 2.89
node 2302 14.675 0 2.89
node 2303 26.875 0 2.89
node 2304 29.975 0 2.89
node 2305 42.175 0 2.89
node 2306 45.275 0 2.89
node 2307 51.375 0 2.89
node 2308 57.475 0 2.89
node 2309 60.575 0 2.89
node 2310 72.775 0 2.89
node 2311 75.875 0 2.89
node 2312 88.075 0 2.89
node 2313 91.175 0 2.89
node 2314 102.75 0 2.89
node 2400 0 0 4.2
node 2401 11.575 0 4.2; # support node
node 2402 14.675 0 4.2; # support node
node 2403 26.875 0 4.2; # support node
node 2404 29.975 0 4.2; # support node
node 2405 42.175 0 4.2; # support node
node 2406 45.275 0 4.2; # support node
node 2407 51.375 0 4.2
node 2408 57.475 0 4.2; # support node
node 2409 60.575 0 4.2; # support node
node 2410 72.775 0 4.2; # support node
node 2411 75.875 0 4.2; # support node
node 2412 88.075 0 4.2; # support node
node 2413 91.175 0 4.2; # support node
node 2414 102.75 0 4.2
node 2500 0 0 5.299
node 2501 11.575 0 5.299
node 2502 14.675 0 5.299
node 2503 26.875 0 5.299
node 2504 29.975 0 5.299
node 2505 42.175 0 5.299
node 2506 45.275 0 5.299
node 2507 51.375 0 5.299
node 2508 57.475 0 5.299
node 2509 60.575 0 5.299
node 2510 72.775 0 5.299
node 2511 75.875 0 5.299
node 2512 88.075 0 5.299
node 2513 91.175 0 5.299
node 2514 102.75 0 5.299
node 2600 0 0 5.3
node 2601 11.575 0 5.3
node 2602 14.675 0 5.3
node 2603 26.875 0 5.3
node 2604 29.975 0 5.3
node 2605 42.175 0 5.3
node 2606 45.275 0 5.3
node 2607 51.375 0 5.3
node 2608 57.475 0 5.3
node 2609 60.575 0 5.3
node 2610 72.775 0 5.3
node 2611 75.875 0 5.3
node 2612 88.075 0 5.3
node 2613 91.175 0 5.3
node 2614 102.75 0 5.3
node 2700 0 0 5.499
node 2701 11.575 0 5.499
node 2702 14.675 0 5.499
node 2703 26.875 0 5.499
node 2704 29.975 0 5.499
node 2705 42.175 0 5.499
node 2706 45.275 0 5.499
node 2707 51.375 0 5.499
node 2708 57.475 0 5.499
node 2709 60.575 0 5.499
node 2710 72.775 0 5.499
node 2711 75.875 0 5.499
node 2712 88.075 0 5.499
node 2713 91.175 0 5.499
node 2714 102.75 0 5.499
node 2800 0 0 5.5
node 2801 11.575 0 5.5
node 2802 14.675 0 5.5
node 2803 26.875 0 5.5
node 2804 29.975 0 5.5
node 2805 42.175 0 5.5
node 2806 45.275 0 5.5
node 2807 51.375 0 5.5
node 2808 57.475 0 5.5
node 2809 60.575 0 5.5
node 2810 72.775 0 5.5
node 2811 75.875 0 5.5
node 2812 88.075 0 5.5
node 2813 91.175 0 5.5
node 2814 102.75 0 5.5
node 2900 0 0 6.033
node 2901 11.575 0 6.033; # support node
node 2902 14.675 0 6.033; # support node
node 2903 26.875 0 6.033; # support node
node 2904 29.975 0 6.033; # support node
node 2905 42.175 0 6.033; # support node
node 2906 45.275 0 6.033; # support node
node 2907 51.375 0 6.033
node 2908 57.475 0 6.033; # support node
node 2909 60.575 0 6.033; # support node
node 2910 72.775 0 6.033; # support node
node 2911 75.875 0 6.033; # support node
node 2912 88.075 0 6.033; # support node
node 2913 91.175 0 6.033; # support node
node 2914 102.75 0 6.033
node 3000 0 0 10.767
node 3001 11.575 0 10.767; # support node
node 3002 14.675 0 10.767; # support node
node 3003 26.875 0 10.767; # support node
node 3004 29.975 0 10.767; # support node
node 3005 42.175 0 10.767; # support node
node 3006 45.275 0 10.767; # support node
node 3007 51.375 0 10.767
node 3008 57.475 0 10.767; # support node
node 3009 60.575 0 10.767; # support node
node 3010 72.775 0 10.767; # support node
node 3011 75.875 0 10.767; # support node
node 3012 88.075 0 10.767; # support node
node 3013 91.175 0 10.767; # support node
node 3014 102.75 0 10.767
node 3100 0 0 12.6
node 3101 11.575 0 12.6; # support node
node 3102 14.675 0 12.6; # support node
node 3103 26.875 0 12.6; # support node
node 3104 29.975 0 12.6; # support node
node 3105 42.175 0 12.6; # support node
node 3106 45.275 0 12.6; # support node
node 3107 51.375 0 12.6
node 3108 57.475 0 12.6; # support node
node 3109 60.575 0 12.6; # support node
node 3110 72.775 0 12.6; # support node
node 3111 75.875 0 12.6; # support node
node 3112 88.075 0 12.6; # support node
node 3113 91.175 0 12.6; # support node
node 3114 102.75 0 12.6
node 3200 0 0 12.749
node 3201 11.575 0 12.749
node 3202 14.675 0 12.749
node 3203 26.875 0 12.749
node 3204 29.975 0 12.749
node 3205 42.175 0 12.749
node 3206 45.275 0 12.749
node 3207 51.375 0 12.749
node 3208 57.475 0 12.749
node 3209 60.575 0 12.749
node 3210 72.775 0 12.749
node 3211 75.875 0 12.749
node 3212 88.075 0 12.749
node 3213 91.175 0 12.749
node 3214 102.75 0 12.749
node 3300 0 0 12.75
node 3301 11.575 0 12.75
node 3302 14.675 0 12.75
node 3303 26.875 0 12.75
node 3304 29.975 0 12.75
node 3305 42.175 0 12.75
node 3306 45.275 0 12.75
node 3307 51.375 0 12.75
node 3308 57.475 0 12.75
node 3309 60.575 0 12.75
node 3310 72.775 0 12.75
node 3311 75.875 0 12.75
node 3312 88.075 0 12.75
node 3313 91.175 0 12.75
node 3314 102.75 0 12.75
node 3400 0 0 12.949
node 3401 11.575 0 12.949
node 3402 14.675 0 12.949
node 3403 26.875 0 12.949
node 3404 29.975 0 12.949
node 3405 42.175 0 12.949
node 3406 45.275 0 12.949
node 3407 51.375 0 12.949
node 3408 57.475 0 12.949
node 3409 60.575 0 12.949
node 3410 72.775 0 12.949
node 3411 75.875 0 12.949
node 3412 88.075 0 12.949
node 3413 91.175 0 12.949
node 3414 102.75 0 12.949
node 3500 0 0 12.95
node 3501 11.575 0 12.95
node 3502 14.675 0 12.95
node 3503 26.875 0 12.95
node 3504 29.975 0 12.95
node 3505 42.175 0 12.95
node 3506 45.275 0 12.95
node 3507 51.375 0 12.95
node 3508 57.475 0 12.95
node 3509 60.575 0 12.95
node 3510 72.775 0 12.95
node 3511 75.875 0 12.95
node 3512 88.075 0 12.95
node 3513 91.175 0 12.95
node 3514 102.75 0 12.95
node 3600 0 0 14.433
node 3601 11.575 0 14.433; # support node
node 3602 14.675 0 14.433; # support node
node 3603 26.875 0 14.433; # support node
node 3604 29.975 0 14.433; # support node
node 3605 42.175 0 14.433; # support node
node 3606 45.275 0 14.433; # support node
node 3607 51.375 0 14.433
node 3608 57.475 0 14.433; # support node
node 3609 60.575 0 14.433; # support node
node 3610 72.775 0 14.433; # support node
node 3611 75.875 0 14.433; # support node
node 3612 88.075 0 14.433; # support node
node 3613 91.175 0 14.433; # support node
node 3614 102.75 0 14.433
node 3700 0 0 15.999
node 3701 11.575 0 15.999
node 3702 14.675 0 15.999
node 3703 26.875 0 15.999
node 3704 29.975 0 15.999
node 3705 42.175 0 15.999
node 3706 45.275 0 15.999
node 3707 51.375 0 15.999
node 3708 57.475 0 15.999
node 3709 60.575 0 15.999
node 3710 72.775 0 15.999
node 3711 75.875 0 15.999
node 3712 88.075 0 15.999
node 3713 91.175 0 15.999
node 3714 102.75 0 15.999
node 3800 0 0 16.0
node 3801 11.575 0 16.0
node 3802 14.675 0 16.0
node 3803 26.875 0 16.0
node 3804 29.975 0 16.0
node 3805 42.175 0 16.0
node 3806 45.275 0 16.0
node 3807 51.375 0 16.0
node 3808 57.475 0 16.0
node 3809 60.575 0 16.0
node 3810 72.775 0 16.0
node 3811 75.875 0 16.0
node 3812 88.075 0 16.0
node 3813 91.175 0 16.0
node 3814 102.75 0 16.0
node 3900 0 0 16.6
node 3901 11.575 0 16.6
node 3902 14.675 0 16.6
node 3903 26.875 0 16.6
node 3904 29.975 0 16.6
node 3905 42.175 0 16.6
node 3906 45.275 0 16.6
node 3907 51.375 0 16.6
node 3908 57.475 0 16.6
node 3909 60.575 0 16.6
node 3910 72.775 0 16.6
node 3911 75.875 0 16.6
node 3912 88.075 0 16.6
node 3913 91.175 0 16.6
node 3914 102.75 0 16.6
# End deck nodes

# node nodeTag x y z
# Begin support nodes
node 4000 12.35 -1.75 -13.9665; # support 1st wall 1st z 1 y 2nd
node 4001 13.125 -3.5 -13.5; # support 1st wall 1st z 1 y 3rd
node 4100 12.35 -1.75 -12.860924; # support 1st wall 1st z 2 y 2nd
node 4101 13.125 -3.5 -12.771849; # support 1st wall 1st z 2 y 3rd
node 4200 12.35 -1.75 -12.860179; # support 1st wall 1st z 3 y 2nd
node 4201 13.125 -3.5 -12.771358; # support 1st wall 1st z 3 y 3rd
node 4300 12.35 -1.75 -12.711825; # support 1st wall 1st z 4 y 2nd
node 4301 13.125 -3.5 -12.67365; # support 1st wall 1st z 4 y 3rd
node 4400 12.35 -1.75 -12.71108; # support 1st wall 1st z 5 y 2nd
node 4401 13.125 -3.5 -12.673159; # support 1st wall 1st z 5 y 3rd
node 4500 12.35 -1.75 -12.6; # support 1st wall 1st z 6 y 2nd
node 4501 13.125 -3.5 -12.6; # support 1st wall 1st z 6 y 3rd
node 4600 12.35 -1.75 -11.2335; # support 1st wall 1st z 7 y 2nd
node 4601 13.125 -3.5 -11.7; # support 1st wall 1st z 7 y 3rd
node 4700 13.9 -1.75 -13.9665; # support 1st wall 2nd z 1 y 2nd
node 4800 13.9 -1.75 -12.860924; # support 1st wall 2nd z 2 y 2nd
node 4900 13.9 -1.75 -12.860179; # support 1st wall 2nd z 3 y 2nd
node 5000 13.9 -1.75 -12.711825; # support 1st wall 2nd z 4 y 2nd
node 5100 13.9 -1.75 -12.71108; # support 1st wall 2nd z 5 y 2nd
node 5200 13.9 -1.75 -12.6; # support 1st wall 2nd z 6 y 2nd
node 5300 13.9 -1.75 -11.2335; # support 1st wall 2nd z 7 y 2nd
node 5400 12.35 -1.75 -5.5665; # support 2nd wall 1st z 1 y 2nd
node 5401 13.125 -3.5 -5.1; # support 2nd wall 1st z 1 y 3rd
node 5500 12.35 -1.75 -5.169149; # support 2nd wall 1st z 2 y 2nd
node 5501 13.125 -3.5 -4.838298; # support 2nd wall 1st z 2 y 3rd
node 5600 12.35 -1.75 -5.168404; # support 2nd wall 1st z 3 y 2nd
node 5601 13.125 -3.5 -4.837807; # support 2nd wall 1st z 3 y 3rd
node 5700 12.35 -1.75 -5.020049; # support 2nd wall 1st z 4 y 2nd
node 5701 13.125 -3.5 -4.740098; # support 2nd wall 1st z 4 y 3rd
node 5800 12.35 -1.75 -5.019304; # support 2nd wall 1st z 5 y 2nd
node 5801 13.125 -3.5 -4.739607; # support 2nd wall 1st z 5 y 3rd
node 5900 12.35 -1.75 -4.2; # support 2nd wall 1st z 6 y 2nd
node 5901 13.125 -3.5 -4.2; # support 2nd wall 1st z 6 y 3rd
node 6000 12.35 -1.75 -3.223396; # support 2nd wall 1st z 7 y 2nd
node 6001 13.125 -3.5 -3.556792; # support 2nd wall 1st z 7 y 3rd
node 6100 12.35 -1.75 -3.22265; # support 2nd wall 1st z 8 y 2nd
node 6101 13.125 -3.5 -3.556301; # support 2nd wall 1st z 8 y 3rd
node 6200 12.35 -1.75 -2.8335; # support 2nd wall 1st z 9 y 2nd
node 6201 13.125 -3.5 -3.3; # support 2nd wall 1st z 9 y 3rd
node 6300 13.9 -1.75 -5.5665; # support 2nd wall 2nd z 1 y 2nd
node 6400 13.9 -1.75 -5.169149; # support 2nd wall 2nd z 2 y 2nd
node 6500 13.9 -1.75 -5.168404; # support 2nd wall 2nd z 3 y 2nd
node 6600 13.9 -1.75 -5.020049; # support 2nd wall 2nd z 4 y 2nd
node 6700 13.9 -1.75 -5.019304; # support 2nd wall 2nd z 5 y 2nd
node 6800 13.9 -1.75 -4.2; # support 2nd wall 2nd z 6 y 2nd
node 6900 13.9 -1.75 -3.223396; # support 2nd wall 2nd z 7 y 2nd
node 7000 13.9 -1.75 -3.22265; # support 2nd wall 2nd z 8 y 2nd
node 7100 13.9 -1.75 -2.8335; # support 2nd wall 2nd z 9 y 2nd
node 7200 12.35 -1.75 2.8335; # support 3rd wall 1st z 1 y 2nd
node 7201 13.125 -3.5 3.3; # support 3rd wall 1st z 1 y 3rd
node 7300 12.35 -1.75 3.22265; # support 3rd wall 1st z 2 y 2nd
node 7301 13.125 -3.5 3.556301; # support 3rd wall 1st z 2 y 3rd
node 7400 12.35 -1.75 3.223396; # support 3rd wall 1st z 3 y 2nd
node 7401 13.125 -3.5 3.556792; # support 3rd wall 1st z 3 y 3rd
node 7500 12.35 -1.75 4.2; # support 3rd wall 1st z 4 y 2nd
node 7501 13.125 -3.5 4.2; # support 3rd wall 1st z 4 y 3rd
node 7600 12.35 -1.75 5.019304; # support 3rd wall 1st z 5 y 2nd
node 7601 13.125 -3.5 4.739607; # support 3rd wall 1st z 5 y 3rd
node 7700 12.35 -1.75 5.020049; # support 3rd wall 1st z 6 y 2nd
node 7701 13.125 -3.5 4.740098; # support 3rd wall 1st z 6 y 3rd
node 7800 12.35 -1.75 5.168404; # support 3rd wall 1st z 7 y 2nd
node 7801 13.125 -3.5 4.837807; # support 3rd wall 1st z 7 y 3rd
node 7900 12.35 -1.75 5.169149; # support 3rd wall 1st z 8 y 2nd
node 7901 13.125 -3.5 4.838298; # support 3rd wall 1st z 8 y 3rd
node 8000 12.35 -1.75 5.5665; # support 3rd wall 1st z 9 y 2nd
node 8001 13.125 -3.5 5.1; # support 3rd wall 1st z 9 y 3rd
node 8100 13.9 -1.75 2.8335; # support 3rd wall 2nd z 1 y 2nd
node 8200 13.9 -1.75 3.22265; # support 3rd wall 2nd z 2 y 2nd
node 8300 13.9 -1.75 3.223396; # support 3rd wall 2nd z 3 y 2nd
node 8400 13.9 -1.75 4.2; # support 3rd wall 2nd z 4 y 2nd
node 8500 13.9 -1.75 5.019304; # support 3rd wall 2nd z 5 y 2nd
node 8600 13.9 -1.75 5.020049; # support 3rd wall 2nd z 6 y 2nd
node 8700 13.9 -1.75 5.168404; # support 3rd wall 2nd z 7 y 2nd
node 8800 13.9 -1.75 5.169149; # support 3rd wall 2nd z 8 y 2nd
node 8900 13.9 -1.75 5.5665; # support 3rd wall 2nd z 9 y 2nd
node 9000 12.35 -1.75 11.2335; # support 4th wall 1st z 1 y 2nd
node 9001 13.125 -3.5 11.7; # support 4th wall 1st z 1 y 3rd
node 9100 12.35 -1.75 12.6; # support 4th wall 1st z 2 y 2nd
node 9101 13.125 -3.5 12.6; # support 4th wall 1st z 2 y 3rd
node 9200 12.35 -1.75 12.71108; # support 4th wall 1st z 3 y 2nd
node 9201 13.125 -3.5 12.673159; # support 4th wall 1st z 3 y 3rd
node 9300 12.35 -1.75 12.711825; # support 4th wall 1st z 4 y 2nd
node 9301 13.125 -3.5 12.67365; # support 4th wall 1st z 4 y 3rd
node 9400 12.35 -1.75 12.860179; # support 4th wall 1st z 5 y 2nd
node 9401 13.125 -3.5 12.771358; # support 4th wall 1st z 5 y 3rd
node 9500 12.35 -1.75 12.860924; # support 4th wall 1st z 6 y 2nd
node 9501 13.125 -3.5 12.771849; # support 4th wall 1st z 6 y 3rd
node 9600 12.35 -1.75 13.9665; # support 4th wall 1st z 7 y 2nd
node 9601 13.125 -3.5 13.5; # support 4th wall 1st z 7 y 3rd
node 9700 13.9 -1.75 11.2335; # support 4th wall 2nd z 1 y 2nd
node 9800 13.9 -1.75 12.6; # support 4th wall 2nd z 2 y 2nd
node 9900 13.9 -1.75 12.71108; # support 4th wall 2nd z 3 y 2nd
node 10000 13.9 -1.75 12.711825; # support 4th wall 2nd z 4 y 2nd
node 10100 13.9 -1.75 12.860179; # support 4th wall 2nd z 5 y 2nd
node 10200 13.9 -1.75 12.860924; # support 4th wall 2nd z 6 y 2nd
node 10300 13.9 -1.75 13.9665; # support 4th wall 2nd z 7 y 2nd
node 10400 27.65 -1.75 -13.9665; # support 5th wall 1st z 1 y 2nd
node 10401 28.425 -3.5 -13.5; # support 5th wall 1st z 1 y 3rd
node 10500 27.65 -1.75 -12.860924; # support 5th wall 1st z 2 y 2nd
node 10501 28.425 -3.5 -12.771849; # support 5th wall 1st z 2 y 3rd
node 10600 27.65 -1.75 -12.860179; # support 5th wall 1st z 3 y 2nd
node 10601 28.425 -3.5 -12.771358; # support 5th wall 1st z 3 y 3rd
node 10700 27.65 -1.75 -12.711825; # support 5th wall 1st z 4 y 2nd
node 10701 28.425 -3.5 -12.67365; # support 5th wall 1st z 4 y 3rd
node 10800 27.65 -1.75 -12.71108; # support 5th wall 1st z 5 y 2nd
node 10801 28.425 -3.5 -12.673159; # support 5th wall 1st z 5 y 3rd
node 10900 27.65 -1.75 -12.6; # support 5th wall 1st z 6 y 2nd
node 10901 28.425 -3.5 -12.6; # support 5th wall 1st z 6 y 3rd
node 11000 27.65 -1.75 -11.2335; # support 5th wall 1st z 7 y 2nd
node 11001 28.425 -3.5 -11.7; # support 5th wall 1st z 7 y 3rd
node 11100 29.2 -1.75 -13.9665; # support 5th wall 2nd z 1 y 2nd
node 11200 29.2 -1.75 -12.860924; # support 5th wall 2nd z 2 y 2nd
node 11300 29.2 -1.75 -12.860179; # support 5th wall 2nd z 3 y 2nd
node 11400 29.2 -1.75 -12.711825; # support 5th wall 2nd z 4 y 2nd
node 11500 29.2 -1.75 -12.71108; # support 5th wall 2nd z 5 y 2nd
node 11600 29.2 -1.75 -12.6; # support 5th wall 2nd z 6 y 2nd
node 11700 29.2 -1.75 -11.2335; # support 5th wall 2nd z 7 y 2nd
node 11800 27.65 -1.75 -5.5665; # support 6th wall 1st z 1 y 2nd
node 11801 28.425 -3.5 -5.1; # support 6th wall 1st z 1 y 3rd
node 11900 27.65 -1.75 -5.169149; # support 6th wall 1st z 2 y 2nd
node 11901 28.425 -3.5 -4.838298; # support 6th wall 1st z 2 y 3rd
node 12000 27.65 -1.75 -5.168404; # support 6th wall 1st z 3 y 2nd
node 12001 28.425 -3.5 -4.837807; # support 6th wall 1st z 3 y 3rd
node 12100 27.65 -1.75 -5.020049; # support 6th wall 1st z 4 y 2nd
node 12101 28.425 -3.5 -4.740098; # support 6th wall 1st z 4 y 3rd
node 12200 27.65 -1.75 -5.019304; # support 6th wall 1st z 5 y 2nd
node 12201 28.425 -3.5 -4.739607; # support 6th wall 1st z 5 y 3rd
node 12300 27.65 -1.75 -4.2; # support 6th wall 1st z 6 y 2nd
node 12301 28.425 -3.5 -4.2; # support 6th wall 1st z 6 y 3rd
node 12400 27.65 -1.75 -3.223396; # support 6th wall 1st z 7 y 2nd
node 12401 28.425 -3.5 -3.556792; # support 6th wall 1st z 7 y 3rd
node 12500 27.65 -1.75 -3.22265; # support 6th wall 1st z 8 y 2nd
node 12501 28.425 -3.5 -3.556301; # support 6th wall 1st z 8 y 3rd
node 12600 27.65 -1.75 -2.8335; # support 6th wall 1st z 9 y 2nd
node 12601 28.425 -3.5 -3.3; # support 6th wall 1st z 9 y 3rd
node 12700 29.2 -1.75 -5.5665; # support 6th wall 2nd z 1 y 2nd
node 12800 29.2 -1.75 -5.169149; # support 6th wall 2nd z 2 y 2nd
node 12900 29.2 -1.75 -5.168404; # support 6th wall 2nd z 3 y 2nd
node 13000 29.2 -1.75 -5.020049; # support 6th wall 2nd z 4 y 2nd
node 13100 29.2 -1.75 -5.019304; # support 6th wall 2nd z 5 y 2nd
node 13200 29.2 -1.75 -4.2; # support 6th wall 2nd z 6 y 2nd
node 13300 29.2 -1.75 -3.223396; # support 6th wall 2nd z 7 y 2nd
node 13400 29.2 -1.75 -3.22265; # support 6th wall 2nd z 8 y 2nd
node 13500 29.2 -1.75 -2.8335; # support 6th wall 2nd z 9 y 2nd
node 13600 27.65 -1.75 2.8335; # support 7th wall 1st z 1 y 2nd
node 13601 28.425 -3.5 3.3; # support 7th wall 1st z 1 y 3rd
node 13700 27.65 -1.75 3.22265; # support 7th wall 1st z 2 y 2nd
node 13701 28.425 -3.5 3.556301; # support 7th wall 1st z 2 y 3rd
node 13800 27.65 -1.75 3.223396; # support 7th wall 1st z 3 y 2nd
node 13801 28.425 -3.5 3.556792; # support 7th wall 1st z 3 y 3rd
node 13900 27.65 -1.75 4.2; # support 7th wall 1st z 4 y 2nd
node 13901 28.425 -3.5 4.2; # support 7th wall 1st z 4 y 3rd
node 14000 27.65 -1.75 5.019304; # support 7th wall 1st z 5 y 2nd
node 14001 28.425 -3.5 4.739607; # support 7th wall 1st z 5 y 3rd
node 14100 27.65 -1.75 5.020049; # support 7th wall 1st z 6 y 2nd
node 14101 28.425 -3.5 4.740098; # support 7th wall 1st z 6 y 3rd
node 14200 27.65 -1.75 5.168404; # support 7th wall 1st z 7 y 2nd
node 14201 28.425 -3.5 4.837807; # support 7th wall 1st z 7 y 3rd
node 14300 27.65 -1.75 5.169149; # support 7th wall 1st z 8 y 2nd
node 14301 28.425 -3.5 4.838298; # support 7th wall 1st z 8 y 3rd
node 14400 27.65 -1.75 5.5665; # support 7th wall 1st z 9 y 2nd
node 14401 28.425 -3.5 5.1; # support 7th wall 1st z 9 y 3rd
node 14500 29.2 -1.75 2.8335; # support 7th wall 2nd z 1 y 2nd
node 14600 29.2 -1.75 3.22265; # support 7th wall 2nd z 2 y 2nd
node 14700 29.2 -1.75 3.223396; # support 7th wall 2nd z 3 y 2nd
node 14800 29.2 -1.75 4.2; # support 7th wall 2nd z 4 y 2nd
node 14900 29.2 -1.75 5.019304; # support 7th wall 2nd z 5 y 2nd
node 15000 29.2 -1.75 5.020049; # support 7th wall 2nd z 6 y 2nd
node 15100 29.2 -1.75 5.168404; # support 7th wall 2nd z 7 y 2nd
node 15200 29.2 -1.75 5.169149; # support 7th wall 2nd z 8 y 2nd
node 15300 29.2 -1.75 5.5665; # support 7th wall 2nd z 9 y 2nd
node 15400 27.65 -1.75 11.2335; # support 8th wall 1st z 1 y 2nd
node 15401 28.425 -3.5 11.7; # support 8th wall 1st z 1 y 3rd
node 15500 27.65 -1.75 12.6; # support 8th wall 1st z 2 y 2nd
node 15501 28.425 -3.5 12.6; # support 8th wall 1st z 2 y 3rd
node 15600 27.65 -1.75 12.71108; # support 8th wall 1st z 3 y 2nd
node 15601 28.425 -3.5 12.673159; # support 8th wall 1st z 3 y 3rd
node 15700 27.65 -1.75 12.711825; # support 8th wall 1st z 4 y 2nd
node 15701 28.425 -3.5 12.67365; # support 8th wall 1st z 4 y 3rd
node 15800 27.65 -1.75 12.860179; # support 8th wall 1st z 5 y 2nd
node 15801 28.425 -3.5 12.771358; # support 8th wall 1st z 5 y 3rd
node 15900 27.65 -1.75 12.860924; # support 8th wall 1st z 6 y 2nd
node 15901 28.425 -3.5 12.771849; # support 8th wall 1st z 6 y 3rd
node 16000 27.65 -1.75 13.9665; # support 8th wall 1st z 7 y 2nd
node 16001 28.425 -3.5 13.5; # support 8th wall 1st z 7 y 3rd
node 16100 29.2 -1.75 11.2335; # support 8th wall 2nd z 1 y 2nd
node 16200 29.2 -1.75 12.6; # support 8th wall 2nd z 2 y 2nd
node 16300 29.2 -1.75 12.71108; # support 8th wall 2nd z 3 y 2nd
node 16400 29.2 -1.75 12.711825; # support 8th wall 2nd z 4 y 2nd
node 16500 29.2 -1.75 12.860179; # support 8th wall 2nd z 5 y 2nd
node 16600 29.2 -1.75 12.860924; # support 8th wall 2nd z 6 y 2nd
node 16700 29.2 -1.75 13.9665; # support 8th wall 2nd z 7 y 2nd
node 16800 42.95 -1.75 -13.9665; # support 9th wall 1st z 1 y 2nd
node 16801 43.725 -3.5 -13.5; # support 9th wall 1st z 1 y 3rd
node 16900 42.95 -1.75 -12.860924; # support 9th wall 1st z 2 y 2nd
node 16901 43.725 -3.5 -12.771849; # support 9th wall 1st z 2 y 3rd
node 17000 42.95 -1.75 -12.860179; # support 9th wall 1st z 3 y 2nd
node 17001 43.725 -3.5 -12.771358; # support 9th wall 1st z 3 y 3rd
node 17100 42.95 -1.75 -12.711825; # support 9th wall 1st z 4 y 2nd
node 17101 43.725 -3.5 -12.67365; # support 9th wall 1st z 4 y 3rd
node 17200 42.95 -1.75 -12.71108; # support 9th wall 1st z 5 y 2nd
node 17201 43.725 -3.5 -12.673159; # support 9th wall 1st z 5 y 3rd
node 17300 42.95 -1.75 -12.6; # support 9th wall 1st z 6 y 2nd
node 17301 43.725 -3.5 -12.6; # support 9th wall 1st z 6 y 3rd
node 17400 42.95 -1.75 -11.2335; # support 9th wall 1st z 7 y 2nd
node 17401 43.725 -3.5 -11.7; # support 9th wall 1st z 7 y 3rd
node 17500 44.5 -1.75 -13.9665; # support 9th wall 2nd z 1 y 2nd
node 17600 44.5 -1.75 -12.860924; # support 9th wall 2nd z 2 y 2nd
node 17700 44.5 -1.75 -12.860179; # support 9th wall 2nd z 3 y 2nd
node 17800 44.5 -1.75 -12.711825; # support 9th wall 2nd z 4 y 2nd
node 17900 44.5 -1.75 -12.71108; # support 9th wall 2nd z 5 y 2nd
node 18000 44.5 -1.75 -12.6; # support 9th wall 2nd z 6 y 2nd
node 18100 44.5 -1.75 -11.2335; # support 9th wall 2nd z 7 y 2nd
node 18200 42.95 -1.75 -5.5665; # support 10th wall 1st z 1 y 2nd
node 18201 43.725 -3.5 -5.1; # support 10th wall 1st z 1 y 3rd
node 18300 42.95 -1.75 -5.169149; # support 10th wall 1st z 2 y 2nd
node 18301 43.725 -3.5 -4.838298; # support 10th wall 1st z 2 y 3rd
node 18400 42.95 -1.75 -5.168404; # support 10th wall 1st z 3 y 2nd
node 18401 43.725 -3.5 -4.837807; # support 10th wall 1st z 3 y 3rd
node 18500 42.95 -1.75 -5.020049; # support 10th wall 1st z 4 y 2nd
node 18501 43.725 -3.5 -4.740098; # support 10th wall 1st z 4 y 3rd
node 18600 42.95 -1.75 -5.019304; # support 10th wall 1st z 5 y 2nd
node 18601 43.725 -3.5 -4.739607; # support 10th wall 1st z 5 y 3rd
node 18700 42.95 -1.75 -4.2; # support 10th wall 1st z 6 y 2nd
node 18701 43.725 -3.5 -4.2; # support 10th wall 1st z 6 y 3rd
node 18800 42.95 -1.75 -3.223396; # support 10th wall 1st z 7 y 2nd
node 18801 43.725 -3.5 -3.556792; # support 10th wall 1st z 7 y 3rd
node 18900 42.95 -1.75 -3.22265; # support 10th wall 1st z 8 y 2nd
node 18901 43.725 -3.5 -3.556301; # support 10th wall 1st z 8 y 3rd
node 19000 42.95 -1.75 -2.8335; # support 10th wall 1st z 9 y 2nd
node 19001 43.725 -3.5 -3.3; # support 10th wall 1st z 9 y 3rd
node 19100 44.5 -1.75 -5.5665; # support 10th wall 2nd z 1 y 2nd
node 19200 44.5 -1.75 -5.169149; # support 10th wall 2nd z 2 y 2nd
node 19300 44.5 -1.75 -5.168404; # support 10th wall 2nd z 3 y 2nd
node 19400 44.5 -1.75 -5.020049; # support 10th wall 2nd z 4 y 2nd
node 19500 44.5 -1.75 -5.019304; # support 10th wall 2nd z 5 y 2nd
node 19600 44.5 -1.75 -4.2; # support 10th wall 2nd z 6 y 2nd
node 19700 44.5 -1.75 -3.223396; # support 10th wall 2nd z 7 y 2nd
node 19800 44.5 -1.75 -3.22265; # support 10th wall 2nd z 8 y 2nd
node 19900 44.5 -1.75 -2.8335; # support 10th wall 2nd z 9 y 2nd
node 20000 42.95 -1.75 2.8335; # support 11th wall 1st z 1 y 2nd
node 20001 43.725 -3.5 3.3; # support 11th wall 1st z 1 y 3rd
node 20100 42.95 -1.75 3.22265; # support 11th wall 1st z 2 y 2nd
node 20101 43.725 -3.5 3.556301; # support 11th wall 1st z 2 y 3rd
node 20200 42.95 -1.75 3.223396; # support 11th wall 1st z 3 y 2nd
node 20201 43.725 -3.5 3.556792; # support 11th wall 1st z 3 y 3rd
node 20300 42.95 -1.75 4.2; # support 11th wall 1st z 4 y 2nd
node 20301 43.725 -3.5 4.2; # support 11th wall 1st z 4 y 3rd
node 20400 42.95 -1.75 5.019304; # support 11th wall 1st z 5 y 2nd
node 20401 43.725 -3.5 4.739607; # support 11th wall 1st z 5 y 3rd
node 20500 42.95 -1.75 5.020049; # support 11th wall 1st z 6 y 2nd
node 20501 43.725 -3.5 4.740098; # support 11th wall 1st z 6 y 3rd
node 20600 42.95 -1.75 5.168404; # support 11th wall 1st z 7 y 2nd
node 20601 43.725 -3.5 4.837807; # support 11th wall 1st z 7 y 3rd
node 20700 42.95 -1.75 5.169149; # support 11th wall 1st z 8 y 2nd
node 20701 43.725 -3.5 4.838298; # support 11th wall 1st z 8 y 3rd
node 20800 42.95 -1.75 5.5665; # support 11th wall 1st z 9 y 2nd
node 20801 43.725 -3.5 5.1; # support 11th wall 1st z 9 y 3rd
node 20900 44.5 -1.75 2.8335; # support 11th wall 2nd z 1 y 2nd
node 21000 44.5 -1.75 3.22265; # support 11th wall 2nd z 2 y 2nd
node 21100 44.5 -1.75 3.223396; # support 11th wall 2nd z 3 y 2nd
node 21200 44.5 -1.75 4.2; # support 11th wall 2nd z 4 y 2nd
node 21300 44.5 -1.75 5.019304; # support 11th wall 2nd z 5 y 2nd
node 21400 44.5 -1.75 5.020049; # support 11th wall 2nd z 6 y 2nd
node 21500 44.5 -1.75 5.168404; # support 11th wall 2nd z 7 y 2nd
node 21600 44.5 -1.75 5.169149; # support 11th wall 2nd z 8 y 2nd
node 21700 44.5 -1.75 5.5665; # support 11th wall 2nd z 9 y 2nd
node 21800 42.95 -1.75 11.2335; # support 12th wall 1st z 1 y 2nd
node 21801 43.725 -3.5 11.7; # support 12th wall 1st z 1 y 3rd
node 21900 42.95 -1.75 12.6; # support 12th wall 1st z 2 y 2nd
node 21901 43.725 -3.5 12.6; # support 12th wall 1st z 2 y 3rd
node 22000 42.95 -1.75 12.71108; # support 12th wall 1st z 3 y 2nd
node 22001 43.725 -3.5 12.673159; # support 12th wall 1st z 3 y 3rd
node 22100 42.95 -1.75 12.711825; # support 12th wall 1st z 4 y 2nd
node 22101 43.725 -3.5 12.67365; # support 12th wall 1st z 4 y 3rd
node 22200 42.95 -1.75 12.860179; # support 12th wall 1st z 5 y 2nd
node 22201 43.725 -3.5 12.771358; # support 12th wall 1st z 5 y 3rd
node 22300 42.95 -1.75 12.860924; # support 12th wall 1st z 6 y 2nd
node 22301 43.725 -3.5 12.771849; # support 12th wall 1st z 6 y 3rd
node 22400 42.95 -1.75 13.9665; # support 12th wall 1st z 7 y 2nd
node 22401 43.725 -3.5 13.5; # support 12th wall 1st z 7 y 3rd
node 22500 44.5 -1.75 11.2335; # support 12th wall 2nd z 1 y 2nd
node 22600 44.5 -1.75 12.6; # support 12th wall 2nd z 2 y 2nd
node 22700 44.5 -1.75 12.71108; # support 12th wall 2nd z 3 y 2nd
node 22800 44.5 -1.75 12.711825; # support 12th wall 2nd z 4 y 2nd
node 22900 44.5 -1.75 12.860179; # support 12th wall 2nd z 5 y 2nd
node 23000 44.5 -1.75 12.860924; # support 12th wall 2nd z 6 y 2nd
node 23100 44.5 -1.75 13.9665; # support 12th wall 2nd z 7 y 2nd
node 23200 58.25 -1.75 -13.9665; # support 13th wall 1st z 1 y 2nd
node 23201 59.025 -3.5 -13.5; # support 13th wall 1st z 1 y 3rd
node 23300 58.25 -1.75 -12.860924; # support 13th wall 1st z 2 y 2nd
node 23301 59.025 -3.5 -12.771849; # support 13th wall 1st z 2 y 3rd
node 23400 58.25 -1.75 -12.860179; # support 13th wall 1st z 3 y 2nd
node 23401 59.025 -3.5 -12.771358; # support 13th wall 1st z 3 y 3rd
node 23500 58.25 -1.75 -12.711825; # support 13th wall 1st z 4 y 2nd
node 23501 59.025 -3.5 -12.67365; # support 13th wall 1st z 4 y 3rd
node 23600 58.25 -1.75 -12.71108; # support 13th wall 1st z 5 y 2nd
node 23601 59.025 -3.5 -12.673159; # support 13th wall 1st z 5 y 3rd
node 23700 58.25 -1.75 -12.6; # support 13th wall 1st z 6 y 2nd
node 23701 59.025 -3.5 -12.6; # support 13th wall 1st z 6 y 3rd
node 23800 58.25 -1.75 -11.2335; # support 13th wall 1st z 7 y 2nd
node 23801 59.025 -3.5 -11.7; # support 13th wall 1st z 7 y 3rd
node 23900 59.8 -1.75 -13.9665; # support 13th wall 2nd z 1 y 2nd
node 24000 59.8 -1.75 -12.860924; # support 13th wall 2nd z 2 y 2nd
node 24100 59.8 -1.75 -12.860179; # support 13th wall 2nd z 3 y 2nd
node 24200 59.8 -1.75 -12.711825; # support 13th wall 2nd z 4 y 2nd
node 24300 59.8 -1.75 -12.71108; # support 13th wall 2nd z 5 y 2nd
node 24400 59.8 -1.75 -12.6; # support 13th wall 2nd z 6 y 2nd
node 24500 59.8 -1.75 -11.2335; # support 13th wall 2nd z 7 y 2nd
node 24600 58.25 -1.75 -5.5665; # support 14th wall 1st z 1 y 2nd
node 24601 59.025 -3.5 -5.1; # support 14th wall 1st z 1 y 3rd
node 24700 58.25 -1.75 -5.169149; # support 14th wall 1st z 2 y 2nd
node 24701 59.025 -3.5 -4.838298; # support 14th wall 1st z 2 y 3rd
node 24800 58.25 -1.75 -5.168404; # support 14th wall 1st z 3 y 2nd
node 24801 59.025 -3.5 -4.837807; # support 14th wall 1st z 3 y 3rd
node 24900 58.25 -1.75 -5.020049; # support 14th wall 1st z 4 y 2nd
node 24901 59.025 -3.5 -4.740098; # support 14th wall 1st z 4 y 3rd
node 25000 58.25 -1.75 -5.019304; # support 14th wall 1st z 5 y 2nd
node 25001 59.025 -3.5 -4.739607; # support 14th wall 1st z 5 y 3rd
node 25100 58.25 -1.75 -4.2; # support 14th wall 1st z 6 y 2nd
node 25101 59.025 -3.5 -4.2; # support 14th wall 1st z 6 y 3rd
node 25200 58.25 -1.75 -3.223396; # support 14th wall 1st z 7 y 2nd
node 25201 59.025 -3.5 -3.556792; # support 14th wall 1st z 7 y 3rd
node 25300 58.25 -1.75 -3.22265; # support 14th wall 1st z 8 y 2nd
node 25301 59.025 -3.5 -3.556301; # support 14th wall 1st z 8 y 3rd
node 25400 58.25 -1.75 -2.8335; # support 14th wall 1st z 9 y 2nd
node 25401 59.025 -3.5 -3.3; # support 14th wall 1st z 9 y 3rd
node 25500 59.8 -1.75 -5.5665; # support 14th wall 2nd z 1 y 2nd
node 25600 59.8 -1.75 -5.169149; # support 14th wall 2nd z 2 y 2nd
node 25700 59.8 -1.75 -5.168404; # support 14th wall 2nd z 3 y 2nd
node 25800 59.8 -1.75 -5.020049; # support 14th wall 2nd z 4 y 2nd
node 25900 59.8 -1.75 -5.019304; # support 14th wall 2nd z 5 y 2nd
node 26000 59.8 -1.75 -4.2; # support 14th wall 2nd z 6 y 2nd
node 26100 59.8 -1.75 -3.223396; # support 14th wall 2nd z 7 y 2nd
node 26200 59.8 -1.75 -3.22265; # support 14th wall 2nd z 8 y 2nd
node 26300 59.8 -1.75 -2.8335; # support 14th wall 2nd z 9 y 2nd
node 26400 58.25 -1.75 2.8335; # support 15th wall 1st z 1 y 2nd
node 26401 59.025 -3.5 3.3; # support 15th wall 1st z 1 y 3rd
node 26500 58.25 -1.75 3.22265; # support 15th wall 1st z 2 y 2nd
node 26501 59.025 -3.5 3.556301; # support 15th wall 1st z 2 y 3rd
node 26600 58.25 -1.75 3.223396; # support 15th wall 1st z 3 y 2nd
node 26601 59.025 -3.5 3.556792; # support 15th wall 1st z 3 y 3rd
node 26700 58.25 -1.75 4.2; # support 15th wall 1st z 4 y 2nd
node 26701 59.025 -3.5 4.2; # support 15th wall 1st z 4 y 3rd
node 26800 58.25 -1.75 5.019304; # support 15th wall 1st z 5 y 2nd
node 26801 59.025 -3.5 4.739607; # support 15th wall 1st z 5 y 3rd
node 26900 58.25 -1.75 5.020049; # support 15th wall 1st z 6 y 2nd
node 26901 59.025 -3.5 4.740098; # support 15th wall 1st z 6 y 3rd
node 27000 58.25 -1.75 5.168404; # support 15th wall 1st z 7 y 2nd
node 27001 59.025 -3.5 4.837807; # support 15th wall 1st z 7 y 3rd
node 27100 58.25 -1.75 5.169149; # support 15th wall 1st z 8 y 2nd
node 27101 59.025 -3.5 4.838298; # support 15th wall 1st z 8 y 3rd
node 27200 58.25 -1.75 5.5665; # support 15th wall 1st z 9 y 2nd
node 27201 59.025 -3.5 5.1; # support 15th wall 1st z 9 y 3rd
node 27300 59.8 -1.75 2.8335; # support 15th wall 2nd z 1 y 2nd
node 27400 59.8 -1.75 3.22265; # support 15th wall 2nd z 2 y 2nd
node 27500 59.8 -1.75 3.223396; # support 15th wall 2nd z 3 y 2nd
node 27600 59.8 -1.75 4.2; # support 15th wall 2nd z 4 y 2nd
node 27700 59.8 -1.75 5.019304; # support 15th wall 2nd z 5 y 2nd
node 27800 59.8 -1.75 5.020049; # support 15th wall 2nd z 6 y 2nd
node 27900 59.8 -1.75 5.168404; # support 15th wall 2nd z 7 y 2nd
node 28000 59.8 -1.75 5.169149; # support 15th wall 2nd z 8 y 2nd
node 28100 59.8 -1.75 5.5665; # support 15th wall 2nd z 9 y 2nd
node 28200 58.25 -1.75 11.2335; # support 16th wall 1st z 1 y 2nd
node 28201 59.025 -3.5 11.7; # support 16th wall 1st z 1 y 3rd
node 28300 58.25 -1.75 12.6; # support 16th wall 1st z 2 y 2nd
node 28301 59.025 -3.5 12.6; # support 16th wall 1st z 2 y 3rd
node 28400 58.25 -1.75 12.71108; # support 16th wall 1st z 3 y 2nd
node 28401 59.025 -3.5 12.673159; # support 16th wall 1st z 3 y 3rd
node 28500 58.25 -1.75 12.711825; # support 16th wall 1st z 4 y 2nd
node 28501 59.025 -3.5 12.67365; # support 16th wall 1st z 4 y 3rd
node 28600 58.25 -1.75 12.860179; # support 16th wall 1st z 5 y 2nd
node 28601 59.025 -3.5 12.771358; # support 16th wall 1st z 5 y 3rd
node 28700 58.25 -1.75 12.860924; # support 16th wall 1st z 6 y 2nd
node 28701 59.025 -3.5 12.771849; # support 16th wall 1st z 6 y 3rd
node 28800 58.25 -1.75 13.9665; # support 16th wall 1st z 7 y 2nd
node 28801 59.025 -3.5 13.5; # support 16th wall 1st z 7 y 3rd
node 28900 59.8 -1.75 11.2335; # support 16th wall 2nd z 1 y 2nd
node 29000 59.8 -1.75 12.6; # support 16th wall 2nd z 2 y 2nd
node 29100 59.8 -1.75 12.71108; # support 16th wall 2nd z 3 y 2nd
node 29200 59.8 -1.75 12.711825; # support 16th wall 2nd z 4 y 2nd
node 29300 59.8 -1.75 12.860179; # support 16th wall 2nd z 5 y 2nd
node 29400 59.8 -1.75 12.860924; # support 16th wall 2nd z 6 y 2nd
node 29500 59.8 -1.75 13.9665; # support 16th wall 2nd z 7 y 2nd
node 29600 73.55 -1.75 -13.9665; # support 17th wall 1st z 1 y 2nd
node 29601 74.325 -3.5 -13.5; # support 17th wall 1st z 1 y 3rd
node 29700 73.55 -1.75 -12.860924; # support 17th wall 1st z 2 y 2nd
node 29701 74.325 -3.5 -12.771849; # support 17th wall 1st z 2 y 3rd
node 29800 73.55 -1.75 -12.860179; # support 17th wall 1st z 3 y 2nd
node 29801 74.325 -3.5 -12.771358; # support 17th wall 1st z 3 y 3rd
node 29900 73.55 -1.75 -12.711825; # support 17th wall 1st z 4 y 2nd
node 29901 74.325 -3.5 -12.67365; # support 17th wall 1st z 4 y 3rd
node 30000 73.55 -1.75 -12.71108; # support 17th wall 1st z 5 y 2nd
node 30001 74.325 -3.5 -12.673159; # support 17th wall 1st z 5 y 3rd
node 30100 73.55 -1.75 -12.6; # support 17th wall 1st z 6 y 2nd
node 30101 74.325 -3.5 -12.6; # support 17th wall 1st z 6 y 3rd
node 30200 73.55 -1.75 -11.2335; # support 17th wall 1st z 7 y 2nd
node 30201 74.325 -3.5 -11.7; # support 17th wall 1st z 7 y 3rd
node 30300 75.1 -1.75 -13.9665; # support 17th wall 2nd z 1 y 2nd
node 30400 75.1 -1.75 -12.860924; # support 17th wall 2nd z 2 y 2nd
node 30500 75.1 -1.75 -12.860179; # support 17th wall 2nd z 3 y 2nd
node 30600 75.1 -1.75 -12.711825; # support 17th wall 2nd z 4 y 2nd
node 30700 75.1 -1.75 -12.71108; # support 17th wall 2nd z 5 y 2nd
node 30800 75.1 -1.75 -12.6; # support 17th wall 2nd z 6 y 2nd
node 30900 75.1 -1.75 -11.2335; # support 17th wall 2nd z 7 y 2nd
node 31000 73.55 -1.75 -5.5665; # support 18th wall 1st z 1 y 2nd
node 31001 74.325 -3.5 -5.1; # support 18th wall 1st z 1 y 3rd
node 31100 73.55 -1.75 -5.169149; # support 18th wall 1st z 2 y 2nd
node 31101 74.325 -3.5 -4.838298; # support 18th wall 1st z 2 y 3rd
node 31200 73.55 -1.75 -5.168404; # support 18th wall 1st z 3 y 2nd
node 31201 74.325 -3.5 -4.837807; # support 18th wall 1st z 3 y 3rd
node 31300 73.55 -1.75 -5.020049; # support 18th wall 1st z 4 y 2nd
node 31301 74.325 -3.5 -4.740098; # support 18th wall 1st z 4 y 3rd
node 31400 73.55 -1.75 -5.019304; # support 18th wall 1st z 5 y 2nd
node 31401 74.325 -3.5 -4.739607; # support 18th wall 1st z 5 y 3rd
node 31500 73.55 -1.75 -4.2; # support 18th wall 1st z 6 y 2nd
node 31501 74.325 -3.5 -4.2; # support 18th wall 1st z 6 y 3rd
node 31600 73.55 -1.75 -3.223396; # support 18th wall 1st z 7 y 2nd
node 31601 74.325 -3.5 -3.556792; # support 18th wall 1st z 7 y 3rd
node 31700 73.55 -1.75 -3.22265; # support 18th wall 1st z 8 y 2nd
node 31701 74.325 -3.5 -3.556301; # support 18th wall 1st z 8 y 3rd
node 31800 73.55 -1.75 -2.8335; # support 18th wall 1st z 9 y 2nd
node 31801 74.325 -3.5 -3.3; # support 18th wall 1st z 9 y 3rd
node 31900 75.1 -1.75 -5.5665; # support 18th wall 2nd z 1 y 2nd
node 32000 75.1 -1.75 -5.169149; # support 18th wall 2nd z 2 y 2nd
node 32100 75.1 -1.75 -5.168404; # support 18th wall 2nd z 3 y 2nd
node 32200 75.1 -1.75 -5.020049; # support 18th wall 2nd z 4 y 2nd
node 32300 75.1 -1.75 -5.019304; # support 18th wall 2nd z 5 y 2nd
node 32400 75.1 -1.75 -4.2; # support 18th wall 2nd z 6 y 2nd
node 32500 75.1 -1.75 -3.223396; # support 18th wall 2nd z 7 y 2nd
node 32600 75.1 -1.75 -3.22265; # support 18th wall 2nd z 8 y 2nd
node 32700 75.1 -1.75 -2.8335; # support 18th wall 2nd z 9 y 2nd
node 32800 73.55 -1.75 2.8335; # support 19th wall 1st z 1 y 2nd
node 32801 74.325 -3.5 3.3; # support 19th wall 1st z 1 y 3rd
node 32900 73.55 -1.75 3.22265; # support 19th wall 1st z 2 y 2nd
node 32901 74.325 -3.5 3.556301; # support 19th wall 1st z 2 y 3rd
node 33000 73.55 -1.75 3.223396; # support 19th wall 1st z 3 y 2nd
node 33001 74.325 -3.5 3.556792; # support 19th wall 1st z 3 y 3rd
node 33100 73.55 -1.75 4.2; # support 19th wall 1st z 4 y 2nd
node 33101 74.325 -3.5 4.2; # support 19th wall 1st z 4 y 3rd
node 33200 73.55 -1.75 5.019304; # support 19th wall 1st z 5 y 2nd
node 33201 74.325 -3.5 4.739607; # support 19th wall 1st z 5 y 3rd
node 33300 73.55 -1.75 5.020049; # support 19th wall 1st z 6 y 2nd
node 33301 74.325 -3.5 4.740098; # support 19th wall 1st z 6 y 3rd
node 33400 73.55 -1.75 5.168404; # support 19th wall 1st z 7 y 2nd
node 33401 74.325 -3.5 4.837807; # support 19th wall 1st z 7 y 3rd
node 33500 73.55 -1.75 5.169149; # support 19th wall 1st z 8 y 2nd
node 33501 74.325 -3.5 4.838298; # support 19th wall 1st z 8 y 3rd
node 33600 73.55 -1.75 5.5665; # support 19th wall 1st z 9 y 2nd
node 33601 74.325 -3.5 5.1; # support 19th wall 1st z 9 y 3rd
node 33700 75.1 -1.75 2.8335; # support 19th wall 2nd z 1 y 2nd
node 33800 75.1 -1.75 3.22265; # support 19th wall 2nd z 2 y 2nd
node 33900 75.1 -1.75 3.223396; # support 19th wall 2nd z 3 y 2nd
node 34000 75.1 -1.75 4.2; # support 19th wall 2nd z 4 y 2nd
node 34100 75.1 -1.75 5.019304; # support 19th wall 2nd z 5 y 2nd
node 34200 75.1 -1.75 5.020049; # support 19th wall 2nd z 6 y 2nd
node 34300 75.1 -1.75 5.168404; # support 19th wall 2nd z 7 y 2nd
node 34400 75.1 -1.75 5.169149; # support 19th wall 2nd z 8 y 2nd
node 34500 75.1 -1.75 5.5665; # support 19th wall 2nd z 9 y 2nd
node 34600 73.55 -1.75 11.2335; # support 20th wall 1st z 1 y 2nd
node 34601 74.325 -3.5 11.7; # support 20th wall 1st z 1 y 3rd
node 34700 73.55 -1.75 12.6; # support 20th wall 1st z 2 y 2nd
node 34701 74.325 -3.5 12.6; # support 20th wall 1st z 2 y 3rd
node 34800 73.55 -1.75 12.71108; # support 20th wall 1st z 3 y 2nd
node 34801 74.325 -3.5 12.673159; # support 20th wall 1st z 3 y 3rd
node 34900 73.55 -1.75 12.711825; # support 20th wall 1st z 4 y 2nd
node 34901 74.325 -3.5 12.67365; # support 20th wall 1st z 4 y 3rd
node 35000 73.55 -1.75 12.860179; # support 20th wall 1st z 5 y 2nd
node 35001 74.325 -3.5 12.771358; # support 20th wall 1st z 5 y 3rd
node 35100 73.55 -1.75 12.860924; # support 20th wall 1st z 6 y 2nd
node 35101 74.325 -3.5 12.771849; # support 20th wall 1st z 6 y 3rd
node 35200 73.55 -1.75 13.9665; # support 20th wall 1st z 7 y 2nd
node 35201 74.325 -3.5 13.5; # support 20th wall 1st z 7 y 3rd
node 35300 75.1 -1.75 11.2335; # support 20th wall 2nd z 1 y 2nd
node 35400 75.1 -1.75 12.6; # support 20th wall 2nd z 2 y 2nd
node 35500 75.1 -1.75 12.71108; # support 20th wall 2nd z 3 y 2nd
node 35600 75.1 -1.75 12.711825; # support 20th wall 2nd z 4 y 2nd
node 35700 75.1 -1.75 12.860179; # support 20th wall 2nd z 5 y 2nd
node 35800 75.1 -1.75 12.860924; # support 20th wall 2nd z 6 y 2nd
node 35900 75.1 -1.75 13.9665; # support 20th wall 2nd z 7 y 2nd
node 36000 88.85 -1.75 -13.9665; # support 21st wall 1st z 1 y 2nd
node 36001 89.625 -3.5 -13.5; # support 21st wall 1st z 1 y 3rd
node 36100 88.85 -1.75 -12.860924; # support 21st wall 1st z 2 y 2nd
node 36101 89.625 -3.5 -12.771849; # support 21st wall 1st z 2 y 3rd
node 36200 88.85 -1.75 -12.860179; # support 21st wall 1st z 3 y 2nd
node 36201 89.625 -3.5 -12.771358; # support 21st wall 1st z 3 y 3rd
node 36300 88.85 -1.75 -12.711825; # support 21st wall 1st z 4 y 2nd
node 36301 89.625 -3.5 -12.67365; # support 21st wall 1st z 4 y 3rd
node 36400 88.85 -1.75 -12.71108; # support 21st wall 1st z 5 y 2nd
node 36401 89.625 -3.5 -12.673159; # support 21st wall 1st z 5 y 3rd
node 36500 88.85 -1.75 -12.6; # support 21st wall 1st z 6 y 2nd
node 36501 89.625 -3.5 -12.6; # support 21st wall 1st z 6 y 3rd
node 36600 88.85 -1.75 -11.2335; # support 21st wall 1st z 7 y 2nd
node 36601 89.625 -3.5 -11.7; # support 21st wall 1st z 7 y 3rd
node 36700 90.4 -1.75 -13.9665; # support 21st wall 2nd z 1 y 2nd
node 36800 90.4 -1.75 -12.860924; # support 21st wall 2nd z 2 y 2nd
node 36900 90.4 -1.75 -12.860179; # support 21st wall 2nd z 3 y 2nd
node 37000 90.4 -1.75 -12.711825; # support 21st wall 2nd z 4 y 2nd
node 37100 90.4 -1.75 -12.71108; # support 21st wall 2nd z 5 y 2nd
node 37200 90.4 -1.75 -12.6; # support 21st wall 2nd z 6 y 2nd
node 37300 90.4 -1.75 -11.2335; # support 21st wall 2nd z 7 y 2nd
node 37400 88.85 -1.75 -5.5665; # support 22nd wall 1st z 1 y 2nd
node 37401 89.625 -3.5 -5.1; # support 22nd wall 1st z 1 y 3rd
node 37500 88.85 -1.75 -5.169149; # support 22nd wall 1st z 2 y 2nd
node 37501 89.625 -3.5 -4.838298; # support 22nd wall 1st z 2 y 3rd
node 37600 88.85 -1.75 -5.168404; # support 22nd wall 1st z 3 y 2nd
node 37601 89.625 -3.5 -4.837807; # support 22nd wall 1st z 3 y 3rd
node 37700 88.85 -1.75 -5.020049; # support 22nd wall 1st z 4 y 2nd
node 37701 89.625 -3.5 -4.740098; # support 22nd wall 1st z 4 y 3rd
node 37800 88.85 -1.75 -5.019304; # support 22nd wall 1st z 5 y 2nd
node 37801 89.625 -3.5 -4.739607; # support 22nd wall 1st z 5 y 3rd
node 37900 88.85 -1.75 -4.2; # support 22nd wall 1st z 6 y 2nd
node 37901 89.625 -3.5 -4.2; # support 22nd wall 1st z 6 y 3rd
node 38000 88.85 -1.75 -3.223396; # support 22nd wall 1st z 7 y 2nd
node 38001 89.625 -3.5 -3.556792; # support 22nd wall 1st z 7 y 3rd
node 38100 88.85 -1.75 -3.22265; # support 22nd wall 1st z 8 y 2nd
node 38101 89.625 -3.5 -3.556301; # support 22nd wall 1st z 8 y 3rd
node 38200 88.85 -1.75 -2.8335; # support 22nd wall 1st z 9 y 2nd
node 38201 89.625 -3.5 -3.3; # support 22nd wall 1st z 9 y 3rd
node 38300 90.4 -1.75 -5.5665; # support 22nd wall 2nd z 1 y 2nd
node 38400 90.4 -1.75 -5.169149; # support 22nd wall 2nd z 2 y 2nd
node 38500 90.4 -1.75 -5.168404; # support 22nd wall 2nd z 3 y 2nd
node 38600 90.4 -1.75 -5.020049; # support 22nd wall 2nd z 4 y 2nd
node 38700 90.4 -1.75 -5.019304; # support 22nd wall 2nd z 5 y 2nd
node 38800 90.4 -1.75 -4.2; # support 22nd wall 2nd z 6 y 2nd
node 38900 90.4 -1.75 -3.223396; # support 22nd wall 2nd z 7 y 2nd
node 39000 90.4 -1.75 -3.22265; # support 22nd wall 2nd z 8 y 2nd
node 39100 90.4 -1.75 -2.8335; # support 22nd wall 2nd z 9 y 2nd
node 39200 88.85 -1.75 2.8335; # support 23rd wall 1st z 1 y 2nd
node 39201 89.625 -3.5 3.3; # support 23rd wall 1st z 1 y 3rd
node 39300 88.85 -1.75 3.22265; # support 23rd wall 1st z 2 y 2nd
node 39301 89.625 -3.5 3.556301; # support 23rd wall 1st z 2 y 3rd
node 39400 88.85 -1.75 3.223396; # support 23rd wall 1st z 3 y 2nd
node 39401 89.625 -3.5 3.556792; # support 23rd wall 1st z 3 y 3rd
node 39500 88.85 -1.75 4.2; # support 23rd wall 1st z 4 y 2nd
node 39501 89.625 -3.5 4.2; # support 23rd wall 1st z 4 y 3rd
node 39600 88.85 -1.75 5.019304; # support 23rd wall 1st z 5 y 2nd
node 39601 89.625 -3.5 4.739607; # support 23rd wall 1st z 5 y 3rd
node 39700 88.85 -1.75 5.020049; # support 23rd wall 1st z 6 y 2nd
node 39701 89.625 -3.5 4.740098; # support 23rd wall 1st z 6 y 3rd
node 39800 88.85 -1.75 5.168404; # support 23rd wall 1st z 7 y 2nd
node 39801 89.625 -3.5 4.837807; # support 23rd wall 1st z 7 y 3rd
node 39900 88.85 -1.75 5.169149; # support 23rd wall 1st z 8 y 2nd
node 39901 89.625 -3.5 4.838298; # support 23rd wall 1st z 8 y 3rd
node 40000 88.85 -1.75 5.5665; # support 23rd wall 1st z 9 y 2nd
node 40001 89.625 -3.5 5.1; # support 23rd wall 1st z 9 y 3rd
node 40100 90.4 -1.75 2.8335; # support 23rd wall 2nd z 1 y 2nd
node 40200 90.4 -1.75 3.22265; # support 23rd wall 2nd z 2 y 2nd
node 40300 90.4 -1.75 3.223396; # support 23rd wall 2nd z 3 y 2nd
node 40400 90.4 -1.75 4.2; # support 23rd wall 2nd z 4 y 2nd
node 40500 90.4 -1.75 5.019304; # support 23rd wall 2nd z 5 y 2nd
node 40600 90.4 -1.75 5.020049; # support 23rd wall 2nd z 6 y 2nd
node 40700 90.4 -1.75 5.168404; # support 23rd wall 2nd z 7 y 2nd
node 40800 90.4 -1.75 5.169149; # support 23rd wall 2nd z 8 y 2nd
node 40900 90.4 -1.75 5.5665; # support 23rd wall 2nd z 9 y 2nd
node 41000 88.85 -1.75 11.2335; # support 24th wall 1st z 1 y 2nd
node 41001 89.625 -3.5 11.7; # support 24th wall 1st z 1 y 3rd
node 41100 88.85 -1.75 12.6; # support 24th wall 1st z 2 y 2nd
node 41101 89.625 -3.5 12.6; # support 24th wall 1st z 2 y 3rd
node 41200 88.85 -1.75 12.71108; # support 24th wall 1st z 3 y 2nd
node 41201 89.625 -3.5 12.673159; # support 24th wall 1st z 3 y 3rd
node 41300 88.85 -1.75 12.711825; # support 24th wall 1st z 4 y 2nd
node 41301 89.625 -3.5 12.67365; # support 24th wall 1st z 4 y 3rd
node 41400 88.85 -1.75 12.860179; # support 24th wall 1st z 5 y 2nd
node 41401 89.625 -3.5 12.771358; # support 24th wall 1st z 5 y 3rd
node 41500 88.85 -1.75 12.860924; # support 24th wall 1st z 6 y 2nd
node 41501 89.625 -3.5 12.771849; # support 24th wall 1st z 6 y 3rd
node 41600 88.85 -1.75 13.9665; # support 24th wall 1st z 7 y 2nd
node 41601 89.625 -3.5 13.5; # support 24th wall 1st z 7 y 3rd
node 41700 90.4 -1.75 11.2335; # support 24th wall 2nd z 1 y 2nd
node 41800 90.4 -1.75 12.6; # support 24th wall 2nd z 2 y 2nd
node 41900 90.4 -1.75 12.71108; # support 24th wall 2nd z 3 y 2nd
node 42000 90.4 -1.75 12.711825; # support 24th wall 2nd z 4 y 2nd
node 42100 90.4 -1.75 12.860179; # support 24th wall 2nd z 5 y 2nd
node 42200 90.4 -1.75 12.860924; # support 24th wall 2nd z 6 y 2nd
node 42300 90.4 -1.75 13.9665; # support 24th wall 2nd z 7 y 2nd
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
fix 1600 1 1 1 0 0 0
fix 1614 1 1 1 0 0 0
fix 1700 1 1 1 0 0 0
fix 1714 1 1 1 0 0 0
fix 1800 1 1 1 0 0 0
fix 1814 1 1 1 0 0 0
fix 1900 1 1 1 0 0 0
fix 1914 1 1 1 0 0 0
fix 2000 1 1 1 0 0 0
fix 2014 1 1 1 0 0 0
fix 2100 1 1 1 0 0 0
fix 2114 1 1 1 0 0 0
fix 2200 1 1 1 0 0 0
fix 2214 1 1 1 0 0 0
fix 2300 1 1 1 0 0 0
fix 2314 1 1 1 0 0 0
fix 2400 1 1 1 0 0 0
fix 2414 1 1 1 0 0 0
fix 2500 1 1 1 0 0 0
fix 2514 1 1 1 0 0 0
fix 2600 1 1 1 0 0 0
fix 2614 1 1 1 0 0 0
fix 2700 1 1 1 0 0 0
fix 2714 1 1 1 0 0 0
fix 2800 1 1 1 0 0 0
fix 2814 1 1 1 0 0 0
fix 2900 1 1 1 0 0 0
fix 2914 1 1 1 0 0 0
fix 3000 1 1 1 0 0 0
fix 3014 1 1 1 0 0 0
fix 3100 1 1 1 0 0 0
fix 3114 1 1 1 0 0 0
fix 3200 1 1 1 0 0 0
fix 3214 1 1 1 0 0 0
fix 3300 1 1 1 0 0 0
fix 3314 1 1 1 0 0 0
fix 3400 1 1 1 0 0 0
fix 3414 1 1 1 0 0 0
fix 3500 1 1 1 0 0 0
fix 3514 1 1 1 0 0 0
fix 3600 1 1 1 0 0 0
fix 3614 1 1 1 0 0 0
fix 3700 1 1 1 0 0 0
fix 3714 1 1 1 0 0 0
fix 3800 1 1 1 0 0 0
fix 3814 1 1 1 0 0 0
fix 3900 1 1 1 0 0 0
fix 3914 1 1 1 0 0 0
# End fixed deck nodes

# fix nodeTag x y z rx ry rz
# Begin fixed support nodes
fix 4001 0 0 1 1 1 0; # support 1 y 1
fix 4101 0 0 1 1 1 0; # support 1 y 2
fix 4201 0 0 1 1 1 0; # support 1 y 3
fix 4301 0 0 1 1 1 0; # support 1 y 4
fix 4401 0 0 1 1 1 0; # support 1 y 5
fix 4501 0 0 1 1 1 0; # support 1 y 6
fix 4601 0 0 1 1 1 0; # support 1 y 7
fix 5401 0 1 1 1 1 0; # support 2 y 1
fix 5501 0 1 1 1 1 0; # support 2 y 2
fix 5601 0 1 1 1 1 0; # support 2 y 3
fix 5701 0 1 1 1 1 0; # support 2 y 4
fix 5801 0 1 1 1 1 0; # support 2 y 5
fix 5901 0 1 1 1 1 0; # support 2 y 6
fix 6001 0 1 1 1 1 0; # support 2 y 7
fix 6101 0 1 1 1 1 0; # support 2 y 8
fix 6201 0 1 1 1 1 0; # support 2 y 9
fix 7201 0 1 1 1 1 0; # support 3 y 1
fix 7301 0 1 1 1 1 0; # support 3 y 2
fix 7401 0 1 1 1 1 0; # support 3 y 3
fix 7501 0 1 1 1 1 0; # support 3 y 4
fix 7601 0 1 1 1 1 0; # support 3 y 5
fix 7701 0 1 1 1 1 0; # support 3 y 6
fix 7801 0 1 1 1 1 0; # support 3 y 7
fix 7901 0 1 1 1 1 0; # support 3 y 8
fix 8001 0 1 1 1 1 0; # support 3 y 9
fix 9001 0 1 1 1 1 0; # support 4 y 1
fix 9101 0 1 1 1 1 0; # support 4 y 2
fix 9201 0 1 1 1 1 0; # support 4 y 3
fix 9301 0 1 1 1 1 0; # support 4 y 4
fix 9401 0 1 1 1 1 0; # support 4 y 5
fix 9501 0 1 1 1 1 0; # support 4 y 6
fix 9601 0 1 1 1 1 0; # support 4 y 7
fix 10401 0 1 1 1 1 0; # support 5 y 1
fix 10501 0 1 1 1 1 0; # support 5 y 2
fix 10601 0 1 1 1 1 0; # support 5 y 3
fix 10701 0 1 1 1 1 0; # support 5 y 4
fix 10801 0 1 1 1 1 0; # support 5 y 5
fix 10901 0 1 1 1 1 0; # support 5 y 6
fix 11001 0 1 1 1 1 0; # support 5 y 7
fix 11801 0 1 1 1 1 0; # support 6 y 1
fix 11901 0 1 1 1 1 0; # support 6 y 2
fix 12001 0 1 1 1 1 0; # support 6 y 3
fix 12101 0 1 1 1 1 0; # support 6 y 4
fix 12201 0 1 1 1 1 0; # support 6 y 5
fix 12301 0 1 1 1 1 0; # support 6 y 6
fix 12401 0 1 1 1 1 0; # support 6 y 7
fix 12501 0 1 1 1 1 0; # support 6 y 8
fix 12601 0 1 1 1 1 0; # support 6 y 9
fix 13601 0 1 1 1 1 0; # support 7 y 1
fix 13701 0 1 1 1 1 0; # support 7 y 2
fix 13801 0 1 1 1 1 0; # support 7 y 3
fix 13901 0 1 1 1 1 0; # support 7 y 4
fix 14001 0 1 1 1 1 0; # support 7 y 5
fix 14101 0 1 1 1 1 0; # support 7 y 6
fix 14201 0 1 1 1 1 0; # support 7 y 7
fix 14301 0 1 1 1 1 0; # support 7 y 8
fix 14401 0 1 1 1 1 0; # support 7 y 9
fix 15401 0 1 1 1 1 0; # support 8 y 1
fix 15501 0 1 1 1 1 0; # support 8 y 2
fix 15601 0 1 1 1 1 0; # support 8 y 3
fix 15701 0 1 1 1 1 0; # support 8 y 4
fix 15801 0 1 1 1 1 0; # support 8 y 5
fix 15901 0 1 1 1 1 0; # support 8 y 6
fix 16001 0 1 1 1 1 0; # support 8 y 7
fix 16801 1 1 1 1 1 0; # support 9 y 1
fix 16901 1 1 1 1 1 0; # support 9 y 2
fix 17001 1 1 1 1 1 0; # support 9 y 3
fix 17101 1 1 1 1 1 0; # support 9 y 4
fix 17201 1 1 1 1 1 0; # support 9 y 5
fix 17301 1 1 1 1 1 0; # support 9 y 6
fix 17401 1 1 1 1 1 0; # support 9 y 7
fix 18201 1 1 1 1 1 0; # support 10 y 1
fix 18301 1 1 1 1 1 0; # support 10 y 2
fix 18401 1 1 1 1 1 0; # support 10 y 3
fix 18501 1 1 1 1 1 0; # support 10 y 4
fix 18601 1 1 1 1 1 0; # support 10 y 5
fix 18701 1 1 1 1 1 0; # support 10 y 6
fix 18801 1 1 1 1 1 0; # support 10 y 7
fix 18901 1 1 1 1 1 0; # support 10 y 8
fix 19001 1 1 1 1 1 0; # support 10 y 9
fix 20001 1 1 1 1 1 0; # support 11 y 1
fix 20101 1 1 1 1 1 0; # support 11 y 2
fix 20201 1 1 1 1 1 0; # support 11 y 3
fix 20301 1 1 1 1 1 0; # support 11 y 4
fix 20401 1 1 1 1 1 0; # support 11 y 5
fix 20501 1 1 1 1 1 0; # support 11 y 6
fix 20601 1 1 1 1 1 0; # support 11 y 7
fix 20701 1 1 1 1 1 0; # support 11 y 8
fix 20801 1 1 1 1 1 0; # support 11 y 9
fix 21801 1 1 1 1 1 0; # support 12 y 1
fix 21901 1 1 1 1 1 0; # support 12 y 2
fix 22001 1 1 1 1 1 0; # support 12 y 3
fix 22101 1 1 1 1 1 0; # support 12 y 4
fix 22201 1 1 1 1 1 0; # support 12 y 5
fix 22301 1 1 1 1 1 0; # support 12 y 6
fix 22401 1 1 1 1 1 0; # support 12 y 7
fix 23201 1 1 1 1 1 0; # support 13 y 1
fix 23301 1 1 1 1 1 0; # support 13 y 2
fix 23401 1 1 1 1 1 0; # support 13 y 3
fix 23501 1 1 1 1 1 0; # support 13 y 4
fix 23601 1 1 1 1 1 0; # support 13 y 5
fix 23701 1 1 1 1 1 0; # support 13 y 6
fix 23801 1 1 1 1 1 0; # support 13 y 7
fix 24601 1 1 1 1 1 0; # support 14 y 1
fix 24701 1 1 1 1 1 0; # support 14 y 2
fix 24801 1 1 1 1 1 0; # support 14 y 3
fix 24901 1 1 1 1 1 0; # support 14 y 4
fix 25001 1 1 1 1 1 0; # support 14 y 5
fix 25101 1 1 1 1 1 0; # support 14 y 6
fix 25201 1 1 1 1 1 0; # support 14 y 7
fix 25301 1 1 1 1 1 0; # support 14 y 8
fix 25401 1 1 1 1 1 0; # support 14 y 9
fix 26401 1 1 1 1 1 0; # support 15 y 1
fix 26501 1 1 1 1 1 0; # support 15 y 2
fix 26601 1 1 1 1 1 0; # support 15 y 3
fix 26701 1 1 1 1 1 0; # support 15 y 4
fix 26801 1 1 1 1 1 0; # support 15 y 5
fix 26901 1 1 1 1 1 0; # support 15 y 6
fix 27001 1 1 1 1 1 0; # support 15 y 7
fix 27101 1 1 1 1 1 0; # support 15 y 8
fix 27201 1 1 1 1 1 0; # support 15 y 9
fix 28201 1 1 1 1 1 0; # support 16 y 1
fix 28301 1 1 1 1 1 0; # support 16 y 2
fix 28401 1 1 1 1 1 0; # support 16 y 3
fix 28501 1 1 1 1 1 0; # support 16 y 4
fix 28601 1 1 1 1 1 0; # support 16 y 5
fix 28701 1 1 1 1 1 0; # support 16 y 6
fix 28801 1 1 1 1 1 0; # support 16 y 7
fix 29601 0 1 1 1 1 0; # support 17 y 1
fix 29701 0 1 1 1 1 0; # support 17 y 2
fix 29801 0 1 1 1 1 0; # support 17 y 3
fix 29901 0 1 1 1 1 0; # support 17 y 4
fix 30001 0 1 1 1 1 0; # support 17 y 5
fix 30101 0 1 1 1 1 0; # support 17 y 6
fix 30201 0 1 1 1 1 0; # support 17 y 7
fix 31001 0 1 1 1 1 0; # support 18 y 1
fix 31101 0 1 1 1 1 0; # support 18 y 2
fix 31201 0 1 1 1 1 0; # support 18 y 3
fix 31301 0 1 1 1 1 0; # support 18 y 4
fix 31401 0 1 1 1 1 0; # support 18 y 5
fix 31501 0 1 1 1 1 0; # support 18 y 6
fix 31601 0 1 1 1 1 0; # support 18 y 7
fix 31701 0 1 1 1 1 0; # support 18 y 8
fix 31801 0 1 1 1 1 0; # support 18 y 9
fix 32801 0 1 1 1 1 0; # support 19 y 1
fix 32901 0 1 1 1 1 0; # support 19 y 2
fix 33001 0 1 1 1 1 0; # support 19 y 3
fix 33101 0 1 1 1 1 0; # support 19 y 4
fix 33201 0 1 1 1 1 0; # support 19 y 5
fix 33301 0 1 1 1 1 0; # support 19 y 6
fix 33401 0 1 1 1 1 0; # support 19 y 7
fix 33501 0 1 1 1 1 0; # support 19 y 8
fix 33601 0 1 1 1 1 0; # support 19 y 9
fix 34601 0 1 1 1 1 0; # support 20 y 1
fix 34701 0 1 1 1 1 0; # support 20 y 2
fix 34801 0 1 1 1 1 0; # support 20 y 3
fix 34901 0 1 1 1 1 0; # support 20 y 4
fix 35001 0 1 1 1 1 0; # support 20 y 5
fix 35101 0 1 1 1 1 0; # support 20 y 6
fix 35201 0 1 1 1 1 0; # support 20 y 7
fix 36001 0 1 1 1 1 0; # support 21 y 1
fix 36101 0 1 1 1 1 0; # support 21 y 2
fix 36201 0 1 1 1 1 0; # support 21 y 3
fix 36301 0 1 1 1 1 0; # support 21 y 4
fix 36401 0 1 1 1 1 0; # support 21 y 5
fix 36501 0 1 1 1 1 0; # support 21 y 6
fix 36601 0 1 1 1 1 0; # support 21 y 7
fix 37401 0 1 1 1 1 0; # support 22 y 1
fix 37501 0 1 1 1 1 0; # support 22 y 2
fix 37601 0 1 1 1 1 0; # support 22 y 3
fix 37701 0 1 1 1 1 0; # support 22 y 4
fix 37801 0 1 1 1 1 0; # support 22 y 5
fix 37901 0 1 1 1 1 0; # support 22 y 6
fix 38001 0 1 1 1 1 0; # support 22 y 7
fix 38101 0 1 1 1 1 0; # support 22 y 8
fix 38201 0 1 1 1 1 0; # support 22 y 9
fix 39201 0 1 1 1 1 0; # support 23 y 1
fix 39301 0 1 1 1 1 0; # support 23 y 2
fix 39401 0 1 1 1 1 0; # support 23 y 3
fix 39501 0 1 1 1 1 0; # support 23 y 4
fix 39601 0 1 1 1 1 0; # support 23 y 5
fix 39701 0 1 1 1 1 0; # support 23 y 6
fix 39801 0 1 1 1 1 0; # support 23 y 7
fix 39901 0 1 1 1 1 0; # support 23 y 8
fix 40001 0 1 1 1 1 0; # support 23 y 9
fix 41001 0 1 1 1 1 0; # support 24 y 1
fix 41101 0 1 1 1 1 0; # support 24 y 2
fix 41201 0 1 1 1 1 0; # support 24 y 3
fix 41301 0 1 1 1 1 0; # support 24 y 4
fix 41401 0 1 1 1 1 0; # support 24 y 5
fix 41501 0 1 1 1 1 0; # support 24 y 6
fix 41601 0 1 1 1 1 0; # support 24 y 7
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
section ElasticMembranePlateSection 460 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 253 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 396 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 527 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 626 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 397 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 254 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 528 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 627 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 398 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 255 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 529 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 628 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 399 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 530 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 256 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 400 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 629 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 531 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 257 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 401 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 61 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 532 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 258 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 402 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 630 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 533 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 631 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 259 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 403 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 534 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 632 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 260 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 404 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 405 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 535 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 633 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 261 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 694 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 536 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 634 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 262 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 406 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 537 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 635 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 263 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 407 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 538 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 539 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 636 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 264 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 408 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 265 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 540 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 637 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 232 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 409 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 266 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 541 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 638 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 410 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 267 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 542 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 639 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 411 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 268 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 543 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 640 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 269 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 412 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 544 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 641 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 270 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 413 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 545 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 642 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 271 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 414 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 546 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 643 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 272 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 415 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 547 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 273 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 644 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 416 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 548 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 274 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 645 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 417 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 549 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 275 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 646 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 110 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 418 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 550 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 276 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 647 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 419 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 551 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 277 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 420 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 648 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 278 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 552 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 421 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 649 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 279 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 553 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 422 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 650 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 280 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 554 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 423 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 555 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 651 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 281 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 424 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 556 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 652 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 172 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 282 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 283 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 425 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 557 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 653 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 379 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 426 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 284 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 558 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 654 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 427 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 285 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 559 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 655 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 428 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 286 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 560 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 656 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 71 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 689 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 54 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 223 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 495 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 113 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 496 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 114 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 497 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 115 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 498 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 116 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 499 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 117 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 500 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 118 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 501 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 119 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 502 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 120 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 503 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 121 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 122 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 504 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 123 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 505 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 506 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 124 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 507 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 125 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 508 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 126 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 509 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 127 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 510 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 128 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 511 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 129 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 512 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 130 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 513 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 131 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 514 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 132 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 515 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 133 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 516 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 135 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 517 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 136 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 582 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 137 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 518 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 138 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 519 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 139 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 520 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 140 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 521 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 141 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 522 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 142 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 523 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 143 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 524 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 144 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 525 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 145 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 526 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 215 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 361 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 461 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 594 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 690 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 216 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 362 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 462 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 595 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 691 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 217 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 363 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 364 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 463 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 596 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 692 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 218 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 365 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 464 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 597 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 693 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 219 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 366 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 465 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 598 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 695 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 220 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 367 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 466 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 599 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 696 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 221 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 368 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 467 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 600 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 697 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 222 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 601 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 698 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 369 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 468 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 224 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 370 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 602 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 699 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 225 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 469 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 371 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 603 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 700 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 226 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 471 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 372 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 472 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 604 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 701 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 227 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 473 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 228 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 373 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 605 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 702 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 474 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 229 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 374 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 606 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 703 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 475 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 230 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 375 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 607 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 704 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 476 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 231 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 376 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 477 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 608 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 377 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 705 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 233 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 478 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 609 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 706 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 378 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 234 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 380 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 479 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 610 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 707 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 235 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 381 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 480 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 611 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 236 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 708 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 382 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 481 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 612 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 709 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 237 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 383 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 482 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 613 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 710 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 238 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 384 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 483 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 614 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 711 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 239 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 385 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 484 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 615 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 712 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 240 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 386 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 485 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 616 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 713 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 241 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 486 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 387 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 617 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 714 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 242 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 487 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 388 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 618 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 715 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 243 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 488 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 389 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 619 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 716 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 244 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 489 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 390 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 620 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 717 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 245 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 490 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 391 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 621 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 248 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 491 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 249 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 392 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 622 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 492 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 250 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 393 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 623 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 493 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 251 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 394 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 624 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 494 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 252 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 395 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 625 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 75 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 181 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 324 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 76 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 247 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 325 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 77 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 246 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 182 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 326 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 78 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 79 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 183 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 327 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 328 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 80 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 184 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 185 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 81 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 329 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 82 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 186 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 83 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 330 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 84 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 187 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 331 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 85 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 188 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 332 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 86 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 189 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 333 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 87 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 190 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 191 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 334 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 335 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 88 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 336 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 192 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 89 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 337 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 193 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 338 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 90 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 91 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 194 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 339 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 195 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 92 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 196 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 340 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 341 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 93 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 197 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 342 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 94 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 198 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 95 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 343 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 199 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 96 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 344 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 200 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 97 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 201 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 345 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 346 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 98 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 202 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 347 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 99 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 203 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 348 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 100 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 204 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 349 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 101 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 350 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 205 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 102 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 351 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 206 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 352 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 103 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 104 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 207 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 353 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 105 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 208 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 209 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 354 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 106 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 210 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 355 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 107 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 108 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 211 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 356 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 109 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 212 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 357 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 111 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 213 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 359 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 214 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 112 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 360 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 561 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 562 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 563 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 564 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 565 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 566 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 567 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 568 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 569 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 570 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 571 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 572 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 573 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 574 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 575 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 576 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 577 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 578 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 579 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 580 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 581 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 583 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 584 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 585 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 586 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 587 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 588 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 589 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 590 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 591 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 74 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 592 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 593 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 146 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 287 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 429 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 147 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 288 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 657 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 289 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 430 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 148 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 290 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 658 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 431 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 149 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 291 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 659 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 432 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 660 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 150 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 292 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 433 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 661 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 293 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 151 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 434 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 662 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 152 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 435 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 470 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 663 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 153 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 294 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 358 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 436 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 664 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 154 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 295 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 296 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 46 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 155 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 437 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 665 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 47 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 156 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 297 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 438 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 666 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 48 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 157 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 298 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 439 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 667 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 49 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 158 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 299 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 440 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 300 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 668 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 50 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 159 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 301 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 441 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 669 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 55 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 160 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 302 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 442 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 51 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 180 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 670 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 161 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 303 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 443 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 671 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 52 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 162 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 304 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 444 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 672 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 53 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 305 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 163 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 306 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 445 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 673 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 56 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 164 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 307 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 446 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 674 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 57 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 308 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 165 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 447 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 675 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 58 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 309 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 166 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 310 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 448 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 676 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 59 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 167 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 311 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 449 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 677 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 60 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 678 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 62 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 168 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 312 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 450 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 63 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 679 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 64 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 169 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 313 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 451 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 680 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 314 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 65 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 170 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 452 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 681 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 66 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 171 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 315 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 453 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 173 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 316 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 682 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 67 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 174 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 454 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 683 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 317 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 68 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 69 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 175 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 455 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 684 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 318 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 319 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 134 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 176 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 456 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 685 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 70 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 177 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 320 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 457 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 686 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 72 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 178 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 321 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 458 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 687 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 73 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 179 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 322 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 459 38400000000.0 0.2 0.362 0.0027240000000000003
section ElasticMembranePlateSection 688 38400000000.0 0.2 1.266 0.0027240000000000003
section ElasticMembranePlateSection 323 38400000000.0 0.2 0.362 0.0027240000000000003
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
element ShellMITC4 100 200 201 301 300 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 101 201 202 302 301 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 102 202 203 303 302 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 103 203 204 304 303 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 104 204 205 305 304 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 105 205 206 306 305 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 106 206 207 307 306 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 107 207 208 308 307 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 108 208 209 309 308 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 109 209 210 310 309 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 110 210 211 311 310 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 111 211 212 312 311 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 112 212 213 313 312 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 113 213 214 314 313 2; # Section3D   starts at (x_frac, z_frac) = (0, 0.018072)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 200 300 301 401 400 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 201 301 302 402 401 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 202 302 303 403 402 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 203 303 304 404 403 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 204 304 305 405 404 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 205 305 306 406 405 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 206 306 307 407 406 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 207 307 308 408 407 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 208 308 309 409 408 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 209 309 310 410 409 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 210 310 311 411 410 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 211 311 312 412 411 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 212 312 313 413 412 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 213 313 314 414 413 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 300 400 401 501 500 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 301 401 402 502 501 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 302 402 403 503 502 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 303 403 404 504 503 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 304 404 405 505 504 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 305 405 406 506 505 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 306 406 407 507 506 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 307 407 408 508 507 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 308 408 409 509 508 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 309 409 410 510 509 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 310 410 411 511 510 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 311 411 412 512 511 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 312 412 413 513 512 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 313 413 414 514 513 3; # Section3D   starts at (x_frac, z_frac) = (0, 0.018102)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 400 500 501 601 600 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 401 501 502 602 601 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 402 502 503 603 602 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 403 503 504 604 603 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 404 504 505 605 604 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 405 505 506 606 605 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 406 506 507 607 606 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 407 507 508 608 607 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 408 508 509 609 608 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 409 509 510 610 609 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 410 510 511 611 610 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 411 511 512 612 611 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 412 512 513 613 612 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 413 513 514 614 613 4; # Section3D   starts at (x_frac, z_frac) = (0, 0.10994)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 500 600 601 701 700 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 501 601 602 702 701 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 502 602 603 703 702 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 503 603 604 704 703 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 504 604 605 705 704 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 505 605 606 706 705 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 506 606 607 707 706 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 507 607 608 708 707 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 508 608 609 709 708 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 509 609 610 710 709 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 510 610 611 711 710 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 511 611 612 712 711 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 512 612 613 713 712 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 513 613 614 714 713 5; # Section3D   starts at (x_frac, z_frac) = (0, 0.10997)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 600 700 701 801 800 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 601 701 702 802 801 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 602 702 703 803 802 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 603 703 704 804 803 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 604 704 705 805 804 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 605 705 706 806 805 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 606 706 707 807 806 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 607 707 708 808 807 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 608 708 709 809 808 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 609 709 710 810 809 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 610 710 711 811 810 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 611 711 712 812 811 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 612 712 713 813 812 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 613 713 714 814 813 6; # Section3D   starts at (x_frac, z_frac) = (0, 0.115964)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 700 800 801 901 900 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 701 801 802 902 901 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 702 802 803 903 902 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 703 803 804 904 903 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 704 804 805 905 904 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 705 805 806 906 905 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 706 806 807 907 906 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 707 807 808 908 907 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 708 808 809 909 908 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 709 809 810 910 909 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 710 810 811 911 910 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 711 811 812 912 911 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 712 812 813 913 912 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 713 813 814 914 913 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 800 900 901 1001 1000 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 801 901 902 1002 1001 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 802 902 903 1003 1002 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 803 903 904 1004 1003 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 804 904 905 1005 1004 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 805 905 906 1006 1005 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 806 906 907 1007 1006 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 807 907 908 1008 1007 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 808 908 909 1009 1008 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 809 909 910 1010 1009 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 810 910 911 1011 1010 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 811 911 912 1012 1011 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 812 912 913 1013 1012 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 813 913 914 1014 1013 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 900 1000 1001 1101 1100 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 901 1001 1002 1102 1101 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 902 1002 1003 1103 1102 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 903 1003 1004 1104 1103 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 904 1004 1005 1105 1104 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 905 1005 1006 1106 1105 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 906 1006 1007 1107 1106 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 907 1007 1008 1108 1107 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 908 1008 1009 1109 1108 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 909 1009 1010 1110 1109 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 910 1010 1011 1111 1110 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 911 1011 1012 1112 1111 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 912 1012 1013 1113 1112 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 913 1013 1014 1114 1113 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1000 1100 1101 1201 1200 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1001 1101 1102 1202 1201 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1002 1102 1103 1203 1202 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1003 1103 1104 1204 1203 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1004 1104 1105 1205 1204 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1005 1105 1106 1206 1205 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1006 1106 1107 1207 1206 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1007 1107 1108 1208 1207 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1008 1108 1109 1209 1208 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1009 1109 1110 1210 1209 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1010 1110 1111 1211 1210 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1011 1111 1112 1212 1211 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1012 1112 1113 1213 1212 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1013 1113 1114 1214 1213 7; # Section3D   starts at (x_frac, z_frac) = (0, 0.115994)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1100 1200 1201 1301 1300 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1101 1201 1202 1302 1301 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1102 1202 1203 1303 1302 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1103 1203 1204 1304 1303 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1104 1204 1205 1305 1304 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1105 1205 1206 1306 1305 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1106 1206 1207 1307 1306 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1107 1207 1208 1308 1307 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1108 1208 1209 1309 1308 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1109 1209 1210 1310 1309 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1110 1210 1211 1311 1310 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1111 1211 1212 1312 1311 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1112 1212 1213 1313 1312 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1113 1213 1214 1314 1313 8; # Section3D   starts at (x_frac, z_frac) = (0, 0.334337)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 1200 1300 1301 1401 1400 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1201 1301 1302 1402 1401 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1202 1302 1303 1403 1402 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1203 1303 1304 1404 1403 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1204 1304 1305 1405 1404 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1205 1305 1306 1406 1405 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1206 1306 1307 1407 1406 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1207 1307 1308 1408 1407 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1208 1308 1309 1409 1408 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1209 1309 1310 1410 1409 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1210 1310 1311 1411 1410 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1211 1311 1312 1412 1411 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1212 1312 1313 1413 1412 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1213 1313 1314 1414 1413 9; # Section3D   starts at (x_frac, z_frac) = (0, 0.334367)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1300 1400 1401 1501 1500 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1301 1401 1402 1502 1501 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1302 1402 1403 1503 1502 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1303 1403 1404 1504 1503 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1304 1404 1405 1505 1504 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1305 1405 1406 1506 1505 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1306 1406 1407 1507 1506 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1307 1407 1408 1508 1507 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1308 1408 1409 1509 1508 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1309 1409 1410 1510 1509 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1310 1410 1411 1511 1510 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1311 1411 1412 1512 1511 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1312 1412 1413 1513 1512 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1313 1413 1414 1514 1513 10; # Section3D   starts at (x_frac, z_frac) = (0, 0.340361)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1400 1500 1501 1601 1600 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1401 1501 1502 1602 1601 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1402 1502 1503 1603 1602 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1403 1503 1504 1604 1603 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1404 1504 1505 1605 1604 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1405 1505 1506 1606 1605 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1406 1506 1507 1607 1606 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1407 1507 1508 1608 1607 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1408 1508 1509 1609 1608 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1409 1509 1510 1610 1609 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1410 1510 1511 1611 1610 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1411 1511 1512 1612 1611 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1412 1512 1513 1613 1612 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1413 1513 1514 1614 1613 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1500 1600 1601 1701 1700 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1501 1601 1602 1702 1701 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1502 1602 1603 1703 1702 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1503 1603 1604 1704 1703 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1504 1604 1605 1705 1704 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1505 1605 1606 1706 1705 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1506 1606 1607 1707 1706 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1507 1607 1608 1708 1707 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1508 1608 1609 1709 1708 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1509 1609 1610 1710 1709 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1510 1610 1611 1711 1710 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1511 1611 1612 1712 1711 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1512 1612 1613 1713 1712 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1513 1613 1614 1714 1713 11; # Section3D   starts at (x_frac, z_frac) = (0, 0.340392)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1600 1700 1701 1801 1800 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1601 1701 1702 1802 1801 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1602 1702 1703 1803 1802 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1603 1703 1704 1804 1803 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1604 1704 1705 1805 1804 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1605 1705 1706 1806 1805 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1606 1706 1707 1807 1806 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1607 1707 1708 1808 1807 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1608 1708 1709 1809 1808 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1609 1709 1710 1810 1809 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1610 1710 1711 1811 1810 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1611 1711 1712 1812 1811 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1612 1712 1713 1813 1812 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1613 1713 1714 1814 1813 12; # Section3D   starts at (x_frac, z_frac) = (0, 0.412952)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 1700 1800 1801 1901 1900 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1701 1801 1802 1902 1901 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1702 1802 1803 1903 1902 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1703 1803 1804 1904 1903 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1704 1804 1805 1905 1904 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1705 1805 1806 1906 1905 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1706 1806 1807 1907 1906 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1707 1807 1808 1908 1907 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1708 1808 1809 1909 1908 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1709 1809 1810 1910 1909 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1710 1810 1811 1911 1910 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1711 1811 1812 1912 1911 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1712 1812 1813 1913 1912 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1713 1813 1814 1914 1913 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1800 1900 1901 2001 2000 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1801 1901 1902 2002 2001 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1802 1902 1903 2003 2002 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1803 1903 1904 2004 2003 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1804 1904 1905 2005 2004 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1805 1905 1906 2006 2005 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1806 1906 1907 2007 2006 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1807 1907 1908 2008 2007 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1808 1908 1909 2009 2008 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1809 1909 1910 2010 2009 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1810 1910 1911 2011 2010 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1811 1911 1912 2012 2011 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1812 1912 1913 2013 2012 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1813 1913 1914 2014 2013 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1900 2000 2001 2101 2100 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1901 2001 2002 2102 2101 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1902 2002 2003 2103 2102 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1903 2003 2004 2104 2103 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1904 2004 2005 2105 2104 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1905 2005 2006 2106 2105 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1906 2006 2007 2107 2106 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1907 2007 2008 2108 2107 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1908 2008 2009 2109 2108 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1909 2009 2010 2110 2109 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1910 2010 2011 2111 2110 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1911 2011 2012 2112 2111 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1912 2012 2013 2113 2112 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 1913 2013 2014 2114 2113 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2000 2100 2101 2201 2200 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2001 2101 2102 2202 2201 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2002 2102 2103 2203 2202 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2003 2103 2104 2204 2203 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2004 2104 2105 2205 2204 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2005 2105 2106 2206 2205 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2006 2106 2107 2207 2206 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2007 2107 2108 2208 2207 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2008 2108 2109 2209 2208 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2009 2109 2110 2210 2209 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2010 2110 2111 2211 2210 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2011 2111 2112 2212 2211 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2012 2112 2113 2213 2212 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2013 2113 2114 2214 2213 13; # Section3D   starts at (x_frac, z_frac) = (0, 0.412982)   density = 2.907 kg/m   thickness = 0.65 m   youngs = 47277.0 MPa   poissons = 0.2
element ShellMITC4 2100 2200 2201 2301 2300 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2101 2201 2202 2302 2301 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2102 2202 2203 2303 2302 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2103 2203 2204 2304 2303 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2104 2204 2205 2305 2304 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2105 2205 2206 2306 2305 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2106 2206 2207 2307 2306 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2107 2207 2208 2308 2307 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2108 2208 2209 2309 2308 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2109 2209 2210 2310 2309 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2110 2210 2211 2311 2310 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2111 2211 2212 2312 2311 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2112 2212 2213 2313 2312 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2113 2213 2214 2314 2313 14; # Section3D   starts at (x_frac, z_frac) = (0, 0.587018)   density = 2.617 kg/m   thickness = 0.787 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2200 2300 2301 2401 2400 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2201 2301 2302 2402 2401 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2202 2302 2303 2403 2402 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2203 2303 2304 2404 2403 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2204 2304 2305 2405 2404 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2205 2305 2306 2406 2405 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2206 2306 2307 2407 2406 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2207 2307 2308 2408 2407 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2208 2308 2309 2409 2408 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2209 2309 2310 2410 2409 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2210 2310 2311 2411 2410 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2211 2311 2312 2412 2411 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2212 2312 2313 2413 2412 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2213 2313 2314 2414 2413 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2300 2400 2401 2501 2500 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2301 2401 2402 2502 2501 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2302 2402 2403 2503 2502 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2303 2403 2404 2504 2503 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2304 2404 2405 2505 2504 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2305 2405 2406 2506 2505 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2306 2406 2407 2507 2506 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2307 2407 2408 2508 2507 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2308 2408 2409 2509 2508 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2309 2409 2410 2510 2509 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2310 2410 2411 2511 2510 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2311 2411 2412 2512 2511 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2312 2412 2413 2513 2512 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2313 2413 2414 2514 2513 15; # Section3D   starts at (x_frac, z_frac) = (0, 0.587048)   density = 2.631 kg/m   thickness = 0.739 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2400 2500 2501 2601 2600 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2401 2501 2502 2602 2601 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2402 2502 2503 2603 2602 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2403 2503 2504 2604 2603 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2404 2504 2505 2605 2604 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2405 2505 2506 2606 2605 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2406 2506 2507 2607 2606 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2407 2507 2508 2608 2607 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2408 2508 2509 2609 2608 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2409 2509 2510 2610 2609 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2410 2510 2511 2611 2610 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2411 2511 2512 2612 2611 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2412 2512 2513 2613 2612 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2413 2513 2514 2614 2613 16; # Section3D   starts at (x_frac, z_frac) = (0, 0.659608)   density = 2.995 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2500 2600 2601 2701 2700 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2501 2601 2602 2702 2701 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2502 2602 2603 2703 2702 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2503 2603 2604 2704 2703 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2504 2604 2605 2705 2704 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2505 2605 2606 2706 2705 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2506 2606 2607 2707 2706 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2507 2607 2608 2708 2707 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2508 2608 2609 2709 2708 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2509 2609 2610 2710 2709 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2510 2610 2611 2711 2710 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2511 2611 2612 2712 2711 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2512 2612 2613 2713 2712 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2513 2613 2614 2714 2713 17; # Section3D   starts at (x_frac, z_frac) = (0, 0.659639)   density = 2.98 kg/m   thickness = 0.65 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 2600 2700 2701 2801 2800 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2601 2701 2702 2802 2801 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2602 2702 2703 2803 2802 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2603 2703 2704 2804 2803 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2604 2704 2705 2805 2804 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2605 2705 2706 2806 2805 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2606 2706 2707 2807 2806 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2607 2707 2708 2808 2807 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2608 2708 2709 2809 2808 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2609 2709 2710 2810 2809 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2610 2710 2711 2811 2810 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2611 2711 2712 2812 2811 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2612 2712 2713 2813 2812 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2613 2713 2714 2814 2813 18; # Section3D   starts at (x_frac, z_frac) = (0, 0.665633)   density = 2.765 kg/m   thickness = 0.65 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2700 2800 2801 2901 2900 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2701 2801 2802 2902 2901 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2702 2802 2803 2903 2902 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2703 2803 2804 2904 2903 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2704 2804 2805 2905 2904 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2705 2805 2806 2906 2905 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2706 2806 2807 2907 2906 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2707 2807 2808 2908 2907 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2708 2808 2809 2909 2908 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2709 2809 2810 2910 2909 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2710 2810 2811 2911 2910 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2711 2811 2812 2912 2911 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2712 2812 2813 2913 2912 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2713 2813 2814 2914 2913 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2800 2900 2901 3001 3000 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2801 2901 2902 3002 3001 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2802 2902 2903 3003 3002 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2803 2903 2904 3004 3003 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2804 2904 2905 3005 3004 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2805 2905 2906 3006 3005 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2806 2906 2907 3007 3006 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2807 2907 2908 3008 3007 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2808 2908 2909 3009 3008 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2809 2909 2910 3010 3009 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2810 2910 2911 3011 3010 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2811 2911 2912 3012 3011 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2812 2912 2913 3013 3012 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2813 2913 2914 3014 3013 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2900 3000 3001 3101 3100 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2901 3001 3002 3102 3101 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2902 3002 3003 3103 3102 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2903 3003 3004 3104 3103 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2904 3004 3005 3105 3104 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2905 3005 3006 3106 3105 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2906 3006 3007 3107 3106 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2907 3007 3008 3108 3107 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2908 3008 3009 3109 3108 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2909 3009 3010 3110 3109 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2910 3010 3011 3111 3110 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2911 3011 3012 3112 3111 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2912 3012 3013 3113 3112 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 2913 3013 3014 3114 3113 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3000 3100 3101 3201 3200 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3001 3101 3102 3202 3201 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3002 3102 3103 3203 3202 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3003 3103 3104 3204 3203 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3004 3104 3105 3205 3204 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3005 3105 3106 3206 3205 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3006 3106 3107 3207 3206 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3007 3107 3108 3208 3207 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3008 3108 3109 3209 3208 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3009 3109 3110 3210 3209 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3010 3110 3111 3211 3210 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3011 3111 3112 3212 3211 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3012 3112 3113 3213 3212 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3013 3113 3114 3214 3213 19; # Section3D   starts at (x_frac, z_frac) = (0, 0.665663)   density = 2.8449999999999998 kg/m   thickness = 0.5 m   youngs = 41291.0 MPa   poissons = 0.2
element ShellMITC4 3100 3200 3201 3301 3300 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3101 3201 3202 3302 3301 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3102 3202 3203 3303 3302 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3103 3203 3204 3304 3303 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3104 3204 3205 3305 3304 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3105 3205 3206 3306 3305 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3106 3206 3207 3307 3306 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3107 3207 3208 3308 3307 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3108 3208 3209 3309 3308 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3109 3209 3210 3310 3309 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3110 3210 3211 3311 3310 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3111 3211 3212 3312 3311 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3112 3212 3213 3313 3312 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3113 3213 3214 3314 3313 20; # Section3D   starts at (x_frac, z_frac) = (0, 0.884006)   density = 3.124 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3200 3300 3301 3401 3400 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3201 3301 3302 3402 3401 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3202 3302 3303 3403 3402 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3203 3303 3304 3404 3403 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3204 3304 3305 3405 3404 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3205 3305 3306 3406 3405 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3206 3306 3307 3407 3406 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3207 3307 3308 3408 3407 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3208 3308 3309 3409 3408 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3209 3309 3310 3410 3409 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3210 3310 3311 3411 3410 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3211 3311 3312 3412 3411 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3212 3312 3313 3413 3412 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3213 3313 3314 3414 3413 21; # Section3D   starts at (x_frac, z_frac) = (0, 0.884036)   density = 3.143 kg/m   thickness = 0.5 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3300 3400 3401 3501 3500 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3301 3401 3402 3502 3501 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3302 3402 3403 3503 3502 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3303 3403 3404 3504 3503 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3304 3404 3405 3505 3504 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3305 3405 3406 3506 3505 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3306 3406 3407 3507 3506 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3307 3407 3408 3508 3507 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3308 3408 3409 3509 3508 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3309 3409 3410 3510 3509 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3310 3410 3411 3511 3510 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3311 3411 3412 3512 3511 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3312 3412 3413 3513 3512 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3313 3413 3414 3514 3513 22; # Section3D   starts at (x_frac, z_frac) = (0, 0.89003)   density = 2.6639999999999997 kg/m   thickness = 0.589 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3400 3500 3501 3601 3600 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3401 3501 3502 3602 3601 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3402 3502 3503 3603 3602 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3403 3503 3504 3604 3603 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3404 3504 3505 3605 3604 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3405 3505 3506 3606 3605 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3406 3506 3507 3607 3606 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3407 3507 3508 3608 3607 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3408 3508 3509 3609 3608 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3409 3509 3510 3610 3609 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3410 3510 3511 3611 3610 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3411 3511 3512 3612 3611 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3412 3512 3513 3613 3612 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3413 3513 3514 3614 3613 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3500 3600 3601 3701 3700 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3501 3601 3602 3702 3701 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3502 3602 3603 3703 3702 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3503 3603 3604 3704 3703 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3504 3604 3605 3705 3704 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3505 3605 3606 3706 3705 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3506 3606 3607 3707 3706 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3507 3607 3608 3708 3707 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3508 3608 3609 3709 3708 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3509 3609 3610 3710 3709 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3510 3610 3611 3711 3710 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3511 3611 3612 3712 3711 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3512 3612 3613 3713 3712 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3513 3613 3614 3714 3713 23; # Section3D   starts at (x_frac, z_frac) = (0, 0.89006)   density = 2.637 kg/m   thickness = 0.655 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3600 3700 3701 3801 3800 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3601 3701 3702 3802 3801 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3602 3702 3703 3803 3802 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3603 3703 3704 3804 3803 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3604 3704 3705 3805 3804 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3605 3705 3706 3806 3805 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3606 3706 3707 3807 3806 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3607 3707 3708 3808 3807 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3608 3708 3709 3809 3808 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3609 3709 3710 3810 3809 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3610 3710 3711 3811 3810 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3611 3711 3712 3812 3811 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3612 3712 3713 3813 3812 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3613 3713 3714 3814 3813 24; # Section3D   starts at (x_frac, z_frac) = (0, 0.981898)   density = 2.724 kg/m   thickness = 0.74 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3700 3800 3801 3901 3900 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3701 3801 3802 3902 3901 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3702 3802 3803 3903 3902 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3703 3803 3804 3904 3903 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3704 3804 3805 3905 3904 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3705 3805 3806 3906 3905 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3706 3806 3807 3907 3906 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3707 3807 3808 3908 3907 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3708 3808 3809 3909 3908 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3709 3809 3810 3910 3909 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3710 3810 3811 3911 3910 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3711 3811 3812 3912 3911 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3712 3812 3813 3913 3912 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
element ShellMITC4 3713 3813 3814 3914 3913 25; # Section3D   starts at (x_frac, z_frac) = (0, 0.981928)   density = 2.724 kg/m   thickness = 0.75 m   youngs = 38400.0 MPa   poissons = 0.2
# End deck shell elements

# element ShellMITC4 eleTag iNode jNode kNode lNode secTag
# Begin pier shell elements
element ShellMITC4 3800 401 4000 4100 501 46; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3801 4000 4001 4101 4100 47; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10000 501 4100 4200 601 48; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 10001 4100 4101 4201 4200 49; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 20000 601 4200 4300 701 50; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 20001 4200 4201 4301 4300 51; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 30000 701 4300 4400 801 52; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 30001 4300 4301 4401 4400 53; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 40000 801 4400 4500 901 54; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 40001 4400 4401 4501 4500 55; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 50000 901 4500 4600 1001 56; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 50001 4500 4501 4601 4600 57; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 60000 402 4700 4800 502 58; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 60001 4700 4001 4101 4800 59; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 70000 502 4800 4900 602 60; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 70001 4800 4101 4201 4900 61; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 80000 602 4900 5000 702 62; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 80001 4900 4201 4301 5000 63; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 90000 702 5000 5100 802 64; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 90001 5000 4301 4401 5100 65; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 100000 802 5100 5200 902 66; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 100001 5100 4401 4501 5200 67; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 110000 902 5200 5300 1002 68; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 110001 5200 4501 4601 5300 69; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 120000 1101 5400 5500 1201 70; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 120001 5400 5401 5501 5500 71; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 130000 1201 5500 5600 1301 72; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 130001 5500 5501 5601 5600 73; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 140000 1301 5600 5700 1401 74; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 140001 5600 5601 5701 5700 75; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 150000 1401 5700 5800 1501 76; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 150001 5700 5701 5801 5800 77; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 160000 1501 5800 5900 1601 78; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 160001 5800 5801 5901 5900 79; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 170000 1601 5900 6000 1701 80; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 170001 5900 5901 6001 6000 81; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 180000 1701 6000 6100 1801 82; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 180001 6000 6001 6101 6100 83; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 190000 1801 6100 6200 1901 84; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 190001 6100 6101 6201 6200 85; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 200000 1102 6300 6400 1202 86; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 200001 6300 5401 5501 6400 87; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 210000 1202 6400 6500 1302 88; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 210001 6400 5501 5601 6500 89; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 220000 1302 6500 6600 1402 90; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 220001 6500 5601 5701 6600 91; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 230000 1402 6600 6700 1502 92; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 230001 6600 5701 5801 6700 93; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 240000 1502 6700 6800 1602 94; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 240001 6700 5801 5901 6800 95; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 250000 1602 6800 6900 1702 96; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 250001 6800 5901 6001 6900 97; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 260000 1702 6900 7000 1802 98; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 260001 6900 6001 6101 7000 99; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 270000 1802 7000 7100 1902 100; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 270001 7000 6101 6201 7100 101; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 280000 2101 7200 7300 2201 102; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 280001 7200 7201 7301 7300 103; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 290000 2201 7300 7400 2301 104; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 290001 7300 7301 7401 7400 105; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 300000 2301 7400 7500 2401 106; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 300001 7400 7401 7501 7500 107; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 310000 2401 7500 7600 2501 108; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 310001 7500 7501 7601 7600 109; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 320000 2501 7600 7700 2601 110; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 320001 7600 7601 7701 7700 111; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 330000 2601 7700 7800 2701 112; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 330001 7700 7701 7801 7800 113; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 340000 2701 7800 7900 2801 114; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 340001 7800 7801 7901 7900 115; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 350000 2801 7900 8000 2901 116; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 350001 7900 7901 8001 8000 117; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 360000 2102 8100 8200 2202 118; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 360001 8100 7201 7301 8200 119; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 370000 2202 8200 8300 2302 120; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 370001 8200 7301 7401 8300 121; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 380000 2302 8300 8400 2402 122; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 380001 8300 7401 7501 8400 123; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 390000 2402 8400 8500 2502 124; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 390001 8400 7501 7601 8500 125; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 400000 2502 8500 8600 2602 126; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 400001 8500 7601 7701 8600 127; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 410000 2602 8600 8700 2702 128; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 410001 8600 7701 7801 8700 129; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 420000 2702 8700 8800 2802 130; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 420001 8700 7801 7901 8800 131; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 430000 2802 8800 8900 2902 132; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 430001 8800 7901 8001 8900 133; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 440000 3001 9000 9100 3101 134; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 440001 9000 9001 9101 9100 135; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 450000 3101 9100 9200 3201 136; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 450001 9100 9101 9201 9200 137; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 460000 3201 9200 9300 3301 138; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 460001 9200 9201 9301 9300 139; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 470000 3301 9300 9400 3401 140; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 470001 9300 9301 9401 9400 141; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 480000 3401 9400 9500 3501 142; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 480001 9400 9401 9501 9500 143; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 490000 3501 9500 9600 3601 144; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 490001 9500 9501 9601 9600 145; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 500000 3002 9700 9800 3102 146; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 500001 9700 9001 9101 9800 147; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 510000 3102 9800 9900 3202 148; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 510001 9800 9101 9201 9900 149; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 520000 3202 9900 10000 3302 150; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 520001 9900 9201 9301 10000 151; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 530000 3302 10000 10100 3402 152; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 530001 10000 9301 9401 10100 153; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 540000 3402 10100 10200 3502 154; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 540001 10100 9401 9501 10200 155; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 550000 3502 10200 10300 3602 156; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 550001 10200 9501 9601 10300 157; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 560000 403 10400 10500 503 158; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 560001 10400 10401 10501 10500 159; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 570000 503 10500 10600 603 160; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 570001 10500 10501 10601 10600 161; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 580000 603 10600 10700 703 162; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 580001 10600 10601 10701 10700 163; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 590000 703 10700 10800 803 164; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 590001 10700 10701 10801 10800 165; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 600000 803 10800 10900 903 166; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 600001 10800 10801 10901 10900 167; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 610000 903 10900 11000 1003 168; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 610001 10900 10901 11001 11000 169; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 620000 404 11100 11200 504 170; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 620001 11100 10401 10501 11200 171; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 630000 504 11200 11300 604 172; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 630001 11200 10501 10601 11300 173; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 640000 604 11300 11400 704 174; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 640001 11300 10601 10701 11400 175; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 650000 704 11400 11500 804 176; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 650001 11400 10701 10801 11500 177; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 660000 804 11500 11600 904 178; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 660001 11500 10801 10901 11600 179; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 670000 904 11600 11700 1004 180; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 670001 11600 10901 11001 11700 181; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 680000 1103 11800 11900 1203 182; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 680001 11800 11801 11901 11900 183; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 690000 1203 11900 12000 1303 184; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 690001 11900 11901 12001 12000 185; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 700000 1303 12000 12100 1403 186; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 700001 12000 12001 12101 12100 187; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 710000 1403 12100 12200 1503 188; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 710001 12100 12101 12201 12200 189; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 720000 1503 12200 12300 1603 190; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 720001 12200 12201 12301 12300 191; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 730000 1603 12300 12400 1703 192; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 730001 12300 12301 12401 12400 193; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 740000 1703 12400 12500 1803 194; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 740001 12400 12401 12501 12500 195; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 750000 1803 12500 12600 1903 196; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 750001 12500 12501 12601 12600 197; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 760000 1104 12700 12800 1204 198; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 760001 12700 11801 11901 12800 199; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 770000 1204 12800 12900 1304 200; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 770001 12800 11901 12001 12900 201; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 780000 1304 12900 13000 1404 202; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 780001 12900 12001 12101 13000 203; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 790000 1404 13000 13100 1504 204; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 790001 13000 12101 12201 13100 205; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 800000 1504 13100 13200 1604 206; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 800001 13100 12201 12301 13200 207; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 810000 1604 13200 13300 1704 208; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 810001 13200 12301 12401 13300 209; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 820000 1704 13300 13400 1804 210; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 820001 13300 12401 12501 13400 211; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 830000 1804 13400 13500 1904 212; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 830001 13400 12501 12601 13500 213; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 840000 2103 13600 13700 2203 214; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 840001 13600 13601 13701 13700 215; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 850000 2203 13700 13800 2303 216; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 850001 13700 13701 13801 13800 217; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 860000 2303 13800 13900 2403 218; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 860001 13800 13801 13901 13900 219; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 870000 2403 13900 14000 2503 220; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 870001 13900 13901 14001 14000 221; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 880000 2503 14000 14100 2603 222; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 880001 14000 14001 14101 14100 223; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 890000 2603 14100 14200 2703 224; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 890001 14100 14101 14201 14200 225; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 900000 2703 14200 14300 2803 226; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 900001 14200 14201 14301 14300 227; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 910000 2803 14300 14400 2903 228; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 910001 14300 14301 14401 14400 229; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 920000 2104 14500 14600 2204 230; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 920001 14500 13601 13701 14600 231; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 930000 2204 14600 14700 2304 232; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 930001 14600 13701 13801 14700 233; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 940000 2304 14700 14800 2404 234; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 940001 14700 13801 13901 14800 235; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 950000 2404 14800 14900 2504 236; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 950001 14800 13901 14001 14900 237; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 960000 2504 14900 15000 2604 238; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 960001 14900 14001 14101 15000 239; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 970000 2604 15000 15100 2704 240; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 970001 15000 14101 14201 15100 241; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 980000 2704 15100 15200 2804 242; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 980001 15100 14201 14301 15200 243; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 990000 2804 15200 15300 2904 244; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 990001 15200 14301 14401 15300 245; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1000000 3003 15400 15500 3103 246; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1000001 15400 15401 15501 15500 247; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1010000 3103 15500 15600 3203 248; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1010001 15500 15501 15601 15600 249; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1020000 3203 15600 15700 3303 250; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1020001 15600 15601 15701 15700 251; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1030000 3303 15700 15800 3403 252; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1030001 15700 15701 15801 15800 253; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1040000 3403 15800 15900 3503 254; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1040001 15800 15801 15901 15900 255; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1050000 3503 15900 16000 3603 256; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1050001 15900 15901 16001 16000 257; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1060000 3004 16100 16200 3104 258; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1060001 16100 15401 15501 16200 259; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1070000 3104 16200 16300 3204 260; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1070001 16200 15501 15601 16300 261; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1080000 3204 16300 16400 3304 262; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1080001 16300 15601 15701 16400 263; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1090000 3304 16400 16500 3404 264; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1090001 16400 15701 15801 16500 265; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1100000 3404 16500 16600 3504 266; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1100001 16500 15801 15901 16600 267; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1110000 3504 16600 16700 3604 268; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1110001 16600 15901 16001 16700 269; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1120000 405 16800 16900 505 270; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1120001 16800 16801 16901 16900 271; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1130000 505 16900 17000 605 272; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1130001 16900 16901 17001 17000 273; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1140000 605 17000 17100 705 274; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1140001 17000 17001 17101 17100 275; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1150000 705 17100 17200 805 276; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1150001 17100 17101 17201 17200 277; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1160000 805 17200 17300 905 278; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1160001 17200 17201 17301 17300 279; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1170000 905 17300 17400 1005 280; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1170001 17300 17301 17401 17400 281; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1180000 406 17500 17600 506 282; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1180001 17500 16801 16901 17600 283; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1190000 506 17600 17700 606 284; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1190001 17600 16901 17001 17700 285; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1200000 606 17700 17800 706 286; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1200001 17700 17001 17101 17800 287; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1210000 706 17800 17900 806 288; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1210001 17800 17101 17201 17900 289; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1220000 806 17900 18000 906 290; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1220001 17900 17201 17301 18000 291; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1230000 906 18000 18100 1006 292; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1230001 18000 17301 17401 18100 293; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1240000 1105 18200 18300 1205 294; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1240001 18200 18201 18301 18300 295; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1250000 1205 18300 18400 1305 296; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1250001 18300 18301 18401 18400 297; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1260000 1305 18400 18500 1405 298; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1260001 18400 18401 18501 18500 299; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1270000 1405 18500 18600 1505 300; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1270001 18500 18501 18601 18600 301; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1280000 1505 18600 18700 1605 302; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1280001 18600 18601 18701 18700 303; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1290000 1605 18700 18800 1705 304; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1290001 18700 18701 18801 18800 305; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1300000 1705 18800 18900 1805 306; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1300001 18800 18801 18901 18900 307; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1310000 1805 18900 19000 1905 308; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1310001 18900 18901 19001 19000 309; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1320000 1106 19100 19200 1206 310; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1320001 19100 18201 18301 19200 311; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1330000 1206 19200 19300 1306 312; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1330001 19200 18301 18401 19300 313; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1340000 1306 19300 19400 1406 314; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1340001 19300 18401 18501 19400 315; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1350000 1406 19400 19500 1506 316; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1350001 19400 18501 18601 19500 317; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1360000 1506 19500 19600 1606 318; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1360001 19500 18601 18701 19600 319; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1370000 1606 19600 19700 1706 320; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1370001 19600 18701 18801 19700 321; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1380000 1706 19700 19800 1806 322; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1380001 19700 18801 18901 19800 323; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1390000 1806 19800 19900 1906 324; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1390001 19800 18901 19001 19900 325; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1400000 2105 20000 20100 2205 326; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1400001 20000 20001 20101 20100 327; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1410000 2205 20100 20200 2305 328; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1410001 20100 20101 20201 20200 329; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1420000 2305 20200 20300 2405 330; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1420001 20200 20201 20301 20300 331; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1430000 2405 20300 20400 2505 332; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1430001 20300 20301 20401 20400 333; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1440000 2505 20400 20500 2605 334; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1440001 20400 20401 20501 20500 335; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1450000 2605 20500 20600 2705 336; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1450001 20500 20501 20601 20600 337; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1460000 2705 20600 20700 2805 338; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1460001 20600 20601 20701 20700 339; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1470000 2805 20700 20800 2905 340; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1470001 20700 20701 20801 20800 341; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1480000 2106 20900 21000 2206 342; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1480001 20900 20001 20101 21000 343; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1490000 2206 21000 21100 2306 344; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1490001 21000 20101 20201 21100 345; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1500000 2306 21100 21200 2406 346; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1500001 21100 20201 20301 21200 347; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1510000 2406 21200 21300 2506 348; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1510001 21200 20301 20401 21300 349; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1520000 2506 21300 21400 2606 350; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1520001 21300 20401 20501 21400 351; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1530000 2606 21400 21500 2706 352; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1530001 21400 20501 20601 21500 353; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1540000 2706 21500 21600 2806 354; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1540001 21500 20601 20701 21600 355; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1550000 2806 21600 21700 2906 356; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1550001 21600 20701 20801 21700 357; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1560000 3005 21800 21900 3105 358; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1560001 21800 21801 21901 21900 359; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1570000 3105 21900 22000 3205 360; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1570001 21900 21901 22001 22000 361; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1580000 3205 22000 22100 3305 362; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1580001 22000 22001 22101 22100 363; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1590000 3305 22100 22200 3405 364; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1590001 22100 22101 22201 22200 365; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1600000 3405 22200 22300 3505 366; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1600001 22200 22201 22301 22300 367; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1610000 3505 22300 22400 3605 368; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1610001 22300 22301 22401 22400 369; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1620000 3006 22500 22600 3106 370; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1620001 22500 21801 21901 22600 371; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1630000 3106 22600 22700 3206 372; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1630001 22600 21901 22001 22700 373; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1640000 3206 22700 22800 3306 374; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1640001 22700 22001 22101 22800 375; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1650000 3306 22800 22900 3406 376; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1650001 22800 22101 22201 22900 377; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1660000 3406 22900 23000 3506 378; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1660001 22900 22201 22301 23000 379; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1670000 3506 23000 23100 3606 380; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1670001 23000 22301 22401 23100 381; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1680000 408 23200 23300 508 382; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1680001 23200 23201 23301 23300 383; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1690000 508 23300 23400 608 384; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1690001 23300 23301 23401 23400 385; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1700000 608 23400 23500 708 386; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1700001 23400 23401 23501 23500 387; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1710000 708 23500 23600 808 388; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1710001 23500 23501 23601 23600 389; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1720000 808 23600 23700 908 390; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1720001 23600 23601 23701 23700 391; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1730000 908 23700 23800 1008 392; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1730001 23700 23701 23801 23800 393; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1740000 409 23900 24000 509 394; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1740001 23900 23201 23301 24000 395; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1750000 509 24000 24100 609 396; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1750001 24000 23301 23401 24100 397; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1760000 609 24100 24200 709 398; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1760001 24100 23401 23501 24200 399; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1770000 709 24200 24300 809 400; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1770001 24200 23501 23601 24300 401; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1780000 809 24300 24400 909 402; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1780001 24300 23601 23701 24400 403; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1790000 909 24400 24500 1009 404; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1790001 24400 23701 23801 24500 405; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1800000 1108 24600 24700 1208 406; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1800001 24600 24601 24701 24700 407; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1810000 1208 24700 24800 1308 408; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1810001 24700 24701 24801 24800 409; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1820000 1308 24800 24900 1408 410; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1820001 24800 24801 24901 24900 411; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1830000 1408 24900 25000 1508 412; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1830001 24900 24901 25001 25000 413; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1840000 1508 25000 25100 1608 414; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1840001 25000 25001 25101 25100 415; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1850000 1608 25100 25200 1708 416; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1850001 25100 25101 25201 25200 417; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1860000 1708 25200 25300 1808 418; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1860001 25200 25201 25301 25300 419; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1870000 1808 25300 25400 1908 420; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1870001 25300 25301 25401 25400 421; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1880000 1109 25500 25600 1209 422; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1880001 25500 24601 24701 25600 423; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1890000 1209 25600 25700 1309 424; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1890001 25600 24701 24801 25700 425; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1900000 1309 25700 25800 1409 426; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1900001 25700 24801 24901 25800 427; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1910000 1409 25800 25900 1509 428; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1910001 25800 24901 25001 25900 429; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1920000 1509 25900 26000 1609 430; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1920001 25900 25001 25101 26000 431; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1930000 1609 26000 26100 1709 432; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1930001 26000 25101 25201 26100 433; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1940000 1709 26100 26200 1809 434; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1940001 26100 25201 25301 26200 435; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1950000 1809 26200 26300 1909 436; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1950001 26200 25301 25401 26300 437; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1960000 2108 26400 26500 2208 438; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1960001 26400 26401 26501 26500 439; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1970000 2208 26500 26600 2308 440; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1970001 26500 26501 26601 26600 441; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1980000 2308 26600 26700 2408 442; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1980001 26600 26601 26701 26700 443; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1990000 2408 26700 26800 2508 444; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 1990001 26700 26701 26801 26800 445; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2000000 2508 26800 26900 2608 446; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2000001 26800 26801 26901 26900 447; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2010000 2608 26900 27000 2708 448; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2010001 26900 26901 27001 27000 449; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2020000 2708 27000 27100 2808 450; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2020001 27000 27001 27101 27100 451; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2030000 2808 27100 27200 2908 452; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2030001 27100 27101 27201 27200 453; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2040000 2109 27300 27400 2209 454; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2040001 27300 26401 26501 27400 455; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2050000 2209 27400 27500 2309 456; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2050001 27400 26501 26601 27500 457; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2060000 2309 27500 27600 2409 458; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2060001 27500 26601 26701 27600 459; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2070000 2409 27600 27700 2509 460; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2070001 27600 26701 26801 27700 461; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2080000 2509 27700 27800 2609 462; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2080001 27700 26801 26901 27800 463; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2090000 2609 27800 27900 2709 464; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2090001 27800 26901 27001 27900 465; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2100000 2709 27900 28000 2809 466; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2100001 27900 27001 27101 28000 467; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2110000 2809 28000 28100 2909 468; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2110001 28000 27101 27201 28100 469; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2120000 3008 28200 28300 3108 470; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2120001 28200 28201 28301 28300 471; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2130000 3108 28300 28400 3208 472; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2130001 28300 28301 28401 28400 473; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2140000 3208 28400 28500 3308 474; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2140001 28400 28401 28501 28500 475; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2150000 3308 28500 28600 3408 476; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2150001 28500 28501 28601 28600 477; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2160000 3408 28600 28700 3508 478; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2160001 28600 28601 28701 28700 479; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2170000 3508 28700 28800 3608 480; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2170001 28700 28701 28801 28800 481; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2180000 3009 28900 29000 3109 482; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2180001 28900 28201 28301 29000 483; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2190000 3109 29000 29100 3209 484; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2190001 29000 28301 28401 29100 485; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2200000 3209 29100 29200 3309 486; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2200001 29100 28401 28501 29200 487; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2210000 3309 29200 29300 3409 488; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2210001 29200 28501 28601 29300 489; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2220000 3409 29300 29400 3509 490; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2220001 29300 28601 28701 29400 491; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2230000 3509 29400 29500 3609 492; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2230001 29400 28701 28801 29500 493; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2240000 410 29600 29700 510 494; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2240001 29600 29601 29701 29700 495; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2250000 510 29700 29800 610 496; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2250001 29700 29701 29801 29800 497; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2260000 610 29800 29900 710 498; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2260001 29800 29801 29901 29900 499; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2270000 710 29900 30000 810 500; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2270001 29900 29901 30001 30000 501; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2280000 810 30000 30100 910 502; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2280001 30000 30001 30101 30100 503; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2290000 910 30100 30200 1010 504; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2290001 30100 30101 30201 30200 505; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2300000 411 30300 30400 511 506; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2300001 30300 29601 29701 30400 507; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2310000 511 30400 30500 611 508; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2310001 30400 29701 29801 30500 509; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2320000 611 30500 30600 711 510; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2320001 30500 29801 29901 30600 511; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2330000 711 30600 30700 811 512; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2330001 30600 29901 30001 30700 513; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2340000 811 30700 30800 911 514; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2340001 30700 30001 30101 30800 515; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2350000 911 30800 30900 1011 516; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2350001 30800 30101 30201 30900 517; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2360000 1110 31000 31100 1210 518; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2360001 31000 31001 31101 31100 519; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2370000 1210 31100 31200 1310 520; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2370001 31100 31101 31201 31200 521; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2380000 1310 31200 31300 1410 522; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2380001 31200 31201 31301 31300 523; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2390000 1410 31300 31400 1510 524; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2390001 31300 31301 31401 31400 525; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2400000 1510 31400 31500 1610 526; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2400001 31400 31401 31501 31500 527; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2410000 1610 31500 31600 1710 528; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2410001 31500 31501 31601 31600 529; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2420000 1710 31600 31700 1810 530; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2420001 31600 31601 31701 31700 531; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2430000 1810 31700 31800 1910 532; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2430001 31700 31701 31801 31800 533; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2440000 1111 31900 32000 1211 534; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2440001 31900 31001 31101 32000 535; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2450000 1211 32000 32100 1311 536; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2450001 32000 31101 31201 32100 537; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2460000 1311 32100 32200 1411 538; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2460001 32100 31201 31301 32200 539; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2470000 1411 32200 32300 1511 540; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2470001 32200 31301 31401 32300 541; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2480000 1511 32300 32400 1611 542; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2480001 32300 31401 31501 32400 543; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2490000 1611 32400 32500 1711 544; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2490001 32400 31501 31601 32500 545; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2500000 1711 32500 32600 1811 546; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2500001 32500 31601 31701 32600 547; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2510000 1811 32600 32700 1911 548; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2510001 32600 31701 31801 32700 549; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2520000 2110 32800 32900 2210 550; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2520001 32800 32801 32901 32900 551; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2530000 2210 32900 33000 2310 552; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2530001 32900 32901 33001 33000 553; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2540000 2310 33000 33100 2410 554; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2540001 33000 33001 33101 33100 555; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2550000 2410 33100 33200 2510 556; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2550001 33100 33101 33201 33200 557; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2560000 2510 33200 33300 2610 558; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2560001 33200 33201 33301 33300 559; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2570000 2610 33300 33400 2710 560; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2570001 33300 33301 33401 33400 561; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2580000 2710 33400 33500 2810 562; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2580001 33400 33401 33501 33500 563; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2590000 2810 33500 33600 2910 564; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2590001 33500 33501 33601 33600 565; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2600000 2111 33700 33800 2211 566; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2600001 33700 32801 32901 33800 567; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2610000 2211 33800 33900 2311 568; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2610001 33800 32901 33001 33900 569; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2620000 2311 33900 34000 2411 570; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2620001 33900 33001 33101 34000 571; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2630000 2411 34000 34100 2511 572; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2630001 34000 33101 33201 34100 573; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2640000 2511 34100 34200 2611 574; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2640001 34100 33201 33301 34200 575; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2650000 2611 34200 34300 2711 576; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2650001 34200 33301 33401 34300 577; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2660000 2711 34300 34400 2811 578; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2660001 34300 33401 33501 34400 579; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2670000 2811 34400 34500 2911 580; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2670001 34400 33501 33601 34500 581; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2680000 3010 34600 34700 3110 582; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2680001 34600 34601 34701 34700 583; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2690000 3110 34700 34800 3210 584; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2690001 34700 34701 34801 34800 585; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2700000 3210 34800 34900 3310 586; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2700001 34800 34801 34901 34900 587; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2710000 3310 34900 35000 3410 588; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2710001 34900 34901 35001 35000 589; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2720000 3410 35000 35100 3510 590; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2720001 35000 35001 35101 35100 591; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2730000 3510 35100 35200 3610 592; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2730001 35100 35101 35201 35200 593; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2740000 3011 35300 35400 3111 594; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2740001 35300 34601 34701 35400 595; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2750000 3111 35400 35500 3211 596; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2750001 35400 34701 34801 35500 597; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2760000 3211 35500 35600 3311 598; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2760001 35500 34801 34901 35600 599; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2770000 3311 35600 35700 3411 600; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2770001 35600 34901 35001 35700 601; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2780000 3411 35700 35800 3511 602; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2780001 35700 35001 35101 35800 603; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2790000 3511 35800 35900 3611 604; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2790001 35800 35101 35201 35900 605; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2800000 412 36000 36100 512 606; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2800001 36000 36001 36101 36100 607; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2810000 512 36100 36200 612 608; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2810001 36100 36101 36201 36200 609; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2820000 612 36200 36300 712 610; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2820001 36200 36201 36301 36300 611; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2830000 712 36300 36400 812 612; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2830001 36300 36301 36401 36400 613; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2840000 812 36400 36500 912 614; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2840001 36400 36401 36501 36500 615; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2850000 912 36500 36600 1012 616; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2850001 36500 36501 36601 36600 617; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2860000 413 36700 36800 513 618; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2860001 36700 36001 36101 36800 619; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2870000 513 36800 36900 613 620; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2870001 36800 36101 36201 36900 621; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2880000 613 36900 37000 713 622; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2880001 36900 36201 36301 37000 623; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2890000 713 37000 37100 813 624; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2890001 37000 36301 36401 37100 625; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2900000 813 37100 37200 913 626; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2900001 37100 36401 36501 37200 627; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2910000 913 37200 37300 1013 628; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2910001 37200 36501 36601 37300 629; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2920000 1112 37400 37500 1212 630; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2920001 37400 37401 37501 37500 631; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2930000 1212 37500 37600 1312 632; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2930001 37500 37501 37601 37600 633; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2940000 1312 37600 37700 1412 634; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2940001 37600 37601 37701 37700 635; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2950000 1412 37700 37800 1512 636; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2950001 37700 37701 37801 37800 637; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2960000 1512 37800 37900 1612 638; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2960001 37800 37801 37901 37900 639; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2970000 1612 37900 38000 1712 640; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2970001 37900 37901 38001 38000 641; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2980000 1712 38000 38100 1812 642; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2980001 38000 38001 38101 38100 643; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2990000 1812 38100 38200 1912 644; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 2990001 38100 38101 38201 38200 645; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3000000 1113 38300 38400 1213 646; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3000001 38300 37401 37501 38400 647; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3010000 1213 38400 38500 1313 648; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3010001 38400 37501 37601 38500 649; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3020000 1313 38500 38600 1413 650; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3020001 38500 37601 37701 38600 651; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3030000 1413 38600 38700 1513 652; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3030001 38600 37701 37801 38700 653; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3040000 1513 38700 38800 1613 654; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3040001 38700 37801 37901 38800 655; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3050000 1613 38800 38900 1713 656; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3050001 38800 37901 38001 38900 657; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3060000 1713 38900 39000 1813 658; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3060001 38900 38001 38101 39000 659; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3070000 1813 39000 39100 1913 660; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3070001 39000 38101 38201 39100 661; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3080000 2112 39200 39300 2212 662; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3080001 39200 39201 39301 39300 663; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3090000 2212 39300 39400 2312 664; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3090001 39300 39301 39401 39400 665; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3100000 2312 39400 39500 2412 666; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3100001 39400 39401 39501 39500 667; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3110000 2412 39500 39600 2512 668; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3110001 39500 39501 39601 39600 669; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3120000 2512 39600 39700 2612 670; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3120001 39600 39601 39701 39700 671; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3130000 2612 39700 39800 2712 672; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3130001 39700 39701 39801 39800 673; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3140000 2712 39800 39900 2812 674; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3140001 39800 39801 39901 39900 675; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3150000 2812 39900 40000 2912 676; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3150001 39900 39901 40001 40000 677; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3160000 2113 40100 40200 2213 678; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3160001 40100 39201 39301 40200 679; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3170000 2213 40200 40300 2313 680; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3170001 40200 39301 39401 40300 681; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3180000 2313 40300 40400 2413 682; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3180001 40300 39401 39501 40400 683; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3190000 2413 40400 40500 2513 684; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3190001 40400 39501 39601 40500 685; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3200000 2513 40500 40600 2613 686; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3200001 40500 39601 39701 40600 687; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3210000 2613 40600 40700 2713 688; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3210001 40600 39701 39801 40700 689; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3220000 2713 40700 40800 2813 690; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3220001 40700 39801 39901 40800 691; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3230000 2813 40800 40900 2913 692; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3230001 40800 39901 40001 40900 693; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3240000 3012 41000 41100 3112 694; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3240001 41000 41001 41101 41100 695; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3250000 3112 41100 41200 3212 696; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3250001 41100 41101 41201 41200 697; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3260000 3212 41200 41300 3312 698; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3260001 41200 41201 41301 41300 699; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3270000 3312 41300 41400 3412 700; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3270001 41300 41301 41401 41400 701; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3280000 3412 41400 41500 3512 702; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3280001 41400 41401 41501 41500 703; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3290000 3512 41500 41600 3612 704; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3290001 41500 41501 41601 41600 705; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3300000 3013 41700 41800 3113 706; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3300001 41700 41001 41101 41800 707; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3310000 3113 41800 41900 3213 708; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3310001 41800 41101 41201 41900 709; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3320000 3213 41900 42000 3313 710; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3320001 41900 41201 41301 42000 711; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3330000 3313 42000 42100 3413 712; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3330001 42000 41301 41401 42100 713; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3340000 3413 42100 42200 3513 714; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3340001 42100 41401 41501 42200 715; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3350000 3513 42200 42300 3613 716; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 1.266 m   youngs = 38400 MPa   poissons = 0.2
element ShellMITC4 3350001 42200 41501 41601 42300 717; # Section3D   starts at (x_frac, z_frac) = (0, 0)   density = 2.724 kg/m   thickness = 0.362 m   youngs = 38400 MPa   poissons = 0.2
# End pier shell elements



timeSeries Linear 1

pattern Plain 1 1 {
# load nodeTag N_x N_y N_z N_rx N_ry N_rz
# Begin loads
load 4301 0 10000 0 0 0 0
# End loads
}

recorder Element -file generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-1,000-0--forces.out -ele 1 400 forces

# recorder Node -file path -node nodeTags -dof direction disp
# Begin translation recorders
recorder Node -file generated-data/bridge-705-debug-3d/opensees-responses/bridge-705-debug-3d-params=-1,000-0-node-y.out -node 100 101 102 103 104 105 106 107 108 109 110 111 112 113 114 200 201 202 203 204 205 206 207 208 209 210 211 212 213 214 300 301 302 303 304 305 306 307 308 309 310 311 312 313 314 400 401 402 403 404 405 406 407 408 409 410 411 412 413 414 500 501 502 503 504 505 506 507 508 509 510 511 512 513 514 600 601 602 603 604 605 606 607 608 609 610 611 612 613 614 700 701 702 703 704 705 706 707 708 709 710 711 712 713 714 800 801 802 803 804 805 806 807 808 809 810 811 812 813 814 900 901 902 903 904 905 906 907 908 909 910 911 912 913 914 1000 1001 1002 1003 1004 1005 1006 1007 1008 1009 1010 1011 1012 1013 1014 1100 1101 1102 1103 1104 1105 1106 1107 1108 1109 1110 1111 1112 1113 1114 1200 1201 1202 1203 1204 1205 1206 1207 1208 1209 1210 1211 1212 1213 1214 1300 1301 1302 1303 1304 1305 1306 1307 1308 1309 1310 1311 1312 1313 1314 1400 1401 1402 1403 1404 1405 1406 1407 1408 1409 1410 1411 1412 1413 1414 1500 1501 1502 1503 1504 1505 1506 1507 1508 1509 1510 1511 1512 1513 1514 1600 1601 1602 1603 1604 1605 1606 1607 1608 1609 1610 1611 1612 1613 1614 1700 1701 1702 1703 1704 1705 1706 1707 1708 1709 1710 1711 1712 1713 1714 1800 1801 1802 1803 1804 1805 1806 1807 1808 1809 1810 1811 1812 1813 1814 1900 1901 1902 1903 1904 1905 1906 1907 1908 1909 1910 1911 1912 1913 1914 2000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 2011 2012 2013 2014 2100 2101 2102 2103 2104 2105 2106 2107 2108 2109 2110 2111 2112 2113 2114 2200 2201 2202 2203 2204 2205 2206 2207 2208 2209 2210 2211 2212 2213 2214 2300 2301 2302 2303 2304 2305 2306 2307 2308 2309 2310 2311 2312 2313 2314 2400 2401 2402 2403 2404 2405 2406 2407 2408 2409 2410 2411 2412 2413 2414 2500 2501 2502 2503 2504 2505 2506 2507 2508 2509 2510 2511 2512 2513 2514 2600 2601 2602 2603 2604 2605 2606 2607 2608 2609 2610 2611 2612 2613 2614 2700 2701 2702 2703 2704 2705 2706 2707 2708 2709 2710 2711 2712 2713 2714 2800 2801 2802 2803 2804 2805 2806 2807 2808 2809 2810 2811 2812 2813 2814 2900 2901 2902 2903 2904 2905 2906 2907 2908 2909 2910 2911 2912 2913 2914 3000 3001 3002 3003 3004 3005 3006 3007 3008 3009 3010 3011 3012 3013 3014 3100 3101 3102 3103 3104 3105 3106 3107 3108 3109 3110 3111 3112 3113 3114 3200 3201 3202 3203 3204 3205 3206 3207 3208 3209 3210 3211 3212 3213 3214 3300 3301 3302 3303 3304 3305 3306 3307 3308 3309 3310 3311 3312 3313 3314 3400 3401 3402 3403 3404 3405 3406 3407 3408 3409 3410 3411 3412 3413 3414 3500 3501 3502 3503 3504 3505 3506 3507 3508 3509 3510 3511 3512 3513 3514 3600 3601 3602 3603 3604 3605 3606 3607 3608 3609 3610 3611 3612 3613 3614 3700 3701 3702 3703 3704 3705 3706 3707 3708 3709 3710 3711 3712 3713 3714 3800 3801 3802 3803 3804 3805 3806 3807 3808 3809 3810 3811 3812 3813 3814 3900 3901 3902 3903 3904 3905 3906 3907 3908 3909 3910 3911 3912 3913 3914 401 4000 4001 501 4100 4101 601 4200 4201 701 4300 4301 801 4400 4401 901 4500 4501 1001 4600 4601 402 4700 4001 502 4800 4101 602 4900 4201 702 5000 4301 802 5100 4401 902 5200 4501 1002 5300 4601 1101 5400 5401 1201 5500 5501 1301 5600 5601 1401 5700 5701 1501 5800 5801 1601 5900 5901 1701 6000 6001 1801 6100 6101 1901 6200 6201 1102 6300 5401 1202 6400 5501 1302 6500 5601 1402 6600 5701 1502 6700 5801 1602 6800 5901 1702 6900 6001 1802 7000 6101 1902 7100 6201 2101 7200 7201 2201 7300 7301 2301 7400 7401 2401 7500 7501 2501 7600 7601 2601 7700 7701 2701 7800 7801 2801 7900 7901 2901 8000 8001 2102 8100 7201 2202 8200 7301 2302 8300 7401 2402 8400 7501 2502 8500 7601 2602 8600 7701 2702 8700 7801 2802 8800 7901 2902 8900 8001 3001 9000 9001 3101 9100 9101 3201 9200 9201 3301 9300 9301 3401 9400 9401 3501 9500 9501 3601 9600 9601 3002 9700 9001 3102 9800 9101 3202 9900 9201 3302 10000 9301 3402 10100 9401 3502 10200 9501 3602 10300 9601 403 10400 10401 503 10500 10501 603 10600 10601 703 10700 10701 803 10800 10801 903 10900 10901 1003 11000 11001 404 11100 10401 504 11200 10501 604 11300 10601 704 11400 10701 804 11500 10801 904 11600 10901 1004 11700 11001 1103 11800 11801 1203 11900 11901 1303 12000 12001 1403 12100 12101 1503 12200 12201 1603 12300 12301 1703 12400 12401 1803 12500 12501 1903 12600 12601 1104 12700 11801 1204 12800 11901 1304 12900 12001 1404 13000 12101 1504 13100 12201 1604 13200 12301 1704 13300 12401 1804 13400 12501 1904 13500 12601 2103 13600 13601 2203 13700 13701 2303 13800 13801 2403 13900 13901 2503 14000 14001 2603 14100 14101 2703 14200 14201 2803 14300 14301 2903 14400 14401 2104 14500 13601 2204 14600 13701 2304 14700 13801 2404 14800 13901 2504 14900 14001 2604 15000 14101 2704 15100 14201 2804 15200 14301 2904 15300 14401 3003 15400 15401 3103 15500 15501 3203 15600 15601 3303 15700 15701 3403 15800 15801 3503 15900 15901 3603 16000 16001 3004 16100 15401 3104 16200 15501 3204 16300 15601 3304 16400 15701 3404 16500 15801 3504 16600 15901 3604 16700 16001 405 16800 16801 505 16900 16901 605 17000 17001 705 17100 17101 805 17200 17201 905 17300 17301 1005 17400 17401 406 17500 16801 506 17600 16901 606 17700 17001 706 17800 17101 806 17900 17201 906 18000 17301 1006 18100 17401 1105 18200 18201 1205 18300 18301 1305 18400 18401 1405 18500 18501 1505 18600 18601 1605 18700 18701 1705 18800 18801 1805 18900 18901 1905 19000 19001 1106 19100 18201 1206 19200 18301 1306 19300 18401 1406 19400 18501 1506 19500 18601 1606 19600 18701 1706 19700 18801 1806 19800 18901 1906 19900 19001 2105 20000 20001 2205 20100 20101 2305 20200 20201 2405 20300 20301 2505 20400 20401 2605 20500 20501 2705 20600 20601 2805 20700 20701 2905 20800 20801 2106 20900 20001 2206 21000 20101 2306 21100 20201 2406 21200 20301 2506 21300 20401 2606 21400 20501 2706 21500 20601 2806 21600 20701 2906 21700 20801 3005 21800 21801 3105 21900 21901 3205 22000 22001 3305 22100 22101 3405 22200 22201 3505 22300 22301 3605 22400 22401 3006 22500 21801 3106 22600 21901 3206 22700 22001 3306 22800 22101 3406 22900 22201 3506 23000 22301 3606 23100 22401 408 23200 23201 508 23300 23301 608 23400 23401 708 23500 23501 808 23600 23601 908 23700 23701 1008 23800 23801 409 23900 23201 509 24000 23301 609 24100 23401 709 24200 23501 809 24300 23601 909 24400 23701 1009 24500 23801 1108 24600 24601 1208 24700 24701 1308 24800 24801 1408 24900 24901 1508 25000 25001 1608 25100 25101 1708 25200 25201 1808 25300 25301 1908 25400 25401 1109 25500 24601 1209 25600 24701 1309 25700 24801 1409 25800 24901 1509 25900 25001 1609 26000 25101 1709 26100 25201 1809 26200 25301 1909 26300 25401 2108 26400 26401 2208 26500 26501 2308 26600 26601 2408 26700 26701 2508 26800 26801 2608 26900 26901 2708 27000 27001 2808 27100 27101 2908 27200 27201 2109 27300 26401 2209 27400 26501 2309 27500 26601 2409 27600 26701 2509 27700 26801 2609 27800 26901 2709 27900 27001 2809 28000 27101 2909 28100 27201 3008 28200 28201 3108 28300 28301 3208 28400 28401 3308 28500 28501 3408 28600 28601 3508 28700 28701 3608 28800 28801 3009 28900 28201 3109 29000 28301 3209 29100 28401 3309 29200 28501 3409 29300 28601 3509 29400 28701 3609 29500 28801 410 29600 29601 510 29700 29701 610 29800 29801 710 29900 29901 810 30000 30001 910 30100 30101 1010 30200 30201 411 30300 29601 511 30400 29701 611 30500 29801 711 30600 29901 811 30700 30001 911 30800 30101 1011 30900 30201 1110 31000 31001 1210 31100 31101 1310 31200 31201 1410 31300 31301 1510 31400 31401 1610 31500 31501 1710 31600 31601 1810 31700 31701 1910 31800 31801 1111 31900 31001 1211 32000 31101 1311 32100 31201 1411 32200 31301 1511 32300 31401 1611 32400 31501 1711 32500 31601 1811 32600 31701 1911 32700 31801 2110 32800 32801 2210 32900 32901 2310 33000 33001 2410 33100 33101 2510 33200 33201 2610 33300 33301 2710 33400 33401 2810 33500 33501 2910 33600 33601 2111 33700 32801 2211 33800 32901 2311 33900 33001 2411 34000 33101 2511 34100 33201 2611 34200 33301 2711 34300 33401 2811 34400 33501 2911 34500 33601 3010 34600 34601 3110 34700 34701 3210 34800 34801 3310 34900 34901 3410 35000 35001 3510 35100 35101 3610 35200 35201 3011 35300 34601 3111 35400 34701 3211 35500 34801 3311 35600 34901 3411 35700 35001 3511 35800 35101 3611 35900 35201 412 36000 36001 512 36100 36101 612 36200 36201 712 36300 36301 812 36400 36401 912 36500 36501 1012 36600 36601 413 36700 36001 513 36800 36101 613 36900 36201 713 37000 36301 813 37100 36401 913 37200 36501 1013 37300 36601 1112 37400 37401 1212 37500 37501 1312 37600 37601 1412 37700 37701 1512 37800 37801 1612 37900 37901 1712 38000 38001 1812 38100 38101 1912 38200 38201 1113 38300 37401 1213 38400 37501 1313 38500 37601 1413 38600 37701 1513 38700 37801 1613 38800 37901 1713 38900 38001 1813 39000 38101 1913 39100 38201 2112 39200 39201 2212 39300 39301 2312 39400 39401 2412 39500 39501 2512 39600 39601 2612 39700 39701 2712 39800 39801 2812 39900 39901 2912 40000 40001 2113 40100 39201 2213 40200 39301 2313 40300 39401 2413 40400 39501 2513 40500 39601 2613 40600 39701 2713 40700 39801 2813 40800 39901 2913 40900 40001 3012 41000 41001 3112 41100 41101 3212 41200 41201 3312 41300 41301 3412 41400 41401 3512 41500 41501 3612 41600 41601 3013 41700 41001 3113 41800 41101 3213 41900 41201 3313 42000 41301 3413 42100 41401 3513 42200 41501 3613 42300 41601 -dof 2 disp
# End translation recorders



system BandGeneral
numberer RCM
constraints Plain
integrator DisplacementControl 4301 2 1.0
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
