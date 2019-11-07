classdef LinearFilters
    methods(Static)
        
        function output_val = adaptive(window, center_index, k)
            mean = mean2(window);
            output_val = mean;
            std_dev = std2(window); %TODO: write own stats methods           
            
            if (std_dev ~= 0 && k ~= 0)
                 snr = mean/std_dev;
                if (k < 0 || k > 1 )
                    k = 1 / snr;
                end
                center_val = window(center_index(1), center_index(2));
                output_val = output_val + (k*(center_val-mean));
            end
        end
    end
end 