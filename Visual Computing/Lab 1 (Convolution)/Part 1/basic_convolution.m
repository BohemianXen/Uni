function filtered_image = basic_convolution(image, kernel)
% returns a convolved greyscale image

% store image and kernel dimensions and create template for new image 
[img_h, img_w] = size(image); 
[krnl_h, krnl_w] = size(kernel);
filtered_image = zeros(img_h, img_w);

% calculate max (+/-) kernal overlap about desired pixel  
offset_h = floor(krnl_h/2);
offset_w = floor(krnl_w/2);

for row=offset_h+1:img_h-offset_h
    for col=offset_w+1:img_w-offset_w  
        sum = 0;
        
        % find index of first element as per the kernal overlap (accounting
        % for non-zero indexing)
        start_row = row - offset_h - 1; 
        start_col = col - offset_w - 1;
        
        for k_row=1:krnl_h
            for k_col=1:krnl_w
                % find index of current comparison pixel as offset from the
                % central pixel
                compare_index_h = start_row+k_row;
                compare_index_w = start_col+k_col;
                
                % confirm that the current comparison index is within the
                % image dimensions then multiply the pixel value with its
                % corresponding kernal value 
                if (compare_index_h <= 0) || (compare_index_w <= 0)
                    continue 
                           
                else %(compare_index_h <= img_h-offset_h) && (compare_index_w <= img_w-offset_w)                 
                    sum = sum + image(compare_index_h, compare_index_w) * kernel(k_row, k_col);
                end
            end
        end

        filtered_image(row, col) = sum; % populate current pixel with new value             
    end
end
 
end

