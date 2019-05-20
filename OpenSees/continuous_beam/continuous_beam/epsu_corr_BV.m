% Ultimate strain of rebar with pitting corrosion - model of Biondini & Vergani
% in terms of delta_s - ratio of corrosion loss!!!
%
%SYNOPSYS
% epsu = EPSU_CORR_BV(epsu0, delta_s, model)
%
%INPUT
% epsu      ultimate strain of uncorroded (sound) rebar /numeric, can be
%           vector, nx1/
% delta_s   ratio of corrosion loss in terms of uncorroded rebar
%           cross-sectional area; = A_s_lost/A_s_0
% model     corrosion model to be applied /string/
%
%OUTPUT
% epsu      ultimate strain reduced due to corrosion
% 
%NOTES
%
%
%REFERENCES
% [1] Biondini, F., & Vergani, M. (2012). Damage modeling and nonlinear analysis of concrete bridges under corrosion Bridge Maintenance, Safety, Management, Resilience and Sustainability (pp. 949-957): CRC Press.

%TODO
% * preserve the input format

function epsu = epsu_corr_BV(epsu0, delta_s, model)

% -------------------------------------------------------------------------
% PRE-PROCESSING
% -------------------------------------------------------------------------
epsu0       = epsu0(:);
delta_s     = delta_s(:);

n_epsu0     = length(epsu0);
n_delta_s   = length(delta_s);

if n_epsu0 == 1 && n_delta_s > 1
    epsu0 = epsu0*ones(size(delta_s));
elseif n_delta_s == 1 && n_epsu0 > 1
    delta_s = delta_s*ones(size(n_epsu0));
elseif n_delta_s ~= n_epsu0
    error('Dimensions of epsu0 and delta mismatch! They should have the same size or only one of them should be a single scalar number!')
end

% -------------------------------------------------------------------------
% MODELS
% -------------------------------------------------------------------------

switch lower(model)
    case 'pitting' % [1]Figure 1. (b)
        % 
    case 'uniform'
        % also given in [1], Figure 1. (a)
    case {'pitting and uniform', 'pu'}
        % also given in [1], Figure 1. (c)
    otherwise
        error(['Unknown model:', model])
end

% [1]Eq.(11)
idx1        = delta_s < 0.016;
idx2        = ~idx1;

epsu        = nan(size(delta_s));
epsu(idx1)  = epsu0(idx1);
epsu(idx2)  = 0.1521*delta_s(idx2).^(-0.4583).*epsu0(idx2);

end