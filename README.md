# Smart Manager

Smart Manager is a system designed to help the payments at Smart Fluent. The Smart Fluent is a local business (in which I work) in the countryside of Pernambuco in Brazil that provides English courses at affordable prices.

## How the payments are done on Smart Fluent
Smart Fluent is a small business in the region that cannot afford to pay the workers with local basics wages, which are roughly $200,00 US dollars. So the workers are paid accordingly to the student's payment.

1. After the student's payment it will be discounted fixed values which are destined to afford the **maintenance** of the business (like paper, ink for the printers, household products, and so on). After that will be discounted values to pay the receptionist and coordinator.
2. Next, each professor will receive half of each student that he or she teaches. And the rest of the money is categorized as the profit of the business.
3. The student may also be a scholar, in which the student will pay only a fraction of the common value. In this case, the professor will also receive half of the value.

## How the database is structured
The database is structured using four different tables:

1. **professors**: which will hold the *id* and the *name* of each professor.
2. **students**: will take an *id* (different from the professor id), a *name*, a *professor_id*, and a *monthly payment*. Finally it will also store a *scholar* attribute that will store if the student is a scholar or not.
3. **expenses**: this table will handle all the fixed expenses in business, like the maintenance, and also the coordinator, and the receptionist payments. it will take a *description*, and a *value*.
4. **payments**: The payments table, which will handle (obviously) all the monthly payments that were done by students. This table will get as attributes: an *id*, a *date_payment*, a *student_id*, a *teacher_id*, a *month* and a *year*

## What technologies are in the project
This project will use: **SQLite** to create the database and manage all the queries; will also be used the **Flask** framework and the **Python** language to handle the server; and of course **HTML**, **CSS** and **JavaScript**.

## Milestones
Here we have some future goals for this project:

* Refactoring some SQLite code and also refactoring the database structure to be more scalable.
* Adding more UI features, and more UX improvements.
