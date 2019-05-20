clear all
close all
clc
global NE



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'PROBDATA'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% get model inputs from MP_Discre
NE=64;  %Total elements 
Rr=9.25; % Mean of pitting factor
Rr_std=1.57; % Standard deviation of pitting factor


% Names of random variables. Default names are 'x1', 'x2', ..., if not explicitely defined.
 s=cell(NE+1:1);
 s(1,1)={'Rr1'};
 s_gfun='Rr1';
 for j=2:NE
     s(j,1)={['Rr',num2str(j)]};
     s_gfun=[s_gfun,',Rr',num2str(j)];
 end
s(NE+1,1)={'Q'};
s(NE+2,1)={'fsy'};
s(NE+3,1)={'fsu'};
s(NE+4,1)={'esu'};

 probdata.name = s;


% Marginal distributions for each random variable
% probdata.marg =  [ (type) (mean) (stdv) (startpoint) (p1) (p2) (p3) (p4) (input_type); ... ];		
marg=zeros(NE+1,9);
for j=1:NE
    marg(j,1)=15;
    marg(j,2)=Rr;
    marg(j,3)=Rr_std;
     if j==NE/2
     marg(j,4)=11;
     else
     marg(j,4)=Rr;
     end
    marg(j,5)=nan;
    marg(j,6)=nan;
    marg(j,7)=nan;
    marg(j,8)=nan;
    marg(j,9)=0;
end
j=NE+1;
    marg(j,1)=15;
    marg(j,2)=150000;
    marg(j,3)=15000;
    marg(j,4)=160000;
    marg(j,5)=nan;
    marg(j,6)=nan;
    marg(j,7)=nan;
    marg(j,8)=nan;
    marg(j,9)=0;
j=NE+2;
    marg(j,1)=2;
    marg(j,2)=440;
    marg(j,3)=28.6;
    marg(j,4)=440;
    marg(j,5)=nan;
    marg(j,6)=nan;
    marg(j,7)=nan;
    marg(j,8)=nan;
    marg(j,9)=0;
j=NE+3;
    marg(j,1)=2;
    marg(j,2)=550;
    marg(j,3)=38.5;
    marg(j,4)=530;
    marg(j,5)=nan;
    marg(j,6)=nan;
    marg(j,7)=nan;
    marg(j,8)=nan;
    marg(j,9)=0;
j=NE+4;
    marg(j,1)=2;
    marg(j,2)=0.08;
    marg(j,3)=0.0072;
    marg(j,4)=0.08;
    marg(j,5)=nan;
    marg(j,6)=nan;
    marg(j,7)=nan;
    marg(j,8)=nan;
    marg(j,9)=0;

probdata.marg =  marg;

% Correlation matrix
probdata.correlation = eye(length(probdata.name));
probdata.correlation(NE/2,NE/2+1)=0.9;
probdata.correlation(NE/2+1,NE/2)=0.9;
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
analysisopt.ffdpara              = -10;      % Parameter for computation of FFD estimates of gradients - Perturbation = stdv/analysisopt.ffdpara;
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

gfundata(1).expression = ['gfun_rf([',s_gfun,'],Q,fsy, fsu, esu)'];
%gfundata(1).expression = 'gfun_rf(a,b,c,d,e,f,g,h,i,j)';
% Give explicit gradient expressions w.r.t. involved random variables (order in probdata.marg),
% if DDM is used (analysisopt.grad_flag='ddm')
% gfundata(1).dgdq       = { '  1 '
%                            ' -1 ' };

% Flag for computation of sensitivities w.r.t. thetag parameters of the limit-state function
% 1: all sensitivities assessed, 0: no sensitivities assessment
gfundata(1).flag_sens  = 0;
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'FEMODEL'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

femodel = [];


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'RANDOMFIELD'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

randomfield = [];

% update before any analysis (must be run only once)
[probdata, gfundata, analysisopt]   = update_data(1, probdata, analysisopt, gfundata, []);

probdata.marg                       = distribution_parameter(probdata.marg);

tic

% ALLformresults                        = form_multiple_dspts(1, probdata, analysisopt, gfundata, [], []);
formresults                        = form(1, probdata, analysisopt, gfundata, [], []);
toc
formresults 
% ALLformresults

