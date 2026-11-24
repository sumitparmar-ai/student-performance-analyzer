import numpy as np

# Student names
students = [
    "Rahul", "Aman", "Priya", "Rohit", "Sneha",
    "Karan", "Anjali", "Vikas", "Neha", "Arjun"
]

# Subject names
subjects = [
    "Maths", "Science", "English", "Physics", "Chemistry"
]

# Student marks dataset
array = np.array([
    [89, 90, 88, 68, 76],
    [76, 88, 85, 46, 55],
    [80, 82, 90, 50, 60],
    [33, 45, 40, 20, 30],
    [32, 40, 35, 88, 25],
    [45, 50, 48, 25, 35],
    [40, 45, 42, 22, 32],
    [35, 40, 38, 18, 78],
    [30, 35, 32, 16, 24],
    [25, 30, 28, 14, 22]
])

# Dataset information
print("Dataset Shape:", array.shape)
print("Total Students:", len(students))
print("Total Subjects:", len(subjects))

# Student-wise calculations

total_marks = array.sum(axis=1)
average_marks = array.mean(axis=1)
highest_marks = array.max(axis=1)
lowest_marks = array.min(axis=1)

print("\nStudent-wise Analysis")

for i in range(len(students)):
    print(f"\nStudent: {students[i]}")
    print("Total Marks:", total_marks[i])
    print("Average Marks:", round(average_marks[i], 2))
    print("Highest Marks:", highest_marks[i])
    print("Lowest Marks:", lowest_marks[i])

# Percentage calculation

percentage = (total_marks / 500) * 100

print("\nStudent Percentage:")

for i in range(len(students)):
    print(students[i], ":", round(percentage[i], 2), "%")


# Pass or Fail

print("\nStudent Result:")

for i in range(len(students)):
    if percentage[i] >= 40:
        status = "Pass"
    else:
        status = "Fail"

    print(students[i], ":", status)


# Subject-wise analysis

subject_average = array.mean(axis=0)
subject_highest = array.max(axis=0)
subject_lowest = array.min(axis=0)

print("\n========== SUBJECT-WISE ANALYSIS ==========")

for i in range(len(subjects)):
    print(f"\nSubject: {subjects[i]}")
    print("Average Marks:", round(subject_average[i], 2))
    print("Highest Marks:", subject_highest[i])
    print("Lowest Marks:", subject_lowest[i])

    # Subject-wise toppers

subject_toppers = np.argmax(array, axis=0)

print("\n========== SUBJECT TOPPERS ==========")

for i in range(len(subjects)):
    student_index = subject_toppers[i]

    print(
        f"{subjects[i]} Topper: "
        f"{students[student_index]} - {array[student_index, i]} marks"
    )

# https://github.com/sumitparmar-ai/student-performance-analyzer.git