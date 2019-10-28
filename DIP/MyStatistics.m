classdef MyStatistics
    methods(Static)
        function mean = avg(window, dimensions)
            mean = sum(window(:))/(dimensions(1)*dimensions(2));       
        end
    end
end 