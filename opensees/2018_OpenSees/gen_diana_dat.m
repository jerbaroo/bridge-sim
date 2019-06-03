%
% [mm], [N]

function gen_diana_dat

clc
close all
% =========================================================================
% PRE-PROCESSING
% =========================================================================
key_T_loc = [-3e4, -2.38E+04, -1.76E+04 ,-3.80E+03	3.80E+03, 1.76E+04	2.38E+04, 3e4];
% [h, b, t1, t2]
key_T_geom = [
    1.25000E+03, 2.15000E+03, 2.00000E+02, 1.10000E+03;... % 4 TSHAPE
    1.25000E+03, 2.15000E+03, 2.00000E+02, 5.00000E+02;... % 36 TSHAPE
    1.25000E+03, 2.15000E+03, 2.00000E+02, 1.10000E+03;... % 67/68 TSHAPE


N1 = -3e4:200:3e4;

% T_geom = [
% 1.25000E+03     1.25000E+03     1.25000E+03
% 2.15000E+03     2.15000E+03     2.15000E+03
% 2.00000E+02     2.00000E+02     2.00000E+02
% 1.10000E+03     1.09032E+03     1.08065E+03];

% n = 3;
% Rebar(1,:) = ones(1,n)*2.45400E+03;
% Rebar(2,:) = ones(1,n)*(1250 - 50);
% Rebar(3,:) = ones(1,n)*2.00000E+05/3.59090E+04;
% 
% aa = 1250 - T_section(T_geom, Rebar)
% bb = [6.950000E+02, 6.967903E+02, 6.985806E+02]
% 
% diff(aa)
% diff(bb)
% =========================================================================
% WRITE THE *.DAT FILE
% =========================================================================

proj_dir        = 'c:\Users\arpada\Working folder\Diana working folder\Cont_beam\Phase 2\udl_no_corrosion';
proj_name       = 'test';

fileID          = fopen([proj_dir, '\', proj_name, '.dat'], 'w');

% -------------------------------------------------------------------------
% HEADER
% -------------------------------------------------------------------------
line = ': Diana Datafile written for Diana 10.1';
fprintf(fileID,line); fprintf(fileID,'\n');
line = [': Automatically generated from Matlab, ', datestr(datetime)];
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'FEMGEN MODEL      : MODEL';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'ANALYSIS TYPE     : Structural 3D';
fprintf(fileID,line); fprintf(fileID,'\n');
line = '''UNITS''';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'LENGTH   MM';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'TIME     SEC';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'TEMPER   CELSIU';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'FORCE    N';
fprintf(fileID,line); fprintf(fileID,'\n');
line = '''MODEL''';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'GRAVAC    -10.0000';
fprintf(fileID,line); fprintf(fileID,'\n');
line = 'GRAVDI 2';
fprintf(fileID,line); fprintf(fileID,'\n');

 

% Dat             = fscanf(fileID, '%c');
fclose(fileID);
