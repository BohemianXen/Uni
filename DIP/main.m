close all

k_size = 3;
kernel = ones(k_size)/(k_size^2);
fast_sort_on = 1;
weights = [3, 2, 1, 1, 2, 3, 1, 1, 1];

[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel, fast_sort_on),...
                    Convolutions('foetus.png', kernel, fast_sort_on));

input = foetus;
% LinearTests.verify_gaussian(input, 1);
% LinearTests.verify_unsharp(input, k_size);
% LinearTests.convolution_speeds(input);
% LinearTests.compare(input, k_size)
   
NonLinearTests.verify_median(input, k_size);
% NonLinearTests.sort_speeds(input)
% NonLinearTests.compare(input, k_size, fast_sort_on, weights);
