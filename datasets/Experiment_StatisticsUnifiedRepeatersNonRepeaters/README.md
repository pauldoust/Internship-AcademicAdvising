This folder contains the following:
	1) C_LOAD: contains the number of courses taken together by student, year, semester which represents the semester load for each student in specific year, semester
	2) COURSE_CREDITS: contains the credits for each course, it was scarpped from spol university website using python crawler(please check software/crawler.py)
	3) Courses_difficulties: contains the course difficulty parameters for each course. The parameter are alpha, beta (please check gonzalo mendez paper). the code is included in (software/main_script.py_
	4) dataset_stats_flow_ready_unified_features: the dataset contains all previous files merged and joined for each student. In other words, we have student features for statistics along with difficulty estimators, semester load and sum of credits of those courses taken at a given semester:
		
		4.1) "('amax', 'ICM00166')": the max achieved grade in course 'ICM00166' which should represents his passing and latest grade.
		4.2) "('PrevLatestGrade', 'ICM00166')": the direct previous mark achieved in 'ICM00166', if he is not a repeater, the average is filled
		4.3) "('count', 'ICM00166')": the number of times 'ICM00166' is taken before
		4.4) "C_LOAD": semester load at the time of statistics (target course)
		4.5) "alpha": the product of alphas for each course taken at the target course's semester
		4.6) "beta": the sum of betas for courses taken at the target course's semester
		4.7) "Course_Theoritical_Credits": the sum of theoritical credits taken at the target course's semester
		4.8) "Course_Practical_Credits": the sum of practical credits taken at the target course's semester
