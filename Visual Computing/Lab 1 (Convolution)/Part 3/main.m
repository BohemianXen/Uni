% extended convolution
close all
image = im2double(imread('cameraman.tif'));
filter_names = ["Horizontal Filter", "Vertical Filter", "Diagonal Filter",... 
                "Sharpening Filter", "Gaussian Blur Filter"];

% TODO: COME UP WITH OWN KERNELS
horizontal_grad = [1 2 1; 0 0 0; -1 -2 -1];
vertical_grad = [1 0 -1; 2 0 -2; 1 0 -1];
diag_grad = [2 1 0; 1 0 -1; 0 -1 2];
sharp = [0 -1 0; -1 5 -1; 0 -1 0];
[gaussian_kernel, normalisation] = gaussian_blur_kernel(1, 5, 5);
fprintf('\nGaussian Kernel Normalisation = %f\n', normalisation);

kernels = horizontal_grad;
kernels(:,:,2) = vertical_grad;
kernels(:,:,3) = diag_grad; 
kernels(:,:,4) = sharp;

filtered_images=zeros(size(image)); 
reference_images=zeros(size(image));
for i=2:5
    filtered_images(:,:,i) = zeros(size(image));
    reference_images(:,:,i) = zeros(size(image));
end

ssds = zeros(5);

for i=1:5
    if i==5
        current_filter = extended_convolution(image, gaussian_kernel);
        current_reference = imfilter(image, gaussian_kernel, 'replicate');
    else
        current_filter =  extended_convolution(image, kernels(:,:,i));
        current_reference = imfilter(image, kernels(:,:,i), 'replicate');
    end   
    filtered_images(:,:,i) = current_filter;
    reference_images(:,:,i) = current_reference;
    % difference = 0.5 + 10 * (filtered - reference);
    ssds(i) = sum((current_filter(:) - current_reference(:)) .^ 2);
end

for i=1:5
    fprintf('\n%s SSD = %.1f\n', filter_names(1, i), ssds(1, i));
end

subplot(332); imshow(image); title('Original Image');
subplot(334); imshow(filtered_images(:,:,1)); title('Horizontal Gradient Filtered Image');
subplot(335); imshow(filtered_images(:,:,2)); title('Vertical Gradient Filtered Image');
subplot(336); imshow(filtered_images(:,:,3)); title('Diagonal Gradient Filtered Image');
subplot(337); imshow(filtered_images(:,:,4)); title('Sharpened Image');
subplot(339); imshow(filtered_images(:,:,4)); title('Gaussian Blurred Image');

