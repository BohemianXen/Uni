% extended convolution
close all
image = im2double(imread('cameraman.tif'));
kernel = ones(5) / 25; %[-1 0 1];
filtered = extended_convolution(image, kernel);
reference = imfilter(image, kernel, 'replicate');
difference = 0.5 + 10 * (filtered - reference);
ssd = sum((filtered(:) - reference(:)) .^ 2);
subplot(131); imshow(filtered); title('Extended convolution');
subplot(132); imshow(reference); title('Reference result');
subplot(133); imshow(difference); title(sprintf('Difference (SSD=%.1f)',ssd));
