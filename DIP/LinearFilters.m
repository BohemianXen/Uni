classdef LinearFilters
    % linear filter algorithm(s)
    
    methods(Static)
        function output_val = unsharp(window, center_index, k)
            % unsharp masking filter; adaptive if k arg does not conform to 0 < k < 1
            
            mean = mean2(window);
            output_val = mean; % will output mean if all values within window are the same
            std_dev = std2(window);           
            
            if (std_dev ~= 0 && k ~= 0)
                 snr = mean/std_dev;
                if (k < 0 || k > 1 )
                    k = 1 / snr; % k inversely proportional to signal to noise ratio
                end
                center_val = window(center_index(1), center_index(2));
                output_val = output_val + (k*(center_val-mean));
            end
        end
        
    end
end 