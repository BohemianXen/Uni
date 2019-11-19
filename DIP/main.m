% fft convolution
close all
k_size = 3;
fast_sort_on = 0;

% image = im2double(imread(char(files(1))));
kernel = ones(k_size)/(k_size^2);
% kernel = MyStatistics.gaussian_filter(1);
[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel, fast_sort_on),...
                    Convolutions('foetus.png', kernel, fast_sort_on));
Tests.verify_gaussian(sar, 0.7);  

% input = sar;
% input.order_weights = [3, 1, 1, 1, 3, 3, 1, 1, 1];
% tstart = tic;
% [filtered, filtered_type] = input.adaptive_compute('adaptive weighted median');
% linear_time = toc(tstart);
% 
% % input.fast_sort = 1;
% [filtered1, filtered1_type] = input.adaptive_compute('adaptive weighted median');
% nonlinear_time = toc(tstart) - linear_time;
% % filtered1 = imfilter(input.image, kernel, 'replicate');
% ssd = sum((filtered(:) - filtered1(:)) .^ 2);
% difference = 0.5 + 10 * (filtered - filtered1);
% 
% % plots
% figure(1)
% subplot(131); imshow(input.image); title('Original Image');
% subplot(132); imshow(filtered); title(sprintf('Filtered Image (%s)', filtered_type));
% subplot(133); imshow(filtered1); title(sprintf('Filtered Image (%s)', filtered1_type));
% 
% figure(2)
% imshow(difference)
