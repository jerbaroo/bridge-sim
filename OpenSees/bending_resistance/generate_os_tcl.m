% Generate tcl file based on the provided input
%
%SYNAPSYS
% tcl_up = GENERATE_OS_TCL(x, fpath)
%
%INPUT
% x         vector of input values (a single value for each!)
%
%OUTPUT
% tcl_up    character string of the tcl file
%
%NOTE:
% the function name and argument structure should be kept!

function tcl_up = generate_os_tcl(x, tcl_path)

% -------------------------------------------------------------------------
% INITIALIZE
% -------------------------------------------------------------------------
fc = x(1);
fsy=560;
fsu=660;
esu=0.05;
P=1500;
E=0;
X = 7;

  L1 = 700;
  L2 = 800;
  L3 = 700;
  Lb = 600;%+30
  eleL = 25;
  n1 = L1/eleL;
  n2 = L2/eleL;
  n3 = L3/eleL;
  nb = Lb/eleL;
  n = n1+n2+n3;
  
% rebar
d_s     = 14;
A_s     =(1-X/100)*d_s.^2.*pi/4;
E_s     = 200*1e3;

esl=fy/E_s;
E_su=(fu-fy)/(esu-esl);
cover=32;
% concrete 
deadload=P*eleL/1e3;

h = 300;
b = 200;
E_c = 21.5*1e3.*((fc/10).^(1/3));
ft=0.3.*(fc-8).^(2/3);
Gt=0.073.*(fc.^0.18);

fb=1.25.*((fc-8).^0.5);
fc=-fc;

% bond
% for elastic multi-linear
u=[-20,-14,-3.6,-1.8,-1,-0.5,-0.1,-0.01,0,0.01,0.1,0.5,1,1.8,3.6,14,20]; %deformation

% for stiffness in 2,3 dof.9
rigidmE = E_c.*h*b;

f=2*d_s*pi*eleL.*fb*[-0.4,-0.4,-1,-1,-0.8,-0.6,-0.3,-0.125,0,0.125,0.3,0.6,0.8,1,1,0.4,0.4]; %force
if X>2
f=f.*exp(log(1.55*exp(-0.219*X))+E);

end
% .........................................................................
% Generate tcl file
% .........................................................................
fileID  = fopen('C:\Users\gasselcl\OneDrive - TNO\Matlab\sumo-toolbox\examples\Bondmodel\model.tcl', 'w');

fprintf(fileID,'wipe'); 
fprintf(fileID,'\n\n');
fprintf(fileID,'model basic -ndm 2 -ndf 3'); 
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% MAT
% -------------------------------------------------------------------------

fprintf(fileID, 'uniaxialMaterial ElasticMultiLinear 1  -strain  %.5e %.5e 0 %.5e %.5e %.5e %.5e  -stress %.5e %.5e 0 %.5e %.5e %.5e %.5e',...
      [-0.0035,fc./E_c,ft./E_c,ft./E_c+(Gt/eleL)./ft,ft./E_c+5*(Gt/eleL)./ft,0.08,fc,fc,ft,0.2.*ft,0.1.*ft,0.1.*ft]);
fprintf(fileID,'\n'); 
 
fprintf(fileID, 'uniaxialMaterial ElasticMultiLinear 2  -strain %.5e %.5e %.5e 0 %.5e %.5e %.5e %.5e -stress %.5e %.5e %.5e 0 %.5e %.5e %.5e %.5e',...
     [-0.1,-esu,-esl,fy/E_s,fy/E_s+(fu-fy)/E_su,0.06,0.1,-fu,-fu,-fy,fy,fu,0,0]);
fprintf(fileID,'\n\n');

fprintf(fileID,'uniaxialMaterial Elastic 3 %.5e', rigidmE); 
fprintf(fileID,'\n');

fprintf(fileID,'uniaxialMaterial ElasticMultiLinear 4 -strain ');
        fprintf(fileID,'%.5e ', u);
        fprintf(fileID,'-stress ');
        fprintf(fileID,'%.5e ', f); 
        fprintf(fileID,'\n');

fprintf(fileID,'uniaxialMaterial ElasticMultiLinear 5  -strain ');
        fprintf(fileID,'%.5e ',u);
        fprintf(fileID,'-stress ');
        fprintf(fileID,'%.5e ',0.8.*f); 
        fprintf(fileID,'\n');
        
%section
fprintf(fileID,'section Fiber 1 {');
fprintf(fileID,'\n');
fprintf(fileID,'patch rect 1 20 1 [expr %.2e]  [expr %.2e]  %.2e %.2e',[-h/2,-b/2,h/2,b/2]); 
fprintf(fileID,'\n');
fprintf(fileID,'}\n');

% % -------------------------------------------------------------------------
% NODES
% -------------------------------------------------------------------------
%up
for j=1:n+1
        if j==n/2+nb/2+1
         fprintf(fileID,'node %i %.3e  0.0',[j,j*eleL+15]);
         fprintf(fileID,'\n'); 
        else
         if j==n/2-nb/2+1
         fprintf(fileID,'node %i %.3e  0.0',[j,j*eleL-15]);
         fprintf(fileID,'\n');    
         else
         fprintf(fileID,'node %i %.3e  0.0',[j,j*eleL]);
         fprintf(fileID,'\n'); 
         end
        end
end

%down
for j=1:n+1
        if j==n/2+nb/2+1
        fprintf(fileID,'node %i %.3e  -%.2e',[j+100,j*eleL+15,h/2-cover]);
        fprintf(fileID,'\n'); 
        else
         if j==n/2-nb/2+1
        fprintf(fileID,'node %i %.3e  -%.2e',[j+100,j*eleL-15,h/2-cover]);
        fprintf(fileID,'\n');     
         else
        fprintf(fileID,'node %i %.3e  -%.2e',[j+100,j*eleL,h/2-cover]);
        fprintf(fileID,'\n');  
         end
        end
end

%bar
for j=1:n1+n2/2+nb/2
       if j==n/2-nb/2+1
        fprintf(fileID,'node %i %.3e  -%.2e',[j+1000,j*eleL-15,h/2-cover]);
        fprintf(fileID,'\n');     
       else
        fprintf(fileID,'node %i %.3e  -%.2e',[j+1000,j*eleL,h/2-cover]);
        fprintf(fileID,'\n'); 
       end
        
end
j=n1+n2/2+nb/2+1;
        fprintf(fileID,'node %i %.3e  -%.2e',[j+1000,j*eleL+15,h/2-cover]);
        fprintf(fileID,'\n'); 
j=n+1-n1-n2/2-nb/2;
        fprintf(fileID,'node %i %.3e  -%.2e',[j+2000,j*eleL-15,h/2-cover]);
        fprintf(fileID,'\n');
for j=n+2-n1-n2/2-nb/2:n+1
        if j==n/2+nb/2+1
        fprintf(fileID,'node %i %.3e  -%.2e',[j+2000,j*eleL+15,h/2-cover]);
        fprintf(fileID,'\n'); 
        else
        fprintf(fileID,'node %i %.3e  -%.2e',[j+2000,j*eleL,h/2-cover]);
        fprintf(fileID,'\n'); 
        end
end

% -------------------------------------------------------------------------
% BC
% -------------------------------------------------------------------------
fprintf(fileID, 'fix 1  1 1 0'); 
fprintf(fileID,'\n');

fprintf(fileID, 'fix %i  0 1 0', n+1); 
fprintf(fileID,'\n');

% -------------------------------------------------------------------------
% Element
% -------------------------------------------------------------------------
% concrete
fprintf(fileID,'geomTransf Linear 1'); 
fprintf(fileID,'\n\n');
for ii = 1:n
    fprintf(fileID, 'element dispBeamColumn %i %i %i %i %i  %i',...
        [ii, ii, ii+1, 5, 1, 1]);
    fprintf(fileID,'\n');
end

%bar
for ii = 1:n1+n2/2+nb/2
    fprintf(fileID, 'element truss %i %i %i %.7e %i',...
        [ii+1e3, ii+1e3, ii+1e3+1, 2*A_s, 2]);
    fprintf(fileID,'\n');
end
for ii = n+1-n1-n2/2-nb/2:n
    fprintf(fileID, 'element truss %i %i %i %.7e %i',...
        [ii+2e3, ii+2e3, ii+2e3+1, 2*A_s, 2]);
    fprintf(fileID,'\n');
end

%bond
for ii = 1:n+1
    fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3',...
        [ii+1e4, ii+1e2, ii, 3, 3, 3]);
    fprintf(fileID,'\n');
end
fprintf(fileID,'\n');


for ii = 1:n1+n2/2+nb/2
    if ii==1
        fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+2e4, ii+1e2, ii+1e3, 3, 3,3]);
    else
    fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+2e4, ii+1e2, ii+1e3, 4, 3,3]);
    end
    fprintf(fileID,'\n');
end
ii=n1+n2/2+nb/2+1;
fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+2e4, ii+1e2, ii+1e3, 5, 3, 3]);
    fprintf(fileID,'\n');
ii=n-n3-n2/2-nb/2+1;
 fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+3e4, ii+1e2,ii+2e3, 5, 3, 3]);
    fprintf(fileID,'\n');
for ii = n-n3-n2/2-nb/2+2:n+1
    if ii==n+1
            fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+3e4, ii+1e2, ii+2e3, 3, 3,3]);
    else
    fprintf(fileID, 'element twoNodeLink %i %i %i -mat %i %i %i -dir 1 2 3 -orient 1 0 0 0 1 0',...
        [ii+3e4, ii+1e2, ii+2e3, 4, 3,3]);
    end
    fprintf(fileID,'\n');
end


% -------------------------------------------------------------------------
% DEAD LOAD
% -------------------------------------------------------------------------
fprintf(fileID,'pattern Plain 2 "Linear" {');
fprintf(fileID,'\n');
  for j=1:n+1
    fprintf(fileID,'load  %i 0.0 -%i 0.0',[j,deadload]);
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
fprintf(fileID,'integrator LoadControl 0.1');
fprintf(fileID,'\n');
fprintf(fileID,'algorithm Newton'); 
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static'); 
fprintf(fileID,'\n\n');
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

fprintf(fileID,'timeSeries Linear 1'); 
fprintf(fileID,'\n\n');

fprintf(fileID,'pattern Plain 1 1 {'); 
fprintf(fileID,'\n');
fprintf(fileID,'load %i 0 -1 0', n1+1); 
fprintf(fileID,'\n');
fprintf(fileID,'load %i 0 -1 0', n1+n2+1);
fprintf(fileID,'\n}');
fprintf(fileID,'\n\n');

% -------------------------------------------------------------------------
% SOLVER OPTIONS
% -------------------------------------------------------------------------
fprintf(fileID,'system  ProfileSPD'); 
fprintf(fileID,'\n');
fprintf(fileID,'numberer RCM'); 
fprintf(fileID,'\n');
fprintf(fileID,'constraints Plain'); 
fprintf(fileID,'\n');

% -------------------------------------------------------------------------
% RECORDER
% -------------------------------------------------------------------------




 line = 'recorder Node -file displacement.out -time -node ';
 fprintf(fileID,line); 
 fprintf(fileID,'  %i  ',n/2+1);
 fprintf(fileID,'-dof 2 disp\n');



% Apply force

% -------------------------------------------------------------------------
% SOLVE
% ------------------------------------------------------------------------- 

fprintf(fileID,'test NormDispIncr 1.0e-3  1000 3'); 
fprintf(fileID,'\n');

fprintf(fileID,'algorithm KrylovNewton -iterate initial -increment initial -maxDim 10'); 
fprintf(fileID,'\n');


fprintf(fileID,'integrator DisplacementControl  %i  2  -0.005',n/2+1);
fprintf(fileID,'\n');
fprintf(fileID,'analysis Static');
fprintf(fileID,'\n');
fprintf(fileID, 'analyze 6000');
fprintf(fileID,'\n');
% fprintf(fileID, 'set i [testIter]');
% fprintf(fileID,'\n');
% 
% fprintf(fileID,'algorithm KrylovNewton -iterate initial -increment initial -maxDim 10'); 
% fprintf(fileID,'\n');
% fprintf(fileID,'integrator DisplacementControl  %i  2  -0.01',n/2+1);
% fprintf(fileID,'\n');
% fprintf(fileID,'analysis Static');
% fprintf(fileID,'\n');
% 
% fprintf(fileID, 'set a 0'); 
% fprintf(fileID,'\n');
% fprintf(fileID, 'set b 0'); 
% fprintf(fileID,'\n');
% fprintf(fileID, 'set c 0'); 
% fprintf(fileID,'\n');
% fprintf(fileID, 'set d 0'); 
% fprintf(fileID,'\n');
% fprintf(fileID, 'set j 0'); 
% fprintf(fileID,'\n');
% 
% fprintf(fileID, 'while { $a <= %i && $b <= %i && $c <= %i && $d <= %i && $j<=2000 && $i<1000} {',[esu,esu,esu,esu]);
% fprintf(fileID,'\n');
% fprintf(fileID, 'analyze 1');
% fprintf(fileID,'\n');
% fprintf(fileID, 'set k [expr {$j+1}]');
% fprintf(fileID,'\n');
% fprintf(fileID, 'set j $k');
% fprintf(fileID,'\n');
% fprintf(fileID, ['set a [eleResponse ',num2str(n1+1e3),' material strain]']);
% fprintf(fileID,'\n');
% fprintf(fileID, ['set b [eleResponse ',num2str(n1+1e3+1),' material strain]']);
% fprintf(fileID,'\n');
% fprintf(fileID, ['set c [eleResponse ',num2str(n1+n2+2e3),' material strain]']);
% fprintf(fileID,'\n');
% fprintf(fileID, ['set d [eleResponse ',num2str(n1+n2+2e3+1),' material strain]']);
% fprintf(fileID,'\n');
% fprintf(fileID, 'set i [testIter]');
% fprintf(fileID,'\n');
% fprintf(fileID, '}');
% fprintf(fileID,'\n');
% ----------------------

% % -------------------------------------------------------------------------
% % GENERATE TCL FILE
% % -------------------------------------------------------------------------
% fID     = fopen(tcl_path, 'r');
% tcl     = fscanf(fID, '%c');
% fclose(fID);
% 
% kyw     = 'set fy';
% idx1    = strfind(tcl, kyw) + length(kyw);
% idx2    = idx1 + 5;
% tcl_up  = [tcl(1:idx1), num2str(fy), tcl(idx2:end)];
% 
% kyw     = 'set As';
% idx1    = strfind(tcl_up, kyw) + length(kyw);
% idx2    = idx1 + 5;
% tcl_up    = [tcl_up(1:idx1), num2str(As), tcl_up(idx2:end)];
% 
% kyw     = 'Concrete01    1';
% idx1    = strfind(tcl_up, kyw) + length(kyw);
% idx2    = idx1 + 6;
% tcl_up  = [tcl_up(1:idx1), num2str(-fc), tcl_up(idx2:end)];
% 
% kyw     = 'Concrete01    2';
% idx1    = strfind(tcl_up, kyw) + length(kyw);
% idx2    = idx1 + 6;
% tcl_up  = [tcl_up(1:idx1), num2str(-fc), tcl_up(idx2:end)];

end