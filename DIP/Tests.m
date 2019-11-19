classdef Tests
    methods(Static)
        function verify_gaussian(input_image, sigma)
            k_size = 2 * ceil(3*sigma) + 1;
            test_kernel = fspecial('gaussian', k_size, sigma);
            my_kernel = MyStatistics.gaussian_filter(sigma);
            input_image.kernel = my_kernel;
            
            test_image = imfilter(input_image.image, test_kernel, 'replicate');
            [filtered, filtered_type] = input_image.fft_compute('My Gaussian (FFT Conv.)');
            [diff, img_diff] = MyStatistics.ssd(test_image, filtered);
            
            figure(1)
            subplot(131); imshow(input_image.image); title('Original Image');
            subplot(132); imshow(test_image); title(sprintf('In-built Filter'));
            subplot(133); imshow(filtered); title(sprintf('%s', filtered_type));

            figure(2)
            imshow(img_diff); title(sprintf('Difference (ssd = %.2f)', diff));
        end
    end
end 