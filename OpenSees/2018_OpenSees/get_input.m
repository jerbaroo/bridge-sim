% [mm] [N]
%
% Jacinto. (2011). Avaliação da Segurança de Pontes Existentes - Abordagem 
% Probabilí-stica Bayesiana. (PhD), Tecnologia da Universidade Nova de 
% Lisboa, Lisboa.
%  
% Jacinto, L., Neves, L.A.C., Santos, L. (2015). Bayesian assessment of an existing 
% bridge: a case study. Structure and Infrastructure Engineering, 12(1), 1-17.

function Input = get_input

% -------------------------------------------------------------------------
% GEOMETRY
% -------------------------------------------------------------------------

L1                      = 18.6*1e3;
L2                      = 22.8*1e3;
L3                      = L1;

Geom.L_span             = [L1, L2, L3];
Geom.l_elem             = 200;

% depth of the cross-section
h                       = 1250;

% web width
w_sup                   = 1100;
w_span                  = 500;

web_xh                  = [-(L1+L2/2), -(L1+L2/2)+L1/3, -(L2/2)-L1/3, -L2/2, -(L2/2)+L2/3];
Geom.web_x              = [web_xh, fliplr(-web_xh)];
web_wh                  = [w_sup, w_span, w_span, w_sup, w_span];
Geom.web_w              = [web_wh, fliplr(web_wh)];

% .........................................................................
% Rebar layout
% .........................................................................
% top rebar - entire length
cover                   = 30;
Rebar_layout(1).L       = [-(L1+L2/2), (L1+L2/2)];          
Rebar_layout(1).n_s     = [8, 8];
Rebar_layout(1).D_s     = [25, 25];
Rebar_layout(1).d_s     = [cover+25/2, cover+1.5*25+12];

% bottom rebar - left span
Rebar_layout(2).L       = [-(L1+L2/2), -L2/2];          
Rebar_layout(2).n_s     = [5, 5, 5];
Rebar_layout(2).D_s     = [25, 25, 25];
Rebar_layout(2).d_s     = [h-50, h-110, h-160];

% bottom rebar - right span span
Rebar_layout(3)         = Rebar_layout(2); 
Rebar_layout(3).L       = [L2/2, (L1+L2/2)];

% bottom rebar - mid span
Rebar_layout(4).L       = [-L2/2, L2/2];          
Rebar_layout(4).n_s     = [6, 5];
Rebar_layout(4).D_s     = [25, 25];
Rebar_layout(4).d_s     = [h-50, h-110];


% -------------------------------------------------------------------------
% RC T section - general
% -------------------------------------------------------------------------

Concrete_gen.numSubdivY = 1;
Concrete_gen.numSubdivZ = 30;

% concrete - material
concrete_model          = 'concrete01';
Concrete_gen.concrete_model = concrete_model;

Ec                      = 35.9*1e12;
fpc                     = -28.8;
Concrete_gen.Ec         = Ec;
Concrete_gen.fpc        = fpc;
Concrete_gen.epsc0      = 2*fpc/Ec;
Concrete_gen.fpcu       = fpc;
Concrete_gen.epsU       = -0.0035;
Concrete_gen.lambda     = 0.2; % does not matter
Concrete_gen.ft         = -fpc/10;%3.69*1e6; % WARNING!
Concrete_gen.Ets        = 1*Ec;

% concrete - section
Concrete_gen.b          = 1100;
Concrete_gen.h          = h;
Concrete_gen.t1         = 200;
Concrete_gen.t2         = 500; % dummy, will change according to Geom.web
Concrete_gen.cover      = (30 + 10);


% rebar - material
rebar_model          = 'steel01';
Rebar_gen.rebar_model = rebar_model;

Es                      = 200*1e12;
fy                      = 348;
esh                     = 1.5*fy/Es;
eult                    = 0.08;
fu                      = 1.15*fy;

Rebar_gen.Es            = Es;
Rebar_gen.fy            = fy;
Rebar_gen.fu            = fu;
Rebar_gen.esh           = esh;
Rebar_gen.eult          = eult;
Rebar_gen.Esh           = (fu - fy)/(eult - esh);

% -------------------------------------------------------------------------
% Loading
% -----------------------------------------------------------------------

Load.Q                  = 150*1e3; % will be scaled until failure

% -------------------------------------------------------------------------
% Collect results
% -------------------------------------------------------------------------

Input.Geom              = Geom;
Input.Geom.Rebar_layout = Rebar_layout;
Input.Concrete_gen      = Concrete_gen;
Input.Rebar_gen         = Rebar_gen;
Input.Load              = Load;

end