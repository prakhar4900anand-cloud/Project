# Statement of the Project

## Problem Statement
Users commonly create weak, predictable, or repeated passwords across multiple accounts, increasing the risk of security breaches. Many people struggle to generate strong passwords manually, and they lack a simple tool to help them create secure passwords and check their strength.  
This project aims to solve this problem by providing a Python-based application that can generate strong random passwords, evaluate the strength of any given password, and optionally save generated passwords for later reference.

## Scope of the Project
The scope of this project includes:
- A command-line based password generator tool.
- Configurable password generation options (length, uppercase, lowercase, digits, and symbols).
- A module to evaluate the strength of passwords based on length and character complexity.
- An optional module to save and view generated passwords using a simple file-based system.
- The project focuses on single-user usage and local execution without any networking or cloud storage.

The project does **not** include features like multi-user authentication, cloud sync, advanced encryption, or GUI interfaces (unless added as enhancement).

## Target Users
- Students and general users who need help creating secure passwords.
- Users who want to quickly generate strong passwords for websites, apps, or accounts.
- People who want a simple and safe way to evaluate the strength of any password.
- Beginners learning cybersecurity best practices or Python programming.

## High-Level Features
- **Secure Password Generation**  
  Generates random passwords based on user-selected settings such as length and character types.

- **Password Strength Evaluation**  
  Analyzes any password and rates it as Weak, Moderate, Strong, or Very Strong based on complexity.

- **Password Policy Configuration**  
  Allows users to customize password length and character inclusion options.

- **(Optional) Password Storage**  
  Saves generated passwords locally for future reference using simple file handling.

- **User-Friendly Menu System**  
  A clean console-based interface that guides users through generation, evaluation, and viewing features.
