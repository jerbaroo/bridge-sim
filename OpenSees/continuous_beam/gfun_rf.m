
function g = gfun_rf(Rr,Q,fsy, fsu, esu)

P      =load_resistance_basic(Rr,fsy, fsu, esu);

g       = P - Q;

end