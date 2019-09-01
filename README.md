# Accurate and Personalized Academic Advising
This repository contains various output of my internship at Inria Labs.
* Datasets
* Experiments
* Presentation
* Report
* Software

### Dataset:
dataset from Electrical and Computer Engineering College of ESPOL University in Guayaquil Ecuador.
### Goal: 
Using this data to build a proactive and interpretable Academic Advising System.
This is done by predicting student future mark in specific subject/semester given the their academic history
### Main Steps:
* Data Preprocessing
    + Data Anonymization
    + Data Integration
    + Data Cleansing
    + Data Transformation
	
* Features Engineering
* Model & Features Selection

### Notes:
- Linear Regression and Random Forest have been tested in this work.
- A separate model has been built to predict an important course
- Linear-time Closed itemset Miner (LCM) algorithm is used to extract the stereotypical semesters for students (courses frequently taken together by students in specific semester)
- A unified model has been built to predict all courses in a stereotypical semester, this model per semester was traine by including course name as an input feature
- A sepe

