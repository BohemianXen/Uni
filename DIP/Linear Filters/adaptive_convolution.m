function filtered_image = adaptive_convolution(image, kernel)
% returns a convolved greyscale image

[krnl_h, krnl_w] = size(kernel);

% calculate max (+/-) kernal overlap about desired pixel  
offset_h = floor(krnl_h/2);
offset_w = floor(krnl_w/2);

% pad input image array by replicating borders as per the offsets
image = padarray(image,[offset_h, offset_w], 'replicate');
[img_h, img_w] = size(image);
filtered_image_prime = zeros(img_h, img_w);

for row=offset_h+1:img_h-offset_h
    for col=offset_w+1:img_w-offset_w  
        window = ones(krnl_h, krnl_w);

        % find index of first element as per the kernal overlap (accounting
        % for non-zero indexing)
        start_row = row - offset_h - 1; 
        start_col = col - offset_w - 1;

        for k_row=1:krnl_h
            for k_col=1:krnl_w
                % find index of current comparison pixel as offset from the
                % central pixel then convolve current comparison pixel
                compare_index_h = start_row + k_row;
                compare_index_w = start_col + k_col;                        
                window(k_row, k_col) = image(compare_index_h, compare_index_w);               
            end
        end
        filtered_image_prime(row, col) = ...
            adaptive_linear(window, [krnl_h, krnl_w], -1); % populate current pixel with new value
    end                 
end

% extract image within the zero pad
filtered_image = filtered_image_prime(1+offset_h:img_h-offset_h, 1+offset_w:img_w-offset_w);

end

