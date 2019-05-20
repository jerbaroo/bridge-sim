%
% [mm], [N]

clearvars
close all
clc

L1      = 18.6*1e3;
L2      = 22.8*1e3;
L3      = L1;

% total depth of teh cross-section
h       = 1250;
% width of the flange
b       = 1100;
% flange thickness
tf      = 200;

% web width
w_sup   = 1100;
w_span  = 500;

% Material
E_c     = 35.9*1e4;
E_s     = 200*1e4;

% -------------------------------------------------------------------------
% WEB width changes
% -------------------------------------------------------------------------
% cross-sections where the web width changes
web_xh  = [-(L1+L2/2), -(L1+L2/2)+L1/3, -(L2/2)-L1/3, -L2/2, -(L2/2)+L2/3];
web_x   = [web_xh, fliplr(-web_xh)];
web_wh  = [w_sup, w_span, w_span, w_sup, w_span];
web_w   = [web_wh, fliplr(web_wh)];

web_fun = @(x) interp1(web_x, web_w, x);

% -------------------------------------------------------------------------
% MESH
% -------------------------------------------------------------------------


Concrete.h      = h;
Concrete.b      = b;
Concrete.t1     = tf;
Concrete.t2     = web_fun(-L1);
Concrete.E      = E_c;

Rebar.D_s       = [25,  25, 25,     25];
Rebar.n_s       = [8,   8,  5,      6];
Rebar.d_s       = [50,  67, 1100,   1170];

Rebar.E         = E_s;

[y_i, A_i, S_i] = T_section(Concrete, Rebar);

ID              = 1;
c_matTag        = 1;
s_matTag        = 10;
S = tcl_T_rc_section(Concrete, Rebar, ID, c_matTag, s_matTag)
