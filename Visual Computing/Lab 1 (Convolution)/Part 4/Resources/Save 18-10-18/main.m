% extended convolution
image = im2double(imread('cameraman.tif'));
kernel = [-1 0 1]; %ones(5) / 25; %[-1 0 1];

tstart = tic;
filtered = extended_convolution(image, kernel);
extended_time = toc(tstart);
disp(extended_time)

tstart_fft = tic;
filtered_fft = fft_convolution(image, kernel);
fft_time = toc(tstart_fft);
disp(fft_time)

reference = imfilter(image, kernel, 'replicate');
difference = 0.5 + 10 * (filtered - reference);
ssd = sum((filtered_fft(:) - reference(:)) .^ 2); %note this is comparing fft now
subplot(141); imshow(filtered); title('Extended convolution');
subplot(142); imshow(filtered_fft); title('FFT convolution');
subplot(143); imshow(reference); title('Reference result');
subplot(144); imshow(difference); title(sprintf('Difference (SSD=%.1f)',ssd));
