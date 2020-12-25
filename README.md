# Smart Manager
Manage payments on Smart Fluent

The Smart Manager is a system designed to help the payments at Smart Fluent. The Smart Fluent is a local business (in which I work) in the countryside of Pernambuco in Brazil that provides English courses at affordable prices.

## How the payments are done on Smart Fluent

The Smart Fluent is a small business in the region that cannot afford to pay the workers with a local basic wage, which is roughly $200,00 US dollars. So the workers are paid accordingly to the student's payment.

1. After the student's payment it will be discounted fixed values which are destined to afford the **maintenance** of the business (like paper, ink for the printers, household products, and so on). After that will be discounted values to pay the receptionist and coordinator.
2. Next, each professor will receive a percentage of each student that he or she teaches. And the rest of the money is categorized as the profit of the business.
3. The student may also be a scholar, in which the student will pay only a fraction of the common value. In this case, the professor will not receive anything from this student's payment.

## How the database is structured
The database is structured using six different tables:

1. **professors**: which will hold the *id* and the *name* of each professor.
2. **students**: will take an *id* (different from the professor id), a *name*, and also will take a *scholarship* attribute that will store if the student is a scholar or not.
3. **courses_prices**: this will handle the *id* of the course, it's *description* and their *value* as well.
4. **wages**: this table will handle all the wages payments that have been made. it will take an *id*, a *description*, and a *value*.
5. **classes**: This table will link students and professors, to keep track of which professor teaches to which student. This table will take a *professor_id* and a *student_id*.
6. **payments**: finally the payments table, will handle (obviously) all the payments that have been made by the students. this table will get a *student_id*, a *data_paid* to keep track of the actual monthly payments, a *value* which will get this value from the **courses_prices** table, and a *payment_datetime* attribute to handle the dates in which the payments were done.

## What technologies are used in the project
This project will be used: **Sqlite** to create the database and manage all the queries; will also be used the **Flask** framework and the **Python** language to handle the server; and of course **HTML**, **CSS** and **JavaScript**.
