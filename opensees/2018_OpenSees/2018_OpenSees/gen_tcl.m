% Generate OpenSees input file (*.tcl)

function gen_tcl(Q, L_span, l_elem, concrete_model, rebar_model)

% -------------------------------------------------------------------------
% PRE-PROCESSING
% -------------------------------------------------------------------------

% RC T section
numSubdivY  = 1;
numSubdivZ  = 30;

% concrete - material
E_c         = 35.9*1e9;
% fpc         = -51.2*1e6;
fpc         = -28.8*1e6;
epsc0       = 2*fpc/E_c;
fpcu        = fpc;
epsU        = -0.0035;
lambda      = 0.2; % does not matter
ft          = -fpc/10;%3.69*1e6; % WARNING!
Ets         = 1*E_c;

% concrete - section
b_top       = 2150*1e-3;
h_top       = 200*1e-3;
b_bot       = 500*1e-3;
h_bot       = 1250*1e-3 - h_top;
cover       = (30 + 10)*1e-3;

% rebar - material
Es          = 200*1e9;
% fy          = 440*1e6;
fy          = 348*1e6;
fu          = 1.15*fy;%500*1e6;
esh         = 1.5*fy/Es;
eult        = 0.08;
Esh         = (fu - fy)/(eult - esh);

% rebar - section/layout
ns          = [16, 5, 6];
As          = [25, 25, 25].^2*pi/4*1e-6;
ds          = [cover, (h_top+h_bot)-cover, (h_top+h_bot)-(cover+50*1e-3)];

for ii = 1:3
   if mod(L_span(1), l_elem) ~= 0
      error('Please provide an element length that is a divider of each span length') ;
   end
end

cL          = [0, cumsum(L_span)];
L           = sum(L_span);
n_node      = L/l_elem + 1;

% =========================================================================
% WRITE THE TCL FILE
% =========================================================================

fileID      = fopen('model.tcl', 'w');

line        = 'wipe';
fprintf(fileID,line); fprintf(fileID,'\n\n');

line        = 'model basic -ndm 2 -ndf 3';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% NODES
% -------------------------------------------------------------------------

nn  = 1:n_node;
nx  = linspace(0, L, n_node);
N   = [nn(:), nx(:), zeros(n_node,1)];
for ii = 1:n_node
    fprintf(fileID, 'node %i %.7e %.7e', [nn(ii), nx(ii), 0]); fprintf(fileID,'\n');
end
fprintf(fileID,'\n');


% -------------------------------------------------------------------------
% BC
% -------------------------------------------------------------------------

ni = N((N(:,2) == cL(1)),1); 
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n');
ni = N((N(:,2) == cL(2)),1); 
fprintf(fileID, 'fix %i  1 1 0', ni); fprintf(fileID,'\n');
ni = N((N(:,2) == cL(3)),1); 
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n');
ni = N((N(:,2) == cL(4)),1); 
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n');

fprintf(fileID,'\n');

line = 'geomTransf Linear 1';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% MAT
% -------------------------------------------------------------------------
% concrete
switch lower(concrete_model)
    case 'concrete02'
        fprintf(fileID,'uniaxialMaterial Concrete02 1 %.7e %.7e %.7e %.7e %.7e %.7e %.7e',...
            [fpc, epsc0, fpcu, epsU, lambda, ft, Ets]);
    case 'concrete01'
        fprintf(fileID,'uniaxialMaterial Concrete01 1 %.7e %.7e %.7e %.7e',...
            [fpc, epsc0, fpcu, epsU]);
    otherwise
        error(['Unknown conrete_model: ', concrete_model])
end
fprintf(fileID,'\n');

% rebar
switch lower(rebar_model)
    case 'reinforcingsteel'
        fprintf(fileID,'uniaxialMaterial ReinforcingSteel 21 %.7e %.7e %.7e %.7e %.7e %.7e',...
            [fy, fu, Es, Esh, esh, eult]);
    case 'steel01'
        fprintf(fileID, 'uniaxialMaterial Steel01    21  %.7e %.7e %.7e', [fy, Es, 0]);
    otherwise
        error(['Unknown conrete_model: ', rebar_model])
end
fprintf(fileID,'\n\n');


% -------------------------------------------------------------------------
% SECTION
% -------------------------------------------------------------------------

% RC T section
line        = 'section Fiber 1 {';
% concrete pathes
fprintf(fileID,line); fprintf(fileID,'\n');
fprintf(fileID,'    patch rect 1 %i %i %.7e %.7e %.7e %.7e',...
    [numSubdivY, numSubdivZ, -h_top, -b_top/2, 0, b_top/2]); fprintf(fileID,'\n');
fprintf(fileID,'    patch rect 1 %i %i %.7e %.7e %.7e %.7e',...
    [numSubdivY, numSubdivZ, -(h_top+h_bot), -b_bot/2, -h_top, b_bot/2]); fprintf(fileID,'\n');
% rebar layers
% top layer
fprintf(fileID,'    layer straight 21 %i %.7e %.7e %.7e %.7e %.7e',...
        [ns(1), As(1), -ds(1), -b_top/2+cover, -ds(1), b_bot/2-cover]); fprintf(fileID,'\n');
% bottom layers
for ii = 2:length(ns)
    fprintf(fileID,'    layer straight 21 %i %.7e %.7e %.7e %.7e %.7e',...
        [ns(ii), As(ii), -ds(ii), -b_bot/2+cover, -ds(ii), b_bot/2-cover]); fprintf(fileID,'\n');
end
line        = '}';
fprintf(fileID,line); fprintf(fileID,'\n\n');

  
% -------------------------------------------------------------------------
% ELEMENT
% -------------------------------------------------------------------------
% RC section
numIntgrPts = 5;
for ii = 1:n_node-1
    fprintf(fileID, 'element dispBeamColumn %i %i %i %i %i %i',...
        [ii, ii, ii+1, numIntgrPts, 1, 1]);
    fprintf(fileID,'\n');
end
fprintf(fileID,'\n');

% -------------------------------------------------------------------------
% LOADING
% -------------------------------------------------------------------------
line = 'timeSeries Linear 1';
fprintf(fileID,line); fprintf(fileID,'\n\n');

line = 'pattern Plain 1 1 {';
fprintf(fileID,line); fprintf(fileID,'\n'); 
ni = N(abs(N(:,2) - L/2) < 0.001, 1); 
fprintf(fileID,'load %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
ni = N(abs(N(:,2) - L/2 - 1) < 0.001, 1);
fprintf(fileID,'load %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
ni = N(abs(N(:,2) - L/2 + 1) < 0.001, 1);
fprintf(fileID,'load %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
line = '}';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% SOLVER OPTIONS
% -------------------------------------------------------------------------
line = 'system BandGeneral';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'numberer RCM';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'constraints Plain';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'test NormDispIncr 1.0e-3  100 3';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'integrator LoadControl 0.005';
% line = 'integrator ArcLength 1 0.005';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'algorithm Newton';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'analysis Static';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% RECORDER
% -------------------------------------------------------------------------
line = 'recorder Node -file rc_section_displX.out -time -node ';
fprintf(fileID,line); 
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'-dof 1 disp\n');

line = 'recorder Node -file rc_section_displY.out -time -node ';
fprintf(fileID,line); 
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'-dof 2 disp\n');

line = 'recorder Element -file rc_section_eleGlobalForce.out -time -ele ';
fprintf(fileID,line); 
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'globalForce\n');


% -------------------------------------------------------------------------
% SOLVE
% -------------------------------------------------------------------------
line = 'analyze 200';
fprintf(fileID,line); 

fclose(fileID);

end

