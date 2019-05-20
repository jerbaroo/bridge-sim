function Input = update_Input(Input)

Geom            = Input.Geom;
Concrete_gen    = Input.Concrete_gen;
Rebar_gen       = Input.Rebar_gen;
Rebar_layout    = Input.Geom.Rebar_layout;

l_elem          = Geom.l_elem;
% check the "mesh"
L_span                  = Geom.L_span;
for ii = 1:3
    if mod(L_span(ii), l_elem) ~= 0
        error('Please provide an element length that is a divider of each span length') ;
    end
end


end