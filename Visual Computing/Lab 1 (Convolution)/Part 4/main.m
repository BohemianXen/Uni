% fft convolution
close all
image = im2double(imread('cameraman.tif'));
total_kernels = 3;

for i=1:total_kernels
    if i==1
        kernel = [-1 0 1];
    elseif i==2
        kernel = ones(5) / 25;
    else
        kernel = fspecial('gaussian', 25);
    end
    
    % filter using Extended Convolution
    tstart = tic;
    filtered = extended_convolution(image, kernel);
    extended_time = toc(tstart)*1000;

    % filter using FFT
    tstart = tic;
    filtered_fft = fft_convolution(image, kernel);
    fft_time = toc(tstart)*1000;

    % reference filter using imfilter andc compare diff w/ FFT method
    tstart = tic;
    reference = imfilter(image, kernel, 'replicate');
    imfilter_time = toc(tstart)*1000;
    difference = 0.5 + 10 * (filtered - reference);
    ssd = sum((filtered_fft(:) - reference(:)) .^ 2);
    
    % plots
    figure(i)
    subplot(221); imshow(reference); title('Reference Result');
    subplot(222); imshow(filtered_fft); title('FFT Convolution');
    subplot(223); imshow(difference); title(sprintf('FFT Diff (SSD=%.1f)',ssd));
    subplot(224); 
    bar(categorical({'Extended', 'FFT','imfilter'}),[extended_time fft_time imfilter_time]); 
    title(sprintf('Execution Times for a %dx%d Kernel', size(kernel)));
    ylabel('Execution Time (ms)');
end
