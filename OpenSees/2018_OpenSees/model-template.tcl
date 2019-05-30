wipe

model basic -ndm 2 -ndf 3

<<NODES>>

<<FIX>>

geomTransf Linear 1

uniaxialMaterial Concrete02 1 -2.8800000e+07 -1.6044568e-03 -2.8800000e+07 -3.5000000e-03 2.0000000e-01 2.8800000e+06 3.5900000e+10
uniaxialMaterial Steel01    2 3.4800000e+08  2.0000000e+11  0.0000000e+00

section Fiber 1 {
    <<PATCHES>>
    patch rect 1 1 30 -2.0000000e-01 -1.0750000e+00 0.0000000e+00 1.0750000e+00
    patch rect 1 1 30 -1.2500000e+00 -2.5000000e-01 -2.0000000e-01 2.5000000e-01
    layer straight 2 16 4.9087385e-04 -4.0000000e-02 -1.0350000e+00 -4.0000000e-02 2.1000000e-01
    layer straight 2 5 4.9087385e-04 -1.2100000e+00 -2.1000000e-01 -1.2100000e+00 2.1000000e-01
    layer straight 2 6 4.9087385e-04 -1.1600000e+00 -2.1000000e-01 -1.1600000e+00 2.1000000e-01
}

<<ELEMENTS>>

timeSeries Linear 1

pattern Plain 1 1 {
<<LOAD>>
}

system BandGeneral
numberer RCM
constraints Plain
test NormDispIncr 1.0e-3  100 3
integrator LoadControl 0.005
algorithm Newton
analysis Static

<<RECORDERS>>

analyze 200
