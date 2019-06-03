function [R_up, delta_tot] = massage_corr_mx(R)

[V, D] = eig(R);
d = diag(D);

idx = d < 0;
if any(idx)
    if min(d) > -1e-3
        d_up = d;
        d_up(idx) = 1e-6;
        D_up = eye(size(R));
        D_up(logical(eye(size(R)))) = d_up;
        R_up = V*D_up*V^-1;
        delta_tot = R - R_up;
    else
        error('The absolute largest negative eigenvalue is too large')
    end
else
    R_up = R;
    delta_tot = zeros(size(R));
end

end