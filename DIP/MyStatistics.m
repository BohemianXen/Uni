classdef MyStatistics
    methods(Static)
        function [diff, diff_image] = ssd(img1, img2)
            diff = sum((img1(:) - img2(:)) .^ 2);
            diff_image = 0.5 + 10 * (img1 - img2);
        end
        function sorted = qsort(vector)
            vector_length = length(vector);
            if (vector_length > 1)
                pivot = vector(ceil(vector_length/2));
                split = 1;
                duplicates = 0;
                for i=1:vector_length
                    if (vector(i) < pivot)
                        [vector(split), vector(i)] = deal(vector(i), vector(split));
                        split = split + 1;
                    elseif (vector(i) == pivot)
                        duplicates = duplicates + 1;
                    else
                        continue
                    end
                end

                low = MyStatistics.qsort(vector(vector < pivot));
                high = MyStatistics.qsort(vector(vector > pivot));
                sorted = [low repelem(pivot, duplicates) high];
            else
                sorted = vector;
            end
        end
        
        function sorted = qsort_plus(new_vals, old_vals, old_median, old_list)
            col_size = size(old_list, 2);
            inserted = 1;
            for i=1:size(old_vals)
               for j=1:col_size
                   if (old_vals(i) == old_list(j))
                       old_list(j) = [];
%                        col_size = col_size - 1;
                       if (new_vals(inserted) <= old_median)
                           old_list = [new_vals(inserted) old_list];
                       else
                           old_list(col_size) = new_vals(inserted);
                       end
                       inserted = inserted + 1;
                       break
                   end
               end
            end
            
            sorted = MyStatistics.qsort(old_list);
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