from fastapi import APIRouter

router = APIRouter()


@router.get("/test")
def test() -> dict[str,int]:
    """
    Create group
    """
    print("Received message")
    # query to db
    return {"number": 5};

@router.get("/create-group")
def create_group() -> int:
    """
    Create group
    """
    print("Received message")
    # query to db
    return 5;
    
