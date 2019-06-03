% Generate OpenSees input file (*.tcl)

function TCL = gen_tcl2(Input, FEM)

% -------------------------------------------------------------------------
% INITIALIZING & PRE-PROCESSING
% -------------------------------------------------------------------------
Geom            = Input.Geom;
Concrete_gen    = Input.Concrete_gen;
Rebar_gen       = Input.Rebar_gen;
Load            = Input.Load;

Concrete        = FEM.Concrete;
Rebar           = FEM.Rebar;

Input           = get_input;
L_span          = Input.Geom.L_span;
l_elem          = Geom.l_elem;

cL              = [0, cumsum(L_span)];
L               = sum(L_span);
n_node          = L/l_elem + 1;
n_elem          = n_node - 1;

% Populate the workspace
concrete_model  = Concrete_gen.concrete_model;
Ec              = Concrete_gen.Ec;
fpc             = Concrete_gen.fpc;
epsc0           = Concrete_gen.epsc0;
fpcu            = Concrete_gen.fpcu;
epsU            = Concrete_gen.epsU;
lambda          = Concrete_gen.lambda; % does not matter
ft              = Concrete_gen.ft;
Ets             = Concrete_gen.Ets;

rebar_model     = Rebar_gen.rebar_model;
Es              = Rebar_gen.Es;
fy              = Rebar_gen.fy;
fu              = Rebar_gen.fu;
esh             = Rebar_gen.esh;
eult            = Rebar_gen.eult;
Esh             = Rebar_gen.Esh;

Q               = Load.Q;

% =========================================================================
% WRITE THE TCL FILE
% =========================================================================

fname           = 'cont_beam.tcl';
fileID          = fopen(fname, 'w');

line            = 'wipe';
fprintf(fileID, line);
fprintf(fileID, '\n\n');

line            = 'model basic -ndm 2 -ndf 3';
fprintf(fileID, line);
fprintf(fileID, '\n\n');
% -------------------------------------------------------------------------
% NODES
% -------------------------------------------------------------------------

nn              = 1:n_node;
nx              = linspace(0, L, n_node);
N               = [nn(:), nx(:), zeros(n_node,1)];
for ii = 1:n_node
    fprintf(fileID, 'node %i %.7e %.7e\n', [nn(ii), nx(ii), 0]);
end
fprintf(fileID,'\n');


% -------------------------------------------------------------------------
% BC
% -------------------------------------------------------------------------

ni              = N((N(:,2) == cL(1)),1);
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n');

ni              = N((N(:,2) == cL(2)),1);
fprintf(fileID, 'fix %i  1 1 0', ni); fprintf(fileID,'\n');

ni              = N((N(:,2) == cL(3)),1);
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n');

ni              = N((N(:,2) == cL(4)),1);
fprintf(fileID, 'fix %i  0 1 0', ni); fprintf(fileID,'\n\n');


% more is needed
line            = 'geomTransf Linear 1';
fprintf(fileID, line);
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% MAT
% -------------------------------------------------------------------------
% concrete
c_matTag = 1;
switch lower(concrete_model)
    case 'concrete02'
        fprintf(fileID, 'uniaxialMaterial Concrete02 %i %.7e %.7e %.7e %.7e %.7e %.7e %.7e',...
            [c_matTag, fpc, epsc0, fpcu, epsU, lambda, ft, Ets]);
    case 'concrete01'
        fprintf(fileID, 'uniaxialMaterial Concrete01 %i %.7e %.7e %.7e %.7e',...
            [c_matTag, fpc, epsc0, fpcu, epsU]);
    otherwise
        error(['Unknown conrete_model: ', concrete_model])
end
fprintf(fileID,'\n');

% rebar
s_matTag = 21;
switch lower(rebar_model)
    case 'reinforcingsteel'
        fprintf(fileID, 'uniaxialMaterial ReinforcingSteel %i %.7e %.7e %.7e %.7e %.7e %.7e',...
            [s_matTag, fy, fu, Es, Esh, esh, eult]);
    case 'steel01'
        fprintf(fileID, 'uniaxialMaterial Steel01    %i  %.7e %.7e %.7e', [s_matTag, fy, Es, 0]);
    otherwise
        error(['Unknown conrete_model: ', rebar_model])
end
fprintf(fileID,'\n');

% -------------------------------------------------------------------------
% SECTION
% -------------------------------------------------------------------------

% RC T fiber section
for ii = 1:n_elem
    ID              = ii;
    S               = tcl_T_rc_section(Concrete(ii), Rebar(ii), ID, c_matTag, s_matTag);
    fprintf(fileID, '%c', S);
end
fprintf(fileID,'\n\n');


% -------------------------------------------------------------------------
% ELEMENT
% -------------------------------------------------------------------------
% RC section
numIntgrPts     = 5;
for ii = 1:n_node-1
    fprintf(fileID, 'element dispBeamColumn %i %i %i %i %i %i',...
        [ii, ii, ii+1, numIntgrPts, 1, 1]);
    fprintf(fileID,'\n');
end
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% LOADING
% -------------------------------------------------------------------------
line            = 'timeSeries Linear 1';
fprintf(fileID,line); fprintf(fileID,'\n\n');

line            = 'pattern Plain 1 1 {';
fprintf(fileID,line); fprintf(fileID,'\n');
ni              = N(abs(N(:,2) - L/2) < 0.001, 1);
fprintf(fileID,'\tload %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
ni              = N(abs(N(:,2) - L/2 - 1) < 0.001, 1);
fprintf(fileID,'\tload %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
ni              = N(abs(N(:,2) - L/2 + 1) < 0.001, 1);
fprintf(fileID,'\tload %i 0 %.7e 0', [ni, -Q]); fprintf(fileID,'\n');
line            = '}';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% SOLVER OPTIONS
% -------------------------------------------------------------------------
line            = 'system BandGeneral';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'numberer RCM';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'constraints Plain';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'test NormDispIncr 1.0e-3  100 3';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'integrator LoadControl 0.005';
% line = 'integrator ArcLength 1 0.005';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'algorithm Newton';
fprintf(fileID,line); fprintf(fileID,'\n');
line            = 'analysis Static';
fprintf(fileID,line); fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% RECORDER
% -------------------------------------------------------------------------
line            = 'recorder Node -file rc_section_displX.out -time -node ';
fprintf(fileID,line);
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'-dof 1 disp\n');

line            = 'recorder Node -file rc_section_displY.out -time -node ';
fprintf(fileID,line);
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'-dof 2 disp\n');

line            = 'recorder Element -file rc_section_eleGlobalForce.out -time -ele ';
fprintf(fileID,line);
fprintf(fileID,'%i ', 1:n_node);
fprintf(fileID,'globalForce\n');


% -------------------------------------------------------------------------
% SOLVE
% -------------------------------------------------------------------------
line            = 'analyze 200';

fprintf(fileID,line);
fclose(fileID);

% it is faster to do with fprintf than with sprintf
fileID          = fopen(fname, 'r');
TCL             = fscanf(fileID, 'c');
fclose(fileID);

end

