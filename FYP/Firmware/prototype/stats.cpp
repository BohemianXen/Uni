// 
// 
// 

#include "stats.h"
#include "math.h"


float mean_f(long dataIn[], int length, int normalisation) {
	long result = 0;
	for (int i = 0; i < length; i++) {
		result += dataIn[i];
	}
	
	if (length != 0) {
		return ((float)result) / (length * 1000 * normalisation);
	} else {
		return 0.0;
	}
}

int updateStdMean(long dataIn[], int length, int normalisation, float *std, float *mean) {
	float result = 0.0;
	*mean = mean_f(dataIn, length, normalisation);
	
	for (int i = 0; i < length; i++) {
		*std += pow((dataIn[i]/(normalisation * 1000)) - *mean, 2);
	}

	if (length != 0) {
		*std = sqrt(*std / length);
	}
	else {
		*std = 0.0;
	}
	return 1;
}