from pydantic import BaseModel, EmailStr


class RegisterUserIn(BaseModel):
    telegram_id: int | None = None
    email: EmailStr | None = None
    full_name: str | None = None
    scientific_field: str | None = None


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
    title: str
    topic: str
    draft_type: str = 'article_plan'


class DraftOut(BaseModel):
    id: str
    title: str
    content: str

    class Config:
        from_attributes = True


class ExpertiseRequestIn(BaseModel):
    user_id: str
    request_type: str
    request_text: str


class FeedbackIn(BaseModel):
    chat_id: str
    rating: int
