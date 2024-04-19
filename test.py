#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Match Case-Ctrl samples according to sample phenotypes (variables) and their weights.
# Including binary variables, nominal variables, ordinal variables, and scale variables.

import os
import pandas as pd
# Load metaccm package
from metaccm.metaccm import standardizedVarValue, matchingVars

# Read phenotype data
csvPath = os.path.join('data', 'metadata-1.csv')
metadata = pd.read_csv(csvPath, index_col=None)

# Specify the variables to match
confoundVars = ['bodySite', 'temperature', 'smokingFreq', 'BMI', 'colour', 'gender']
weightVars = [0.8, 0.05, 0.05, 0.025, 0.025, 0.05]
varTypes = ['nominal', 'scale', 'ordinal', 'scale', 'nominal', 'binary']
RequireDiffVar = ['weather']
# Standardize variable values
data = standardizedVarValue(data=metadata, standardVars=confoundVars+RequireDiffVar, varType=varTypes+['nominal'])
# Build a matching queue
data_balanced = matchingVars(data=data,
                             label='label',
                             matchVars=confoundVars,
                             weight=weightVars,
                             RequireDiffVar=RequireDiffVar)
# Save the dataframe to a CSV file
data_balanced.to_csv('result/pairedCohort.csv', index=False)
