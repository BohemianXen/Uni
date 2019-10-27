function filtered_image = fft_convolution(image, kernel)
% returns a convolved greyscale image

kernel = flip(kernel); % flip kernel ahead of fft2 convolve
[krnl_h, krnl_w] = size(kernel);
offset_h = floor(krnl_h/2);
offset_w = floor(krnl_w/2);


% pad input image array by replicating borders as per the offsets
image = padarray(image,[offset_h, offset_w], 'replicate');
[img_h, img_w] = size(image);

% convolve using fft2 and return to spacial domain using ifft2
filtered_image_prime = ifft2(fft2(image) .* fft2(kernel,img_h,img_w));

% extract image data, ignoring pre-padding done by fft2
filtered_image = filtered_image_prime(krnl_h:img_h,krnl_w:img_w);

end

