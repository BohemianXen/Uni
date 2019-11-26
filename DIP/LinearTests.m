classdef LinearTests
    methods(Static)
        function verify_gaussian(input_image, sigma)
            k_size = 2 * ceil(3*sigma) + 1;
            test_kernel = fspecial('gaussian', k_size, sigma);
            my_kernel = MyStatistics.gaussian_filter(sigma);
            input_image.kernel = my_kernel;
            
            test_image = imfilter(input_image.image, test_kernel, 'replicate');
            filtered = input_image.fft_compute();
            [diff, img_diff] = MyStatistics.ssd(test_image, filtered);
            
            figure(1)
            subplot(131); imshow(input_image.image); title(sprintf('Original Image (sigma=%.2f)', sigma));
            subplot(132); imshow(test_image); title(sprintf('In-built Filter'));
            subplot(133); imshow(filtered); title('My Gaussian (FFT Conv.)');

            figure(2)
            imshow(img_diff); title(sprintf('Difference (ssd = %.2f)', diff));
        end
        
        function verify_unsharp(input_image, k_size)
            input_image.kernel = ones(k_size)/k_size^2;
            
            test_image = imsharpen(input_image.image);
            filtered = input_image.adaptive_compute('unsharp');
            [diff, img_diff] = MyStatistics.ssd(test_image, filtered);
            
            figure(1)
            subplot(131); imshow(input_image.image); title('Original Image');
            subplot(132); imshow(test_image); title(sprintf('imsharpen'));
            subplot(133); imshow(filtered); title('My (Adaptive k) Unsharp Filter');

            figure(2)
            imshow(img_diff); title(sprintf('Difference (ssd = %.2f)', diff));
        end
        
        function fft_montage(input_image, mean)
            sizes = [3, 5, 9, 25];
            sigmas = [0.33, 0.5, 1, 2];
            images = cell(1, length(sizes));
            
            for i=1:length(sizes)
                if (mean)
                    input_image.kernel = ones(sizes(i))/(sizes(i)^2);
                else
                    input_image.kernel = MyStatistics.gaussian_filter(sigmas(i));
                end
                images{i} = input_image.fft_compute();
            end
            
            montage(images)
            if (mean)
                title('Mean Filter Montage (3, 5, 9, and 25 Sized Kernels)')
            else
                title('Gaussian Filter Montage (0.33, 0.5, 1, and 2 Std. Deviations)')
            end
        end
        
        function unsharp_montage(input_image)
            sizes = [3, 5, 9, 25];
            images = cell(1, length(sizes));
            
            for i=1:length(sizes)
                input_image.kernel = ones(sizes(i))/(sizes(i)^2);
                images{i} = input_image.adaptive_compute('unsharp');
            end
            
            montage(images)
            title('Unsharp Filter Montage (3, 5, 9, and 25 Sized Kernels)')
        end
        
        function convolution_speeds(input_image)
            [start, stop, step] = deal(3, 55, 2);
            points = ((stop-start)/step) + 1;
            [conv_times, fft_times, imfilter_times] = deal(zeros(1, points));
            k_sizes = linspace(start, stop, points);
            
            for i=1:points
                kernel = ones(k_sizes(i))/(k_sizes(i)^2);
                input_image.kernel = kernel;
                
                tstart = tic;
                input_image.adaptive_compute('mean');
                exec_time = toc(tstart);
                conv_times(i) = exec_time;
               
                tstart = tic;
                input_image.fft_compute();
                exec_time = toc(tstart);
                fft_times(i) = exec_time;
                
                tstart = tic;
                img3 = imfilter(input_image.image, kernel,'replicate');
                exec_time = toc(tstart);
                imfilter_times(i) = exec_time;
                
            end
            
            max_time = max([conv_times fft_times imfilter_times]);
            conv_times = (conv_times ./ max_time);
            fft_times = (fft_times ./ max_time);
            imfilter_times = (imfilter_times ./ max_time);
        
            bar(k_sizes, [conv_times(:) fft_times(:) imfilter_times(:)], 'grouped'); 
            title('Execution Times by Kernel Size');
            xlabel('Kernel Size')
            ylabel('Normalised Execution Time')
            legend('Standard Conv.', 'FFT','imfilter')
            
        end
        
        function compare(input_image, k_size)
            edge_method = 'sobel';
            input_edge = edge(input_image.image, edge_method);
            input_image.kernel = ones(k_size)/k_size^2;         
            
            tstart = tic;
            mean = input_image.fft_compute();
            mean_time = toc(tstart);
            mean_edge = edge(mean, edge_method);

            tstart = tic;
            unsharp = input_image.adaptive_compute('unsharp');
            unsharp_time = toc(tstart);
            unsharp_edge = edge(unsharp, edge_method);
            
            sigma = (k_size-1)/6;
            input_image.kernel = MyStatistics.gaussian_filter(sigma);
            tstart = tic;
            gaussian = input_image.fft_compute();
            gaussian_time = toc(tstart);
            gaussian_edge = edge(gaussian, edge_method);

            % plots
            figure(1)
            subplot(232); imshow(input_image.image); 
            title(sprintf('Original Image - %dx%d Kernel Size', k_size, k_size));
            subplot(234); imshow(mean); title('Mean Filter');
            subplot(235); imshow(gaussian); title(sprintf('Gaussian Filter (sigma=%.2f)', sigma));
            subplot(236); imshow(unsharp); title('Unsharp Filter');
            
            figure(2)
            subplot(232); imshow(input_edge); 
            title(sprintf('Original Image Edge Detection - %dx%d Kernel Size', k_size, k_size));
            subplot(234); imshow(mean_edge); title('Mean Filter Edge Detection');
            subplot(235); imshow(gaussian_edge); title(sprintf('Gaussian Filter (sigma=%.2f) Edge Detection', sigma));
            subplot(236); imshow(unsharp_edge); title('Unsharp Filter Edge Detection');
            
            figure(3)
            x = categorical({'Mean', 'Gaussian', 'Unsharp'});
            x = reordercats(x, {'Mean', 'Gaussian', 'Unsharp'});
            bar(x, [mean_time, gaussian_time, unsharp_time]); 
            title(sprintf('Execution Times for a %dx%d Kernel', k_size, k_size));
            ylabel('Execution Time (s)')
        end    
   
    end
end 