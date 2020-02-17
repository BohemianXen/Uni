classdef NonLinearFilters
    % nonlinear filter algorithms
    
    methods(Static)
        function [output_val, sorted] = median(values, center_index, fast_sort_on, new_vals, old_vals, old_median, old_list)
            % returns the median within a window
            
            % use the faster partial sort if requested
            if (fast_sort_on)
                sorted = MyStatistics.qsort_plus(new_vals, old_vals, old_median, old_list);...
            else 
                sorted = MyStatistics.qsort(values);
                
            end
             output_val = sorted(center_index);
        end
        
        function [output_val, sorted] = weighted(values, weights)
            % returns the median within the window after applying replication weights
          
            weighted = repelem(values, weights); % repeats each element in window by corresponding weights
            sorted = MyStatistics.qsort(weighted);
            output_val = sorted(ceil(sum(weights)/2));         
        end
        
        function output_val = adaptive_weighted(window, distances, w, c)
            % implementation of adaptive weighted median algo from notes
            
            mean = mean2(window);
            std_dev = std2(window);        
            weights = ones(size(window));
           
            % apply algo only if window has variation
            if (mean ~= 0 || std_dev ~= 0)               
                k = std_dev/mean;
                weights = weights .* w; % set all weights to central weights first
                weights = ceil(weights - (distances * c * k));
                weights(weights<0) = 0; % round negative weights up to 0
                
                % apply weights to window, sort, and return median value
                weighted = repelem(window(:), weights(:)); 
                sorted = MyStatistics.qsort(weighted);
                output_val = sorted( ceil(sum(weights(:))/2));
            else
                window = window(:);
                output_val = window(ceil(length(window/2))); % central pixel
            end 
        end
    end
end 