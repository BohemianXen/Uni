close all

% set kernel size and test weights
k_size = 9;
weights3 = [3, 3, 3, 1, 1, 1, 1, 1, 1];
weights5 = ones(1, 25); 
weights5(1:18) = repelem(weights3, 2);
weights7 = ones(1, 49);
weights7(1:36) = repelem(weights3, 4);
weights9 = ones(1, 81);
weights9(1:54) = repelem(weights3, 6); 

weights = weights3;
switch(k_size)
    case 5
        weights = weights5;
    case 7
        weights = weights7;
    case 9
        weights = weights9;
end

% create Convolution objects, one for each image
kernel = ones(k_size)/(k_size^2);
fast_sort_on = 1;
c_constant = 0.5;
[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel, fast_sort_on, c_constant),...
                    Convolutions('foetus.png', kernel, fast_sort_on, c_constant));

%------------------------------- Best Results -----------------------------
sar.kernel = MyStatistics.gaussian_filter(1);
linear_sar = sar.fft_compute(); 
linear_sar_edge = edge(linear_sar);
sar.kernel = ones(3)/9; 
nonlinear_sar = sar.adaptive_compute('median');
nonlinear_sar_edge = edge(nonlinear_sar);
sar_edge = edge(sar.image);

foetus.kernel = ones(9)/81;
linear_foetus = foetus.adaptive_compute('unsharp'); 
linear_foetus_edge = edge(linear_foetus);
nonlinear_foetus = foetus.adaptive_compute('median');
nonlinear_foetus_edge = edge(nonlinear_foetus);
foetus_edge = edge(foetus.image);

sar_images = {sar.image, linear_sar, nonlinear_sar,sar_edge, linear_sar_edge, nonlinear_sar_edge};
foetus_images = {foetus.image, linear_foetus, nonlinear_foetus, foetus_edge, linear_foetus_edge, nonlinear_foetus_edge};

montage(sar_images, 'Size', [2, 3])
title('Gaussian Filter(sigma=1.0) vs. 3x3 Median Filter (SAR Image)')
figure(2)
montage(foetus_images, 'Size', [2, 3])
title('9x9 Unsharp Masking Filter vs. 9x9 Median Filter (Foetus Image)')

%----------------------Tests (comment in as appropriate)-------------------

input = sar;
% LinearTests.fft_montage(input, 0);
% LinearTests.unsharp_montage(input);
LinearTests.verify_gaussian(input, 1);
% LinearTests.verify_unsharp(input, k_size);
% LinearTests.convolution_speeds(input);
% LinearTests.compare(input, k_size)
  
% NonLinearTests.montage(input, 'median')
% NonLinearTests.weighted_montage(input, k_size, weights);
% NonLinearTests.adaptive_montage(input, k_size);
% NonLinearTests.verify_median(input, k_size);
% NonLinearTests.sort_speeds(input)
% NonLinearTests.compare(input, k_size, weights, c_constant);
