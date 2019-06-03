%
% [mm], [N]

% function mod_diana_dat

clearvars
clc
close all

proj_dir        = 'c:\Users\arpada\Working folder\Diana working folder\Cont_beam\Phase 2\udl_no_corrosion';
proj_name       = 'udl_no_corrosion';

full_path       = [proj_dir, '\', proj_name, '.dat'];
fileID          = fopen(full_path, 'r');
Dat             = fscanf(fileID, '%c');


N = get_nodes(full_path);

plot(N(:,2), N(:,3), 'x-')
fclose(fileID);
% =========================================================================
% PRE-PROCESSING
% =========================================================================

% =========================================================================
% WRITE THE *.DAT FILE
% =========================================================================


% -------------------------------------------------------------------------
% HEADER
% -------------------------------------------------------------------------


% end