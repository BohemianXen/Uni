close all

k_size = 3;
kernel = ones(k_size)/(k_size^2);
weights3 = [3, 2, 1, 1, 2, 3, 1, 1, 1];
weights5 = ones(1, 25); 
weights5(1:18) = repelem(weights3, 2);
weights7 = ones(1, 49);
weights7(1:36) = repelem(weights3, 4);
weights9 = ones(1, 81);
weights9(1:54) = repelem(weights3, 6); 

fast_sort_on = 1;
[sar, foetus] = deal(Convolutions('nzjers1.jpg', kernel, fast_sort_on),...
                    Convolutions('foetus.png', kernel, fast_sort_on));

input = sar;
% LinearTests.verify_gaussian(input, 1);
% LinearTests.verify_unsharp(input, k_size);
% LinearTests.convolution_speeds(input);
% LinearTests.compare(input, k_size)
   
% NonLinearTests.verify_median(input, k_size);
% NonLinearTests.sort_speeds(input)
NonLinearTests.compare(input, k_size, weights3);
