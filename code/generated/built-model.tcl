wipe

model basic -ndm 2 -ndf 3

node 1 0.0 0
node 2 0.2 0
node 3 0.4 0
node 4 0.6000000000000001 0
node 5 0.8 0
node 6 1.0 0
node 7 1.2000000000000002 0
node 8 1.4000000000000001 0
node 9 1.6 0
node 10 1.8 0
node 11 2.0 0
node 12 2.2 0
node 13 2.4000000000000004 0
node 14 2.6 0
node 15 2.8000000000000003 0
node 16 3.0 0
node 17 3.2 0
node 18 3.4000000000000004 0
node 19 3.6 0
node 20 3.8000000000000003 0
node 21 4.0 0
node 22 4.2 0
node 23 4.4 0
node 24 4.6000000000000005 0
node 25 4.800000000000001 0
node 26 5.0 0
node 27 5.2 0
node 28 5.4 0
node 29 5.6000000000000005 0
node 30 5.800000000000001 0
node 31 6.0 0
node 32 6.2 0
node 33 6.4 0
node 34 6.6000000000000005 0
node 35 6.800000000000001 0
node 36 7.0 0
node 37 7.2 0
node 38 7.4 0
node 39 7.6000000000000005 0
node 40 7.800000000000001 0
node 41 8.0 0
node 42 8.200000000000001 0
node 43 8.4 0
node 44 8.6 0
node 45 8.8 0
node 46 9.0 0
node 47 9.200000000000001 0
node 48 9.4 0
node 49 9.600000000000001 0
node 50 9.8 0
node 51 10.0 0
node 52 10.200000000000001 0
node 53 10.4 0
node 54 10.600000000000001 0
node 55 10.8 0
node 56 11.0 0
node 57 11.200000000000001 0
node 58 11.4 0
node 59 11.600000000000001 0
node 60 11.8 0
node 61 12.0 0
node 62 12.200000000000001 0
node 63 12.4 0
node 64 12.600000000000001 0
node 65 12.8 0
node 66 13.0 0
node 67 13.200000000000001 0
node 68 13.4 0
node 69 13.600000000000001 0
node 70 13.8 0
node 71 14.0 0
node 72 14.200000000000001 0
node 73 14.4 0
node 74 14.600000000000001 0
node 75 14.8 0
node 76 15.0 0
node 77 15.200000000000001 0
node 78 15.4 0
node 79 15.600000000000001 0
node 80 15.8 0
node 81 16.0 0
node 82 16.2 0
node 83 16.400000000000002 0
node 84 16.6 0
node 85 16.8 0
node 86 17.0 0
node 87 17.2 0
node 88 17.400000000000002 0
node 89 17.6 0
node 90 17.8 0
node 91 18.0 0
node 92 18.2 0
node 93 18.400000000000002 0
node 94 18.6 0
node 95 18.8 0
node 96 19.0 0
node 97 19.200000000000003 0
node 98 19.400000000000002 0
node 99 19.6 0
node 100 19.8 0
node 101 20.0 0

fix 1 0 1 0
fix 15 0 1 0
fix 29 0 1 0
fix 43 0 1 0
fix 58 0 1 0
fix 72 0 1 0
fix 86 0 1 0
fix 101 0 1 0

geomTransf Linear 1

uniaxialMaterial Concrete02 1 -2.8800000e+07 -1.6044568e-03 -2.8800000e+07 -3.5000000e-03 2.0000000e-01 2.8800000e+06 3.5900000e+10
uniaxialMaterial Steel01    2 3.4800000e+08  2.0000000e+11  0.0000000e+00

section Fiber 1 {
    patch rect 1 1 30 -2.0000000e-01 -1.0750000e+00 0.0000000e+00 1.0750000e+00
    patch rect 1 1 30 -1.2500000e+00 -2.5000000e-01 -2.0000000e-01 2.5000000e-01
}

element dispBeamColumn 1 1 2 5 1 1
element dispBeamColumn 2 2 3 5 1 1
element dispBeamColumn 3 3 4 5 1 1
element dispBeamColumn 4 4 5 5 1 1
element dispBeamColumn 5 5 6 5 1 1
element dispBeamColumn 6 6 7 5 1 1
element dispBeamColumn 7 7 8 5 1 1
element dispBeamColumn 8 8 9 5 1 1
element dispBeamColumn 9 9 10 5 1 1
element dispBeamColumn 10 10 11 5 1 1
element dispBeamColumn 11 11 12 5 1 1
element dispBeamColumn 12 12 13 5 1 1
element dispBeamColumn 13 13 14 5 1 1
element dispBeamColumn 14 14 15 5 1 1
element dispBeamColumn 15 15 16 5 1 1
element dispBeamColumn 16 16 17 5 1 1
element dispBeamColumn 17 17 18 5 1 1
element dispBeamColumn 18 18 19 5 1 1
element dispBeamColumn 19 19 20 5 1 1
element dispBeamColumn 20 20 21 5 1 1
element dispBeamColumn 21 21 22 5 1 1
element dispBeamColumn 22 22 23 5 1 1
element dispBeamColumn 23 23 24 5 1 1
element dispBeamColumn 24 24 25 5 1 1
element dispBeamColumn 25 25 26 5 1 1
element dispBeamColumn 26 26 27 5 1 1
element dispBeamColumn 27 27 28 5 1 1
element dispBeamColumn 28 28 29 5 1 1
element dispBeamColumn 29 29 30 5 1 1
element dispBeamColumn 30 30 31 5 1 1
element dispBeamColumn 31 31 32 5 1 1
element dispBeamColumn 32 32 33 5 1 1
element dispBeamColumn 33 33 34 5 1 1
element dispBeamColumn 34 34 35 5 1 1
element dispBeamColumn 35 35 36 5 1 1
element dispBeamColumn 36 36 37 5 1 1
element dispBeamColumn 37 37 38 5 1 1
element dispBeamColumn 38 38 39 5 1 1
element dispBeamColumn 39 39 40 5 1 1
element dispBeamColumn 40 40 41 5 1 1
element dispBeamColumn 41 41 42 5 1 1
element dispBeamColumn 42 42 43 5 1 1
element dispBeamColumn 43 43 44 5 1 1
element dispBeamColumn 44 44 45 5 1 1
element dispBeamColumn 45 45 46 5 1 1
element dispBeamColumn 46 46 47 5 1 1
element dispBeamColumn 47 47 48 5 1 1
element dispBeamColumn 48 48 49 5 1 1
element dispBeamColumn 49 49 50 5 1 1
element dispBeamColumn 50 50 51 5 1 1
element dispBeamColumn 51 51 52 5 1 1
element dispBeamColumn 52 52 53 5 1 1
element dispBeamColumn 53 53 54 5 1 1
element dispBeamColumn 54 54 55 5 1 1
element dispBeamColumn 55 55 56 5 1 1
element dispBeamColumn 56 56 57 5 1 1
element dispBeamColumn 57 57 58 5 1 1
element dispBeamColumn 58 58 59 5 1 1
element dispBeamColumn 59 59 60 5 1 1
element dispBeamColumn 60 60 61 5 1 1
element dispBeamColumn 61 61 62 5 1 1
element dispBeamColumn 62 62 63 5 1 1
element dispBeamColumn 63 63 64 5 1 1
element dispBeamColumn 64 64 65 5 1 1
element dispBeamColumn 65 65 66 5 1 1
element dispBeamColumn 66 66 67 5 1 1
element dispBeamColumn 67 67 68 5 1 1
element dispBeamColumn 68 68 69 5 1 1
element dispBeamColumn 69 69 70 5 1 1
element dispBeamColumn 70 70 71 5 1 1
element dispBeamColumn 71 71 72 5 1 1
element dispBeamColumn 72 72 73 5 1 1
element dispBeamColumn 73 73 74 5 1 1
element dispBeamColumn 74 74 75 5 1 1
element dispBeamColumn 75 75 76 5 1 1
element dispBeamColumn 76 76 77 5 1 1
element dispBeamColumn 77 77 78 5 1 1
element dispBeamColumn 78 78 79 5 1 1
element dispBeamColumn 79 79 80 5 1 1
element dispBeamColumn 80 80 81 5 1 1
element dispBeamColumn 81 81 82 5 1 1
element dispBeamColumn 82 82 83 5 1 1
element dispBeamColumn 83 83 84 5 1 1
element dispBeamColumn 84 84 85 5 1 1
element dispBeamColumn 85 85 86 5 1 1
element dispBeamColumn 86 86 87 5 1 1
element dispBeamColumn 87 87 88 5 1 1
element dispBeamColumn 88 88 89 5 1 1
element dispBeamColumn 89 89 90 5 1 1
element dispBeamColumn 90 90 91 5 1 1
element dispBeamColumn 91 91 92 5 1 1
element dispBeamColumn 92 92 93 5 1 1
element dispBeamColumn 93 93 94 5 1 1
element dispBeamColumn 94 94 95 5 1 1
element dispBeamColumn 95 95 96 5 1 1
element dispBeamColumn 96 96 97 5 1 1
element dispBeamColumn 97 97 98 5 1 1
element dispBeamColumn 98 98 99 5 1 1
element dispBeamColumn 99 99 100 5 1 1
element dispBeamColumn 100 100 101 5 1 1

timeSeries Linear 1

pattern Plain 1 1 {

load 101 0 -50000.0 0
}

system BandGeneral
numberer RCM
constraints Plain
test NormDispIncr 1.0e-3  100 3
integrator LoadControl 0.005
algorithm Newton
analysis Static


recorder Node -file generated/node-x.out -node 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 -dof 1 disp
recorder Node -file generated/node-y.out -node 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 -dof 2 disp
recorder Element -file generated/elem.out -ele1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 globalForce
recorder Element -file generated/stress-strain.out -ele 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100 101 section 1 fiber 0 0.5 stressStrain

analyze 200
