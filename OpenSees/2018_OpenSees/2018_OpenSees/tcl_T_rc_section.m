% Generate tcl code snippet coding a reinforced concrete T-section (fiber)
%
%     b
% o--------o
%
% |--------| o   o      o--> Z
% |        | |t1 |      |
% |--|  |--| o   |      |Y
%    |  |        | h
%    |  |        |
%    ----        o
%    o--o
%     t2

function S = tcl_T_rc_section(Concrete, Rebar, ID, c_matTag, s_matTag)

% -------------------------------------------------------------------------
% Pre-process
% -------------------------------------------------------------------------

h       = Concrete.h;
b       = Concrete.b;
t1      = Concrete.t1;
t2      = Concrete.t2;

D_s     = Rebar.D_s;
n_s     = Rebar.n_s;
d_s     = Rebar.d_s;

% -------------------------------------------------------------------------
% Generate the OS code snippet
% -------------------------------------------------------------------------

S = sprintf('section Fiber %i {\n', ID);
% patch rect $matTag $numSubdivY $numSubdivZ $yI $zI $yJ $zJ
% flange
S = [S, sprintf('\tpatch rect %i %i %i %.5e %.5e %.5e %.5e\n' , c_matTag, 1, 3, -t1,-b/2 , 0,b/2 )];
% web
S = [S, sprintf('\tpatch rect %i %i %i %.5e %.5e %.5e %.5e\n' , c_matTag, 1, 10, -h, -t2/2,-t1 ,t2/2 )];

% rebar
for ii = 1:length(D_s)
    % layer straight $matTag $numBars $areaBar $yStart $zStart $yEnd $zEnd
    A_s_ii  = D_s(ii)^2*pi/4;
    d_s_ii  = d_s(ii);
    yStart  = -d_s_ii;
    yEnd    = -d_s_ii;
    if abs(d_s_ii) < abs(t1)
        zStart  = -t2/2;
        zEnd    = t2/2;
    else
        zStart  = -220;
        zEnd    = 220;
    end
    
    S = [S, sprintf('\tlayer straight %i %i %.5e %.5e %.5e %.5e %.5e\n' , s_matTag, n_s(ii), A_s_ii, yStart, zStart, yEnd, zEnd)];
end

S = [S, sprintf('}\n')];

end