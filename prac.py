# Topics covered:
# - Array creation: np.array(), zeros(), ones(), full()
# - arange(), linspace()
# - Random arrays
# - Array attributes: shape, ndim, size, dtype
# - Indexing and slicing
# - Reshaping: reshape(), flatten()
# - Mathematical operations
# - Aggregation: sum(), mean(), min(), max()
# - Axis operations
# - Boolean masking and filtering
# - Sorting

# Features to build:
# 1. Store marks of 10 students in 5 subjects.
# 2. Calculate subject-wise average.
# 3. Find highest and lowest marks.
# 4. Identify students scoring above 80.
# 5. Calculate total and percentage.
# 6. Rank students based on performance.


import numpy as np

array = np.array([
    [89, 90, 88, 68, 76],
    [76, 88, 85, 46, 55],
    [80, 82, 78, 50, 60],
    [33, 45, 40, 20, 30],
    [32, 40, 35, 15, 25],
    [45, 50, 48, 25, 35],
    [40, 45, 42, 22, 32],
    [35, 40, 38, 18, 28],
    [30, 35, 32, 16, 24],
    [25, 30, 28, 14, 22]
])

print(array)
print(array.shape)
print(array.ndim)
print(array.size)


print(array.sum(axis=0)) # subject-wise total
print(array.sum(axis=1)) # student-wise total
print(array.mean(axis=1)) # student-wise average
print(array.max(axis=0)) # subject-wise highest marks
print(array.max(axis=1)) # student-wise highest marks
print(array.min(axis=0)) # subject-wise lowest marks
print(array.min(axis=1)) # student-wise lowest marks

print(array > 50)
print(array[array > 50]) # students scoring above 50

avg = array.mean(axis=1)
print(avg)

print(avg >= 40) # students scoring above 40

# to check pass or fail

for i in range(len(avg)):
    if avg[i] >= 40:
        print(f"student {i+1} is passed")
    else:
        print(f"student {i+1} is failed")

# to check the highest marks
total_marks = array.sum(axis = 1)
print(total_marks)

# print(total_marks.argmax())

# # topper details
# topper_index = total_marks.argmax()
# print(f"Topper is student {topper_index + 1}")
# print(f"Topper marks are {total_marks[topper_index]}")

# # Ranking
# ranking = array.argsort(total_marks)[::-1]
# print("Student ranking:")

# for index in enumerate(ranking):
#     print(f"Rank {i+1}: Srudent {index+1} - {total_marks[index]} marks")

ranking = np.argsort(total_marks)[::-1]
print(ranking)
# print("Student Ranking:")

# for i, index in enumerate(ranking):
#     print(f"Rank {i+1}: Student {index+1} - {total_marks[index]} marks")


# # Topper in each subject:

# # total_sub_marks = array.argmax(axis=0)
# # print(total_sub_marks)
# # topper_subjects = array.argmax(axis=0)
# # print("Topper in each subject:")
# # for i, index in enumerate(topper_subjects):
# #     print(f"Topper in subject - Maths: Student{index+1} - {total_marks[index]}")

# subject_toppers = np.argmax(array, axis=0)
# print(subject_toppers)

# subjects = ["Maths", "Science", "English", "Physics", "Chemistry"]

# for i in range(len(subjects)):
#     student_index = subject_toppers[i]
#     highest_marks = array[student_index, i]

#     print(f"{subjects[i]} Topper: Student {student_index+1} - {highest_marks} marks")

# # Final Report

# for i in range(len(array)):
#     print("Student:",i+1)
#     print("Total:",total_marks[i])
#     print("Average:",avg[i])

import numpy as np

# Student-wise calculations
total_marks = array.sum(axis=1)
average_marks = array.mean(axis=1)
highest_marks = array.max(axis=1)
lowest_marks = array.min(axis=1)

# Ranking system
ranking = np.argsort(total_marks)[::-1]

print("========== STUDENT PERFORMANCE REPORT ==========")

for i in range(len(array)):

    if average_marks[i] >= 40:
        status = "Pass"
    else:
        status = "Fail"

    # Find student's rank
    rank = list(ranking).index(i) + 1

    print(f"\nStudent {i+1}")
    print("Total Marks:", total_marks[i])
    print("Average Marks:", round(average_marks[i], 2))
    print("Highest Marks:", highest_marks[i])
    print("Lowest Marks:", lowest_marks[i])
    print("Status:", status)
    print("Rank:", rank)

print("\n================================================")