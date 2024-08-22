from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from models import Tasks, Categories
from schema import TaskSchema
from schema import TaskCreateSchema


class TaskRepository:
    def __init__(self, db_session: Session):
        self.db_session = db_session


    def get_tasks(self):
        query = select(Tasks)
        with self.db_session as session:
            task: list[Tasks] = session.execute(query).scalars(Tasks).all()
            return task
        
    def get_task(self, task_id: int):
        query = select(Tasks).where(Tasks.id == task_id)
        with self.db_session as session:
            task = session.execute(query).scalar_one_or_none()
            return task
        
    def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        task_model = Tasks(
            name=task.name, 
            pomodoro_count=task.pomodoro_count, 
            category_id=task.category_id, 
            user_id=user_id)
        with self.db_session as session:
            session.add(task_model)
            session.commit()
            return task_model.id
        
    def update_task_name(self, task_id: int, user_id: int, name: str):
        query = update(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id).values(name=name).returning(Tasks.id)
        with self.db_session as session:
            task_id = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
    
    def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session as session:
            result = session.execute(query)  # Сохраняем результат выполнения запроса
            session.commit()  # Сначала делаем commit изменений
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Task not found")

    def get_tasks_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        with self.db_session as session:
            tasks: list[Tasks] = session.execute(query).scalars(Tasks).all()
            return tasks
        
    def get_user_task(self, user_id: int, task_id: int) -> Tasks:
        query = select(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session as session:
            task = session.execute(query).scalar_one_or_none()
            return task
    
