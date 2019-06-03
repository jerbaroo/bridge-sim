
function Resis=load_resistance(fc,fsy,fsu,esu,As1,As2,As3,Rr,P)
% -------------------------------------------------------------------------
% OPTIONS
% -------------------------------------------------------------------------
% fsy=440;
% fsu=550;
% esu=0.08;
% fc=51.2;
%  As2=5400;
%  As1=7856;
% As3=7364;
%Rr=0;
model(fsy,fsu,esu,fc,As1,As2,As3,Rr,P);
os_dir  = 'C:\Users\jiangq\Desktop\code\continuous_beam\uniform\';
delete([os_dir, 'section.out'])
fname   = 'NewBeam.tcl';


        % -------------------------------------------------------------------------
        % ANALYSIS
        % -------------------------------------------------------------------------
        mwd     = pwd;
        cd(os_dir)

        dos(['"C:\Users\jiangq\Desktop\OpenSees2.5.0-x64.exe\OpenSees.exe" ', fname]);
        %[~,~]=dos(['"C:\Users\jiangq\Desktop\OpenSees2.5.0-x64.exe\OpenSees.exe" ', fname]);
        cd(mwd)

        % -------------------------------------------------------------------------
        % POSTPROCESS
        % -------------------------------------------------------------------------

        O = dlmread([os_dir, 'section.out']);
        
        [Resis, idx] = max(O(:,1));
        
        plot(-O(:,2),O(:,1))
        hold on
        plot(-O(idx,2), Resis, 'ro')
        xlabel('Deflection mm')
        ylabel('Load N')
        
       

