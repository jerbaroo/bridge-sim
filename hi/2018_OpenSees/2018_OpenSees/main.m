% Mang, C., Jason, L., & Davenne, L. (2015). A new bond slip model for reinforced concrete structures: Validation by modelling a reinforced concrete tie. Engineering Computations, 32(7), 1934-1958. doi: 10.1108/EC-11-2014-0234

clearvars
close all
clc

% [N], [m]

% -------------------------------------------------------------------------
% INPUT & OPTIONS
% -------------------------------------------------------------------------

L_span      = [18.6, 22.8, 18.6];
Q           = 500*1e3;
l_elem      = 0.2;

concrete_model      = 'concrete01';
% concrete_model      = 'concrete02';

rebar_model         = 'steel01';
% rebar_model         = 'reinforcingsteel';

% .........................................................................
% Numerical model specific (OpenSees)
% .........................................................................

% -------------------------------------------------------------------------
% ANALYSIS
% -------------------------------------------------------------------------

numerical_solu(Q, L_span, l_elem, concrete_model, rebar_model) 