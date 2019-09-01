#!/usr/bin/env python
# coding: utf-8

# In[36]:


import pandas as pd
import numpy as np
import math
from scipy.stats import kurtosis
from scipy.stats import skew



Experiment = "\SecondSemester"
DataFolder = "\data\\"
Path = r"C:\Users\mpouldou\Desktop\lcm" + Experiment + DataFolder
Features_Set = set([ 'NEW_COD_STUDENT', 'SEMESTER', 'YEAR', 'COURSE_ID', 'GRADE', 'GPA', 'PROFESSOR_ID', 'ID', 'Course_encode', 'COURSE_NAME'])


# def concatentated_grades(x):
#      return ",".join([str(y) for y in x])

def concatentated_courses(x):
    if len(x.values) <= 2:
        return ""
    return " ".join([str(y) for y in x])
#     return " ".join([str(y) for y in x])
# 	return ""

def join_historic_data( historia_academia_path, teaching_materials_path, graduates_all_dep_path):
    df_historia_academia = pd.read_csv(historia_academia_path)
    df_teaching_materials = pd.read_csv(teaching_materials_path)
    df_graduates_all_dep = pd.read_csv(graduates_all_dep_path)
    print("1")
    
    df_historia_academia.GRADE = df_historia_academia.GRADE[df_historia_academia.GRADE != "0,00"]
    df_historia_academia = pd.merge(df_graduates_all_dep, df_historia_academia, on=["NEW_COD_STUDENT"])

    print("2")
    df_historia_academia_extended = pd.merge(df_historia_academia, df_teaching_materials, on=["COURSE_ID"])
    # df_historia_academia_extended = pd.merge(df_historia_academia, df_teaching_materials, on=["COURSE_ID", "COURSE_TRACK", "YEAR", "SEMESTER"])

    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "1T" if x == "1S" else x)
    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "2T" if x == "2S" else x)
    df_historia_academia_extended.SEMESTER = df_historia_academia_extended.SEMESTER.apply(lambda x: "3T" if x == "3S" else x)
    print("3")

    df_historia_academia_extended2 = df_historia_academia_extended.to_csv (Path + "historia_academia_extended.csv", index = None, header=True) 
    print("33")

#     df_dataset = pd.merge(df_graduates_all_dep, df_historia_academia_extended, on=["NEW_COD_STUDENT"])

    
#     df_dataset2 = df_dataset.to_csv (Path + "dataset_joined.csv", index = None, header=True) 

    return df_historia_academia_extended


def clean_dataset( joined_data):
    print("4")

    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "1T" if x == "1S" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "2T" if x == "2S" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "3T" if x == "3S" else x)

    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "1T" if x == "1B" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "2T" if x == "2B" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "3T" if x == "3B" else x)


    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "4T" if x == "4B" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "5T" if x == "5B" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "6T" if x == "6B" else x)
    joined_data.SEMESTER = joined_data.SEMESTER.apply(lambda x: "7T" if x == "7B" else x)

    joined_data.GRADE = joined_data.GRADE.str.replace(",", ".", case = False)
    # print(joined_data.GRADE)
    joined_data.GRADE = pd.to_numeric(joined_data.GRADE)
    joined_data.GRADE = joined_data.GRADE[joined_data.GRADE != 0]
    joined_data.GRADE = joined_data.GRADE[joined_data.GRADE != None]
    joined_data.GRADE = joined_data.GRADE[joined_data.GRADE.notna()]
    joined_data = joined_data[joined_data.GRADE.notnull()]
    joined_data.GRADE = joined_data.GRADE[joined_data.GRADE != np.nan]
    
#     print('cell: ', joined_data[joined_data.NEW_COD_STUDENT == 1451].GRADE)
    
    for column in joined_data:
    	if column not in Features_Set:
    		joined_data = joined_data.drop(column, axis=1)

    df_flow2 = joined_data.to_csv (Path + Experiment + "_flow.csv" , index = None, header=True)
    return joined_data




def convertToTransactions(cleanded_data):
	transactions = cleanded_data.groupby(['NEW_COD_STUDENT', 'YEAR', 'SEMESTER']).agg({'Course_encode': concatentated_courses, 'COURSE_NAME':concatentated_courses, 'COURSE_ID' : concatentated_courses}).reset_index()
	transactions = transactions[transactions.Course_encode !=""]
	transactions2 = transactions.to_csv(Path + Experiment + "_transaction.csv" , index = None, header=True)
	return transactions

def main():
    historia_academia_path = Path + "historia_academica_anonym.csv"
    teaching_materials_path = Path + "materias_anonym_clean_filtered.csv"
    graduates_all_dep = Path + "graduadosComputacion_anonym.csv"
    df_dataset = join_historic_data(historia_academia_path, teaching_materials_path, graduates_all_dep)
    print("ss4")
    cleaned_data = clean_dataset(df_dataset)
    transaction_table = convertToTransactions(cleaned_data)
    # print(transaction_table)
    transaction_table  = transaction_table[transaction_table.Course_encode !=""]
    np.savetxt(r'C:\Users\mpouldou\Desktop\lcm\transactions.txt', transaction_table.Course_encode, delimiter=" ", fmt="%s")
    print("ss5")


    
main()    


# In[134]:


def ProcessedBefore (processedSets, newSet):
    print('currentSet: ', newSet)
    print('processedSets: ', str(processedSets))
    replace = False
    for processedSet in processedSets:
        if processedSet == newSet:
            return True
        if newSet.issubset(processedSet):
            print(str(newSet), "is contained in: ", str(processedSet))
            return True
        elif processedSet.issubset(newSet):
            print('remove: ', str(processedSet), "is contained in: ", str(newSet))
            processedSet = 'None'
            replace = True
    
    processedSets.append(newSet)
#     if len(processedSets) == 0 or replace == True:
#         processedSets.append(newSet)

    print("finally: ", str(processedSets))

Experiment = "\SecondSemester"
DataFolder = "\data\\"
Path = r"C:\Users\mpouldou\Desktop\lcm" + Experiment + DataFolder

f = open(r'C:\Users\mpouldou\Desktop\lcm\out.txt', "r")
fw = open(r'C:\Users\mpouldou\Desktop\lcm\out_filtered.txt',"w+")
teaching_materials_path = Path + "materias_anonym_clean_filtered.csv"
df_teaching_materials = pd.read_csv(teaching_materials_path)
processedSets = []
while True:
    line = f.readline()
    transaction = line.split("#SUP:")[0]
    if len(transaction.split()) < 3:
        pass
    else:
        newLine = ""
        currentSet = set()
        for course in transaction.split():
            courseCode = df_teaching_materials.loc[df_teaching_materials['Course_encode'] == int(course)].iloc[0].COURSE_ID
#             print(courseCode.COURSE_ID)
#             newLine = newLine + str(course) + " "
            currentSet.add(int(course))
        ProcessedBefore(processedSets,  currentSet)
        print('*********')

        
    
    # check if line is not empty
    if not line:
        break
print("final Sets: ", processedSets)
for finalSet in processedSets:
    print("writing: ", str(finalSet))
    print("**************")
    newLine = ""
    for item in finalSet:
        courseCode = df_teaching_materials.loc[df_teaching_materials['Course_encode'] == int(item)].iloc[0].COURSE_ID
        newLine = newLine + str(courseCode) + " "
    fw.write(str(newLine)+"\r\n")
f.close()
fw.close()

