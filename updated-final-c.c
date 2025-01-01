// #include <stdio.h>
// #include <string.h>
// #include <stdbool.h>
// #include <stdlib.h>
// #include <ctype.h>

// // Structure to hold user data
// typedef struct {
//     char course[50];
//     char branch[50];
//     char name[50];
//     char fatherName[50];
//     char motherName[50];
//     char dob[15];
//     char category[20];
//     char mobileNumber[20];
//     char religion[30];
//     //char rollNo[20];
//     char emailId[50];
// } Student;


// // Function to trim leading and trailing whitespace
// void trim(char *str) {
//     // Remove leading whitespace
//     int start = 0, end = strlen(str) - 1;
//     while (isspace(str[start])) start++;
    
//     // Remove trailing whitespace
//     while (end > start && isspace(str[end])) end--;
    
//     // Move the trimmed string to the beginning
//     int i;
//     for (i = 0; i <= end - start; i++) {
//         str[i] = str[start + i];
//     }
//     str[i] = '\0';
// }


// // Function to convert string to lowercase
// void to_lowercase(char *str) {
//     for (int i = 0; str[i]; i++) {
//         str[i] = tolower(str[i]);
//     }
// }

// // Function to clear the screen (cross-platform)
// void ClearScreen() {
// #ifdef _WIN32
//     system("cls");
// #else
//     system("clear");
// #endif
// }


// // Improved SearchInCSV function
// bool SearchInCSV(const char *filePath, const char *course, const char *branch, const char *name, Student students[], int *count) {
//     FILE *file = fopen("C:\\coding\\RKGIT\\hii\\NOW.csv", "r");
//     if (!file) {
//         printf("Error: Could not open the file.\n");
//         return false;
//     }

//     char line[512];
//     *count = 0;  // Initialize match count
    
//     // Skip the header row
//     if (!fgets(line, sizeof(line), file)) {
//         fclose(file);
//         return false;
//     }

//     // Prepare search terms by trimming and converting to lowercase
//     char courseTrimmed[50], branchTrimmed[50], nameTrimmed[50];
//     strcpy(courseTrimmed, course);
//     strcpy(branchTrimmed, branch);
//     strcpy(nameTrimmed, name);
//     trim(courseTrimmed);
//     trim(branchTrimmed);
//     trim(nameTrimmed);
//     to_lowercase(courseTrimmed);
//     to_lowercase(branchTrimmed);
//     to_lowercase(nameTrimmed);

//     while (fgets(line, sizeof(line), file) && *count < 100) {
//         Student temp = {0}; // Initialize all fields to zero/empty
        
//         char *token;
//         char lineCopy[512];
//         strcpy(lineCopy, line);
        
//         // Parse each field
//         token = strtok(lineCopy, ",");
//         if (!token) continue;
//         strncpy(temp.course, token, sizeof(temp.course) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.branch, token, sizeof(temp.branch) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.name, token, sizeof(temp.name) - 1);
        
//         // Continue parsing other fields
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.fatherName, token, sizeof(temp.fatherName) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.motherName, token, sizeof(temp.motherName) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.dob, token, sizeof(temp.dob) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.category, token, sizeof(temp.category) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.mobileNumber, token, sizeof(temp.mobileNumber) - 1);
        
//         token = strtok(NULL, ",");
//         if (!token) continue;
//         strncpy(temp.religion, token, sizeof(temp.religion) - 1);
        
//         // token = strtok(NULL, ",");
//         // if (!token) continue;
//         // strncpy(temp.rollNo, token, sizeof(temp.rollNo) - 1);
        
//         token = strtok(NULL, "\n");
//         if (!token) continue;
//         strncpy(temp.emailId, token, sizeof(temp.emailId) - 1);

//         // Trim all fields
//         trim(temp.course);
//         trim(temp.branch);
//         trim(temp.name);

//         // Convert to lowercase for case-insensitive comparison
//         char tempCourse[50], tempBranch[50], tempName[50];
//         strcpy(tempCourse, temp.course);
//         strcpy(tempBranch, temp.branch);
//         strcpy(tempName, temp.name);
//         to_lowercase(tempCourse);
//         to_lowercase(tempBranch);
//         to_lowercase(tempName);
//         // Case-insensitive comparison
//         if (strcmp(tempCourse, courseTrimmed) == 0 && 
//             strcmp(tempBranch, branchTrimmed) == 0 && 
//             strcmp(tempName, nameTrimmed) == 0) {
            
//             // Copy matched student to results
//             students[*count] = temp;
//             (*count)++;
//         }
//     }

//     fclose(file);
//     return (*count > 0);
// }

// // Function to display student data
// void DisplayStudentData(const Student *student) {
//     printf("Course: %s\n", student->course);
//     printf("Branch: %s\n", student->branch);
//     printf("Name: %s\n", student->name);
//     printf("Father's Name: %s\n", student->fatherName);
//     printf("Mother's Name: %s\n", student->motherName);
//     printf("Date of Birth: %s\n", student->dob);
//     printf("Category: %s\n", student->category);
//     printf("Mobile Number: %s\n", student->mobileNumber);
//     printf("Religion: %s\n", student->religion);
//     //printf("Roll No: %s\n", student->rollNo);
//     printf("Email ID: %s\n", student->emailId);
// }

// // Main function
// int main() {
//     char course[50], branch[50], name[50];
//     Student students[100]; // Array to store up to 100 matching records
//     int count = 0;

//     // Get the course, branch, and name from the user
//     printf("Enter Course: ");
//     fgets(course, sizeof(course), stdin);
//     course[strcspn(course, "\n")] = 0; // Remove newline character

//     printf("Enter Branch: ");
//     fgets(branch, sizeof(branch), stdin);
//     branch[strcspn(branch, "\n")] = 0; // Remove newline character

//     printf("Enter Name: ");
//     fgets(name, sizeof(name), stdin);
//     name[strcspn(name, "\n")] = 0; // Remove newline character

//     ClearScreen();

//     // Search for matching records
//     if (SearchInCSV(NULL, course, branch, name, students, &count)) {
//         printf("Found %d matching record(s)\n", count);
//         for (int i = 0; i < count; i++) {
//             printf("\n--- Record %d ---\n", i + 1);
//             DisplayStudentData(&students[i]);
//         }
//         getchar(); // Wait for user input
//     } else {
//         printf("No matching records found.\n");
//     }

//     return 0;
// }



#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <stdlib.h>
#include <ctype.h>

// Structure to hold user data
typedef struct {
    char course[50];
    char branch[50];
    char name[50];
    char fatherName[50];
    char motherName[50];
    char dob[15];
    char category[20];
    char mobileNumber[20];
    char religion[30];
    char emailId[50];
} Student;

// Function to trim leading and trailing whitespace
void trim(char *str) {
    int start = 0, end = strlen(str) - 1;
    while (isspace(str[start])) start++;
    while (end > start && isspace(str[end])) end--;
    for (int i = 0; i <= end - start; i++) {
        str[i] = str[start + i];
    }
    str[end - start + 1] = '\0';
}

// Function to convert string to lowercase
void to_lowercase(char *str) {
    for (int i = 0; str[i]; i++) {
        str[i] = tolower(str[i]);
    }
}

// Search function with fixed file handling and logic
bool SearchInCSV(const char *filePath, const char *course, const char *branch, const char *name, Student students[], int *count) {
    FILE *file = fopen("C:\\coding\\RKGIT\\Hii\\NOW.csv", "r");  // Use the provided file path
    if (!file) {
        printf("Error: Could not open the file at path: %s\n", filePath);
        return false;
    }

    char line[512];
    *count = 0;

    // Skip the header row
    if (!fgets(line, sizeof(line), file)) {
        fclose(file);
        return false;
    }

    // Prepare search terms
    char courseTrimmed[50], branchTrimmed[50], nameTrimmed[50];
    strcpy(courseTrimmed, course);
    strcpy(branchTrimmed, branch);
    strcpy(nameTrimmed, name);
    trim(courseTrimmed);
    trim(branchTrimmed);
    trim(nameTrimmed);
    to_lowercase(courseTrimmed);
    to_lowercase(branchTrimmed);
    to_lowercase(nameTrimmed);

    // Process each line
    while (fgets(line, sizeof(line), file) && *count < 100) {
        Student temp = {0};
        char *token = strtok(line, ",");
        if (token) strncpy(temp.course, token, sizeof(temp.course) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.branch, token, sizeof(temp.branch) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.name, token, sizeof(temp.name) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.fatherName, token, sizeof(temp.fatherName) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.motherName, token, sizeof(temp.motherName) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.dob, token, sizeof(temp.dob) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.category, token, sizeof(temp.category) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.mobileNumber, token, sizeof(temp.mobileNumber) - 1);
        token = strtok(NULL, ",");
        if (token) strncpy(temp.religion, token, sizeof(temp.religion) - 1);
        token = strtok(NULL, "\n");
        if (token) strncpy(temp.emailId, token, sizeof(temp.emailId) - 1);

        // Trim and prepare for comparison
        trim(temp.course);
        trim(temp.branch);
        trim(temp.name);

        char tempCourse[50], tempBranch[50], tempName[50];
        strcpy(tempCourse, temp.course);
        strcpy(tempBranch, temp.branch);
        strcpy(tempName, temp.name);
        to_lowercase(tempCourse);
        to_lowercase(tempBranch);
        to_lowercase(tempName);

        // Match logic
        if (strcmp(tempCourse, courseTrimmed) == 0 &&
            strcmp(tempBranch, branchTrimmed) == 0 &&
            strcmp(tempName, nameTrimmed) == 0) {
            students[*count] = temp;
            (*count)++;
        }
    }

    fclose(file);
    return (*count > 0);
}
//Function to display student data
void DisplayStudentData(const Student *student) {
    printf("Course: %s\n", student->course);
    printf("Branch: %s\n", student->branch);
    printf("Name: %s\n", student->name);
    printf("Father's Name: %s\n", student->fatherName);
    printf("Mother's Name: %s\n", student->motherName);
    printf("Date of Birth: %s\n", student->dob);
    printf("Category: %s\n", student->category);
    printf("Mobile Number: %s\n", student->mobileNumber);
    printf("Religion: %s\n", student->religion);
    //printf("Roll No: %s\n", student->rollNo);
    printf("Email ID: %s\n", student->emailId);
}

// Main function
int main() {
    char course[50], branch[50], name[50];
    Student students[100]; // Array to store up to 100 matching records
    int count = 0;

    // Get the course, branch, and name from the user
    printf("Enter Course: ");
    fgets(course, sizeof(course), stdin);
    course[strcspn(course, "\n")] = 0; // Remove newline character

    printf("Enter Branch: ");
    fgets(branch, sizeof(branch), stdin);
    branch[strcspn(branch, "\n")] = 0; // Remove newline character

    printf("Enter Name: ");
    fgets(name, sizeof(name), stdin);
    name[strcspn(name, "\n")] = 0; // Remove newline character

    //ClearScreen();

    // Search for matching records
    if (SearchInCSV(NULL, course, branch, name, students, &count)) {
        printf("Found %d matching record(s)\n", count);
        for (int i = 0; i < count; i++) {
            printf("\n--- Record %d ---\n", i + 1);
            DisplayStudentData(&students[i]);
        }
        getchar(); // Wait for user input
    } else {
        printf("No matching records found.\n");
    }

    return 0;
}
