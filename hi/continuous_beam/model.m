function model(Rr,fsy0, fsu0, esu0)

global NE



LL1=18600;
LL2=22800;
n=NE;
colWidth =1100;
colDepth =1250;
% Rr=20*ones(n,1);
% Rr(n/3,1)=RrV(1,1);
% Rr(n/3+1,1)=RrV(1,2);
% Rr(n/2,1)=RrV(1,3);
% Rr(n/2+1,1)=RrV(1,4);
% Rr(2*n/3,1)=RrV(1,5);
% Rr(2*n/3+1,1)=RrV(1,6);
Rr=Rr';
fc=-51.2;
As1=7856;
As2=5400;
As3=7364;

d1=42.5;
d2=79.5;
d3=160;
d4=110;
d5=50;

deadload1=3*LL1/20;
deadload2=3*LL2/20;


%pitting corrosion
D0= 25;% rebar dimension
i_corr= 2; % current density [microA/cm^2]
t=50; % time since corrosion initiation[year]
p = 0.0116*i_corr*t*Rr; %  maximum pit depth, Eq.2 [1][mm]

delta = p/D0;
delta_s=pen_depth_to_area_loss(delta);%reducton of As2
esu = esu0*epsu_corr_BV(1, delta_s, 'pitting');
fsy = fsy0*epsu_corr_L(1, 0, delta_s, 0.0016*100);
fsu = fsu0*epsu_corr_L(1, 0, delta_s, 0.0026*100);
As2 =As2*(1-delta_s);
As3 =As3*(1-delta_s);
%other factors
eshi0=fsy0/200e3;
eshi=fsy/200e3;

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
fprintf(fileID, 'uniaxialMaterial Concrete02  1  %.2e -0.0009 %.2e -0.0035 0.5 0.0  47000',...
      [fc,  0.8*fc]);
 fprintf(fileID,'\n');

% .........................................................................
% rebar
% .........................................................................

  fprintf(fileID, 'uniaxialMaterial ElasticMultiLinear  2  -strain 0.0 %.5e %.5e 0.5  -stress  0.0  %.5e %.5e %.5e',...
     [eshi0,esu0, fsy0, fsu0, 0]);
 fprintf(fileID,'\n\n'); 
 
for j=1:n
 sn=num2str(1000+j);
  if fsu(j)<fsy(j)
     fsy(j)=fsu(j);
     eshi=fsy/200e3;
 end
 fprintf(fileID, ['uniaxialMaterial ElasticMultiLinear  ',sn]);
 fprintf(fileID,'  -strain 0.0 %.5e %.5e 0.5  -stress  0.0  %.2e %.2e %.2e',[eshi(j),esu(j), fsy(j), fsu(j),0]);
 fprintf(fileID,'\n\n');
end       
% -------------------------------------------------------------------------
% SECTION
% -------------------------------------------------------------------------
  y1=colDepth/2.0;
  z1=colWidth/2.0;
  
  for j=1:20
       sn=num2str(j);
         fprintf(fileID,['section Fiber ',sn,' {']);
         fprintf(fileID,'\n');
         fprintf(fileID,['patch rect 1 10 1',' [expr ',num2str(-y1),']  [expr ',num2str(-z1),']  ',num2str(y1),' ',num2str(z1)]);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d1),']  0  [expr ',num2str(y1-d1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d2),']  0  [expr ',num2str(y1-d2),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(160-d3),'] 0 [expr ',num2str(160-d3),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(110-d4),'] 0 [expr ',num2str(110-d4),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(50-d5),'] 0 [expr ',num2str(50-d5),'] 0']);
         fprintf(fileID,'\n}\n\n');
  end 
  for j=21:44
        sn=num2str(j);
         fprintf(fileID,['section Fiber ',sn,' {']);
         fprintf(fileID,'\n');
         fprintf(fileID,['patch rect 1 10 1',' [expr ',num2str(-y1),']  [expr ',num2str(-z1),']  ',num2str(y1),' ',num2str(z1)]);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d1),']  0  [expr ',num2str(y1-d1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d2),']  0  [expr ',num2str(y1-d2),'] 0']);    
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight ',num2str(1000+j),' 1  ',num2str(As2(j)*5/11),' [expr ',num2str(d4-y1),'] 0 [expr ',num2str(d4-y1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight ',num2str(1000+j),' 1  ',num2str(As2(j)*6/11),' [expr ',num2str(d5-y1),'] 0 [expr ',num2str(d5-y1),'] 0']);
         fprintf(fileID,'\n}\n\n');
  end
 for j=45:64
      sn=num2str(j);
         fprintf(fileID,['section Fiber ',sn,' {']);
         fprintf(fileID,'\n');
         fprintf(fileID,['patch rect 1 10 1',' [expr ',num2str(-y1),']  [expr ',num2str(-z1),']  ',num2str(y1),' ',num2str(z1)]);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d1),']  0  [expr ',num2str(y1-d1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  2  1  ',num2str(As1/2),' [expr ',num2str(y1-d2),']  0  [expr ',num2str(y1-d2),'] 0']);       
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(d3-y1),'] 0 [expr ',num2str(d3-y1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(d4-y1),'] 0 [expr ',num2str(d4-y1),'] 0']);
         fprintf(fileID,'\n');
         fprintf(fileID,['layer straight  ',num2str(1000+j),'   1  ',num2str(As3(j)/3),' [expr ',num2str(d5-y1),'] 0 [expr ',num2str(d5-y1),'] 0']); 
         fprintf(fileID,'\n}\n\n');
  end
% -------------------------------------------------------------------------
% NODES
% -------------------------------------------------------------------------
 for j=1:21
        sn=num2str(j);
        fprintf(fileID,['node ',sn,' ',num2str((j-1)*LL1/20),'  0.0']);
        fprintf(fileID,'\n');
 end
  for j=22:45
        sn=num2str(j);
        if j<=31
        fprintf(fileID,['node ',sn,' ',num2str(LL1+(j-21)*(LL2-3000)/20),'  0.0']);
        else
            if j>=35
        fprintf(fileID,['node ',sn,' ',num2str(LL1+LL2/2+1500+(j-35)*(LL2-3000)/20),'  0.0']);        
            else
            fprintf(fileID,['node ',sn,' ',num2str(LL1+LL2/2-1500+(j-31)*750),'  0.0']);        
            end
        end
        fprintf(fileID,'\n');
  end

  for j=46:65
        sn=num2str(j);
        fprintf(fileID,['node ',sn,' ',num2str(LL1+LL2+(j-45)*LL1/20),'  0.0']);
        fprintf(fileID,'\n');
 end
% -------------------------------------------------------------------------
% BC
% -------------------------------------------------------------------------
fprintf(fileID, 'fix 1  1 1 0'); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(21),'  0  1  0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(45),'  0  1  0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['fix  ',num2str(65),'  0  1  0']); 
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% ELEMENT
% -------------------------------------------------------------------------
 for j=1:20
        sn=num2str(j);
        fprintf(fileID,['element  dispBeamColumn ',sn,' ',num2str(j),'  ',num2str(j+1),'  5  ',num2str(j),'  1']);
        fprintf(fileID,'\n');
 end
  for j=21:44
        sn=num2str(j);
        fprintf(fileID,['element  dispBeamColumn ',sn,' ',num2str(j),'  ',num2str(j+1),'  5  ',num2str(j),'  1']);
        fprintf(fileID,'\n');
  end
  for j=45:64
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
  for j=1:21
    fprintf(fileID,'load  %i 0.0 -%i 0.0',[j,deadload1/2]);
    fprintf(fileID,'\n');
  end
    for j=22:44
    fprintf(fileID,'load  %i 0.0 -%i 0.0',[j,deadload2/2]);
    fprintf(fileID,'\n');
    end
    for j=45:65
    fprintf(fileID,'load  %i 0.0 -%i 0.0',[j,deadload1/2]);
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
fprintf(fileID,'test NormDispIncr 1.0e-3  50 3'); 
fprintf(fileID,'\n');
fprintf(fileID,'integrator LoadControl 1');
fprintf(fileID,'\n');
fprintf(fileID,'algorithm Newton'); 
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static'); 
fprintf(fileID,'\n\n');
% -------------------------------------------------------------------------
% SOLVE
% -------------------------------------------------------------------------
fprintf(fileID, 'analyze 20'); 
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% LIVE LOAD
% -------------------------------------------------------------------------
fprintf(fileID, 'loadConst -time 0.0'); 
fprintf(fileID,'\n\n');
fprintf(fileID, 'pattern Plain 1  "Linear" {'); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2-1),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2+1),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n');
fprintf(fileID, ['load  ',num2str(n/2+3),' 0.0 -1.0 0.0']); 
fprintf(fileID,'\n}\n');
% -------------------------------------------------------------------------
% RECORDER
% -------------------------------------------------------------------------
fprintf(fileID, ['recorder Node -file section.out -time -node ',num2str(n/2+1),' -dof 2 disp']); 
fprintf(fileID,'\n');            
% -------------------------------------------------------------------------
% SOLVER OPTIONS
% -------------------------------------------------------------------------
fprintf(fileID,'system ProfileSPD'); 
fprintf(fileID,'\n');
fprintf(fileID,'numberer RCM'); 
fprintf(fileID,'\n');
fprintf(fileID,'constraints Plain'); 
fprintf(fileID,'\n');
fprintf(fileID,'test NormUnbalance 1.0e-2 30  5'); 
fprintf(fileID,'\n');
fprintf(fileID,['integrator DisplacementControl  ',num2str(n/2+1),'  2  ',num2str(dY)]);
fprintf(fileID,'\n');
fprintf(fileID,'algorithm Newton'); 
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static'); 
fprintf(fileID,'\n\n');
% -------------------------------------------------------------------------
% SOLVE
% -------------------------------------------------------------------------
fprintf(fileID, 'set a 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set b 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set c 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set d 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set e 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set f 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'set h 0'); 
fprintf(fileID,'\n');
fprintf(fileID, 'while { $a <= %i && $b <= %i && $c <= %i && $d <= %i && $e <= %i && $f <= %i && $h<1000} {',[esu(n/2),esu(n/2+1),esu0,esu0,esu0,esu0]);
fprintf(fileID,'\n');
fprintf(fileID, 'analyze 1');
fprintf(fileID,'\n');
fprintf(fileID, ['set a [eleResponse ',num2str(n/2),' section 5 fiber -575 0 ',num2str(1000+n/2),' strain]']);
fprintf(fileID,'\n');
fprintf(fileID, ['set b [eleResponse ',num2str(n/2+1),' section 1 fiber -575 0 ',num2str(1000+n/2+1),' strain]']);
fprintf(fileID,'\n');
fprintf(fileID, ['set c [eleResponse ',num2str(20),' section 5 fiber 582.5 0 2 strain]']);
fprintf(fileID,'\n');
fprintf(fileID, ['set d [eleResponse ',num2str(21),' section 1 fiber 582.5 0 2 strain]']);
fprintf(fileID,'\n');
fprintf(fileID, ['set e [eleResponse ',num2str(44),' section 5 fiber 582.5 0 2 strain]']);
fprintf(fileID,'\n');
fprintf(fileID, ['set f [eleResponse ',num2str(45),' section 1 fiber 582.5 0 2 strain]']);
fprintf(fileID,'\n');
fprintf(fileID, 'set k [expr {$h+1}]');
 fprintf(fileID,'\n');
 fprintf(fileID, 'set h $k');
 fprintf(fileID,'\n');
fprintf(fileID, '}');
fprintf(fileID,'\n');

fclose(fileID);





