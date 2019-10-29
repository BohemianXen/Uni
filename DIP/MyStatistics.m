classdef MyStatistics
    methods(Static)
        function val = avg(window)
            val = mean(window); %sum(window(:))/(dimensions(1)*dimensions(2));       
        end
        
        function [sorted] = sort(vector, pivot_index)
            pivot = vector(pivot_index);   
        end
        
        function [kernel] = gaussian_filter(sigma)
        %creates a size x size sized gaussain kernel (with sd of value sigma) along
        %with the sum of all the elements 

        size = 2 * ceil(3*sigma) + 1;
        kernel = zeros(size, size);
        variance = sigma^2;

        %offsets from center of image
        center = floor(size/2);

        %gaussian equation in 2D - TODO: Only generate one quadrant and replicate
        for row=-center:center
            for col=-center:center
                val = (1/(2*pi*variance))*exp(-(col^2 + row^2)/(2*variance));
                kernel(row+center+1, col+center+1) = val;
            end
        end

        kernel = kernel/sum(kernel(:)); %normalise
        end
    end
end 