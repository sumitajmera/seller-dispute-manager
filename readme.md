<!-- If working in virtual environment -->
Activate the virtual env and run the below command :
pip install -r requirements.txt

<!-- Clear the migrations -->
Tasks ---> migrations ----> this folder should have only one file __init__.py , remove all other files

<!-- To remove the db.sqlite3 -->
Run this command : rm db.sqlite3 

python manage.py makemigrations
python manage.py migrate

<!-- To create random 50 users -->
Run this command : python manage.py create_users

<!-- API EndPoints -->
Tasks API (TasksViewSet)

GET	    /tasks/	                  Fetch all tasks
GET	    /tasks/{tasks_id}/	      Get a specific task

POST    /tasks/{task_id}/assign/  To assign task to users
Payload : {
  "assigned_users": [3,2]
}

User-Assigned Tasks API (UserTasksViewSet)

GET	    /user-tasks/?user_id=1	   Fetch tasks assigned to user id=1


<!-- SAMPLE API Requests and responses -->

<!-- To create tasks :  -->

curl --location 'localhost:8000/task/' \
--header 'Content-Type: application/json' \
--data '{
  "name": "Five Task",
  "description": "Fix homepage issue"
}'

Response : 
{
    "id": 12,
    "name": "Five Task",
    "description": "Fix homepage issue",
    "created_at": "2025-03-26T04:52:35.888128Z",
    "task_type": null,
    "completed_at": null,
    "status": "pending",
    "assigned_users": []
}

<!-- To assign tasks : -->

curl --location 'localhost:8000/task/11/assign/' \
--header 'Content-Type: application/json' \
--data '{
  "assigned_users": [46]
}'

Response : 
{
    "message": "Task assigned successfully"
}

<!-- To get tasks assigned to a user -->
curl --location 'localhost:8000/user_task/?user_id=46'

Response :
{
    "count": 11,
    "next": "http://localhost:8000/user_task/?page=2&user_id=46",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "First Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:07:50.170847Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 2,
            "name": "Second Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:07:54.879600Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 3,
            "name": "Third Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:08:01.215918Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 4,
            "name": "Fourth Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:08:05.574639Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 5,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:34:56.268273Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 6,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:51:56.220108Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 7,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:51:58.741238Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 8,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:33.683985Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 9,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:34.346862Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 10,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:34.979479Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        }
    ]
}

<!-- To get specific task : -->

curl --location 'localhost:8000/task/2'

Response:
{
    "id": 2,
    "name": "Second Task",
    "description": "Fix homepage issue",
    "created_at": "2025-03-26T02:07:54.879600Z",
    "task_type": null,
    "completed_at": null,
    "status": "pending",
    "assigned_users": [
        {
            "id": 46,
            "username": "user45_XjIf",
            "email": "user45_XjIf@example.com",
            "phone": "9876571075",
            "date_of_birth": "2003-11-15"
        }
    ]
}

<!-- To get all tasks :  -->

curl --location 'localhost:8000/tasks'

Response : 
{
    "count": 12,
    "next": "http://localhost:8000/task/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "First Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:07:50.170847Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 2,
            "name": "Second Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:07:54.879600Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 3,
            "name": "Third Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:08:01.215918Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 4,
            "name": "Fourth Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T02:08:05.574639Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 5,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:34:56.268273Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 6,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:51:56.220108Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 7,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:51:58.741238Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 8,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:33.683985Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 9,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:34.346862Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        },
        {
            "id": 10,
            "name": "Five Task",
            "description": "Fix homepage issue",
            "created_at": "2025-03-26T04:52:34.979479Z",
            "task_type": null,
            "completed_at": null,
            "status": "pending",
            "assigned_users": [
                {
                    "id": 46,
                    "username": "user45_XjIf",
                    "email": "user45_XjIf@example.com",
                    "phone": "9876571075",
                    "date_of_birth": "2003-11-15"
                }
            ]
        }
    ]
}