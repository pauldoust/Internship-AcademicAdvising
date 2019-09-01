#!/usr/bin/env python
# coding: utf-8

# In[148]:


#************************************* Initialization ********************************************

####################
##### Imports ######
####################
import pandas as pd
import numpy as np
import math
from scipy.stats import kurtosis
from scipy.stats import skew

from pandas.api.types import is_string_dtype
from pandas.api.types import is_numeric_dtype

import os
####################
#### Parameters ####
####################
Experiment = "\SecondSemester"
DataFolder = "\data\\"
OrPath = r"C:\Users\mpouldou\final-data" + "\SecondSemester" + DataFolder
# Path = r"C:\Users\mpouldou\final-data" + Experiment + DataFolder
MainPath = r"C:\Users\mpouldou\final-data"
semesterFilePath = r"C:\Users\mpouldou\final-data" + Experiment + DataFolder + "semesters.txt"
# Courses_to_include = ['FIEC03012', 'ICM00604', 'ICM00646', 'ICF00489', 'ICM00216', 'ICF00463', 'FIEC04341', 'FIEC04358', 'ICM00901']
Features_Set = set([ 'NEW_COD_STUDENT', 'SEMESTER', 'YEAR', 'COURSE_ID', 'GRADE', 'GPA', 'PROFESSOR_ID', 'ID'])

# Courses_to_include = ['FIEC03012', 'ICM00604', 'ICM00646', 'ICF00489', 'ICM00216', 'ICF00463', 'FIEC04341', 'FIEC04358', 'ICM00901']
# Target_Courses = ['FIEC03012', 'ICM00604', 'ICM00646', 'ICF00489']
# Target_Courses_amax = [('amax', 'FIEC03012'), ('amax', 'ICM00604'), ('amax', 'ICM00646'), ('amax', 'ICF00489')]
# Target_Courses_prev = [('PrevLatestGrade', 'FIEC03012'), ('PrevLatestGrade', 'ICM00604'), ('PrevLatestGrade', 'ICM00646'), ('PrevLatestGrade', 'ICF00489')]
# Target_Courses_count = [('count', 'FIEC03012'), ('count', 'ICM00604'), ('count', 'ICM00646'), ('count', 'ICF00489')]


# In[114]:


def join_historic_data( historia_academia_path, teaching_materials_path, graduates_all_dep_path, Experiment):
    df_historia_academia = pd.read_csv(historia_academia_path)
    df_teaching_materials = pd.read_csv(teaching_materials_path)
    df_graduates_all_dep = pd.read_csv(graduates_all_dep_path)
    
    
    df_historia_academia_extended = pd.merge(df_historia_academia, df_teaching_materials, on=["COURSE_ID", "COURSE_TRACK", "YEAR", "SEMESTER"])

    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "1T" if x == "1S" else x)
    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "2T" if x == "2S" else x)
    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "3T" if x == "3S" else x)

    df_historia_academia_extended2 = df_historia_academia_extended.to_csv (MainPath +Experiment+ "\\historia_academia_extended.csv", index = None, header=True) 

    df_dataset = pd.merge(df_graduates_all_dep, df_historia_academia_extended, on=["NEW_COD_STUDENT"])

    
    df_dataset2 = df_dataset.to_csv (MainPath + Experiment + "\\dataset_joined.csv", index = None, header=True) 

    return df_dataset


# In[115]:


def concatentated_grades(x):
     return ",".join([str(y) for y in x])

def PrevLatestGrade(x):
    if len(x.values) == 1:
        return x.values[0]
    else:
        return x.values[1]

    
def Sum_GPA_Squared(x):
     return (x * x).sum()
    
def Sum_GPAxMARK(x):
    return (x['GRADE'] * x['GPA']).sum()

def Sum_GPAsubMARK(x):
    return (x['GPA'] - x['GRADE']).sum()

def SkewnessOfDifferences(x):
    return (x['GPA'] - x['GRADE']).skew()


# In[116]:


def clean_dataset( joined_data, Courses_to_include, Experiment):
    
    df_flow = joined_data.loc[ (joined_data['COURSE_ID'].isin( Courses_to_include )) ]     
    df_flow.SEMESTER = df_flow.SEMESTER.apply(lambda x: "1T" if x == "1S" else x)
    df_flow.SEMESTER = df_flow.SEMESTER.apply(lambda x: "2T" if x == "2S" else x)
    df_flow.SEMESTER = df_flow.SEMESTER.apply(lambda x: "3T" if x == "3S" else x)

    df_flow.GRADE = df_flow.GRADE.replace({',': '.'}, regex=True)
    df_flow.GRADE = pd.to_numeric(df_flow.GRADE)
            
    df_flow2 = df_flow.to_csv (MainPath + Experiment + "\\" + Experiment + "_flow.csv" , index = None, header=True)
    return df_flow


# In[146]:


def marks_features_extraction(cleanded_data, Target_Course, Target_Courses_amax, Experiment):
    features_set = set([ 'NEW_COD_STUDENT', 'SEMESTER', 'YEAR', 'COURSE_ID', 'GRADE', 'GPA', 'PROFESSOR_ID', 'ID'])

    for column in cleanded_data:
        if column not in features_set:
            cleanded_data = cleanded_data.drop(column, axis=1)
        
    cleanded_data = cleanded_data.sort_values(by=['NEW_COD_STUDENT','COURSE_ID', 'YEAR', 'SEMESTER'],ascending=[False, False, False,False])
    df_flow_pivot = cleanded_data.pivot_table(index='NEW_COD_STUDENT', columns='COURSE_ID', values='GRADE', aggfunc=[ np.max, PrevLatestGrade, 'count'])

    df_flow_pivot = pd.merge(cleanded_data, df_flow_pivot, how="inner",on="NEW_COD_STUDENT")
    targetCol = ('count', Target_Course)
    
    df_flow_pivot[targetCol] = df_flow_pivot[targetCol].apply(lambda x: x-1)
    
#     df_flow_pivot = df_flow_pivot[df_flow_pivot[targetCol].notnull()]
# #     for course in Feature_Courses:
# #         feature_col = ('amax', course)
# #         df_flow_pivot = df_flow_pivot[df_flow_pivot[feature_col].notnull()]


    df_flow_pivot = df_flow_pivot.sort_values(by=['NEW_COD_STUDENT','COURSE_ID', 'YEAR', 'SEMESTER'],ascending=[False, False, True,True])

#     df_flow_pivot = df_flow_pivot.drop_duplicates(subset=['NEW_COD_STUDENT'], keep='last')
    
    df_flow_pivot.loc[(df_flow_pivot[targetCol] == 0), ('PrevLatestGrade', Target_Course)] = df_flow_pivot[(df_flow_pivot[targetCol] == 0)][('PrevLatestGrade', Target_Course)].mean()
    
#     df_flow_pivot["IS_REPEATER"] = (df_flow_pivot[targetCol] > 0).astype(int)
    df_flow_pivot["TargetGrade"] = df_flow_pivot[('amax', Target_Course)]
    df_flow_pivot["TargetCourse"] = Target_Course
    for column in df_flow_pivot:
#         if column in Target_Courses_amax or Target_Courses_prev or Target_Courses_count:
        if is_numeric_dtype(df_flow_pivot[column]):
            df_flow_pivot[column].fillna((df_flow_pivot[column].mean()), inplace=True)
        if column in Target_Courses_amax:
#             print('col to delete: ', column)
            df_flow_pivot = df_flow_pivot.drop(column, axis=1)

    df_flow_pivot = df_flow_pivot[df_flow_pivot['COURSE_ID'] == Target_Course]
    df_flow_pivot = df_flow_pivot.drop('COURSE_ID', axis=1)
    print('Path: Exp: targetCoruse', MainPath + Experiment + "\\" + Target_Course + "_flow_ready_unified.csv")

    df_flow_pivot2 = df_flow_pivot.to_csv (MainPath + Experiment + "\\" +  Target_Course + "_flow_ready_unified.csv", index = None, header=True)

    return df_flow_pivot


# In[118]:


def difficulty_features_extraction(cleaned_data, Experiment):
#     df_flow = cleaned_data
    cleaned_data.GRADE = cleaned_data.GRADE.replace({',': '.'}, regex=True)
    cleaned_data.GRADE = pd.to_numeric(cleaned_data.GRADE)

    df_flow_grouped = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"])['GRADE'].mean().reset_index()
#     df_flow_grouped = cleaned_data.groupby(["COURSE_ID"])['GRADE'].mean().reset_index()

#     df_flow_grouped['alpha_Num'] = cleaned_data.groupby(["COURSE_ID"])['GPA'].apply(Sum_GPA_Squared).reset_index()['GPA']
    df_flow_grouped['alpha_Num'] = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"])['GPA'].apply(Sum_GPA_Squared).reset_index()['GPA']

    df_flow_grouped['alpha_Denom'] = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"]).apply(Sum_GPAxMARK).reset_index()[0]
#     df_flow_grouped['alpha_Denom'] = cleaned_data.groupby(["COURSE_ID"]).apply(Sum_GPAxMARK).reset_index()[0]

    df_flow_grouped['alpha'] = df_flow_grouped['alpha_Num'] / df_flow_grouped['alpha_Denom']

    df_flow_grouped['beta_Num'] = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"]).apply(Sum_GPAsubMARK).reset_index()[0]
#     df_flow_grouped['beta_Num'] = cleaned_data.groupby(["COURSE_ID"]).apply(Sum_GPAsubMARK).reset_index()[0]
#     df_flow_grouped['beta_Denom'] = cleaned_data.groupby(["COURSE_ID"])['GRADE'].count().reset_index()['GRADE']
    df_flow_grouped['beta_Denom'] = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"])['GRADE'].count().reset_index()['GRADE']
    df_flow_grouped['beta'] = df_flow_grouped['beta_Num'] / df_flow_grouped['beta_Denom']

#     df_flow_grouped['Skewness'] = cleaned_data.groupby(["COURSE_ID"]).apply(SkewnessOfDifferences).reset_index()[0]
    df_flow_grouped['Skewness'] = cleaned_data.groupby(["COURSE_ID", "PROFESSOR_ID"]).apply(SkewnessOfDifferences).reset_index()[0]
    
    df_flow_grouped2 = df_flow_grouped.to_csv (MainPath + Experiment  + "\\Courses_difficulties.csv", index = None, header=True)

    return df_flow_grouped


# In[119]:


def courses_load_features_extraction(allData, courses_difficulties, courses_credits, Experiment):
    df_all_student_courses = allData
    df_courses_difficulties = courses_difficulties
    df_courses_credits = courses_credits


    #merge to get other difficulties factor
#     df_all_student_courses =  pd.merge(df_all_student_courses, df_courses_difficulties, on=["COURSE_ID"])
    df_all_student_courses =  pd.merge(df_all_student_courses, df_courses_difficulties, on=["COURSE_ID", "PROFESSOR_ID"])
    #merge to get Credits
    df_all_student_courses =  pd.merge(df_all_student_courses, df_courses_credits, on=["COURSE_ID"])

#     grouped.filter(lambda x: x['B'].mean() > 3.)
#     df_all_student_courses_agg = df_all_student_courses.groupby(['NEW_COD_STUDENT', 'YEAR', 'SEMESTER']).agg({'ID': 'count', 'alpha': 'max', 'beta': 'max', "Course_Theoritical_Credits":"sum", "Course_Practical_Credits":"sum", "Skewness" : "mean"}).reset_index()
  
    df_all_student_courses_agg = df_all_student_courses.loc[df_all_student_courses['COURSE_ID'] != 'FIEC01735'].groupby(['NEW_COD_STUDENT', 'YEAR', 'SEMESTER']).agg({'ID': 'count', 'alpha': 'max', 'beta': 'max', "Course_Theoritical_Credits":"sum", "Course_Practical_Credits":"sum", "Skewness" : "mean"}).reset_index()

    df_all_student_courses_agg['Skewness_Target'] = df_courses_difficulties.loc[df_courses_difficulties['COURSE_ID'] == 'FIEC01735'].groupby(['COURSE_ID']).agg({'Skewness' : 'mean'}).reset_index().iloc[0]['Skewness'] 
    df_all_student_courses_agg['alpha_Target'] = df_courses_difficulties.loc[df_courses_difficulties['COURSE_ID'] == 'FIEC01735'].groupby(['COURSE_ID']).agg({'alpha' : 'max'}).reset_index().iloc[0]['alpha']
    df_all_student_courses_agg['beta_Target'] = df_courses_difficulties.loc[df_courses_difficulties['COURSE_ID'] == 'FIEC01735'].groupby(['COURSE_ID']).agg({'beta' : 'max'}).reset_index().iloc[0]['beta']
#     print(df_all_student_courses_agg)

  


    df_all_student_courses_agg.rename(columns={'ID': 'C_LOAD'}, inplace=True)

    df_all_student_courses_agg2 = df_all_student_courses_agg.to_csv (MainPath + Experiment + "\\C_LOAD.csv", index = None, header=True)

    
    return df_all_student_courses_agg


# In[120]:


def finalFeatures(marks_features, df_course_load, Experiment):  
#     df_course_load = pd.read_csv (Path + "C_LOAD.csv")
    final_dataset = pd.merge(marks_features, df_course_load, on=["NEW_COD_STUDENT", "YEAR", "SEMESTER"])
    
    final_dataset = final_dataset.to_csv (MainPath + Experiment  + "\\" + Experiment + "_flow_ready_unified_features.csv", index = None, header=True)

    return final_dataset


# In[133]:


def main(Target_Courses, Courses_to_include, Target_Courses_amax, Target_Courses_prev, Target_Courses_count, Experiment):
    historia_academia_path = OrPath + "historia_academica_anonym.csv"
    teaching_materials_path = OrPath + "materias_anonym_clean.csv"
    graduates_all_dep = OrPath + "exAlumnosConHistoriaAcademica_anonym.csv"
    df_courses_credits = pd.read_csv (OrPath + "COURSE_CREDITS.csv") 
    
    df_dataset = join_historic_data(historia_academia_path, teaching_materials_path, graduates_all_dep, Experiment)
    cleaned_data = clean_dataset(df_dataset, Courses_to_include, Experiment)
    
    finalTargetCourses_Featrues = pd.DataFrame()
    for course in Target_Courses:
        marks_features = marks_features_extraction (cleaned_data, course, Target_Courses_amax, Experiment)
        finalTargetCourses_Featrues = pd.concat([finalTargetCourses_Featrues, marks_features], axis=0)
    
    finalTargetCourses2 = finalTargetCourses_Featrues.to_csv (MainPath + Experiment  + "\\finalTargetCourses.csv", index = None, header=True)


    
    difficulty_features = difficulty_features_extraction (df_dataset, Experiment)
    course_load_features = courses_load_features_extraction(df_dataset, difficulty_features, df_courses_credits, Experiment)
    final_dataset = finalFeatures(finalTargetCourses_Featrues, course_load_features, Experiment)

  


# In[150]:


def parseSemesterModels(filePath):
    f = open(filePath)
    experimentNo = 1
    while True:
        # read line
        Courses_to_include = []
        Target_Courses = []
        Target_Courses_amax = []
        Target_Courses_prev = []
        Target_Courses_count = []
        line = f.readline()
        # check if line is not empty
        if not line:
            break

        print('line: ', line)
        toPredict = line.split(":")[0]
        prerequisite = line.split(":")[1]
        Experiment = "\Experiment" + str(experimentNo)
        if not os.path.exists(MainPath + Experiment ):
            os.mkdir(MainPath + Experiment )
        for target in toPredict.split():
                Target_Courses.append(target)
                targetAmax = ('amax', target)
                targetPrev = ('PrevLatestGrade', target)
                targetCount = ('count', target)
                Target_Courses_amax.append(targetAmax)
                Target_Courses_prev.append(targetPrev)
                Target_Courses_count.append(targetCount)
                Courses_to_include.append(target)

        for course in prerequisite.split():
                Courses_to_include.append(course)
    
        print("final Target_Courses: ", Target_Courses)
#         print("final Target_Courses_amax: ", Target_Courses_amax)
#         print("final Target_Courses_prev: ", Target_Courses_prev)
#         print("final Target_Courses_count: ", Target_Courses_count)
        print("final Courses_to_include: ", Courses_to_include)
        
        experimentNo += 1
        main(Target_Courses, Courses_to_include, Target_Courses_amax, Target_Courses_prev, Target_Courses_count, Experiment)  
        print("Finish: ", experimentNo)
    f.close()

parseSemesterModels(semesterFilePath)

