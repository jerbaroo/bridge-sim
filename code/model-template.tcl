wipe

model basic -ndm 2 -ndf 3

<<NODES>>

<<FIX>>

geomTransf Linear 1

uniaxialMaterial Concrete02 1 -2.8800000e+07 -1.6044568e-03 -2.8800000e+07 -3.5000000e-03 2.0000000e-01 2.8800000e+06 3.5900000e+10
uniaxialMaterial Steel01    2 3.4800000e+08  2.0000000e+11  0.0000000e+00

<<SECTIONS>>

<<ELEMENTS>>

timeSeries Linear 1

pattern Plain 1 1 {
<<LOAD>>
}

system BandGeneral
numberer RCM
constraints Plain
integrator LoadControl 1
algorithm Linear
analysis Static

<<RECORDERS>>

analyze 1
