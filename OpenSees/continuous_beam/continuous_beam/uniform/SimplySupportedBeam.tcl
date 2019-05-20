# units: meter, N
# Remove existing model
wipe
# Define model builder
# --------------------
model basic -ndm 2 -ndf 3
# Define materials for nonlinear columns
# ------------------------------------------
set fc 51.20;#concrete strength
set fsy 440.00;# Yield stress
set fsu 550.00;# ultimate stress
set esu 0.08000;# ultimate strain 
set E 200e3;    # Young's modulus
set eshi 0.00220;# yield strain
set Esi 1555.27;# harding Youngs modulus

# CONCRETE                              tag   f'c    ec0   f'cu        ecu

uniaxialMaterial Concrete01    1 -$fc   -0.0009   [expr -0.8*$fc]  -0.0035

# STEEL
#                               
uniaxialMaterial ElasticMultiLinear  3  -strain 0.0 $eshi $esu   0.5  -stress 0.0 $fsy  $fsu  $fsu 
#uniaxialMaterial MultiLinear 3 $eshi $fsy $esu $fsu 0.5 $fsu
# Define cross-section for nonlinear columns
# ------------------------------------------

# Define section
section Fiber 1 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 2 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 3 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 4 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 5 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 6 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 7 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 8 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 9 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 10 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 11 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 12 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 13 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 14 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 15 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 16 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 17 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 18 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 19 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 20 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 21 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 22 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 23 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 24 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 25 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 26 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 27 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 28 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 29 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 30 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 31 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 32 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 33 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 34 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 35 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 36 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 37 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 38 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 39 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 40 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 41 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 42 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 43 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 44 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 45 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 46 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 47 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 48 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 49 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 50 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 51 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 52 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 53 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 54 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 55 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 56 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 57 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 58 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 59 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
section Fiber 60 {
patch rect 1 10 1 [expr -625]  [expr -550]  625 550
layer straight 3 1 7856  [expr 535] 460 [expr 535] [expr -460]
layer straight 3 1 3928 [expr -535] 460 [expr -535] [expr -460]
}
# End of define section'
# Define node
node 1 0  0.0
node 2 1000  0.0
node 3 2000  0.0
node 4 3000  0.0
node 5 4000  0.0
node 6 5000  0.0
node 7 6000  0.0
node 8 7000  0.0
node 9 8000  0.0
node 10 9000  0.0
node 11 10000  0.0
node 12 11000  0.0
node 13 12000  0.0
node 14 13000  0.0
node 15 14000  0.0
node 16 15000  0.0
node 17 16000  0.0
node 18 17000  0.0
node 19 18000  0.0
node 20 19000  0.0
node 21 20000  0.0
node 22 21000  0.0
node 23 22000  0.0
node 24 23000  0.0
node 25 24000  0.0
node 26 25000  0.0
node 27 26000  0.0
node 28 27000  0.0
node 29 28000  0.0
node 30 29000  0.0
node 31 30000  0.0
node 32 31000  0.0
node 33 32000  0.0
node 34 33000  0.0
node 35 34000  0.0
node 36 35000  0.0
node 37 36000  0.0
node 38 37000  0.0
node 39 38000  0.0
node 40 39000  0.0
node 41 40000  0.0
node 42 41000  0.0
node 43 42000  0.0
node 44 43000  0.0
node 45 44000  0.0
node 46 45000  0.0
node 47 46000  0.0
node 48 47000  0.0
node 49 48000  0.0
node 50 49000  0.0
node 51 50000  0.0
node 52 51000  0.0
node 53 52000  0.0
node 54 53000  0.0
node 55 54000  0.0
node 56 55000  0.0
node 57 56000  0.0
node 58 57000  0.0
node 59 58000  0.0
node 60 59000  0.0
node 61 60000  0.0
# End of define node
# Fix degrees of freedom
fix  1  1  1  0
fix  21  0  1  0
fix  41  0  1  0
fix 61 0 1 0
# End of fix degrees of freedom
#define geotransformation
geomTransf Linear 1
# Define element
element  dispBeamColumn 1 1  2  5  1  1
element  dispBeamColumn 2 2  3  5  2  1
element  dispBeamColumn 3 3  4  5  3  1
element  dispBeamColumn 4 4  5  5  4  1
element  dispBeamColumn 5 5  6  5  5  1
element  dispBeamColumn 6 6  7  5  6  1
element  dispBeamColumn 7 7  8  5  7  1
element  dispBeamColumn 8 8  9  5  8  1
element  dispBeamColumn 9 9  10  5  9  1
element  dispBeamColumn 10 10  11  5  10  1
element  dispBeamColumn 11 11  12  5  11  1
element  dispBeamColumn 12 12  13  5  12  1
element  dispBeamColumn 13 13  14  5  13  1
element  dispBeamColumn 14 14  15  5  14  1
element  dispBeamColumn 15 15  16  5  15  1
element  dispBeamColumn 16 16  17  5  16  1
element  dispBeamColumn 17 17  18  5  17  1
element  dispBeamColumn 18 18  19  5  18  1
element  dispBeamColumn 19 19  20  5  19  1
element  dispBeamColumn 20 20  21  5  20  1
element  dispBeamColumn 21 21  22  5  21  1
element  dispBeamColumn 22 22  23  5  22  1
element  dispBeamColumn 23 23  24  5  23  1
element  dispBeamColumn 24 24  25  5  24  1
element  dispBeamColumn 25 25  26  5  25  1
element  dispBeamColumn 26 26  27  5  26  1
element  dispBeamColumn 27 27  28  5  27  1
element  dispBeamColumn 28 28  29  5  28  1
element  dispBeamColumn 29 29  30  5  29  1
element  dispBeamColumn 30 30  31  5  30  1
element  dispBeamColumn 31 31  32  5  31  1
element  dispBeamColumn 32 32  33  5  32  1
element  dispBeamColumn 33 33  34  5  33  1
element  dispBeamColumn 34 34  35  5  34  1
element  dispBeamColumn 35 35  36  5  35  1
element  dispBeamColumn 36 36  37  5  36  1
element  dispBeamColumn 37 37  38  5  37  1
element  dispBeamColumn 38 38  39  5  38  1
element  dispBeamColumn 39 39  40  5  39  1
element  dispBeamColumn 40 40  41  5  40  1
element  dispBeamColumn 41 41  42  5  41  1
element  dispBeamColumn 42 42  43  5  42  1
element  dispBeamColumn 43 43  44  5  43  1
element  dispBeamColumn 44 44  45  5  44  1
element  dispBeamColumn 45 45  46  5  45  1
element  dispBeamColumn 46 46  47  5  46  1
element  dispBeamColumn 47 47  48  5  47  1
element  dispBeamColumn 48 48  49  5  48  1
element  dispBeamColumn 49 49  50  5  49  1
element  dispBeamColumn 50 50  51  5  50  1
element  dispBeamColumn 51 51  52  5  51  1
element  dispBeamColumn 52 52  53  5  52  1
element  dispBeamColumn 53 53  54  5  53  1
element  dispBeamColumn 54 54  55  5  54  1
element  dispBeamColumn 55 55  56  5  55  1
element  dispBeamColumn 56 56  57  5  56  1
element  dispBeamColumn 57 57  58  5  57  1
element  dispBeamColumn 58 58  59  5  58  1
element  dispBeamColumn 59 59  60  5  59  1
element  dispBeamColumn 60 60  61  5  60  1
# End of define element

# Define dead load
pattern Plain 2 "Linear" {
load  1 0.0 -1.0 0.0
load  2 0.0 -1.0 0.0
load  3 0.0 -1.0 0.0
load  4 0.0 -1.0 0.0
load  5 0.0 -1.0 0.0
load  6 0.0 -1.0 0.0
load  7 0.0 -1.0 0.0
load  8 0.0 -1.0 0.0
load  9 0.0 -1.0 0.0
load  10 0.0 -1.0 0.0
load  11 0.0 -1.0 0.0
load  12 0.0 -1.0 0.0
load  13 0.0 -1.0 0.0
load  14 0.0 -1.0 0.0
load  15 0.0 -1.0 0.0
load  16 0.0 -1.0 0.0
load  17 0.0 -1.0 0.0
load  18 0.0 -1.0 0.0
load  19 0.0 -1.0 0.0
load  20 0.0 -1.0 0.0
load  21 0.0 -1.0 0.0
load  22 0.0 -1.0 0.0
load  23 0.0 -1.0 0.0
load  24 0.0 -1.0 0.0
load  25 0.0 -1.0 0.0
load  26 0.0 -1.0 0.0
load  27 0.0 -1.0 0.0
load  28 0.0 -1.0 0.0
load  29 0.0 -1.0 0.0
load  30 0.0 -1.0 0.0
load  31 0.0 -1.0 0.0
load  32 0.0 -1.0 0.0
load  33 0.0 -1.0 0.0
load  34 0.0 -1.0 0.0
load  35 0.0 -1.0 0.0
load  36 0.0 -1.0 0.0
load  37 0.0 -1.0 0.0
load  38 0.0 -1.0 0.0
load  39 0.0 -1.0 0.0
load  40 0.0 -1.0 0.0
load  41 0.0 -1.0 0.0
load  42 0.0 -1.0 0.0
load  43 0.0 -1.0 0.0
load  44 0.0 -1.0 0.0
load  45 0.0 -1.0 0.0
load  46 0.0 -1.0 0.0
load  47 0.0 -1.0 0.0
load  48 0.0 -1.0 0.0
load  49 0.0 -1.0 0.0
load  50 0.0 -1.0 0.0
load  51 0.0 -1.0 0.0
load  52 0.0 -1.0 0.0
load  53 0.0 -1.0 0.0
load  54 0.0 -1.0 0.0
load  55 0.0 -1.0 0.0
load  56 0.0 -1.0 0.0
load  57 0.0 -1.0 0.0
load  58 0.0 -1.0 0.0
load  59 0.0 -1.0 0.0
load  60 0.0 -1.0 0.0
}
#End of define dead load

integrator LoadControl 3000

system   ProfileSPD;	
	
test  NormDispIncr 1.0e-3 20  3
	
numberer RCM
	
constraints Plain
	
algorithm Newton
	
analysis Static
# Do the analysis
	
analyze 10

loadConst -time 0.0

# Compute increment	

set numIncr 1000;	# Number of analysis increments
# Call the section analysis procedure
set Y  [expr 1000.0];
set dY [expr $Y/$numIncr]

# Define reference force	
pattern Plain 1  "Linear" {
load  30 0.0 -1.0 0.0
load  31 0.0 -1.0 0.0
load  32 0.0 -1.0 0.0
}
recorder Node -file section.out -time -node 31 -dof 2 disp
recorder Element -file element.out -time -ele 30 section 5 fiber -535 0  3  stress
# End of define reference force
# Use displacement control at node 2 for analysis
integrator DisplacementControl  31  2 -$dY
# End of define displacement
#integrator LoadControl 0.1

# Define analysis parameters
	
system   ProfileSPD;	
	
test NormUnbalance 1.0e-3 30  5
	
numberer RCM
	
constraints Plain
	
algorithm Newton
	
analysis Static
	
# Do the analysis
#analyze $numIncr
 set a 0
 while { $a <= $esu } {
 	analyze 1
 	set a [eleResponse 30 section 5 fiber -535 0 3 strain]
	
}







