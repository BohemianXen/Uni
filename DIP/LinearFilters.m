classdef LinearFilters
    methods(Static)
        
        function output_val = adaptive(window, dimensions, k)
            center_val = window(ceil(dimensions(1)/2), ceil(dimensions(2)/2));
            std_dev = std2(window); %TODO: write own stats methods
            mean = MyStatistics.avg(window, dimensions);
            snr = mean/std_dev;

            if (k < 0 || k > 1 )
                k = 1 / snr;
            %     disp(k)
            end
            output_val = mean + (k*(center_val-mean));
        end
    end
end 