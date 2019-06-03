%% Midpoint method with correlated random variables for a bar in 1D 
% modified from code by Robin van der Have
function [data,Cor_M]=MP_Discre(A,A_std,CF,cl,lc,distribution)

global NE
global LL
%% Input model

% Input model parameters 
% start timer

data=zeros(1,3);%transfer data to main_reli
data(1,1)=NE;
data(1,2)=A;
data(1,3)=A_std;

% Dependend model parameters 
NN=2*NE+1;% number of nodes
xx=linspace(0,LL,NN);% X-coordinates

NC=[1:NN;xx]';% Nodal coordinates (Node number, Nodal coordinate)

% Matrix for Endnode coordinates (Node number, Nodal coordinate)
ENC=zeros(NE+1,2);

for i=1:NE+1
  for j=1:2
    ENC(i,j)=NC(2*i-1,j);  
  end
end
MNC=zeros(NE,2);

% Matrix for midnode coordinates (Node number, Nodal coordinate)
for i=1:NE
  for j=1:2
   MNC(i,j)=NC(i*2,j); 
  end
end


%% Random field
% Input random field 
Dim=1; % Model/RF dimension
mean=A;% Mean RF
std=A_std;% Standard deviation RF 


% Random field mesh (midpoint method) 
Mesh=MNC(:,2); 

% Generate correlation matrix
    Cor_M=CovDec_Cor(Dim,mean,std,CF,cl,lc,Mesh,distribution); 
 

