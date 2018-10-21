% basic convolution 
close all
image = im2double(imread('cameraman.tif'));
kernel = ones(5) / 25; %[-1 0 1];
filtered = basic_convolution(image, kernel);
subplot(121); imshow(image); title('Input image');
subplot(122); imshow(filtered); title('Filtered image');