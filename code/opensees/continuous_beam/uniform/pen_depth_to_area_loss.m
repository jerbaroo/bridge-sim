% Rebar area loss from penetration depth (both normalized!)
%
%SYNOPSYS
% delta_s = PEN_DEPTH_TO_AREA_LOSS(delta)
%
%INPUT
% delta     = p/D0
%  where p = x_max the maximum penetration depth
%        D0 is the uncorroded diamater of the rebar
%
%OUTPUT
% delta_s   = A_s_lost/A_s_0
%
%NOTES
% * for pitting corrosion: p = x_max (maximum penetration depth)
%
%REFERENCES
% [1] Biondini, F., & Vergani, M. (2012). Damage modeling and nonlinear analysis of concrete bridges under corrosion Bridge Maintenance, Safety, Management, Resilience and Sustainability (pp. 949-957): CRC Press.

function delta_s = pen_depth_to_area_loss(delta)
    % input check
    if any(delta < 0 | delta > 1)
       error('delta must be between 0 and 1 (inclusive)!') 
    end
    
    % [1]Eq.(8)
    beta            = 2*delta.*sqrt(1 - delta.^2);
    % [1]Eq.(9)
    theta1          = 2*asin(beta);
    % [1]Eq.(10)
    idx1            = beta == 0 & delta == 0;
    idx2            = ~idx1;
    theta2          = nan(size(delta));
    theta2(idx1)    = 0;
    theta2(idx2)    = 2*asin(beta(idx2)./(2*delta(idx2)));
    % [1]Eq.(6)
    delta_s1        = 1/(2*pi)*(theta1 - 2*beta.*abs(1 - 2*delta.^2));
    % [1]Eq.(7)
    delta_s2        = 2*delta.^2/pi.*(theta2 - beta);
    % [1]Eq.(5)
    idx1            = delta <= 1/sqrt(2);
    idx2            = ~idx1;
    delta_s         = nan(size(delta));
    delta_s(idx1)   = delta_s1(idx1) + delta_s2(idx1);
    delta_s(idx2)   = 1 - delta_s1(idx2) + delta_s2(idx2);
    
end