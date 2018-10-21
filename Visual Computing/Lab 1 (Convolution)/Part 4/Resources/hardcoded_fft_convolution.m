function filtered_image = fft_convolution(image, kernel)
% returns a convolved greyscale image

[krnl_h, krnl_w] = size(kernel);

% calculate max (+/-) kernal overlap about desired pixel  
offset_h = floor(krnl_h/2);
offset_w = floor(krnl_w/2);

% pad input image array by replicating borders as per the offsets
image = padarray(image,[offset_h, offset_w], 'replicate');
[img_h, img_w] = size(image);

filtered_image_prime = ifft2(fft2(image) .* fft2(kernel,img_h,img_w));

% extract image within the zero pad
filtered_image = filtered_image_prime(1+offset_h:img_h,2+offset_w:img_w)*-1;%(1:img_h, 2:257);

end

% REVERSE ENGINEER
