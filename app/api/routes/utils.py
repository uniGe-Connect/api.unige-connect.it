from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.resources.message_resource import Message
from app.utils import generate_test_email, send_email

router = APIRouter()


@router.post(
    "/test-email/",
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True
