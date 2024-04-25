#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Match Case-Ctrl samples according to sample phenotypes (variables) and their weights.
# Including binary variables, nominal variables, ordinal variables, and scale variables.

# import os
import pandas as pd
# Load metaccm package
from metaccm.metaccm import standardizedVarValue, matchingVars
from metaccm.metaccmpro import metaccmPro
from metaccm.weightCalculate import weightCalculate
from metaccm.diffStatistics import permanovaSingle

# Read phenotype data
csvPath = 'data/metadata-1.csv'
metadata = pd.read_csv(csvPath, index_col=None)

# Specify the variables to match
confoundVars = ['bodySite', 'temperature', 'smokingFreq', 'BMI', 'colour', 'gender']
varTypes = ['nominal', 'scale', 'ordinal', 'scale', 'nominal', 'binary']
RequireDiffVar = ['weather']
# Standardize variable values
data = standardizedVarValue(data=metadata, standardVars=confoundVars+RequireDiffVar, varType=varTypes+['nominal'])

# Calculate weight by function
weightVars,q_vals = weightCalculate(data=data, label='label', confoundVars=confoundVars, varType=varTypes)
print(weightVars,'\n',q_vals)
# or set weight directly.
weightVars = [1.5, 0.2, 0.5, 0.6, 0.4, 0.3]

# Build a matching cohort
data_balanced_1 = matchingVars(data=data, label='label', matchVars=confoundVars, weight=weightVars, RequireDiffVar=RequireDiffVar).iloc[:40]
data_balanced_1.to_csv('result/pairedCohort-metaccm.csv', index=False)

# Using CCMPro function - Build a matching cohort
data_balanced_2 = metaccmPro(data=data, sample='sampleID', label='label', matchVars=confoundVars, weight=weightVars).iloc[:40]
data_balanced_2.to_csv('result/pairedCohort-metaccmPro.csv', index=False)

# Calculate PERMANOVA statistics
abd = pd.read_csv('data/abundance-1.csv', index_col='sampleID')
label = data['label'].values
F0, p0 = permanovaSingle(abd, label)

abd1 = abd.loc[data_balanced_1['sampleID']]
label1 = data.set_index('sampleID').loc[data_balanced_1['sampleID']].reset_index()['label'].values
F1, p1 = permanovaSingle(abd1, label1)

abd2 = abd.loc[data_balanced_2['sampleID']]
label2 = data.set_index('sampleID').loc[data_balanced_2['sampleID']].reset_index()['label'].values
F2, p2 = permanovaSingle(abd2, label2)

print(F0, p0, '\n', F1, p1, '\n', F2, p2)

