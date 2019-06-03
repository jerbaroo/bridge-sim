function Cor_M = CovDec_Cor(Dim,mean,std,CF,c1,lc,Mesh,distribution) 
%CovDec returns correlated random variables for a isotropic gaussain field 
%
% Output:
% Cor_M: Correlation Matrix of random variables 
%
% Input:
% Dim: Model dimension (1, 2, 3) % mean: Mean value random field
% std: Standard deviation random field
% CF: Type of correlation function ('Exp', 'SExp') 
% Exp: Exponential correlation function
% Exp = c1+(1-c1)*exp(-delta_x/lc)
% SExp: Squared exponential correlation function
% SExp = c1+(1-c1)*exp(-(delta_x/lc)^2)
% Where delta_x is the lag distance which can be detemined with
% the coordinates of the Mesh
% c1: threshold value for correlation function
% lc: Correlation length/scale of fluctuation in both directions 
% Mesh: Matrix containing the coordinates of the random field mesh 
% Dec: Decomposition method (chol/eigen)
if Dim==1 
    %Determine Correlation matrix
Cor_M=zeros(length(Mesh),length(Mesh)); 
  if strcmp(CF,'Exp')==1 
    for i=1:length(Mesh)
      for j=1:length(Mesh) 
        Cor_M(i,j)=c1+(1-c1)*exp(-abs((Mesh(i)-Mesh(j)))/lc); 
      end
    end
  elseif strcmp(CF,'SExp')==1 
    for i=1:length(Mesh)
      for j=1:length(Mesh)
       Cor_M(i,j)=c1+(1-c1)*exp(-((abs(Mesh(i)-Mesh(j)))/lc)^2); 
       end
    end
  else disp('CorF must be equal to Exp or SExp') 
 end
elseif Dim==2 %Determine Correlation matrix
   Cor_M=zeros(length(Mesh),length(Mesh)); 
    if strcmp(CF,'Exp')==1 
       for i=1:length(Mesh)
          for j=1:length(Mesh)
           Cor_M(i,j)=c1+(1-c1)*exp(-(sqrt((Mesh(i,1)-Mesh(j,1))^2 ... 
            +(Mesh(i,2)-Mesh(j,2))^2))/lc);
          end
       end
   elseif strcmp(CF,'SExp')==1 
       for i=1:length(Mesh)
           for j=1:length(Mesh)
        Cor_M(i,j)=c1+(1-c1)*exp(-((sqrt((Mesh(i,1)-Mesh(j,1))^2 ... 
        +(Mesh(i,2)-Mesh(j,2))^2))/lc)^2);
           end
       end
    else disp('CorF must be equal to Exp or SExp') 
    end
elseif Dim==3
    disp('not programmed') 
end

if strcmp(distribution,'lognormal')==1 
        std_norm=sqrt(log(1+(std/mean)^2));
        mean_norm=log(mean)-0.5*std_norm^2; 
        Cor_M=(exp(Cor_M*std_norm^2)-1)/(exp(std_norm^2)-1); 
end

end
