# Expense Ease
#### Video Demo:  https://www.youtube.com/watch?v=XjgdkFEAbL0
#### Description:
Expense Ease is a basic budget tracker that tracks the users expense and income. It also gives a monthly anlaysis of the users income and expense through pie diagrams. The user can add their expense and income using various categories. They are also given the ability to add their own personal categories.
## Database
I created a database called budget.db that contains three tables. Users which stores the login information of the user. For the password hash method was used. Also the id of the users is autoincremented.
The info table contains the information about all the income and expense the user does. The expense and income each have different categories.
The third table made was categories. It keeps track of the categories a user has each in income and expense. As I have included the ability for users to include their own category I had to make a new table to ensure that a category added by one user does not add as a category in another users interface.
## Register
In register, I allowed the user to enter their basic username and password details along with some basic checks. If the entered data passes the checks, the user information is added into the users table. If it does not pass any condition then the problem gets printed on the same page as it is defined in the register.html page where the "if var is defined" syntax is used. Also they are added into the category table in which each user gets the pre decided categories to use. We also give the current session the value of the user's id.
## Login
The login page is pretty basic. Through login.html we get the users username and password. Then further it is checked if the the user info is present in the users table. If it is present the user is redirected to the homepage and the session is given the value of the users id.
## Logout
The session of the user is cleared and the user is redirected to the homepage.
## Homepage and layout.html
For designing the homepage and the basic layout I used the bootstrap themes. And the navigation bar (similar to the finance problem set) uses the list items depending on if the session id is present or not.
For homepage, I used an animation to display some text, where the colour of the text changes. Also some basic features of the application are specified on cards which were developed through the bootstrap theme.
## Income and expense
In the income and expense pages, the user enters the money he spent or gained in the form according to categories. The information is added to the info table. I was initially going to create two tables for income and expense respectively. However, I made one table named info itself and created a type column where the type of the transaction, that is 'income' or 'expense' is mentioned. I did this, because I wanted to print the entire budget history in the history page. Hence I made one table itself. After entering either the income or the expense, the user is redirected to the history page which makes sure that the info was added successfully.
For the html pages I passed the personalized categories of income and expense through the category table using the jinja template.
## Category
The category page has the simple task of adding the category. The page lets the user select if he wants to add a category to 'income' or 'expense'. Accordingly it is added to the category table along with the user id to add the category only for this user and not for others.
## History
The history page has two parts: history and analysis. The table in the history page gives information about all the expense and income according to the date. This is done by passing the info and using jinja template. Also the income rows are coloured green and the expense rows are coloured red. Also the total income and the total expense of the user is printed.
For the analysis, I used google charts. The user is allowed to select a month according to which a pie diagram for income and expense for that month according to criterias is made. For this, I had to learn how to pass the data into the javascript of the page and further had to learn more about google charts. Also in app.py I learnt strftime which sends a certain part of the date column which helped me send the data only of a particular month.
# This was ExpenseEase

