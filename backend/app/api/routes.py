from fastapi import APIRouter, HTTPException, Depends


from app.models.schemas import (
    ChatRequest,
    ChatResponse
)


from app.models.user_schema import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse
)


from app.agents.router import router_agent


from app.database.chat_repository import (
    chat_repository
)


from app.services.auth_service import (
    auth_service
)


from app.services.session_service import (
    session_service
)


from app.core.dependencies import (
    get_current_user
)


router = APIRouter()


@router.post(
    "/sessions"
)
def create_session(
    current_user: dict = Depends(
        get_current_user
    )
):

    session_id = (
        session_service.create_session()
    )

    return {
        "session_id": session_id
    }


@router.get(
    "/sessions"
)
def get_user_sessions(
    current_user: dict = Depends(
        get_current_user
    )
):

    user_id = current_user.get(
        "sub"
    )

    return (
        chat_repository.get_user_sessions(
            user_id
        )
    )


@router.get(
    "/sessions/{session_id}"
)
def get_session_history(
    session_id: str,
    current_user: dict = Depends(
        get_current_user
    )
):

    user_id = current_user.get(
        "sub"
    )

    return (
        chat_repository.get_session_chats(
            user_id=user_id,
            session_id=session_id
        )
    )


@router.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    current_user: dict = Depends(
        get_current_user
    )
):

    user_id = current_user.get(
        "sub"
    )

    reply = router_agent.route(
        message=request.message,
        user_id=user_id,
        session_id=request.session_id
    )

    return ChatResponse(
        reply=reply
    )


@router.get(
    "/history"
)
def get_chat_history(
    current_user: dict = Depends(
        get_current_user
    )
):

    user_id = current_user.get(
        "sub"
    )

    return (
        chat_repository.get_user_chats(
            user_id
        )
    )


@router.get(
    "/auth/me"
)
def get_current_user_profile(
    current_user: dict = Depends(
        get_current_user
    )
):

    user_id = current_user.get(
        "sub"
    )

    try:

        return (
            auth_service.get_user_profile(
                user_id
            )
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


@router.post(
    "/auth/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate
):

    try:

        new_user = (
            auth_service.register_user(
                name=user.name,
                email=user.email,
                password=user.password
            )
        )

        return new_user

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post(
    "/auth/login",
    response_model=TokenResponse
)
def login_user(
    user: UserLogin
):

    try:

        token = (
            auth_service.login_user(
                email=user.email,
                password=user.password
            )
        )

        return token

    except ValueError as e:

        raise HTTPException(
            status_code=401,
            detail=str(e)
        )