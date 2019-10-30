classdef NonLinearFilters
    methods(Static)
        
        function output_val = median(values, center_index)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(center_index);         
        end
    end
end 