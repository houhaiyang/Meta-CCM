
<div align=center><img width="410.5" height="94" src="docs/logo.png"/></div>


# Meta-CCM

[![PyPI - Downloads](https://img.shields.io/pypi/dm/metaccm?label=metaccm%20on%20PyPi)](https://pypi.org/project/metaccm/) 


- Author: Haiyang Hou
- Date: 2024-04-25
- Version: v1.0.1
- If you want to use this package, please indicate the source and tell me in "lssues". Free use.

This is an algorithm for building a "Case-Ctrl" matching cohort to minimize the influence of confusing variables.

## Current function

* Used to construct a "Case-Ctrl" matching cohort.

* Based on matadata

* Support different variable types


## Description

This project is based on Python 3.11+ and developed using PyCharm 2024 on Windows 11.

Refer to the "Main function explanation" section for algorithm design.

-------------

## Installation
Requirements: python>=3.11, numpy, pandas, scikit-learn, statsmodels, peroxymanova==0.3.2.

Pay attention to the installation of scikit-learn package.

##### Install Meta-CCM

Install through PyPI:
```commandline
pip install metaccm
```
Install through local:
```commandline
pip install dist/metaccm-1.0.1-py3-none-any.whl
```

-------------

## Example usage

Please refer to test.py for an example.

#### Import dependency package
```python
import os
import pandas as pd
from metaccm.metaccm import standardizedVarValue, matchingVars
from metaccm.metaccmpro import metaccmPro
from metaccm.weightCalculate import weightCalculate
```
#### Prepare data
```python
csvPath = os.path.join('data', 'metadata-1.csv')
metadata = pd.read_csv(csvPath, index_col=None)

confoundVars = ['bodySite', 'temperature', 'smokingFreq', 'BMI', 'colour', 'gender']
varTypes = ['nominal', 'scale', 'ordinal', 'scale', 'nominal', 'binary']
RequireDiffVar = ['weather']

# Standardized data
data = standardizedVarValue(data=metadata, standardVars=confoundVars+RequireDiffVar, varType=varTypes+['nominal'])
```
#### Weight
Calculate weight by function
```python
weightVars,q_vals = weightCalculate(data=data, label='label', confoundVars=confoundVars, varType=varTypes)
print(weightVars,'\n',q_vals)
```
or set weight directly.
```python
weightVars = [1.5, 0.2, 0.5, 0.6, 0.4, 0.3]
```

The varType can only take four values: ‘nominal’, ‘scale’, ‘ordinal’, and ‘binary’.
The weightVars are relative weights and can be any floating-point number.

#### Example 1: One experiment of matching different types of variables
```python
data_balanced_1 = matchingVars(data=data, label='label', matchVars=confoundVars, weight=weightVars, RequireDiffVar=RequireDiffVar).iloc[:40]
data_balanced_1.to_csv('result/pairedCohort-metaccm.csv', index=False)
```

#### Example 2: Using the sample distance matrix to match the nearest "Case-Ctrl" sample pairs first.
```python
data_balanced_2 = metaccmPro(data=data, sample='sampleID', label='label', matchVars=confoundVars, weight=weightVars).iloc[:40]
data_balanced_2.to_csv('result/pairedCohort-metaccmPro.csv', index=False)
```

-------------

## Main function explanation

#### matchingVars(...)
```text
>>> help(matchingVars)

matchingVars(data: pd.DataFrame, label: str, matchVars: list[str], weight: list[float], RequireDiffVar: list[str])
    This is a function to realize the matching algorithm, which matches positive and negative samples according to specific criteria.
    Here’s a breakdown of the steps involved:
    
    1) Initialize the pairID and matchType variables.
    2) Loop through the positive samples (pos_var) until either the positive or negative sample list is empty.
    3) Select a positive sample and create a copy of the negative samples.
    4) Check if there are any requirements (RequireDiffVar) for selecting negative samples that are different from the positive sample.
    5) Filter out negative samples that do not meet the requirements.
    6) If no suitable negative samples remain, remove the current positive sample and continue to the next iteration.
    7) Calculate a matching score for each remaining negative sample based on certain match variables and weights (Use the matchingScore function) .
    8) Select the negative sample with the lowest matching score (closest).
    9) Assign pairID, matchType, and pair the positive and negative samples together.
    10) Add the matched pairs to separate dataframes and remove them from the sample pool.
    11) Concatenate the matched pairs dataframes, sort them by pairID, and return the balanced data.
    
    Overall, the function aims to balance the positive and negative samples by creating pairs that meet specific criteria. It ensures that each positive sample is matched with a suitable negative sample based on the matching score.
    
    :param data: (DataFrame) This parameter represents the dataset containing the samples that need to be balanced. It could include both positive and negative samples.
    :param label: (String) Represents a label in a dataset. It is used to distinguish between positive and negative samples.
    :param matchVars: (List of strings) Is a list of variables that need to be matched, which will be used to calculate the matching score between positive and negative samples.
    :param weight: (List of floats) This parameter represents the weight assigned to each match variable when calculating the matching score. It allows giving more importance to certain variables in the matching process.
    :param RequireDiffVar: (List of strings) This parameter specifies whether there are any requirements for selecting negative samples that are different from positive samples. It could be used to ensure diversity in the matched pairs.
    :return: (DataFrame) This function is expected to return a balanced dataset with pairs of positive and negative samples that meet the specified criteria. The pairs are matched based on the matching score calculated using the matchVars and weights.

```


#### matchingScore(...)
```text
>>> help(matchingScore)

matchingScore(negS: pd.DataFrame, posS: pd.DataFrame, weight: list[float])
    The function matchingScore calculates a matching score based on the input negative samples (negS), positive samples (posS), and weights (weight).
    Here is a breakdown of the processing steps:
    
    1) Copy the values of positive samples (posS) to match the number of rows in negative samples (negS) to create an expanded DataFrame posS_expanded.
    2) Extract the numerical columns from negative samples, reset the index, extract the corresponding numerical columns from posS_expanded, and convert them to numeric type.
    3) Extract the categorical columns from negative samples, reset the index, extract the corresponding categorical columns from posS_expanded, and convert them to string type.
    4) Calculate the squared differences of numerical columns, i.e., (negS - posS) ** 2.
    5) Determine the equality of categorical columns and convert the equality status to integers.
    6) Merge the DataFrames diff_squared and char_equal to create the DataFrame result.
    7) Convert the weights (weight) to a NumPy array.
    8) Multiply each row of result with the weights vector to calculate the matching scores.
    9) Return the calculated matching scores as a NumPy array.
    
    In summary, this function processes numerical column differences squared and categorical column equalities with weights to produce an array of matching scores.
    
    :param negS: (DataFrame) DataFrame of negative samples.
    :param posS: (DataFrame) DataFrame of positive samples.
    :param weight: (array) Array of weights for calculating the score.
    :return: (array) Array of matching scores.
```

-------------

## References
[1] Vujkovic-Cvijin I, Sklar J, Jiang L, et al. Host variables confound gut microbiota studies of human disease[J]. Nature, 2020, 587(7834): 448-454.

[2] Anderson M J. A new method for non-parametric multivariate analysis of variance[J]. 2001.



