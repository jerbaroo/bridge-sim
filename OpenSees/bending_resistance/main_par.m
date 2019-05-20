clearvars
close all
clc

% INPUT
n_run                   = 13; % dummy

Model.working_dir       = 'C:\Users\arpada\Working_folder\Opensees_working_folder\bending_resistance\';
Model.input_file        = 'bending_resistance.tcl';
Model.os_exe            = 'C:\Program Files\OpenSees\bin\OpenSees.exe';
Model.input_var(1,:)    = linspace(40, 50, n_run); % fy
Model.input_var(2,:)    = linspace(4.0, 4.2, n_run); % As
Model.input_var(3,:)    = linspace(2.8, 3.2, n_run); % fc
Model.out_file          = {'section1.out'};
Model.verbose           = 1;
% Model.keep_last_batch   = 0; % keep everything about the runs in the last
% batch
% Model.keep_results   = 0; % keep all out_files

% RUN
[R, p_tot]              = parallel_os(Model);

disp(R)

% plot(p_tot);
ps = p_tot.par2struct.ItStart;
pe = p_tot.par2struct.ItStop;

mean(pe-ps)
sum(pe-ps)

