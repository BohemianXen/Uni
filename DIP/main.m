% fft convolution
close all
files = {'nzjers1.jpg', 'foetus.png'};

% image = im2double(imread(char(files(1))));
kernel = ones(25, 25); % gaussian_filter(0.5); %ones(3, 3)
[sar, foetus] = deal(Convolutions(im2double(imread('nzjers1.jpg')), kernel),...
                    Convolutions(im2double(imread('foetus.png')), kernel));
                
    
input = foetus;
tstart = tic;
filtered = input.adaptive_compute('adaptive linear');
filtered_fft = input.fft_compute();
extended_time = toc(tstart)*1000;

% plots
% figure(1)
subplot(121); imshow(input.image); title('Original Image');
subplot(122); imshow(filtered); title('Filtered Image');
