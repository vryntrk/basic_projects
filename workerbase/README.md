SUMMARY
Workerbase combines Python's file I/O operations and data science techniques to manage worker 
information and operate its own text-based database.
All operations depend on interactive Y/N prompts.

*** add.py checks if database file exists. If not, the function creates a file with the appropriate
headers. Then, it creates a unique 6-digit ID for each worker and starts asking for worker information.
At every step, it validates the input format. The worker is added to the file unless there is a mistake.
---RULES---
1) Age must be between 18 and 99.
2) Gender must be entered as 'male' or 'female'.
---EXTRAS---
The function allows to add a name or surname consisting of more than one word (e.g. 'Wolfgang Amadeus', 'Van Gogh').

*** find.py checks the file corruption and existence. If there is a problem it displays a warning.
---CATEGORIES---
1) Displaying all workers.
2) Find by name. e.g. searching for the name 'Can' displays both 'Ali Can' and 'Alican'.
3) Find by surname. It displays just the exact matches. e.g. user cannot see 'Van Gogh' by typing 'Van'.
4) Classifying by age(s). It allows custom age range. User must ensure the minimum age is not greater than the maximum age and 18 to 99 rule.
5) Gender filter. User must enter the gender as 'male' or 'female'.

*** remove.py checks the file corruption and existence similar to 'find.py'. If there is a problem it
warns the user. User has to enter a part of the name of the worker which will be removed. Then, it
displays appropriate ones on terminal and asks for worker's ID to remove the worker.
---EXTRAS---
User can cancel the operation by typing 'cancel' at both the name and ID sections.

*** edit.py checks the file corruption and existence similar to 'find.py'. If there is a problem it
warns the user. edit.py benefits from find.py to display the worker who being searching for. Also, it
prevents data corruption. It takes worker's ID and asks for the field which will be changed. If
there is no problem with rules the function updates the database file.
---EXTRAS---
User can cancel the operation by typing 'cancel' at ID section or by typing '5' at category section.

REQUIREMENTS
Pandas Library