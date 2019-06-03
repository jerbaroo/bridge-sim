% Moment Curvature Example
%
% Based on:
%   http://opensees.berkeley.edu/wiki/index.php/Moment_Curvature_Example


function M = bending_resistance(fy, As, fc)

% -------------------------------------------------------------------------
% OPTIONS
% -------------------------------------------------------------------------
os_dir  = 'c:\Users\arpada\Working_folder\Opensees_working_folder\Nowak_example_5.2\';
delete([os_dir, '*'])

% fname   = 'MomentCurvature5-2_original.tcl';
fname   = 'MomentCurvature5-2.tcl';

b       = 12;
d       = 19;

% EC conform


switch lower (type)
    case {'ec', 'eurocode'}
        xc      = As*fy/(fc*b);
        M       = (d - xc/2)*xc*b*fc;
    case 'nowak'
        % from Nowak
        M       = As*fy*d - 0.59*(As*fy)^2/(fc*b);
    case {'os', 'opensees'}
        % -------------------------------------------------------------------------
        % GENERATE THE TCL FILE - naive & fragile
        % -------------------------------------------------------------------------

        fID     = fopen([pwd, '\', fname], 'r');
        D       = fscanf(fID, '%c');
        fclose(fID);

        kyw     = 'set fy';
        idx1    = strfind(D, kyw) + length(kyw);
        idx2    = idx1 + 5;
        D_up = [D(1:idx1), num2str(fy), D(idx2:end)];

        kyw     = 'set As';
        idx1    = strfind(D_up, kyw) + length(kyw);
        idx2    = idx1 + 5;
        D_up    = [D_up(1:idx1), num2str(As), D_up(idx2:end)];
        
        kyw     = 'Concrete01    1';
        idx1    = strfind(D_up, kyw) + length(kyw);
        idx2    = idx1 + 6;
        D_up    = [D_up(1:idx1), num2str(-fc), D_up(idx2:end)];
        
        kyw     = 'Concrete01    2';
        idx1    = strfind(D_up, kyw) + length(kyw);
        idx2    = idx1 + 6;
        D_up    = [D_up(1:idx1), num2str(-fc), D_up(idx2:end)];

        fID     = fopen([os_dir, fname], 'w');
        fwrite(fID, D_up);
        fclose(fID);

        % -------------------------------------------------------------------------
        % ANALYSIS
        % -------------------------------------------------------------------------
        mwd     = pwd;
        cd(os_dir)

        % two output arguments suppress the echo, Matlab magic :)
%         dos(['"c:\Program Files\OpenSees\bin\OpenSees.exe" ', fname]);
        [~, ~]  = dos(['"c:\Program Files\OpenSees\bin\OpenSees.exe" ', fname]);
        cd(mwd)

        % -------------------------------------------------------------------------
        % POSTPROCESS
        % -------------------------------------------------------------------------

        O = dlmread([os_dir, 'section1.out']);

        [M, idx] = max(O(:,1));
        plot(O(:,2),O(:,1))
        hold on
        plot(O(idx,2), M, 'ro')
        xlabel('Curvature 1/in')
        ylabel('Moment kip-in')
    otherwise
        error(['Unknown type: ', type])
end



