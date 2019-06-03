% % 
 function g = gfun_uni(fc, fsy, fsu, esu,As1,As2,As3, R, Q)

  Resis      =load_resistance(fc,fsy,fsu,esu,As1,As2,As3,R,P);
%  
  g       = Resis - Q;
% 
% 
% function g = gfun_uni(Rr,Q)
% 
% P      =load_resistance(Rr);
% 
% g       = P - Q;
% 
