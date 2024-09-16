Capstone Management Project



By James Chen, Max Xiong Andy Wang, Jaeyoung (Jennifer) Sung, Mathew Stepfner and Tristan Fischer




(a) Installation Manual
1. Commands to run Capstone Compass
        Clone the project's code repository, run docker-compose up postgres to build the database, then run docker-compose up frontend. Now the application should be available at localhost:3000
2. Environment variables and secrets.        
A default admin account is automatically inserted into the database when it is built. This is available inside the backend/projdb.sql file.
        The username and password required to launch a direct psql session are available inside the docker-compose file.
        The backend servers host address and running ports are present inside the docker-compose.yml file. These variables are also redefined inside backend/dockerfile and the backend/server.py file.
        The email address that the application uses to send emails is defined in backend/server.py.
        The key used for encoding and decoding JWT tokens is visible inside the backend/authentication.py.
(b) System Architecture Diagram
Frontend Components
The frontend of the system is built using React, consisting of several main components that each handle specific parts of the UI and user interactions:
Dashboard Components:
* Dashboard: The main user dashboard provides different views and functionalities based on the user role (e.g. student, tutor, coordinator, admin and client). The dashboard component handles routing to different sections of the application based on the user role.
Admin Components:
* Admin: This component is responsible for managing administrative tasks that include subcomponents such as ‘ManageSkills’ and ‘ManageProjects’, which allow the admin to manage skills and projects respectively.
* ManageSkills: Handles the creation and management of skills
* ManageProjects: Handles the creation and management of projects
User Components:
* Profile: Manages user profile, including fetching and updating user data, managing user-specific skills and preferences.
Project Components:
* ProjectDetailsModal: Displays detailed information about a project, allowing clients to edit project details and manage associated skills.
* Projects: Lists all the projects, including functionality for managing projects
* CreateProject: Provides a form for creating new projects
Group Components:
* CreateGroup: Provides a form for creating new groups
* Groups (GroupIn, GroupNotIn, GroupRequests): Manage groups and requests, displaying different states and actions related to groups. 
Misc Components:
* Home: Handles user login and initial setup
* Modal: A reusable component for displaying modal throughout the application
* Register: Handles user registration
* Reset: Manages password reset functionality
* Utils: Utility components like ‘BackButton’ and ‘LogoutButton’
* NotificationBox: Displays notifications


Data Flow
1. User Inputs: Users will interact with the frontend components through forms and buttons. These interactions trigger methods to fetch or send data.
2. Routing: Based on the user role, different components are rendered to provide a tailored experience for each type of user (admin, student, client, tutor)
3. Frontend to backend: The frontend component makes API calls to the backend (e.g. fetchSkills, handleCreateProject). Data is sent as JSON or form data.
4. State Management: The state in frontend components is updated based on user interactions and backend responses to ensure a dynamic and responsive user experience.
5. The backend receives http requests and then formats them into sql commands to pull or push data to the database
6. The backend then returns debug data and return data as json back to the frontend for displaying
Front-end UML Diagram  






________________


Front-end UML Diagram cont.  
Backend dataflow  


  Database  




(c) Design Justifications
Frontend Design
Initially, the front-end design was structured around a basic user interface with limited functionalities. The primary components included a dashboard for each user role, project, group and profile management. 
During the development process, feedback from the client and our own realisation of unrealistic designs highlighted several issues:
* Users found the initial navigation structure confusing due to the placement of certain buttons. This feedback prompted us to add labels and reorganise the navigation for better clarity.
* There was a need for more intuitive modals for viewing and editing details as the initial design lacked user-friendly modals, which made data management difficult.
* Feedback also pointed out the overall design’s lack of dynamism and the absence of real-time validation and feedback. Hence, it led us to adopt a more cohesive theme and introduce dynamic backgrounds, especially on the home page.
In response to the feedback, we made several significant changes to the frontend design:
Dashboard design changes:
The dashboard was redesigned to provide a more user-friendly interface. The new design features a clearer layout with better separation of functionalities based on user roles. Each user role now has a tailored dashboard displaying relevant information and actions. Further, by dynamically loading components specific to the user’s role, we ensure that users see only the information and actions related to them, enhancing the overall user experience.  
        Routing Methods for Efficiency:
The routing methods were restructured to improve efficiency and user experience. By utilising React Router, we implemented client-side routing, which allowed for smoother transitions between pages without full page reloads. 
        Separation of Components:
User profile and group management functionalities were separated into distinct components (Profile, Groups, GroupIn, GroupNotIn, and GroupRequests). The separation of components improved code maintainability and allowed for more focused development of each functionality. Further, components were grouped logically to ensure the codebase was organised and easier to navigate. 
        Dynamic Theming:
We adopted a dynamic theme for the home page, including a moving sea-themed background. This change made the design more visually appealing and also provided a more engaging user experience. 
        Skill Management:
For students to add skills to their profile and clients to add skills to their projects, we implemented a user-friendly method where skills can be added or removed by simply clicking on them. This design choice was based on feedback requesting easier skill management. For example, the ‘Profile ’component fetches and displays a list of available skills and user-specific skills. Clicking on a skill adds it to the user's profile, while clicking on a listed skill removes it. This interaction model simplifies skill management, making it more intuitive for users.


Complex Components:
Dashboard: The ‘Dashboard’ component is dynamic and adapts based on the user role. This required sophisticated state management to ensure the correct components and data were loaded for each user type. Conditional rendering and hooks like ‘useEffect()’ and ‘useState()’ were extensively used to manage these dynamic aspects. Additionally, context-based state management was implemented for better scalability and maintainability.
ProjectDetailsModal: ‘ProjectDetailsModal’ component handles both the display and editing of project details. It includes multiple states for managing edit modes, form inputs, and validation errors. The component fetches project data when opened and updates it in real-time as users make changes. Error handling and feedback mechanisms were included to improve user experience.
Forms: The CreateProject and CreateGroup components were implemented with forms providing real-time feedback to users. Simple state management using React's ‘useState()’ and form handling logic were used to manage form state and validation directly within the components. Custom hooks were used to manage field-specific states and validations, making the forms modular and reusable.


Backend Components
Authentication
Users can create and access their accounts in a safe and secure manner as passwords are hashed then stored into the database and JSON Web Token’s are implemented to authenticate the user. Each users will be allows to manage and edit basic information such as their names and reset their passwords after providing a unique 6 digit code which will be emailed to them when the request is made. Each user role has unique permissions and features with administrator accounts having the most permissions and students being the default role that is assigned upon registration. Initially, we wanted to implement a feature that would allow users to update other users roles, for example tutors having the ability to change a user from a student to tutor, a coordinator having the ability to change a user to a student, tutor or coordinator. However, we later modified that feature to only administrators having the ability to update roles with as we identified that it could potentially create an array of security and integrity concerns. Having an administrator over see all these changes would allow for a safer and more enjoyable user experience.
Groups
All users can create a group with the creator as the group owner and view other groups if not already in a group. The reason to have a group owner in our design is to help to improve our join request system in our initial design. On the forum of this course COMP3900, we have identified many posts saying some random user has joined their group without notifying, or some user joins a pre-formed group making the admins have to manually remove that user which is very inconvenient. Our design of the join request system will brilliantly resolve this issue, where all users can send a join request to a group, and the group owner has the ability to accept/decline the request. This resolves the issue by helping out students with preformed groups to more easily monitor their members, and more importantly, it also helps students who don’t have a group to send multiple join requests to find a group which improves from the current system where students are uncertain if a group still requires members.  The only downside to this design is that the group owner might not be able to see the join request and handle them in time. Therefore, based on this initial design, we decided to also send a notification to the group owner when a join request is made to that group. In addition, all users in the group can see the join request (but no privilege to handle) so that they can remind the group owner to help improve this issue. 
Projects
Client users can create and edit their projects, which is much more flexible than submitting projects to the course and then releasing static copies to students. Meanwhile, we allow coordinators and admins to create projects for clients, so that they can assert clients that are not familiar with the system. In the worst case, admin can create the project on the behalf of the client.
Students can view all the projects, but clients can only see their own project. This is for students to decide which projects they are interested in.
Initially only clients can be project owners. Based on the demand that the admin wants to demonstrate how to create a project, so we permitted him to be a project owner as well.
Channel and messages
Our proposal pinpointed the unpleasantness of relying on external chats. The system we developed has built-in channels for both groups and projects, offering students and clients efficient communication channels. We modified it such that tutors can monitor the chat and facilitate the progression.
Channels are created automatically along with groups and projects to reduce the overhead of managing the system.
Admin can send messages on the behalf of others. This can be convenient in scenarios like the course wants to make announcements to all projects as clients. 
While users are automatically added to and removed from the channel when they join and leave group/project, admin can manually add and remove users in channels. This adds an extra layer of flexibility to our system.
Skills
Skills are created by the course and selected by students and project owners. Matched skills will then be weighted in our algorithm of assigning projects to groups.
We decided to have the course to determine the skills rather than students coming up their owns, so that the allocation algorithm makes the maximal utility out of skills matching. 
Preferences
In our design for preference, we made all students able to select their own preference list instead of just making a group preference. This allows all students to express their own interest, and everyone can make their own vote if there are diversified opinions on project selection. We initially planned to do a group preference, but we found that this design is more flexible. If a group is well communicated with an agreed preference list, they can still let only one user have a preference list (like what we have now) or let multiple users select the same ordered preferences, which will function the same as what we have for this course.
Automatic Allocation Algorithm
To assign projects to each group we wanted to improve the experience for both groups and administrators we decided the best way to do so would be to implement an automatic project allocation system, doing some brainstorming we figured the best approach would be one that isn't too complicated so that it can run fast even with a large amount of projects and groups, we decided on using an application of assignment problem, by using the sum of skills within a group and the average preferences of the group we can construct a matrix which indicates how good a match each project is for each group, we can then use the assignment problem to find the optimal solution so that all groups receive the best possible project with as little compromise as possible, to perform this process we used Scipys solver for the linear assignment problem called scipy.optimize.linear_sum_assignment which utilizes Numpys optimized matrices to perform the solution quickly. These projects are then automatically assigned to each group.
Notifications
Notifications are essential for users to get attention to important information. We initially followed the project requirements which sends a notification when there is a message, project update and allocation. Furthermore, as mentioned in the section for groups, we decided to also send a notification to the group owner when a join request is sent, and to the applicant when the request is handled (accepted/rejected). In terms of implementation, we added the send notification directly into the functions which triggers sending notification, and we also added server routes to view and delete notifications.
Database
Using a relational database over a non relational database, as the core purposes of the system are dependent on relations between objects, such as users belonging to groups and projects being assigned to groups. The users table is a single table with no direct children. This generates a small amount of waste, such as all users having a ‘group’ field when some users should never be allocated to groups. This is overall acceptable, as there will be a much greater proportion of users with the student role, and the tradeoff for simplicity is worthwhile. 


























(d) User-Driven Evaluation of Solution 
Main Features of the Solution:
1. Dashboard: A dynamic, tailored dashboard for each user role that provides quick access to relevant informations and actions
2. Authentication: Registration, Login, Update User Detail & Change Password
3. Group Management: Create, Join and Manage groups with functionalities like viewing group members and handling join requests
4. Preference Management: Add, Edit and View preference list
5. Project Management: Create, Edit, Assign
6. Notifications: Clean and organised notification system that allows user to view any important changes (e.g. added to group, assigned to a project). Able to delete single notifications.
7. Group Message: Send and receive messages from group members in a group chat. 
8. Skill Management: Authorised users can create new skills. Allow users (students & clients) to add or remove skills to projects or profile. 


Objectives for Evaluating the Effectiveness of the Solution:
1. Usability
2. Efficiency
3. User Satisfaction
4. Security
5. Scalability
6. Accessibility
7. Responsiveness


Frontend
To provide a seamless and intuitive end-user perspective, the frontend of Capstone Compass was designed with the users in mind, aiming to fulfil all the objectives throughout the project. While selectively choosing what to display on the dashboard, we aimed to further enhance navigation with labelled buttons and efficient client-side routing. There were positive feedbacks to the dynamic theme and intuitive modals, which simplify interactions and increase satisfaction. Furthermore, our secure login, registration, and password reset functionalities ensure robust security for user data. Despite the scalability and maintainability achieved through modular component design, some features such as editing preferences and allowing clients to view student profiles were not implemented due to time constraints. While initial feedback indicates general accessibility, further work is needed for complete WCAG compliance. Overall, the frontend solution effectively meets the primary needs of users and clients, providing a solid foundation for future enhancements.


Authentication
The objectives of authentication relates to providing users with a safe and secure environment to manage and develop their capstone projects. With basic generic features such as registration, log in features, the ability to reset the users details and passwords as well as the ability for aministrators to update the permissions of a user to their respective roles within the project. We wanted to ensure that passwords would be stored in secure manner as well as the ability to authenticate requests made to the server by a user provide the greatest level of security. Our team was able to achieve all these key objectives through storing an storing the users password after hashing it. We also implemented JSON Web Token’s rather than implementing sessions to ensure the security, scalability of our platform as well as the stateless nature of JWT’s to guarantee to the performance of our server as we would not be required to store sessions within the database. To ensure that users would be able to securely reset their passwords, a random 6 digit code would be emailed directly to the users email through a mail address maintained directly in the software, and upon providing the correct code the user would be able to reset their password. Some alternative features that we hoped to succeed in implementation included the ability to run a mailing service directly through docker using SMTP with services including Mailtrap or SendGrid as well as 2 factor authentication for login, however these features were extremely challenging when attempts were made to implement these features. The ability to reset the users email address and the ability verify emails upon registration were features that were intended for implementation but due to timeframe constraints were not implemented during this iteration.


Groups
Our focus for group functions including users being able to create, view, join and leave groups efficiently and covering all possible edge cases. Our objective for groups is to make the methods easy to use and improve user experience from current design of the platform(Moodle).  Most functions such as creating groups are kept simple with only a group name will be required with some standard checks like repeated group name not being allowed and users can not already be in a group; check if a user is already in a group when trying to leave group etc. These checks are essential to enhance user experience reducing problems occurring during operations. Other functions such as viewing and leaving groups are adopted from the current system, which we believe is already very convenient and straightforward. To cover our improvements for functions related to groups, we will refer to our design feature of having a group owner and the join request system from the previous section. For this system to work out, we made the following rules: the user creating the group will automatically be the group owner, and there is no direct method to transfer the owner to someone else in the group except when the owner leaves the group which will automatically pass the owner role in the order of join time. The group will be automatically removed when the last user leaves the group to avoid the existence of empty groups. Furthermore, whenever a user joins/creates a group, we will immediately remove all the join requests the user has sent to avoid a user in multiple groups. With these designs, our implementation satisfies our objectives of keeping the system simple, as well as improving user experience.
Projects
While the spec can never cover everything, we do wish to have a comprehensive project description available, instead of relying on clarifying in the chat entirely. The project spec we have in this course is merely a single file, but our projects consist of multiple fields including specializations, group count, background, requirements and etc. This enriched the available information in the description in a well-structured manner, such that students can find what they are interested in without being overwhelmed by information. 
On the other hand, we don’t want clients to be scared by all those fields that need to be filled in. Therefore we allowed them to create the project with the title only, then progressively add in those optional fields whenever they are ready. Again, we made updating projects a very simple task, so clients add information to the spec iteratively.
Channels and messages
Group chats assist the collaboration of teams, and project chats  serve as the supplement of project specification. On top of functionalities of usual message channels, we provide absolute root control for the admin account. Not only that it can view, edit and delete messages, but also add/remove users in channels, even send messages on the behalf of others under special circumstances. We believe this helps the course to monitor and assist the progress of each group and project. 
Just like some existing messaging applications, we plan to have an indicator for the number of unread messages to help users to keep updated.
Preferences
As one of the key features to the capstone project management system, preference is also something we would like to improve. In our implementation, we made the functions simple with only actions add, edit and view. We allow students to add projects to the preference list with a given rank, and we allow editing of preference(covering the case of delete preferences) for users to be able to reselect before the assignment of projects. As mentioned in the previous section, we have enabled individual preference lists to make all students be able to express themself and vote for their own preference, with the function of being able to view group members’ preference to give them an idea of their interested areas. Following the requirement, we allowed users with role client, coordinator and admin to be able to view student preferences for assigning projects and making updates for projects. Our project assigning algorithm is capable of combining individual preferences into a group preference using scores. In terms of effectiveness, we would prefer our system over the current system where each group only has one preference list which is a special case of our system (one member submitting a preference list). Although this might not be very useful for groups who are well communicated and decided a preference list, this will benefit those groups with randomly allocated members and help them to have a better idea of their “unfamiliar” team members and handle the case when someone is absent from a meeting by being able to express their preference without communicating.
Notifications
Our aim for notifications is to make sure users do not miss out on important information. From the requirement spec, the basic requirements for notifications includes project assigning and updating as well as from channel messages. With our design of join request, we also decided to send a notification when sending a join request to the group owner and the result of the join request to the applicant. Our objective is to make notification a clean page of the important information to the users, however, the spec requires us to send a notification whenever there is a new message for all users in a channel, which could easily stack up to hundreds of messages leading to massive amounts of notifications. Our solution to treat this problem under time pressure is to include a delete notification function for users to keep their notification box clean which is a simple design that could be improved in the future.




(e) Limitations and Future Work
Limitation of the frontend
While developing the frontend, we encountered several limitations that we had to work around. Not all features were implemented as initially planned. For example, the ability for users to edit their preferences and for clients to view student profiles were not completed. This was primarily due to the fact that most of the frontend work was handled by one person for the majority of the project. Although we added another team member towards the end, the scalability and complexity of the project meant we did not have enough manpower to fully implement all the backend features on the frontend. Additionally, the frontend could not achieve full compliance with WCAG standards due to time constraints and resource limitations.
To address the limitations encountered during the development of the frontend, several key areas of future work have been identified. Firstly, completing the unfinished features such as allowing users to edit their preferences and enabling clients to view student profiles is essential. We will require additional time and resources to ensure these developments are robust and user-friendly. Further, to improve accessibility by achieving full WCAG compliance, it involves conducting accessibility testing, making necessary adjustments to UI that ensures the system is accessible to all users. Ultimately, to continuously improve user experience, our team must gather and integrate user feedback through surveys, usability testing sessions and monitoring user behaviour within the application.
Authentication 
The current design of the registration does not require users to verify their email addresses and this could create issues where they would not be able to properly reset their passwords when forgotten. This is may be resolved by simply requiring the users to complete an email verification similarly to the 6 digit code mailed with the reset password request. Furthermore, to provide a better users experience we would have preferred the user to be emailed a link that redirects them to a reset password page, however, this was unrealistic for us to implement with the level of experience so we ultimately opted with the simpler solution but this is definitely an avenue to improve the program that could be implemented in the future. Other features that we should aim to implement in future to provide a more secure program is through the implementation of two factor authentication.


Groups
As mentioned in our design justification, there exists a downside to the current design when the group owner is inactive which will lead to join requests not being handled in time. This can be improved if we add an additional boolean field when creating a group that the group creator can decide whether a join request is needed for joining the group. Groups with join request required can ensure no random user is able to join their group for both pre-formed groups and groups who would like to check applicant details before group formation. Whereas a group owner who doesn’t have much requirement for members can choose to make users join a group without a join request to simplify steps.
Projects
Although we provide plentiful attributes for the client to decorate his project, one deficiency is that those fields are merely strings. It would be much more flexible if clients can upload files of varies formats, like images and video, to help them elaborating their projects.
Another feature that can be added is, having the admin or coordinators to approve a project before publishing it to students. While we want to allow clients to update their projects iteratively, we need to avoid students experiencing frequent changes in the spec.




Channels and Messages 
Similar to projects, we wished to have chats that are compatible with more formats rather than merely strings. Also, we planned to give permissions to the admin so that it can create channels manually. In short, we really want to achieve the level of flexibility that common social apps have in our system. 
Preference
The current system does not check whether a group has at least one member having a preference list for the automatic assigning system. In our current design, it should just assign the group the project by maximising the total score of all the groups. Admins can also choose to manually assign the projects to groups to address issues with automatic assignments. Although this is not really a limitation, as all groups should know the date before the date to finalise preference. We can still improve the design by sending a notification before the due date of the preference list, which leads to the improvement in notifications below, to allow admins to directly send a notification to all students.
Notifications
There exist multiple limitations to the current notification designs. Firstly,  whenever there is a new message, a notification will be added to the top of the notification box. Messages is unlike the join requests, project updates and assignment, with low amount of occurrence. It will easily blow up the notification box when there are tons of new messages send. Currently, we have the function to delete notifications, to address this problem. However, to completely fix this problem will lead to a redesign of the message notification where we can replace the notification for messages in the same channel by a new notification with a new timestamp to ensure only one notification for messages in a channel will show up.
Database
There are two important pieces of work that should be done to the database. Namely, using cryptographic functions to salt and hash when inserting into the database, rather than on the backend, and shifting from storing projects as plain text fields inside the database to storing file paths to files containing the information. These are both relatively simple to implement, with password hash salting being available through inbuilt PostgreSQL functions, and file I/O for data just generally being easily implemented. The former will protect against rainbow tables, and the latter will save on storage and generally improve query performance, as connections will be freed faster as they only fetch a file path over fetching entire large text fields. 












(f) Engineering Practices 
Throughout the development of our project, we implemented various engineering practices to ensure fulfilling project outcomes. 
Dockerization
To ensure a consistent development environment and streamline the deployment process, we implemented Dockerization. We encapsulated our application and its dependencies within Docker containers to guarantee consistent behaviour across different environments. Dockerisation simplified the deployment process and also enhanced the scalability and reliability of our application. Furthermore, it enabled us to create isolated environments for development, testing, and production, reducing the risk of environment-specific bugs and ensuring smoother transitions between stages of development.
  

Version control & Iterative development
Version control and iterative development are crucial key practices implemented throughout the development of our project. These practices ensure that during the developmental process of the project we were able to track and manage the changes to the software ensuring that the requirements for key features are achieved before progressing with the next iteration. This was a key component streamlining efficient task allocation and completion for our project.
Pull Requests & Code Reviews
We utilised pull requests as a key part of our development process. Majority of the changes to the codebase were made through a pull request, which allowed us to review and discuss the changes before they were merged. Further, code reviews were conducted by team members to ensure that the changes adhered to our coding standards, were free of bugs, and met the project requirements. 
  

Design before coding
Designing the architecture, planning and visualising the program prior to actually coding enabled us to understand the full requirements of each feature and unify the vision for the feature between the frontend and the backend team, eliminating any misunderstandings while also allowing us to identify any key issues or limitations early into the development process.


Test automation & Software testing
Ensuring that we were able to have tests and automating the tests allowed our team to regularly run tests alongside developing the features, this massively increased our efficiency as well as the accuracy and reliability of our development process. Furthermore, software testing allows us to ensure that all edge-cases are addressed and that our features would meet all the requirements that we had previously agreed upon.
  
  





Dynamic programming
To ensure that our software would be dynamic and adaptable, our team ensured that our code would be simple and consistent. Not only would this ensure that anyone who wanted to work on a feature in later iterations would not have any issues understanding the code, but we also ensured minimal code reliant and dependency which will correlate to minimal changes being required if a feature were to be updated and changed. By maintaining this practice, we ensured that our program could be constantly updated and improved.
