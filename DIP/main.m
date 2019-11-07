% fft convolution
close all
files = {'nzjers1.jpg', 'foetus.png'};
k_size = 3;

% image = im2double(imread(char(files(1))));
kernel = ones(k_size)/(k_size^2); %MyStatistics.gaussian_filter(2);
[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel),...
                    Convolutions('foetus.png', kernel));
                
input = sar;
tstart = tic;
[filtered, filtered_type] = input.adaptive_compute('median');
linear_time = toc(tstart);

input.order_weights = [3, 1, 3, 1, 1, 1, 1, 1, 1];
[filtered1, filtered1_type] = input.adaptive_compute('weighted median');
nonlinear_time = toc(tstart) - linear_time;

ssd = sum((filtered(:) - filtered1(:)) .^ 2);
difference = 0.5 + 10 * (filtered - filtered1);

% plots
figure(1)
subplot(131); imshow(input.image); title('Original Image');
subplot(132); imshow(filtered); title(sprintf('Filtered Image (%s)', filtered_type));
subplot(133); imshow(filtered1); title(sprintf('Filtered Image (%s)', filtered1_type));

% figure(2)
% imshow(difference)
