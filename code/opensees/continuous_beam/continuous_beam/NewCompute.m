clear all
close all
clc

n=300;
LL=60000;
colWidth=1100;
colDepth=1250;
cover=90;
deadload=3*LL/n;

fc=-51.2;
fsy=440;
fsu=550;
esu=0.08;
eshi=fsy/200e3;
Esi= 1.1*(fsu-fsy)/(esu-eshi);
As1=7856;
As2=3928;

Y=-1000;
numIcr=1000;
dY=Y/numIcr;
% =========================================================================
% WRITE THE TCL FILE
% =========================================================================
os_dir  = 'C:\Users\jiangq\Desktop\code\continuous_beam\';
fname   = 'NewBeam.tcl';

fileID     = fopen([os_dir, '\', fname], 'w');
fprintf(fileID,'wipe'); 
fprintf(fileID,'\n\n');
fprintf(fileID,'model basic -ndm 2 -ndf 3');
fprintf(fileID,'\n\n');
fprintf(fileID,'geomTransf Linear 1');
fprintf(fileID,'\n\n');
% -------------------------------------------------------------------------
% MAT
% -------------------------------------------------------------------------
% .........................................................................
% concrete
% .........................................................................
 fprintf(fileID,'uniaxialMaterial Concrete01 1 %.2e -0.0009 %.2e -0.0035',...
            [fc, 0.8*fc]);
 fprintf(fileID,'\n');

% .........................................................................
% rebar
% .........................................................................
 fprintf(fileID, 'uniaxialMaterial ElasticMultiLinear  3  -strain 0.0 %.5e %.5e 0.5  -stress  0.0  %.2e %.2e %.2e',...
     [eshi,esu, fsy, fsu, fsu]);
 fprintf(fileID,'\n\n');
       
% -------------------------------------------------------------------------
% SECTION
% -------------------------------------------------------------------------
  y1=colDepth/2.0;
  z1=colWidth/2.0;
  for j=1:n
        sn=num2str(j);
         fprintf(fileID,['section Fiber ',sn,' {']);
         fprintf(fileID,'\n');
         fprintf(fileID,['patch rect 1 10 1',' [expr ',num2str(-y1),']  [expr ',num2str(-z1),']  ',num2str(y1),' ',num2str(z1)]);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight 3 1  ',num2str(As1),' [expr ',num2str(y1-cover),'] ',num2str(z1-cover),' [expr ',num2str(y1-cover),'] [expr ',num2str(cover-z1),']']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight 3 1  ',num2str(As2),' [expr ',num2str(cover-y1),'] ',num2str(z1-cover),' [expr ',num2str(cover-y1),'] [expr ',num2str(cover-z1),']']);
         fprintf(fileID,'\n}\n\n');
  end
% -------------------------------------------------------------------------
% NODES
% -------------------------------------------------------------------------
 for j=1:n+1
        sn=num2str(j);
        fprintf(fileID,['node ',sn,' ',num2str((j-1)*LL/n),'  0.0']);
        fprintf(fileID,'\n');
 end
% -------------------------------------------------------------------------
% BC
% -------------------------------------------------------------------------
fprintf(fileID, 'fix 1  1 1 0'); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(n/3+1),'  0  1  0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(2*n/3+1),'  0  1  0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(n+1),'  0  1  0']); 
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% ELEMENT
% -------------------------------------------------------------------------
 for j=1:n
        sn=num2str(j);
        fprintf(fileID,['element  dispBeamColumn ',sn,' ',num2str(j),'  ',num2str(j+1),'  5  ',num2str(j),'  1']);
        fprintf(fileID,'\n');
 end
  fprintf(fileID,'\n\n');
% -------------------------------------------------------------------------
% DEAD LOAD
% -------------------------------------------------------------------------
fprintf(fileID,'pattern Plain 2 "Linear" {');
fprintf(fileID,'\n');
  for j=1:n
    fprintf(fileID,['load  ',num2str(j),' 0.0 -1.0 0.0']);
    fprintf(fileID,'\n');
  end
    fprintf(fileID,'}\n\n');
% -------------------------------------------------------------------------
% SOLVER OPTIONS
% -------------------------------------------------------------------------
fprintf(fileID,'system ProfileSPD'); 
fprintf(fileID,'\n');
fprintf(fileID,'numberer RCM'); 
fprintf(fileID,'\n');
fprintf(fileID,'constraints Plain'); 
fprintf(fileID,'\n');
fprintf(fileID,'test NormDispIncr 1.0e-3  20 3'); 
fprintf(fileID,'\n');
fprintf(fileID,['integrator LoadControl ',num2str(deadload)]);
fprintf(fileID,'\n');
fprintf(fileID,'algorithm Newton'); 
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static'); 
fprintf(fileID,'\n\n');

% fprintf(fileID, ['recorder Node -file section.out -time -node ',num2str(n/4+1),'  ' ,num2str(n/2+1),'  ' ,num2str(3*n/4+1),'  ' ,' -dof 2 disp']); 
% fprintf(fileID,'\n');            
% fprintf(fileID, ['recorder Element -file element.out -time -ele ',num2str(n/2),' section 5  fiber  -535  0  3  stress']); 
% fprintf(fileID,'\n\n'); 
% -------------------------------------------------------------------------
% SOLVE
% -------------------------------------------------------------------------
fprintf(fileID, 'analyze 10'); 
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% LIVE LOAD
% -------------------------------------------------------------------------
fprintf(fileID, 'loadConst -time 0.0'); 
fprintf(fileID,'\n\n');
fprintf(fileID, 'pattern Plain 1  "Linear" {'); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2+1),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2+2),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n}\n');
% -------------------------------------------------------------------------
% RECORDER
% -------------------------------------------------------------------------
fprintf(fileID, ['recorder Node -file section.out -time -node ',num2str(n/2+1),' -dof 2 disp']); 
fprintf(fileID,'\n');            
fprintf(fileID, ['recorder Element -file element.out -time -ele ',num2str(n/2-1),'  ',num2str(n/2),'  ',num2str(n/2+1),' force']); 
fprintf(fileID,'\n\n');      
% -------------------------------------------------------------------------
% % SOLVER OPTIONS
% % -------------------------------------------------------------------------
fprintf(fileID,'system ProfileSPD'); 
fprintf(fileID,'\n');
fprintf(fileID,'numberer RCM'); 
fprintf(fileID,'\n');
fprintf(fileID,'constraints Plain'); 
fprintf(fileID,'\n');
fprintf(fileID,'test NormUnbalance 1.0e-3 30  5'); 
fprintf(fileID,'\n');
fprintf(fileID,['integrator DisplacementControl  ',num2str(n/2+1),'  2  ',num2str(dY)]);
fprintf(fileID,'\n');
fprintf(fileID,'algorithm Newton'); 
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static'); 
fprintf(fileID,'\n\n');
% % -------------------------------------------------------------------------
% % SOLVE
% % -------------------------------------------------------------------------
fprintf(fileID, 'set a 0'); 
fprintf(fileID,'\n');
fprintf(fileID, ['while { $a <= ',num2str(esu),'} {']);
fprintf(fileID,'\n');
fprintf(fileID, 'analyze 1');
fprintf(fileID,'\n');
fprintf(fileID, ['set a [eleResponse ',num2str(n/2),' section 5 fiber -535 0 3 strain]']);
fprintf(fileID,'\n');
fprintf(fileID, '}');
fprintf(fileID,'\n');

fclose(fileID);
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

