function P=load_resistance_basic(Rr,fsy, fsu, esu)

% -------------------------------------------------------------------------
% OPTIONS
% -------------------------------------------------------------------------

model(Rr,fsy, fsu, esu);
os_dir  = 'C:\Users\jiangq\Desktop\code\continuous_beam\';
delete([os_dir, 'section.out'])
fname   = 'NewBeam.tcl';


        % -------------------------------------------------------------------------
        % ANALYSIS
        % -------------------------------------------------------------------------
        mwd     = pwd;
        cd(os_dir)

        dos(['"C:\Users\jiangq\Desktop\OpenSees2.5.0-x64.exe\OpenSees.exe" ', fname]);
        cd(mwd)

        % -------------------------------------------------------------------------
        % POSTPROCESS
        % -------------------------------------------------------------------------

        O = dlmread([os_dir, 'section.out']);
        
        [P, idx] = max(O(:,1));
        
        plot(-O(:,2),O(:,1))
        hold on
        plot(-O(idx,2), P, 'ro')
        xlabel('Deflection mm')
        ylabel('Load N')
        
       

