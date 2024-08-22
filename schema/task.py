from pydantic import BaseModel, model_validator
from typing import Optional

class TaskSchema(BaseModel):
    id: Optional[int] = None  # Сделать поле id необязательным, так как обычно id генерирует сама база данных
    name: str
    pomodoro_count: int
    category_id: int
    user_id: int
    # created_at: Optional[str] = None # = None значит, что поле не обязательно присутствует в модели
    # created_at: int = Field(alias="createdAt") # alias позволяет использовать другое имя поля в API ответах. Это значит, что в ответах будет "createdAt" вместо "created_at"
    # created_at: int = Field(exclude=True) # exclude=True позволяет исключить поле из ответ

    class Config:
        from_attributes = True # from_attributes позволяет автоматически создать поля из атрибутов модели


    @model_validator(mode="after") # валидатор вызывается после создания объекта. Model_validator позволяет добавлять валидацию к полям модели. Таки образом, когда на endpoint поступит запрос с некорректными данными
    def validate_pomodoro_count_and_name_is_not_none(self):
        if self.pomodoro_count is None and self.name is None:
            raise ValueError("Name and Pomodoro count must be provided")
        return self
    


class TaskCreateSchema(BaseModel):
    name: str
    pomodoro_count: int
    category_id: int
