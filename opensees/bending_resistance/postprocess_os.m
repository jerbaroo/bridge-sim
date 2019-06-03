% Postprocess the OpenSees analysis results
%
%SYNAPSYS
% R = POSTPROCESS_OS(job_dir)
%
%INPUT
% x         vector of input values (a single value for each!)
%
%OUTPUT
% R         results (potentially a vector)
%
%NOTE:
% The function name and argument structure should be kept!

function R = postprocess_os(job_dir)

        fpath = fullfile(job_dir, 'section1.out');
        Out = dlmread(fpath);
        M   = max(Out(:,1));
        R   = M;
end