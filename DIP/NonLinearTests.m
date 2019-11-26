classdef NonLinearTests
    methods(Static)
        function verify_median(input_image, k_size)
            input_image.kernel = ones(k_size)/k_size^2;
            input_image.fast_sort = 1;
            
            test_image = medfilt2(input_image.image, [k_size k_size], 'symmetric');
            filtered = input_image.adaptive_compute('median');
            [diff, img_diff] = MyStatistics.ssd(test_image, filtered);
            
            figure(1)
            subplot(131); imshow(input_image.image); title('Original Image');
            subplot(132); imshow(test_image); title(sprintf('medfilt2'));
            subplot(133); imshow(filtered); title('My Median Filter');

            figure(2)
            imshow(img_diff); title(sprintf('Difference (ssd = %.2f)', diff));
        end
        
        function montage(input_image, type)
            sizes = [3, 5, 9, 25];
            images = cell(1, length(sizes));
             
            for i=1:length(sizes)
                input_image.kernel = ones(sizes(i))/(sizes(i)^2);
                images{i} = input_image.adaptive_compute(type);
            end
            
            montage(images)
            title(sprintf('%s Filter Montage (3, 5, 9, and 25 Sized Kernels)', type))
        end
        
        function weighted_montage(input_image, kernel_size, weights)
            images = cell(1, 3);
            input_image.kernel = ones(kernel_size)/(kernel_size^2);
            
            input_image.order_weights = weights;
            images{1} = input_image.adaptive_compute('weighted median');
            
            central = ones(1, 25);
            central(13) = 3;
            input_image.order_weights = central;
            images{2} = input_image.adaptive_compute('weighted median');
            
            input_image.order_weights = flip(weights); 
            images{3} = input_image.adaptive_compute('weighted median');
            
            montage(images, 'Size', [1 3])
            title(sprintf('Top Biased , Central Pixel, and Bottom Biased Weights (%dx%d Kernel Size)', kernel_size, kernel_size));
        end
        
        function adaptive_montage(input_image, kernel_size)
            constants = [0.5 1 5];
            images = cell(1, 3);
            input_image.kernel = ones(kernel_size)/(kernel_size^2);
            
            for i=1:length(constants)
                input_image.constant = constants(i);
                images{i} = input_image.adaptive_compute('adaptive weighted median');
            end
            
            montage(images, 'Size', [1, 3])
            title('Adaptive Weighted Median Filter Montage (w=10, c=0.5, 1, 5)')
        end
        
        function sort_speeds(input_image)
            [start, stop, step] = deal(3, 25, 2);
            points = ((stop-start)/step) + 1;
            [qsort_times, qsort_plus_times, medfilt_times] = deal(zeros(1, points));
            k_sizes = linspace(start, stop, points);
            
            for i=1:points
                kernel = ones(k_sizes(i))/(k_sizes(i)^2);
                input_image.kernel = kernel;
                input_image.fast_sort = 0;
                tstart = tic;
                input_image.adaptive_compute('median');
                exec_time = toc(tstart);
                qsort_times(i) = exec_time;
               
                input_image.fast_sort = 1;
                tstart = tic;
                input_image.adaptive_compute('median');
                exec_time = toc(tstart);
                qsort_plus_times(i) = exec_time;
                
                tstart = tic;
                img3 = medfilt2(input_image.image, size(kernel), 'symmetric');
                exec_time = toc(tstart);
                medfilt_times(i) = exec_time;
                
            end
            
%             max_time = max([qsort_times qsort_plus_times medfilt_times]);
%             qsort_times = (qsort_times ./ max_time);
%             qsort_plus_times = (qsort_plus_times ./ max_time);
%             medfilt_times = (medfilt_times ./ max_time);
%         
            bar(k_sizes, [qsort_times(:) qsort_plus_times(:) medfilt_times(:)], 'grouped'); 
            title('Execution Times by Kernel Size');
            xlabel('Kernel Size')
            ylabel('Execution Time (s)')
            legend('qsort', 'qsort plus','medfilt2')
            
        end
        
        function compare(input_image, k_size, weights, c_constant)
            edge_method = 'sobel';
            input_edge = edge(input_image.image, edge_method);
            input_image.kernel = ones(k_size)/k_size^2;
            input_image.fast_sort = 1;
            input_image.constant = c_constant;
            
            tstart = tic;
            median = input_image.adaptive_compute('median');
            median_time = toc(tstart);
            median_edge = edge(median, edge_method);
            
            input_image.order_weights = weights;
            tstart = tic;
            weighted = input_image.adaptive_compute('weighted median');
            weighted_time = toc(tstart);
            weighted_edge = edge(weighted, edge_method);
            
            tstart = tic;
            adaptive_weighted = input_image.adaptive_compute('adaptive weighted median');
            adaptive_weighted_time = toc(tstart);
            adaptive_weighted_edge = edge(adaptive_weighted, edge_method);

            % plots
            figure(1)
            subplot(232); imshow(input_image.image); 
            title(sprintf('Original Image - %dx%d Kernel Size', k_size, k_size));
            subplot(234); imshow(median); title('Median');
            subplot(235); imshow(weighted); title('Weighted Median');
            subplot(236); imshow(adaptive_weighted); 
            title(sprintf('Adaptive Weighted Median (w=10, c=%.2f)', input_image.constant));
            
            figure(2)
            subplot(232); imshow(input_edge); 
            title(sprintf('Original Image Edge Detection - %dx%d Kernel Size', k_size, k_size));
            subplot(234); imshow(median_edge); title('Median Edge Detection');
            subplot(235); imshow(weighted_edge); title('Weighted Median Edge Detection');
            subplot(236); imshow(adaptive_weighted_edge); 
             title(sprintf('Adaptive Weighted Median Edge Detection (w=10, c=%.2f)', input_image.constant));
            
            figure(3)
            x = categorical({'Median', 'Weighted Median', 'Adaptive Weighted Median'});
            x = reordercats(x, {'Median', 'Weighted Median', 'Adaptive Weighted Median'});
            bar(x, [median_time, weighted_time, adaptive_weighted_time]); 
            title(sprintf('Execution Times for a %dx%d Kernel', k_size, k_size));
            ylabel('Execution Time (s)')
        end    
   
    end
end 