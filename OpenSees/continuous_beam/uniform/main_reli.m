clear all
close all
clc

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'PROBDATA'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
global NE
global LL
global colWidth
global colDepth
global cover

NE=62;  %Total elements 
LL=60000;% Length of the beam 
colWidth =1100;%Cross section width
colDepth =1250; %Cross section depth
cover=90;%Concrete cover

% Names of random variables. Default names are 'x1', 'x2', ..., if not explicitely defined.
probdata.name = { 'fc'
                  'fsy'
                  'fsu'
                  'esu'
                  'As1'
                  'As2'
                  'As3'
                  'R'
                  'Q'
                %  'P'
                %  'theta'
                  };
%  probdata.name = { 'Rr'
%                   'Q'
%                    };
%    probdata.name = { 'fy'
%                  
%                    };             
% Marginal distributions for each random variable
 %probdata.marg =  [ (type) (mean) (stdv) (startpoint) (p1) (p2) (p3) (p4) (input_type); ... ];								  
% probdata.marg =  [  15   9.25  1.57   9.25  nan  nan  nan  nan 0;
%                      15  150000 15000 300000 nan  nan  nan  nan 0];
%  probdata.marg =  [  2   440  28.6  440    nan  nan  nan  nan 0];               
probdata.marg =  [  2   51.2  3.584  51.2    nan  nan  nan  nan 0;
                    2   440  28.6  440  nan  nan  nan  nan 0;
                    2   550  38.5  550  nan  nan  nan  nan 0;
                    2   0.08  0.0072  0.08  nan  nan  nan  nan 0;
                    2   7859  157  7859  nan  nan  nan  nan  0;
                    2   5400  108  5400  nan  nan  nan  nan 0;
                    2   7364  147  7364  nan  nan  nan  nan 0;
                    15  9.24  1.20   9.24  nan  nan  nan  nan 0;
                    15  150000 15000  150000 nan  nan  nan  nan 0;
                  %  1   3      0.3    3     nan   nan   nan  nan 0;
                  %  2   1.04   0.05  1.04  nan   nan   nan  nan 0;
                    ];
% Correlation matrix
probdata.correlation = eye(length(probdata.name));

probdata.transf_type = 3;
probdata.Ro_method   = 1;
probdata.flag_sens   = 1;


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'ANALYSISOPT'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

analysisopt.echo_flag            = 1;
analysisopt.multi_proc           = 0;        % 1: block_size g-calls sent simultaneously
                                             %    - gfunbasic.m is used and a vectorized version of gfundata.expression is available.
                                             %      The number of g-calls sent simultaneously (block_size) depends on the memory
                                             %      available on the computer running FERUM.
                                             %    - gfunxxx.m user-specific g-function is used and able to handle block_size computations
                                             %      sent simultaneously, on a cluster of PCs or any other multiprocessor computer platform.
                                             % 0: g-calls sent sequentially
analysisopt.block_size           = 500000;   % Number of g-calls to be sent simultaneously

% FORM analysis options
analysisopt.i_max                = 500;      % Maximum number of iterations allowed in the search algorithm
analysisopt.e1                   = 0.05;     % Tolerance on how close design point is to limit-state surface
analysisopt.e2                   = 0.05;     % Tolerance on how accurately the gradient points towards the origin
analysisopt.step_code            = 0;        % 0: step size by Armijo rule, otherwise: given value is the step size
analysisopt.Recorded_u           = 1;        % 0: u-vector not recorded at all iterations, 1: u-vector recorded at all iterations
analysisopt.Recorded_x           = 1;        % 0: x-vector not recorded at all iterations, 1: x-vector recorded at all iterations

% FORM, SORM analysis options
analysisopt.grad_flag            = 'ffd';    % 'ddm': direct differentiation, 'ffd': forward finite difference
analysisopt.ffdpara              = 10;      % Parameter for computation of FFD estimates of gradients - Perturbation = stdv/analysisopt.ffdpara;
                                             % Recommended values: 1000 for basic limit-state functions, 50 for FE-based limit-state functions
analysisopt.ffdpara_thetag       = 100;      % Parameter for computation of FFD estimates of dbeta_dthetag
                                             % perturbation = thetag/analysisopt.ffdpara_thetag if thetag ~= 0 or 1/analysisopt.ffdpara_thetag if thetag == 0;
                                             % Recommended values: 1000 for basic limit-state functions, 100 for FE-based limit-state functions

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'GFUNDATA' (one structure per gfun)  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Type of limit-state function evaluator:
% 'basic': the limit-state function is defined by means of an analytical expression or a Matlab m-function,
%          using gfundata(lsf).expression. The function gfun.m calls gfunbasic.m, which evaluates gfundata(lsf).expression.
% 'xxx':   the limit-state function evaluation requires a call to an external code.  The function gfun.m calls gfunxxx.m,
%          which evaluates gfundata(lsf).expression where gext variable is a result of the external code.
gfundata(1).evaluator  = 'basic';
gfundata(1).type       = 'expression';   % Do no change this field!

% Expression of the limit-state function:
gfundata(1).expression = 'gfun_uni(fc, fsy, fsu, esu,As1,As2,As3, R,Q)';

% Give explicit gradient expressions w.r.t. involved random variables (order in probdata.marg),
% if DDM is used (analysisopt.grad_flag='ddm')
% gfundata(1).dgdq       = { '  1 '
%                            ' -1 ' };

% Flag for computation of sensitivities w.r.t. thetag parameters of the limit-state function
% 1: all sensitivities assessed, 0: no sensitivities assessment
gfundata(1).flag_sens  = 1;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'FEMODEL'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

femodel = [];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'RANDOMFIELD'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

randomfield = [];

%update before any analysis (must be run only once)
[probdata, gfundata, analysisopt]   = update_data(1, probdata, analysisopt, gfundata, []);

probdata.marg                       = distribution_parameter(probdata.marg);

formresults                         = form(1, probdata, analysisopt, gfundata, [], []);

%sormpfresults = sorm_pf(1,probdata,analysisopt,gfundata,[],[]);
%sormpfresults
formresults