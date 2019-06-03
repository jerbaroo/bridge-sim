% Ultimate strain of rebar with pitting corrosion - Linear model
% can be used for other properties as well which vary linearly with
% corrosion
%
%SYNOPSYS
% epsu = EPSU_CORR_L(epsu0, epsy, delta_s, alpha_su)
%
%INPUT
% epsu0     ultimate strain of uncorroded (sound) rebar /numeric, 1x1/
% epsy0     yield strain of uncorroded (sound) rebar /numeric, 1x1/
%
%OUTPUT
% epsu      ultimate strain reduced due to corrosion
% 
%NOTES
% delta_s = A_s_lost/A_s_0
%
%REFERENCES
% [1] 

%TODO
% * preserve the input format

function epsu = epsu_corr_L(epsu0, epsy, delta_s, alpha_su)

% -------------------------------------------------------------------------
% PRE-PROCESSING
% -------------------------------------------------------------------------
if nargin < 3
    alpha_su = 3.7;
end

delta_s     = delta_s(:);

% not general!
epsu0       = epsu0*ones(size(delta_s));
epsy        = epsy*ones(size(delta_s));

% -------------------------------------------------------------------------
% MODEL
% -------------------------------------------------------------------------

% [1]Eq.
epsu        = epsu0.*(1 - alpha_su.*delta_s);
% enforce physics
epsu(epsu<0)= epsy(1);


end