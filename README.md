# Qurate ReadMe


**Description**

This was completed in the ninth week out of twelve of the General Assembly software engineering immersive course. This was a group project and we were given a week to create a web app using Python, Django and PostgreSQL as our database. 

**Deployment link:**

https://quratee.fly.dev/

After clicking on the link, navigate to the sign up page to create an account and start adding posts!




**Getting Started/Code Installation**

Download and Open in VS code


**Timeframe & Working Team (Solo/Pair/Group)**

We were given a week and I was working with Tom Reeve and Findlay Gerrard.


**Technologies Used**

Django, Python as the programming language, HTML, CSS and DTL (Django Template Language), and PostgreSQL and neonDB as our database server. 



**Brief**
Your App Must:
☐ Be a full-stack Django application.
☐ Connect to and perform data operations on a PostgreSQL database (the default SQLLite3 database is not acceptable).
☐ If consuming an API (OPTIONAL), have at least one data entity (Model) in addition to the built-in User model. The related entity can be either a one-to-many (1:M) or a many-to-many (M:M) relationship.
☐ If not consuming an API, have at least two data entities (Models) in addition to the built-in User model. It is preferable to have at least one one-to-many (1:M) and one many-to-many (M:M) relationship between entities/models.
☐ Have full-CRUD data operations across any combination of the app's models (excluding the User model). For example, creating/reading/updating posts and creating/deleting comments qualifies as full-CRUD data operations.
☐ Authenticate users using Django's built-in authentication.
☐ Implement authorization by restricting access to the Creation, Updating & Deletion of data resources using the login_required decorator in the case of view functions; or, in the case of class-based views, inheriting from the LoginRequiredMixin class.
☐ Be deployed online using Heroku. Presentations must use the deployed application.
The app may optionally:
☐ Upload images to AWS S3
☐ Consume an API (installation of the Requests package will be necessary)
Other Requirements:
☐ Your team must manage team contributions and collaboration using Git/GitHub team work-flow. Here are some references:


**Planning**

Since this was a group project there was a designation of tasks required. For our group it was quite fluid in the sense we made a list everyday of what needed to be done and we one by one claimed whichever we wanted to each do. This approach was quite effective for my particular group but I am aware that this may not be the case for other groups but nonetheless I learnt a lot.

Below is a Trello page used as our project management tool:

<img width="1275" alt="Screenshot 2023-08-13 at 16 35 11" src="https://github.com/khadijaagha/project-3-qurate/assets/130927994/c884bb73-4a77-4f00-a341-be231882221c">



In our Trello, we created an ice box of features that we would want to implement and then in our Current/MVP were the must haves/requirements. As they were completed we would move them into the completed box. There were a few things from our icebox that we managed to implement, this includes a search bar, followers list, chat function and an art collections API that would serve as our ‘inspiration’ page. 





In the start when deciding our other data entities and models we created an Entity Relationship Diagram (ERD). Our data models apart from the user include; profile, posts, tags and comments. In order to perform CRUD on our users with more flexibility we created the profile model which is essentially referencing the user model. 


In the planning stages, we also created wireframes of our app on Figma. We looked at many websites for inspiration to ensure a clean and cohesive UI. Some websites we looked at were Saatchi Gallery and awwwards.com.

**Build/Code Process**



I did the initial routing and rendering of the basic HTML templates. I worked on being able to add comments to individual posts, I also worked on the liking of posts and comments functionality. Through agreement, my team member further refined the like functionality as we preferred the way he wrote it. Additionally I worked on the basic CRUD delete and edit actions. Lastly, I worked on the CSS of the post details page.


This was the first time where I was utilising the print function to see if the endpoint was even reaching the desired function. 
This function handles the deletion of a post with the specified post_id. It ensures that the deletion is performed only when the request method is "POST" to prevent accidental deletions. After successful deletion, it reloads the 'explore.html' template with the updated list of posts for the user to view.







Here I am defining the function to display the details of a post after clicking on it. The post will display how many likes it has and ensures a user cannot like a post again if they already have. The function is also displaying the comments, the number of likes on each comment, again a user cannot like a comment again.



These two functions are quite simple. In the PostDelete function, for some reason the success url would give an error in the browser when navigating back to the user’s feed after deleting a post. So after researching I came across reverse_lazy that seemed to do the trick. 






This function handles the liking and unliking of a comment associated with a specific post. If the user clicks the "like" button for the comment, it adds the comment to their liked comments. If the user clicks the "unlike" button, it removes the comment from their liked comments. After processing the like/unlike action, the user is redirected back to the detail page of the post.

The first two lines of the function retrieve the Post object and the Profile object corresponding to the pk and the currently logged-in user (whose ID is obtained from request.user.id), respectively.
The if block checks whether the current user (represented by the profile) has already liked the post. It does this by querying the post_likes ManyToMany relationship on the Profile model to see if the post with the given pk exists in the set of liked posts.
If the post has not been liked by the user (i.e., it doesn't exist in profile.post_likes), the code enters the if block. Inside the if block, it adds the post object to the profile.post_likes set using the add() method, indicating that the user has liked the post. After adding the post, it saves the changes to the profile object.
On the other hand, if the post has already been liked by the user (i.e., it exists in profile.post_likes), the code enters the elif block. Inside the elif block, it removes the post object from the profile.post_likes set using the remove() method, indicating that the user wants to undo their like. After removing the post, it saves the changes to the profile object.
After handling the like/unlike action, the function redirects the user back to the page they were previously on. This is achieved using the HttpResponseRedirect class provided by Django, and it makes use of the 'HTTP_REFERER' key from request.META to obtain the referring URL.






This is the like_comment function
The first two lines of the function retrieve the Comment object and the Profile object corresponding to the comment_id and the currently logged-in user respectively. The if block checks whether the current user (represented by the profile) has already liked the comment. It does this by querying the comment_likes ManyToMany relationship on the Profile model to see if the comment with the given comment_id exists in the set of liked comments.
If the comment has not been liked by the user (i.e., it doesn't exist in profile.comment_likes), the code enters the if block. Inside the if block, it adds the comment object to the profile.comment_likes set using the add() method, indicating that the user has liked the comment. After adding the comment, it saves the changes to the profile object.
On the other hand, if the comment has already been liked by the user (i.e., it exists in profile.comment_likes), the code enters the elif block. Inside the elif block, it removes the comment object from the profile.comment_likes set using the remove() method, indicating that the user wants to undo their like. After removing the comment, it saves the changes to the profile object.
After handling the like/unlike action, the function redirects the user to the detail page of the post with the given post_id. This is achieved using the redirect() function provided by Django, passing the appropriate view name ('detail') and the post_id.
In summary, this function handles the liking and unliking of a comment associated with a specific post. If the user clicks the "like" button for the comment, it adds the comment to their liked comments. If the user clicks the "unlike" button, it removes the comment from their liked comments. After processing the like/unlike action, the user is redirected back to the detail page of the post.


**Challenges**

There were quite a few hiccups during the development process. In the beginning when trying to connect to the database it was first an issue for me, but turned out it was as simple as putting in the correct database details

In the start when doing our CSS we noticed that none of it would load. After an hour and then finally needing some help from our instructor, we found out that the CSS was cached, so we had to refresh the page each time using command + shift + ‘R’.

There were also issues including GitHub when pulling and pushing from the development branch to our respective feature branches. An instance when this occurred was when I was trying to pull from the development branch and every file was updating except for my views.py file, didn't notice this until a couple of the core functions were missing which was quite a mystery for all of us. We all came to conclusion that I should copy paste the views.py from one of my group members as we had spent a lot of time on GitHub issues and needed to get on with the project

**Wins**


Towards the conclusion of the project, I found immense satisfaction in the way our team collaborated harmoniously, fostering a seamless and effective work dynamic. The strong bond among team members was truly inspiring, and it significantly contributed to our project's success.

Personally, I take pride in the sections of code that I contributed to. I dedicated myself to these areas, ensuring they met high standards of functionality and maintainability. The sense of accomplishment I felt when witnessing my code in action was truly rewarding.

As the project evolved, I cherished the invaluable learning experiences gained from working closely with my team. The collaborative spirit and the opportunity to take ownership of my code instilled in me a profound appreciation for the power of teamwork in achieving shared goals.

I am grateful for the chance to contribute my skills and be a part of such a supportive and motivated team. Moving forward, I look forward to further honing my abilities and embracing future opportunities for growth and cooperation.

**Key Learnings/Takeaways**

Throughout the project, I had the opportunity to work extensively with Django, and I must say, my confidence in using this framework has grown significantly. The logical structure and organisation of Django resonated with me, making it a natural fit for my development style.

Working on this project as part of a collaborative team was a transformative experience. The power of effective teamwork became evident as we seamlessly coordinated our efforts, supported one another, and shared valuable insights. Collaborating with team members and receiving feedback during the development process allowed me to appreciate the importance of open communication and cohesion in delivering successful projects.

As the project progressed, I found that many Django concepts were further solidified in my mind. The hands-on development process enabled me to deepen my understanding of key concepts, such as models, views, and templates. By actively applying these concepts, I gained the confidence to tackle more complex challenges with ease.

Moreover, the experience of working within a team environment taught me invaluable soft skills, such as adaptability, active listening, and the ability to contribute effectively to group discussions. These skills have not only improved my performance as a team member but also enriched my overall approach to problem-solving and collaboration.

With the successful completion of this project, I am eager to continue expanding my skills and exploring new opportunities in Django development. The journey has been both fulfilling and transformative, and I am enthusiastic about the possibilities that lie ahead as I continue to grow as a developer.





**Bugs**

Mobile version of the website is good, although where the username is displayed on the top left of the screen overlaps the columns defined, that could be improved and make the app more responsive.



**Future Improvements**

Overall, I take great satisfaction in the final outcome of the project. While I'm pleased with the platform's functionality and purpose—providing artists with a space to showcase their work—I acknowledge areas for further improvement to enhance the user experience.

One aspect I would like to implement is a checkout function, enabling users to purchase artwork directly from the platform. By incorporating this feature, the platform's value proposition will be reinforced, providing a seamless experience for both artists and art enthusiasts.

In terms of aesthetics, I plan to refine the web design to make it more visually appealing and user-friendly. Improving the responsiveness of the design is a priority, ensuring that users can access and enjoy the platform effortlessly across different devices and screen sizes.

While there are some small tweaks I'd like to make to the visuals, overall, I am genuinely content with the progress and results achieved during this project. As I continue to evolve and iterate on the platform, I am excited to see it grow into an even more engaging and valuable space for artists and art lovers alike.
