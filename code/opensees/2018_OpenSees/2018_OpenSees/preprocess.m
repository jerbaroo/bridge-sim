function FEM = preprocess(Input)

Geom            = Input.Geom;
Concrete_gen    = Input.Concrete_gen;
Rebar_gen       = Input.Rebar_gen;
Rebar_layout    = Input.Geom.Rebar_layout;

L_span          = Geom.L_span;
l_elem          = Geom.l_elem;

L_tot           = sum(L_span);
n_node          = L_tot/l_elem + 1;
n_elem          = n_node - 1;

node_nr         = 1:n_node;
node_coord(:,1) = -L_tot/2:l_elem:L_tot/2;
node_coord(:,2) = 0;

% -------------------------------------------------------------------------
% Generate cross-sections
% -------------------------------------------------------------------------
web_fun         = @(x) interp1(Geom.web_x, Geom.web_w, x);
n_rl            = length(Input.Geom.Rebar_layout);

% initialize
Concrete(n_node-1)  = Concrete_gen;

Rebar_gen.n_s       = [];
Rebar_gen.D_s       = [];
Rebar_gen.d_s       = [];
Rebar(n_node-1)     = Rebar_gen;

for ii = 1:n_node-1
    Concrete(ii)    = Concrete_gen;
    Rebar(ii)       = Rebar_gen;
    
    x_ii1           = node_coord(ii,1);
    x_ii2           = node_coord(ii+1,1);
    x_iic           = mean([x_ii1, x_ii2]);
    
    w               = web_fun(x_iic);
    Concrete(ii).t2 = w;
    
    for jj = 1:n_rl
        L_rl_jj1    = Rebar_layout(jj).L(1);
        L_rl_jj2    = Rebar_layout(jj).L(2);
        n_s_jj      = Rebar_layout(jj).n_s;
        D_s_jj      = Rebar_layout(jj).D_s;
        d_s_jj      = Rebar_layout(jj).d_s;
        
        if x_iic > L_rl_jj1 && x_iic <= L_rl_jj2
            Rebar(ii).n_s   = [Rebar(ii).n_s, n_s_jj];
            Rebar(ii).D_s   = [Rebar(ii).D_s, D_s_jj];
            Rebar(ii).d_s   = [Rebar(ii).d_s, d_s_jj];
        end
    end
end

% -------------------------------------------------------------------------
% Collect variables
% -------------------------------------------------------------------------

FEM.Concrete    = Concrete;
FEM.Rebar       = Rebar;
FEM.node_nr     = node_nr;
FEM.node_coord  = node_coord;

end