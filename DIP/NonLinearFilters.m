classdef NonLinearFilters
    % linear filter algorithm(s)
    
    methods(Static)
        function [output_val, sorted] = median(values, center_index, fast_sort_on, new_vals, old_vals, old_median, old_list)
            % returns the median within a window
            
            % use the faster partial sort if requested
            if (fast_sort_on)
                sorted = MyStatistics.qsort_plus(new_vals, old_vals, old_median, old_list);
            else 
                sorted = MyStatistics.qsort(values);
                
            end
             output_val = sorted(center_index);
        end
        
        function [output_val, sorted] = weighted(values, center_index, weights, fast_sort_on, new_vals, old_vals,old_median, old_list)
            % returns the median within the window after applying replication weights
            if (fast_sort_on)
                sorted = MyStatistics.qsort_plus(new_vals, old_vals, old_median, old_list);
            else 
                sorted = MyStatistics.qsort(values);
            end
            weighted = repelem(sorted, weights); % repeats each element in sorted window by corresponding weights
            output_val = weighted(center_index);         
        end
        
        function output_val = adaptive_weighted(window, distances, w, c)
            % implementation of adaptive weighted median algo from notes
            
            mean = mean2(window);
            std_dev = std2(window);        
            weights = ones(size(window));
            weights = weights .* w; % set all weights to central weights first
           
            % apply algo only if window has variation
            if (mean ~= 0 || std_dev ~= 0)               
                k = std_dev/mean;
                weights = ceil(weights - (distances * c * k));
                weights(weights<0) = 0; % round negative weights up to 0
                
                % apply weights to window, sort, and return median value
                sorted = repelem(window(:), weights(:)); 
                sorted = MyStatistics.qsort(sorted);
                center_index = ceil(sum(weights(:))/2);
                output_val = sorted(center_index);
            else
                window = window(:);
                output_val = window(ceil(length(window/2)));
            end 
        end
    end
end 