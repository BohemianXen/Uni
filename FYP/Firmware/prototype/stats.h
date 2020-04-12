// stats.h

#ifndef _STATS_h
#define _STATS_h

float mean_f(long dataIn[], int length, int normalisation);
int updateStdMean(long dataIn[], int length, int normalisation, float* std, float *mean);

#endif

