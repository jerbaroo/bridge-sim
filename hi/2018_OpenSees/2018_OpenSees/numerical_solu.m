% OpenSees

function numerical_solu(Q, L_span, l_elem, concrete_model, rebar_model)

% -------------------------------------------------------------------------
% PREPROCESS
% -------------------------------------------------------------------------
% remove old result files
delete('*.out')
delete('*.')

% generate the tcl file for OpenSees
gen_tcl(Q, L_span, l_elem, concrete_model, rebar_model)

% -------------------------------------------------------------------------
% ANALYSIS
% -------------------------------------------------------------------------
tic
dos(['"c:\Program Files\OpenSees\bin\OpenSees.exe" ', 'model.tcl']);
% [~, ~]  = dos(['"c:\Program Files\OpenSees\bin\OpenSees.exe" ', fname]);
toc

% -------------------------------------------------------------------------
% POSTPROCESS
% -------------------------------------------------------------------------


% deflection of the RC section of the concrete
dX_rc        = dlmread('rc_section_displY.out', ' ');
load_scale   = dX_rc(:,1);
[~, idx]     = max(abs(dX_rc(end,2:end)));
dmax         = dX_rc(:,idx);
% dX_rc        = dX_rc(end,:);
dX_rc(:,1)     = [];

% internal forces
F_rc        = dlmread('rc_section_eleGlobalForce.out', ' ');
F_rc        = F_rc(end,:);
F_rc(1)     = [];
M_rci       = -[F_rc(3:6:end), -F_rc(end)];
M_rcj       = [-F_rc(3), F_rc(6:6:end)];
M_rc        = (M_rci + M_rcj)/2;


% PLOT
xx          = 0:l_elem:60;

figure
plot(xx, -dX_rc*1e3, 'Color', 0.7*ones(1,3))
set(gca,'Ydir','reverse')
hold on
hp = plot([0,cumsum(L_span)], zeros(length(L_span)+1,1), 'o-', 'Color', 'black');
hp.MarkerFaceColor =[0,0,0];

xlabel('Position, $x$ [m]')
ylabel('Delfection, $d_\mathrm{y}$ [mm]')
xlim([0, sum(L_span)])
prettify(gcf)

figure
plot(xx, M_rc/1e3)
set(gca,'Ydir','reverse')
hold on
hp = plot([0,cumsum(L_span)], zeros(length(L_span)+1,1), 'o-', 'Color', 'black');
hp.MarkerFaceColor =[0,0,0];

xlabel('Position, $x$ [m]')
ylabel('Bending moment, $M$ [kNm]')
xlim([0, sum(L_span)])
prettify(gcf)

figure
Q_max = max(Q*load_scale/1e3);
disp(['Q_max = ', num2str(Q_max), ' [kN](x3)'])
plot(-dmax*1e3, Q*load_scale/1e3)

xlabel('Max. deflection, [mm]')
ylabel('Load, $Q$ [kN]')
prettify(gcf)

end