**Quiz App**
This project is a Python-based quiz application with a graphical user interface (GUI), using PySide2 for GUI components and Firebase for backend data storage and retrieval. The application allows users to select a question bank, take quizzes, and view their results.

**Features**
Startup Window: A launch window where users can select a question bank to start the quiz.
Quiz Interface: A user-friendly interface to display questions and answer choices.
Question Navigation: Users can navigate through different questions using the next and previous buttons.
Result Calculation and Display: The application calculates the score at the end of the quiz and displays the results.
Firebase Integration: Utilizes Firebase for storing quiz data and user results.
User Preferences: Stores and retrieves user preferences, such as username and selected question bank.
Error Handling: Displays error messages if necessary files or data are not found.

**Getting Started**

**Prerequisites**
Python 3.x
PySide2
Firebase Admin SDK
Installation
Clone the repository:


git clone https://github.com/your_username_/QuizApp.git
Install the required packages:

pip install PySide2 firebase-admin
Set up Firebase:

Create a Firebase project.
Download the Firebase Admin SDK service account key.
Update the credentials.json path in the script.
Run the application:


**Usage**
Upon launching the application, select a question bank from the dropdown menu and click the 'Start Quiz' button. Answer the quiz questions and navigate using the 'Next' and 'Previous' buttons. Submit your answers to view your score. Results will be uploaded to Firebase for record-keeping.

**Contributing**
Contributions to enhance the Quiz App are welcome. Feel free to fork the repository and create a pull request with your improvements. You can also open an issue for bugs, suggestions, or feature requests.

License
This project is licensed under the MIT License - see the LICENSE file for details.

Acknowledgments
Thanks to the PySide2 team for the GUI toolkit.
Firebase Admin SDK for backend storage and retrieval functionalities.
