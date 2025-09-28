README – Caspar Ashworth FYP
Project Title: Development of a Smart Sports-Specific Workout Generator Using Optimization Algorithms
Student ID: 2010518
Course: BSc (Hons) Computer Science – Brunel University London
Submission Date: 09 April 2025

Project Summary
This project is a Python-based application that generates personalised, sport-specific gym workout plans using optimization algorithms. It aims to provide accessible, algorithmically designed training for users based on their sport, fitness level, preferences, and constraints (e.g., injuries).

The application uses one of the following algorithms:
- Genetic Algorithm (GA)
- Simulated Annealing (SA)
- Ant Colony Optimization (ACO)

User feedback is integrated into the system using a Large Language Model (LLM), which extracts and applies constraints such as preferred/avoided muscle groups or exercises.

How to Run the Program

Requirements
- Python 3.10+
- Required libraries:
  - tkinter / customtkinter
  - openai
  - sqlite3
  - numpy
  - pandas
  - pytest (for testing)

Installation
1. Clone or unzip the project files.
2. Navigate to the project folder.
3. Ensure your environment includes the required libraries (`pip install -r requirements.txt` if needed).
4. Launch the application via:

python gui.py

LLM Integration
This project uses OpenAI's GPT-4o for:
- Processing user feedback into constraints (llmConstraints)
- Evaluating the quality of workout plans (llmAsAJudge)

My API key is no longer attached and has been disabled from my OpenAI account due to this now being made public on GitHub, if you wish to test the LLM intergration then fill in the sace on line 14 of main with a key.

Video Demonstration
A full walkthrough of the GUI, backend, and plan generation is available here:
https://youtu.be/HwgPNBeuX1Y

(Also referenced in Appendix C of the dissertation.)

Testing
To run unit tests:
pytest unitTestMain.py

To profile algorithms:
python parameterTestMain.py

Submission Notes
All files in this ZIP are submitted as supporting material for my final-year project and are referenced in the accompanying dissertation. No real personal data is used; all generated data is synthetic.
