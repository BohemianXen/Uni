classdef NonLinearFilters
    methods(Static)
        
        function [output_val, sorted] = median(values, center_index, fast_sort_on, new_vals, old_vals,old_median, old_list)
            if (fast_sort_on)
                sorted = MyStatistics.qsort_plus(new_vals, old_vals, old_median, old_list);
            else 
                sorted = MyStatistics.qsort(values);
                
            end
             output_val = sorted(center_index); 
        end
        
        function [output_val, sorted] = weighted(values, center_index, weights, fast_sort_on, new_vals, old_vals,old_median, old_list)
            if (fast_sort_on)
                sorted = MyStatistics.qsort_plus(new_vals, old_vals, old_median, old_list);
            else 
                sorted = MyStatistics.qsort(values);
            end
            weighted = repelem(sorted, weights);
            output_val = weighted(center_index);         
        end
        
        function output_val = adaptive_weighted(window, distances, w, c)
            mean = mean2(window);
            std_dev = std2(window);        
            weights = ones(size(window));
            weights = weights .* w;
            if (mean ~= 0)               
                k = std_dev/mean;
                weights = ceil(weights - (distances * c * k));
                weights(weights<0) = 0;
            end
            
            sorted = repelem(window(:), weights(:));
            sorted = MyStatistics.qsort(sorted);
            center_index = ceil(sum(weights(:))/2);
            output_val = sorted(center_index);         
        end
        
        function output_val = os(values, position)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(position);
        end
    end
end 