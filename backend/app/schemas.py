from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterUserIn(BaseModel):
    telegram_id: int | None = None
    email: EmailStr | None = None
    full_name: str | None = Field(default=None, max_length=255)
    scientific_field: str | None = Field(default=None, max_length=255)


class UserOut(BaseModel):
    id: str
    telegram_id: int | None
    email: str | None
    full_name: str | None
    scientific_field: str | None
    subscription_status: str

    class Config:
        from_attributes = True


class DraftGenerateIn(BaseModel):
    user_id: str
    title: str = Field(min_length=3, max_length=255)
    topic: str = Field(min_length=5, max_length=2000)
    draft_type: str = Field(default='article_plan', max_length=50)


class DraftOut(BaseModel):
    id: str
    title: str
    content: str

    class Config:
        from_attributes = True


class ExpertiseRequestIn(BaseModel):
    user_id: str
    request_type: str = Field(min_length=3, max_length=100)
    request_text: str = Field(min_length=10, max_length=5000)


class FeedbackIn(BaseModel):
    chat_id: str
    rating: int

    @field_validator('rating')
    @classmethod
    def validate_rating(cls, value: int) -> int:
        if value not in {1, 2, 3, 4, 5}:
            raise ValueError('rating must be between 1 and 5')
        return value


class PaymentActivateIn(BaseModel):
    user_id: str
    plan_name: str
