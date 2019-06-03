function model(fc,fsy,fsu,esu)

global NE
global LL
global colWidth
global colDepth
global cover

os_dir  = 'C:\Users\jiangq\Desktop\code\continuous_beam\uniform\';
fname   = 'SimplySupportedBeam.tcl';

        fID     = fopen([os_dir, '\', fname], 'r');
        D       = fscanf(fID, '%c');
        fclose(fID);
      
        
        %define parameters
       
        n=NE;
        eshi=fsy/200e3;
        Esi= 1.1*(fsu-fsy)/(esu-eshi);
        %change properties    
        kyw1     = 'set fc';
        kyw2    = '#concrete strength';
        idx1    = strfind(D, kyw1) + length(kyw1);
        idx2    = strfind(D, kyw2);
        D_1 = [D(1:idx1), num2str(fc,'% 10.2f'),';', D(idx2:end)];

        kyw1     = 'set fsy';
        kyw2= '# Yield stress';
        idx1    = strfind(D_1, kyw1) + length(kyw1);
        idx2    = strfind(D_1, kyw2);
        
        D_2    = [D_1(1:idx1), num2str(fsy,'% 10.2f'),';', D_1(idx2:end)];
        
        kyw1     = 'set fsu';
        kyw2= '# ultimate stress';
        idx1    = strfind(D_2, kyw1) + length(kyw1);
        idx2    = strfind(D_2, kyw2);
        
        D_3    = [D_2(1:idx1), num2str(fsu,'% 10.2f'),';', D_2(idx2:end)];

        kyw1     = 'set esu';
        kyw2= '# ultimate strain';
        idx1    = strfind(D_3, kyw1) + length(kyw1);
        idx2    = strfind(D_3, kyw2);
        
        D_4    = [D_3(1:idx1), num2str(esu,'% 10.5f'),';', D_3(idx2:end)];
        
         kyw1     = 'set eshi';
        kyw2= '# yield strain';
        idx1    = strfind(D_4, kyw1) + length(kyw1);
        idx2    = strfind(D_4, kyw2);
        
        D_5    = [D_4(1:idx1), num2str(eshi,'% 10.5f'),';', D_4(idx2:end)];
        
         kyw1     = 'set Esi';
        kyw2= '# harding Youngs modulus';
        idx1    = strfind(D_5, kyw1) + length(kyw1);
        idx2    = strfind(D_5, kyw2);
        
        D_6    = [D_5(1:idx1), num2str(Esi,'% 10.2f'),';', D_5(idx2:end)];
        % section
        kyw1     = '# Define section';
        kyw2     ='# End of define section';

        idx1    = strfind(D_6, kyw1) + length(kyw1);
        idx2    = strfind(D_6, kyw2);

       
        D_sec    = D_6(1:idx1);
        y1=colDepth/2.0;
        z1=colWidth/2.0;
        for j=1:n
        sn=num2str(j);
        sstart=['section Fiber ',sn,' {',newline];
        smiddle=['patch rect 1 10 1',' [expr ',num2str(-y1),']  [expr ',num2str(-z1),']  ',num2str(y1),' ',num2str(z1),newline];
        send=['layer straight 3 1',' 7856 ',' [expr ',num2str(y1-cover),'] ',num2str(z1-cover),' [expr ',num2str(y1-cover),'] [expr ',num2str(cover-z1),']',newline,...
              'layer straight 3 1',' 3928',' [expr ',num2str(cover-y1),'] ',num2str(z1-cover),' [expr ',num2str(cover-y1),'] [expr ',num2str(cover-z1),']',newline,'}',newline];
        
        D_sec    = [D_sec, sstart,smiddle,send];
        end
        
        D_sec    = [D_sec, D_6(idx2:end)];
               
        %define node
        kyw1     = '# Define node';
        kyw2     ='# End of define node';
        idx1    = strfind(D_sec, kyw1)+ length (kyw1);
        idx2    = strfind(D_sec,kyw2);
        D_node    = D_sec(1:idx1);

        for j=1:n+1
        sn=num2str(j);
        snode=['node ',sn,' ',num2str((j-1)*LL/n),'  0.0',newline];
        
        D_node    = [D_node, snode];
        end
        
        D_node    = [D_node, D_sec(idx2:end)];
        
        
        %define member
        kyw1     = '# Define element';
        kyw2     ='# End of define element';
        idx1    =strfind(D_node, kyw1) + length(kyw1);
        idx2    =strfind(D_node, kyw2);
        D_mem    = D_node(1:idx1);

        for j=1:n
        sn=num2str(j);
        smember=['element  dispBeamColumn ',sn,' ',num2str(j),'  ',num2str(j+1),'  5  ',num2str(j),'  1',newline];
       
        D_mem    = [D_mem, smember];
        end
        
        D_mem    = [D_mem, D_node(idx2:end)];     
        
        %define dead load
        kyw1     = '# Define dead load';
        kyw2     ='#End of define dead load';
        idx1    =strfind(D_mem, kyw1) + length(kyw1);
        idx2    =strfind(D_mem, kyw2);
        D_deadload    = D_mem(1:idx1);
        
        deadload=['pattern Plain 2 "Linear" {',newline];
        for j=1:n
            deadload = [deadload,'load  ',num2str(j),' 0.0 -1.0 0.0',newline];
        end
         deadload = [deadload,'}',newline];
        D_deadload    = [D_deadload, deadload,D_mem(idx2:end)];
        
        %define reference force
        kyw1     = 'pattern Plain 1  "Linear" {';
        kyw2     ='# End of define reference force';
        idx1    =strfind(D_deadload, kyw1) + length(kyw1);
        idx2    =strfind(D_deadload, kyw2);
        D_load    = D_deadload(1:idx1);
        liveload=['load  ',num2str(n/2),' 0.0 -1.0 0.0',newline,...
              'load  ',num2str(n/2+1),' 0.0 -1.0 0.0',newline,...
              'load  ',num2str(n/2+2),' 0.0 -1.0 0.0',newline,...
              '}',newline,'recorder Node -file section.out -time -node ',num2str(n/2+1),' -dof 2 disp',newline...
           'recorder Element -file element.out -time -ele ',num2str(n/2),' section 5 fiber -535 0  3  stress',newline];
        
       D_load    = [D_load, liveload,D_deadload(idx2:end)];
        
        %define displacement
        kyw1     = '# Use displacement control at node 2 for analysis';
        kyw2     ='# End of define displacement';
                
        idx1    =strfind(D_load, kyw1) + length(kyw1);
        idx2    =strfind(D_load, kyw2);
        D_dis    = D_load(1:idx1);
        sdis=['integrator DisplacementControl  ',num2str(n/2+1),'  2 -$dY',newline];
        D_dis    = [D_dis, sdis,D_load(idx2:end)];
        
        % fix dofs
        kyw1     = '# Fix degrees of freedom';
        kyw2     ='# End of fix degrees of freedom';
                
        idx1    =strfind(D_dis, kyw1) + length(kyw1);
        idx2    =strfind(D_dis, kyw2);
        D_fix    = D_dis(1:idx1);
        sfix=['fix  1  1  1  0',newline,...
              'fix  ',num2str(n/3+1),'  0  1  0',newline,...
              'fix  ',num2str(2*n/3+1),'  0  1  0',newline,...
              'fix ',num2str(n+1),' 0 1 0',newline];
        D_fix    = [D_fix, sfix,D_dis(idx2:end)];

        %write sentence
        fID     = fopen([os_dir, fname], 'w');
        fwrite(fID, D_fix);
        fclose(fID);


