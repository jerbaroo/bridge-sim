clearvars
close all
clc


Input   = get_input;

% currently only input check
Input   = update_Input(Input);

FEM     = preprocess(Input);

TCL     = gen_tcl2(Input, FEM);