function filtered_image = fft_convolution(image, kernel)
% returns a convolved greyscale image

[krnl_h, krnl_w] = size(kernel);

% calculate max (+/-) kernal overlap about desired pixel  
offset_h = floor(krnl_h/2);
offset_w = floor(krnl_w/2);

% pad input image array by replicating borders as per the offsets
image = padarray(image,[offset_h, offset_w], 'replicate');
[img_h, img_w] = size(image);

[img_h, img_w] = size(image);
filtered_image_prime = zeros(img_h, img_w);

col_block_size = 4; col_step = col_block_size/2;
temp = zeros(1, col_block_size);
temp(1:3) = kernel;

for row=1+offset_h:img_h-offset_h
    for col=1+offset_w:col_step:img_w-col_step
        try
            block = image(row,(col-offset_w):(col-offset_w)+(col_block_size-1));
        catch
            disp('uh oh')
        end
        filtered_image_prime(row, col:col+col_block_size-1) = ifft2(fft2(block) .* fft2(temp)); % populate current pixel with new value
    end  
end

% extract image within the zero pad
filtered_image = filtered_image_prime(offset_h+1:img_h-offset_h, offset_w+1:img_w-offset_w);

end

