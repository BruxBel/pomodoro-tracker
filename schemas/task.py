from pydantic import BaseModel, model_validator


# Схема для создания задачи (без id)
class TaskCreate(BaseModel):
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    @model_validator(mode="after")
    def check_name_or_pomodoro_count_is_not_none(self):
        if self.name is None and self.pomodoro_count is None:
            raise ValueError("name or pomodoro_count must be provided")
        return self


# Схема для возврата задачи (с id)
class Task(BaseModel):
    id: int
    name: str | None = None
    pomodoro_count: int | None = None
    category_id: int

    class Config:
        from_attributes = True
