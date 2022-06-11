.. Food-Insecurity-Analysis documentation master file, created by
   sphinx-quickstart on Sat Jun 11 00:29:45 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Food Insecurity Analysis's documentation!
====================================================

|Stars|_ |Forks|_ |Issues|_



.. |Stars| image:: https://img.shields.io/github/stars/shenweichen/deepctr.svg
.. _Stars: https://github.com/HaoyuWang0/Food-Insecurity-Analysis

.. |Forks| image:: https://img.shields.io/github/forks/shenweichen/deepctr.svg
.. _Forks: https://github.com/HaoyuWang0/Food-Insecurity-Analysis/fork


.. |Issues| image:: https://img.shields.io/github/issues/shenweichen/deepctr.svg
.. _Issues: https://github.com/HaoyuWang0/Food-Insecurity-Analysis/issues

This project is a **Food Insecurity Analysis**. 

The main purpose is to visualize American Food Insecurity Data and develop relevant Machine Learning/Statistical models to deliver visualizations and metrics.


.. toctree::
   :maxdepth: 5
   :caption: Contents:
  
   README
   Food_Insecurity_Analysis.ipynb
   modules
   
   

   
.. toctree::

*******************
Q&A
*******************

What is Food Insecurity?
--------------------------

A person is food insecure if they lack consistent access to nutritious food. There are several levels of severity to food insecurity. At the highest severity households may be food insecure - at times they are uncertain of having or unable to acquire, enough food to meet the dietary needs of all their members due to insufficient money or resources. Households could have low food security - were able to obtain enough food to avoid a substantial disruption to their eating patterns by relying on resources like Federal assistance programs or local food pantries. Finally there are households that have very low food security - these households are ones that sacrificed the normal eating patterns of one or more household members in order to sustain the food intake of the rest of their members. Note that people who can only access food that does not meet the nutritional needs to sustain a healthy lifestyle are also food insecure, in other words someone only having access to burgers can still be food insecure.

How accessible is nutritious food? 
-----------------------------------

In searching for a way to easily represent rates of food insecurity one can look at the cost per meal in a county. Those with exorbitantly high costs in comparison to a low median wage show how income inequality has an extreme effect on food insecurity. The cost per meal is determined by the department of agriculture’s recommended nutritional value in a meal compared to the average cost of the constituent ingredients to make a nutritional meal. In some cases a high cost per meal is present in areas with low food insecurity; this paradox may be indicative of gentrification or the process in which low income households are moved out of an area due to how expensive it becomes. Although the remaining residents may not have a problem accessing food the underlying problem is being moved elsewhere, that hungry people still need to find food.

   
Can we measure food insecurity with multiple factors?
------------------------------------------------------
In our ptoject, we use Factors: 
  | 1. Food Insecurity Rate 
  | 2. Food Insecure Population Density 
  | 3. Child Food Insecurity Rate 
  | 4. Budget Shortfall 
  | 5. FI Trending 
| For each factor above, we give a ranking score for every county, where 0 represents the lowest food insecurity. Then we calculate the mean ranking scores for counties and visualize them in a choropleth map. Light colors indicate a low food insecurity degree.
 

 
.. toctree::

####################
Dependencies
####################


The project depends on numpy, pandas, sklearn, plotly and scikit-learn, matplotlib etc. The packge version is listed below:



**For Data Visualization:**
---------------------------

.. code-block::

   ->plotly                        5.8.1
   ->numpy                         1.22.4 
   ->pandas                        1.4.2
   ->matplotlib                    3.5.2 
   ->urllib                        1.26.9 
   ->scipy                         1.8.1



**For Ranking model:**
------------------------

.. code-block::

   ->plotly                        5.8.1
   ->pandas                        1.4.2
   ->urllib                        1.26.9 
   ->scipy                         1.8.1


**For Test:**
-----------------

.. code-block::

   ->coverage                      6.4.1
   ->plotly                        5.8.1
   ->numpy                         1.22.4 
   ->pandas                        1.4.2
   ->matplotlib                    3.5.2 
   ->urllib                        1.26.9 
   ->scipy                         1.8.1
   ->unittest                      3.10.5
   
   
.. toctree::

##########
DataSet
##########
.. [Ref] https://data.bls.gov/cew/apps/data_views/data_views.htm#tab=Tables
.. [Ref] https://www.census.gov/programs-surveys/cbp/data/datasets.html
.. [Ref] https://data.census.gov/cedsci/table?q=food%20stamps&y=2020
.. [Ref] https://map.feedingamerica.org


    

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
