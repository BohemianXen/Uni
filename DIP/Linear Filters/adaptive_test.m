% fft convolution
close all
files = {'..\nzjers1.jpg', '..\foetus.png'};
image = im2double(imread(char(files(2))));


kernel = ones(7, 7); 
% filter using Extended Convolution
tstart = tic;
filtered = adaptive_convolution(image, kernel);
extended_time = toc(tstart)*1000;

% plots
% figure(1)
subplot(121); imshow(image); title('Original Image');
subplot(122); imshow(filtered); title('Filtered Image');
