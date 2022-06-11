# Food Insecurity Analysis
ECE 229 Group 3 Project, Spring 2022

## Introduction
According to the United States Department of Agriculture in 2020, 13.8 million households were food insecure, meaning they lacked consistent access to nutritional food. In this project, we made our dashboard with the express purpose to cater to people who want to make a positive change in their community but may not have a strong statistical background. Whether it be a politician’s policy decisions, an organization’s efficient budget or perhaps an individual’s personal time any of these groups can use our dashboard to view a graphical analysis of food insecurity over the past decade in America in order to best allocate their resources to impoverished groups.

## Full Documentation 


## Dashboard Website
http://44.232.168.218:8866/

## Built-with
- Json 2.0.9
- Numpy 1.21.5
- Pandas 1.3.4
- Plotly 5.8.0
- Scipy 1.7.1

## File Structure
```
- data
 | -- 2018_fi_data.csv
 | -- ...
 |
- picture
 | -- pytest_coverage.png
 | -- pytest_result.png
 |
- county_ranking_model.py
 |
- ProjectCodeCombine.py
 |
- test_ProjectCodeCombine.py
 |
- firate.ipynb
 |
- Food Insecurity Analysis.ipynb
 |
- README.md
```

The *data* folder contains all data files.

The *picture* folder contains the pictures for pytest.

*county_ranking_model.py* and *firate.ipynb* are the source code, which are combined and tested in *ProjectCodeCombine.py* and *test_ProjectCodeCombine.py*.

All visualizations and descriptions are presented in *Food Insecurity Anlysis.ipynb*. You can view it by
```
$ jupyter notebook Food\ Insecurity\ Analysis.ipynb
```


## pytest

To run the pytest
```bash
pytest test_ProjectCodeCombine.py -v
```

To check the coverage
```bash
pip install coverage
coverage run test_ProjectCodeCombine.py
coverage report -m
```

### pytest report:
![Alt text](picture/pytest_result.png?raw=true)

### coverage report:
![Alt text](picture/pytest_coverage.png?raw=true)
