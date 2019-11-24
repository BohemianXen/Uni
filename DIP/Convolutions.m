classdef Convolutions
    properties(SetAccess = protected)
        image
    end
    properties(SetAccess = public)
        kernel
        krnl_h
        krnl_w
        krnl_c
        order_weights
        fast_sort
    end

    methods
%--------------------------------------------------------------------------
        function self = Convolutions(filename, kernel, fast_sort)
            self.image = im2double(imread(filename));
            self.kernel = kernel;
            self.order_weights = ones(1, self.krnl_h * self.krnl_w);
            self.fast_sort = fast_sort;
        end
        
%--------------------------------------------------------------------------
        function img = get.image(self)
            img = self.image;
        end
        
        function krn = get.kernel(self)
            krn = self.kernel;
        end
        
        function self = set.kernel(self, new_kernel)
            self.kernel = new_kernel;
            [self.krnl_h, self.krnl_w] = size(new_kernel);
            self.krnl_c = [ceil(self.krnl_h/2), ceil(self.krnl_w/2)];
        end
        
        function weights = get.order_weights(self)
            weights = self.order_weights;   
        end
        
        function self = set.order_weights(self, weights)
            if self.krnl_h * self.krnl_w == length(weights)
                self.order_weights = weights;
            else
                disp('New weights are of differing size to the kernel')
            end
        end
        
        function fast_sort = get.fast_sort(self)
            fast_sort = self.fast_sort;
        end
        
        function self = set.fast_sort(self, fast_sort)
            self.fast_sort = fast_sort;
        end
        
%--------------------------------------------------------------------------
        % Adaptive Conv.
        function filtered_image = adaptive_compute(self, type)
           % returns a convolved greyscale self.image

            % calculate max (+/-) kernal overlap about desired pixel  
            offset_h = floor(self.krnl_h/2);
            offset_w = floor(self.krnl_w/2);
            krnl_c_vector = ceil((self.krnl_h * self.krnl_w)/2);                

            % pad input self.image array by replicating borders as per the offsets
            img = padarray(self.image,[offset_h, offset_w], 'replicate');
            [img_h, img_w] = size(img);
            filtered_image_prime = zeros(img_h, img_w);
            
            distances_complete = ~strcmp(type, 'adaptive weighted median');
            old_window = zeros(self.krnl_h, self.krnl_w);
            new_vals = zeros(1, self.krnl_h);
            old_vals = new_vals;
            output_val = 0;
           
            for row=offset_h+1:img_h-offset_h
                 fast_sort_on = 0;
                 sorted_vals = zeros(1, self.krnl_h * self.krnl_w);
                for col=offset_w+1:img_w-offset_w  
                    % find index of first element as per the kernal overlap (accounting
                    % for non-zero indexing)
                    start_row = row - offset_h - 1; 
                    start_col = col - offset_w - 1;
                    
                    window = img(start_row+1:start_row+self.krnl_h,...
                                         start_col+1:start_col+self.krnl_w);
                    if (self.fast_sort)
                        new_vals = window(:, self.krnl_w);
                        old_vals = old_window(:, 1);
                        old_window = window;
                    end
                           
                    if (~distances_complete)
                        distances = zeros(self.krnl_h, self.krnl_w);
                        for k_row=1:self.krnl_h
                            for k_col=1:self.krnl_w
                                distances(k_row, k_col) = sqrt((self.krnl_c(1) - k_row)^2 + (self.krnl_c(2) - k_col)^2);
                            end
                        end
                        distances_complete = 1;
                    end
      
                    switch(type)
                         % populate current pixel with new value
                        case 'mean'
                            output_val = sum(window .* self.kernel, 'all');
                        case 'unsharp'
                            output_val = LinearFilters.unsharp(window, self.krnl_c, -1);
                        case 'median'
                            [output_val, sorted_vals] = NonLinearFilters.median(window(:), krnl_c_vector, fast_sort_on, new_vals, old_vals, output_val, sorted_vals);
                        case 'weighted median'
                            [output_val, sorted_vals] = NonLinearFilters.weighted(window(:), krnl_c_vector, self.order_weights, fast_sort_on, new_vals, old_vals, output_val, sorted_vals);
                        case 'adaptive weighted median'
                            output_val = NonLinearFilters.adaptive_weighted(window, distances, 10, 0.5);
%                         case 'order statistics'
%                             output_val = NonLinearFilters.os(window(:), krnl_c_vector);
                    end
                    filtered_image_prime(row, col) = output_val;
                    if (self.fast_sort)
                        fast_sort_on = 1;
                    end
                end                 
            end

            % extract img within the zero pad
            filtered_image = filtered_image_prime(1+offset_h:img_h-offset_h, 1+offset_w:img_w-offset_w);
        end
        
%--------------------------------------------------------------------------   
        % FFT Conv.  
        function filtered_image = fft_compute(self)
            % returns a convolved greyscale image

            self.kernel = flip(self.kernel); % flip kernel ahead of fft2 convolve
            [self.krnl_h, self.krnl_w] = size(self.kernel);
            offset_h = floor(self.krnl_h/2);
            offset_w = floor(self.krnl_w/2);


            % pad input image array by replicating borders as per the offsets
            img = padarray(self.image,[offset_h, offset_w], 'replicate');
            [img_h, img_w] = size(img);

            % convolve using fft2 and return to spacial domain using ifft2
            filtered_image_prime = ifft2(fft2(img) .* fft2(self.kernel,img_h,img_w));

            % extract image data, ignoring pre-padding done by fft2
            filtered_image = filtered_image_prime(self.krnl_h:img_h,self.krnl_w:img_w);
        end
    end
end

