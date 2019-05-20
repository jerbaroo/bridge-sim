clear all
close all
clc

uqlab;
global NE

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%  DATA FIELDS IN 'PROBDATA'  %%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% get model inputs from MP_Discre
NE=60;  %Total elements 
Rr=9.25; % Mean Cross-sectional area of reinforcement
Rr_std=1.57; % Standard deviation 


% Names of random variables. Default names are 'x1', 'x2', ..., if not explicitely defined.
 s=cell(NE+1:1);
 s(1,1)={'Rr1'};
 s_gfun='X(:,1)';
 for j=2:NE
     s(j,1)={['Rr',num2str(j)]};
     s_gfun=[s_gfun,',X(:,',num2str(j),')'];
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
%     if j==NE/2
%     marg(j,4)=11;
%     else
%     marg(j,4)=9;
%     end
    marg(j,4)=Rr;
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



% To QLab data input (FERUM -> UQLab function shold be written)
rv_name         = probdata.name;
marg            = probdata.marg;
n_rv            = length(rv_name);

%..........................................................................
% Marginal distributions for each random variable
%..........................................................................

for ii = 1:n_rv
    marg_ii = marg(ii,:);
    X              = rv_name{ii};
    switch marg_ii(1)
        case 1 
            dist = 'Gaussian';
        case 2
            dist = 'Lognormal';
        case 15
            dist = 'Gumbel';
        otherwise
            error('Unknown distribution type.')
    end
    IOpts.Marginals(ii).Name = rv_name{ii}; 
    IOpts.Marginals(ii).Type = dist;
    IOpts.Marginals(ii).Moments = [marg_ii(2), marg_ii(3)];
end

%..........................................................................
% Correlation matrix
%..........................................................................

IOpts.Copula.Type = 'Gaussian';
IOpts.Copula.Parameters = probdata.correlation;
% Create and store the input object in UQLab
myInput = uq_createInput(IOpts);

% COMPUTATIONAL MODEL
% Create a limit state function model based on a string (vectorized)
% MOpts.mString = ['gfun_rf(RrL,[',s_gfun,'],RrR,Q,fsy, fsu, esu)'];
MOpts.mString =[ 'gfun_rf([',s_gfun,'],X(:,61),X(:,62),X(:,63),X(:,64))'];
MOpts.isVectorized = 0; 
myModel = uq_createModel(MOpts);

SSimOptions.Type        = 'Reliability';
SSimOptions.Method      = 'Subset';
SSimOptions.Simulation.TargetCoV = 0.1; % based on the manual it has no effect on SS 
SSimOptions.Subset.p0 = 0.1;
SSimOptions.Simulation.MaxSampleSize = 1e4;
SSimOptions.Simulation.BatchSize = 1000;

% Run the subset simulation
t_simu = tic;
SSimAnalysis = uq_createAnalysis(SSimOptions);
t_total_sec = toc(t_simu);

%  Print out a report of the results
uq_print(SSimAnalysis);

%  Create a graphical representation of the results
uq_display(SSimAnalysis);

save(['SS_UQLab', sprintf('%i-%i-%i_%i-%i-%.f', clock), '.mat'], 'SSimAnalysis', 'myInput', 'SSimOptions', 'myModel', 'IOpts', 'MOpts')


