# Scala Programming for Data Science — Lab Exercises 13 to 19

This repository contains complete implementations and explanatory Colab notebooks for Scala Data Science Lab Exercises (13 to 19).

> 📄 **Lab Practical Report**: Download the comprehensive verified report for Exercises 13 to 17: [Scala_Lab_Exercises_13_to_17.pdf](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Scala_Lab_Exercises_13_to_17.pdf) (12 Pages with Aim, Theory, Verified Scala Code, Terminal Outputs, and Algorithmic Analysis).

---

## 📁 Repository Structure

| Exercise | Topic | Colab Notebook (`.ipynb`) | Standalone Scala Script (`.scala`) |
| :--- | :--- | :--- | :--- |
| **All Exercises** | **Master All-in-One Notebook** | [Scala_Data_Science_Lab_All_Exercises.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Scala_Data_Science_Lab_All_Exercises.ipynb) | — |
| **Ex 13** | **Arrays in Scala** | [Exercise_13_Arrays.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_13_Arrays.ipynb) | [Exercise_13_Arrays.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_13_Arrays.scala) |
| **Ex 14** | **Lists, Sets, & Tuples** | [Exercise_14_Lists_Sets_Tuples.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_14_Lists_Sets_Tuples.ipynb) | [Exercise_14_Lists_Sets_Tuples.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_14_Lists_Sets_Tuples.scala) |
| **Ex 15** | **HashMap Collisions & Conflicts**| [Exercise_15_HashMap_Collisions.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_15_HashMap_Collisions.ipynb) | [Exercise_15_HashMap_Collisions.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_15_HashMap_Collisions.scala) |
| **Ex 16** | **Functional Combinators** | [Exercise_16_Functional_Combinators.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_16_Functional_Combinators.ipynb) | [Exercise_16_Functional_Combinators.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_16_Functional_Combinators.scala) |
| **Ex 17** | **Case Classes** | [Exercise_17_Case_Classes.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_17_Case_Classes.ipynb) | [Exercise_17_Case_Classes.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_17_Case_Classes.scala) |
| **Ex 18** | **Saddle & Vegas** | [Exercise_18_Saddle_and_Vegas.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_18_Saddle_and_Vegas.ipynb) | [Exercise_18_Saddle_and_Vegas.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_18_Saddle_and_Vegas.scala) |
| **Ex 19** | **Breeze & Plotly.Scala** | [Exercise_19_Breeze_and_Plotly.ipynb](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_19_Breeze_and_Plotly.ipynb) | [Exercise_19_Breeze_and_Plotly.scala](file:///c:/Users/Rohan/Desktop/vit/SEM%201/Prog%20For%20Data%20Science/Prac/Exercise_19_Breeze_and_Plotly.scala) |

---

## 🚀 How to Run in Google Colab

1. **Open Google Colab**: Navigate to [colab.research.google.com](https://colab.research.google.com).
2. **Upload Notebook**: Click **Upload** and select any `.ipynb` file from this folder (or `Scala_Data_Science_Lab_All_Exercises.ipynb`).
3. **Setup Almond Scala Kernel**:
   Execute the first code cell in the notebook:
   ```bash
   !curl -Lo coursier https://git.io/coursier-cli && chmod +x coursier
   !./coursier launch --fork almond:0.13.14 --scala 2.13.12 -- --install
   ```
4. **Reload Kernel**:
   - Go to menu **Runtime** ➔ **Manage Sessions** ➔ terminate the active session (or simply reload your browser tab).
   - Reconnect to the runtime and select **Scala** as the kernel.
5. **Run All Cells**:
   - Click **Runtime** ➔ **Run all** (`Ctrl + F9`).
