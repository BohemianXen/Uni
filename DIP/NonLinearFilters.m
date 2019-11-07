classdef NonLinearFilters
    methods(Static)
        
        function output_val = median(values, center_index)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(center_index);         
        end
        
        function output_val = weighted_median(values, center_index, weights)
            sorted = MyStatistics.qsort(values);
            sorted = repelem(sorted, weights);
            output_val = sorted(center_index);         
        end
        
        function output_val = os(values, position)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(position);
        end
    end
end 