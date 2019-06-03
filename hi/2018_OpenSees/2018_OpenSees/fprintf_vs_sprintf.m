clearvars
close all
clc

N = 1e2;

% fprintf
t1 = tic;
fname           = 'cont_beam1.tcl';
fileID          = fopen(fname, 'w');

nn = 1:N;
for ii = 1:N
    fprintf(fileID, 'node %i\n', nn(ii));
end
fprintf(fileID,'\n');
fclose(fileID);
toc(t1)

% sprintf
t2 = tic;
S = [];
for ii = 1:N
    line    = sprintf('node %i\n', nn(ii));
    S       = sprintf('%c', S, line);
end
fname           = 'cont_beam2.tcl';
fileID          = fopen(fname, 'w');
fprintf(fileID, S);
fclose(fileID);
toc(t2)