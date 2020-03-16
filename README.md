# my_org_chart
Name : Venkatesh Ramchandra Kamtham Roll no : 17035054 college : IIT BHU Varanasi

Link for a video demo of the application : https://drive.google.com/drive/folders/1D5nY1RDB8Sy4HIYmz4AzdZpip6a1D3_Z?usp=sharing

   Some key points:
  * Built using django framework
  * recursive iteration using django template
  * use of hashing ( dict(key=>list ()) ) to iterate over Hierarchy Tree structure
  * addition and deletion of employees in existing structure
  * searching the employees over name , location and employee id
  * Scalable , consistant and goood performance system
  
  To start the app on your local server 
  
   * open command prompt and go to project directory
   * turn on the virtual environment
      > myvenv\Scripts\activate
   * migrate the data
      > python manage.py makemigrations
      
      > python manage.py migrate
   * run the server
      > python manage.py runserver

![](https://github.com/shrvenk/my_org_chart/blob/master/Screenshot%20(869).png)
