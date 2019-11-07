classdef NonLinearFilters
    methods(Static)
        
        function output_val = median(values, center_index)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(center_index);         
        end
        
        function output_val = weighted(values, center_index, weights)
            sorted = MyStatistics.qsort(values);
            sorted = repelem(sorted, weights);
            output_val = sorted(center_index);         
        end
        
        function output_val = adaptive_weighted(window, distances, w, c)
            mean = mean2(window);
%             output_val = mean;
            std_dev = std2(window); %TODO: write own stats methods           
%             distances = MyStatistics.distances(size(window));
            weights = ones(size(window));
            weights = weights .* w;
            if (mean ~= 0)               
                k = std_dev/mean;
                temp = distances * c * k;
                weights = ceil(weights - temp);
            end
            poop = repelem(window(:), weights(:));
            sorted = MyStatistics.qsort(poop);
            center_index = ceil(sum(weights(:))/2);
            output_val = sorted(center_index);         
        end
        
        function output_val = os(values, position)
            sorted = MyStatistics.qsort(values);
            output_val = sorted(position);
        end
    end
end 