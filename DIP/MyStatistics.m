classdef MyStatistics
    % general mathematical functions
    
    methods(Static)
        function [diff, diff_image] = ssd(img1, img2)
            % return the sum of the squares differences of two images as well 
            % as an image depicting this so the differing locations can be assessed 
            diff = sum((img1(:) - img2(:)) .^ 2);
            diff_image = 0.5 + 10 * (img1 - img2);
        end
        
        function sorted = qsort(vector)
            % quick sort algo based on a single central pivot
            vector_length = length(vector);
            
            if (vector_length > 1)
                pivot = vector(ceil(vector_length/2)); % pivot on center index
                split = 1; % index of split point
                duplicates = 0; % number of times pivot value occurs in the vector
                
                for i=1:vector_length
                    if (vector(i) < pivot)
                        % swap split and current and index if current value is less
                        % than the pivot
                        [vector(split), vector(i)] = deal(vector(i), vector(split));
                        split = split + 1;
                    elseif (vector(i) == pivot)
                        duplicates = duplicates + 1; % increment duplicates counter
                    else
                        continue
                    end
                end
                
                % recursively sort the low and high sub-vectors then
                % recombine to create a sorted vector
                low = MyStatistics.qsort(vector(vector < pivot));
                high = MyStatistics.qsort(vector(vector > pivot));
                sorted = [low repelem(pivot, duplicates) high];
            else
                sorted = vector; % no sorting needed
            end
        end
        
        function sorted = qsort_plus(new_vals, old_vals, old_median, old_list)
            % function for minimising sorting needed if outgoing and
            % incoming window values are known
            
            col_size = length(old_list); % number of old/new values
            inserted = 1; % number of values processed
            
            for i=1:length(old_vals)
               for j=1:col_size
                   if (old_vals(i) == old_list(j))
                       old_list(j) = []; % remove old values from sorted list

                       % place the new value at the start or end of the sorted list 
                       % depending on whether or not it exceeds the median
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
            
            sorted = MyStatistics.qsort(old_list); % sort the new array
        end
        
        function [kernel] = gaussian_filter(sigma)
        % creates a gaussian array based on std deviation sigma

        size = 2 * ceil(3*sigma) + 1; % calculate kernel size based on sigma
        kernel = zeros(size, size);
        variance = sigma^2;

        % offsets from center of image
        center = floor(size/2);

        % gaussian equation in 2D
        for row=-center:center
            for col=-center:center
                val = (1/(2*pi*variance))*exp(-(col^2 + row^2)/(2*variance));
                kernel(row+center+1, col+center+1) = val;
            end
        end

        kernel = kernel/sum(kernel(:)); % normalise
        end
    end
end 