classdef Convolutions
    properties(SetAccess = protected)
        image
    end
    properties(SetAccess = public)
        kernel
        krnl_h
        krnl_w
    end
    methods
        function self = Convolutions(image, kernel)
            self.image = image; 
            self.kernel = kernel;
            [self.krnl_h, self.krnl_w] = size(self.kernel);
        end
        
        function img = get.image(self)
            img = self.image;
        end
        
        function filtered_image = adaptive_compute(self, type)
           % returns a convolved greyscale self.image

            

            % calculate max (+/-) kernal overlap about desired pixel  
            offset_h = floor(self.krnl_h/2);
            offset_w = floor(self.krnl_w/2);

            % pad input self.image array by replicating borders as per the offsets
            self.image = padarray(self.image,[offset_h, offset_w], 'replicate');
            [img_h, img_w] = size(self.image);
            filtered_image_prime = zeros(img_h, img_w);

            for row=offset_h+1:img_h-offset_h
                for col=offset_w+1:img_w-offset_w  
                    window = ones(self.krnl_h, self.krnl_w);
                    sum = 0;

                    % find index of first element as per the kernal overlap (accounting
                    % for non-zero indexing)
                    start_row = row - offset_h - 1; 
                    start_col = col - offset_w - 1;

                    for k_row=1:self.krnl_h
                        for k_col=1:self.krnl_w
                            % find index of current comparison pixel as offset from the
                            % central pixel then convolve current comparison pixel
                            compare_index_h = start_row + k_row;
                            compare_index_w = start_col + k_col;                        
                            window(k_row, k_col) = self.image(compare_index_h, compare_index_w);
                            sum = sum + self.image(compare_index_h, compare_index_w) * self.kernel(k_row, k_col);
                            
                        end
                    end
                    
                    switch(type)
                        case 'adaptive linear'
                            filtered_image_prime(row, col) = LinearFilters.adaptive(window, [self.krnl_h, self.krnl_w], -1); % populate current pixel with new value
                        case 'mean'
                            filtered_image_prime(row, col) = LinearFilters.adaptive(window, [self.krnl_h, self.krnl_w], 0);
                        case 'box'
                            filtered_image_prime(row, col) = sum;
                    end
                end                 
            end

            % extract self.image within the zero pad
            filtered_image = filtered_image_prime(1+offset_h:img_h-offset_h, 1+offset_w:img_w-offset_w);
        end
        
        function filtered_image = fft_compute(self)
            % returns a convolved greyscale image

            self.kernel = flip(self.kernel); % flip kernel ahead of fft2 convolve
            [self.krnl_h, self.krnl_w] = size(self.kernel);
            offset_h = floor(self.krnl_h/2);
            offset_w = floor(self.krnl_w/2);


            % pad input image array by replicating borders as per the offsets
            padded_img = padarray(self.image,[offset_h, offset_w], 'replicate');
            [img_h, img_w] = size(padded_img);

            % convolve using fft2 and return to spacial domain using ifft2
            filtered_image_prime = ifft2(fft2(padded_img) .* fft2(self.kernel,img_h,img_w));

            % extract image data, ignoring pre-padding done by fft2
            filtered_image = filtered_image_prime(self.krnl_h:img_h,self.krnl_w:img_w);
        end
    end
end

