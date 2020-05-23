/**
* @file stats.cpp
*
* Statistical subroutines tailored for fall detector model inputs.
*
* @author Ralph Mukusa
* contact: ralph.mukusa@gmail.com
*
**/

#include "stats.h"
#include "math.h"


/**
 * Calculates the mean of an array, scales, and normalises as required for acc/gyro.
 *
 * @param long* dataIn: 1D array holding the input data.
 * @param int length: Length of the input array.
 * @param int normalisation: A normalisation factor for the inputs; 4(gs) for acc, 2000(dps) for gyro.
 * @return float: The mean of the inputs.
**/
float mean_f(long dataIn[], int length, int normalisation) {
	long result = 0;
	for (int i = 0; i < length; i++) { result += dataIn[i]; }  // Sum input values
	
	if (length != 0) {
		return ((float) result) / (length * 1000 * normalisation);  // Divide sum by length, scale, and normalise
	} 
	else {
		return 0.0;
	}
}


/**
 * Calculates the mean then std of an array, scales, and normalises as required for acc/gyro.
 *
 * @param long* dataIn: 1D array holding the input data.
 * @param int length: Length of the input array.
 * @param int normalisation: A normalisation factor for the inputs; 4(gs) for acc, 2000(dps) for gyro.
 * @param float* std: Pointer to std calculati	on destination.
 * @param float* mean:  Pointer to mean calculation destination.
 * @return int: Success of mean and std calculations.
**/
int updateStdMean(long dataIn[], int length, int normalisation, float *std, float *mean) {
	*mean = mean_f(dataIn, length, normalisation);
	
	for (int i = 0; i < length; i++) {
		// Normalise inputs then remove their mean and square each value
		*std += pow(((float)dataIn[i]/(normalisation * 1000)) - *mean, 2);
	}

	if (length != 0) {
		*std = sqrt(*std / length);
	}
	else {
		*std = 0.0;
	}
	return 1;  // TODO: when to return 0 if failure (e.g. input length of zero instead of just ignoring) 
}
