% fft convolution
close all
files = {'nzjers1.jpg', 'foetus.png'};
k_size = 3;

% image = im2double(imread(char(files(1))));
kernel = ones(k_size)/(k_size^2); %MyStatistics.gaussian_filter(2);
[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel),...
                    Convolutions('foetus.png', kernel));
                
input = foetus;
tstart = tic;
[filtered, filtered_type] = input.adaptive_compute('adaptive linear');
[filtered1, filtered1_type] = input.adaptive_compute('mean');
extended_time = toc(tstart)*1000;

% plots
% figure(1)
subplot(131); imshow(input.image); title('Original Image');
subplot(132); imshow(filtered); title(sprintf('Filtered Image (%s)', filtered_type));
subplot(133); imshow(filtered1); title(sprintf('Filtered Image (%s)', filtered1_type));
