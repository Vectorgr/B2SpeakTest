from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from b2speak_api.application.use_cases.speak_evaluation import UploadSpeakEvaluationUseCase
from b2speak_api.application.use_cases.speaking_image import  SpeakingImageUseCase
from b2speak_api.application.use_cases.user import UserUseCase
from b2speak_api.config import get_speak_evaluation_use_case, get_speaking_image_use_case, get_user_use_case
from b2speak_api.domain.models.user import User, UserCreate
from b2speak_api.domain.repositories.user import UserRepository
from b2speak_api.infrastructure.auth import create_access_token, decode_access_token, get_password_hash, verify_password


bearer_scheme = HTTPBearer(auto_error=True)

def bearer_token(token: HTTPAuthorizationCredentials = Security(bearer_scheme)):
    return token.credentials

router = APIRouter()

async def get_current_user(token: str = Depends(bearer_token), use_case: UserUseCase = Depends(get_user_use_case)):
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    email = payload.get("sub")
    user = await use_case.get_by_email(email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/speak-evaluation")
async def upload_audio(
    file: UploadFile = File(...),
    selected_picture: str | None = None,
    use_case: UploadSpeakEvaluationUseCase = Depends(get_speak_evaluation_use_case),
    current_user: User = Depends(get_current_user)
):
    content = await file.read()
    return await use_case.execute(content, selected_picture=selected_picture, user_id=current_user._id)

@router.get("/speak-evaluation/{evaluation_id}")
async def get_evaluation(evaluation_id: str, use_case: UploadSpeakEvaluationUseCase = Depends(get_speak_evaluation_use_case)):
    return await use_case.get(evaluation_id)

@router.get("/speak-evaluation/user/{user_id}")
async def get_evaluation(use_case: UploadSpeakEvaluationUseCase = Depends(get_speak_evaluation_use_case), current_user: User = Depends(get_current_user)):
    return await use_case.getByUserId(current_user._id)

@router.get("/speak-evaluation/filename/{filename}")
async def get_evaluation(filename: str, use_case: UploadSpeakEvaluationUseCase = Depends(get_speak_evaluation_use_case), current_user: User = Depends(get_current_user)):
    return await use_case.getByFileName(filename)

@router.post("/speaking-image")
async def upload_image(
    file: UploadFile = File(...),
    use_case: SpeakingImageUseCase = Depends(get_speaking_image_use_case),
    current_user: User = Depends(get_current_user)
):
    content = await file.read()
    return await use_case.add(content, user_id=current_user._id)

@router.get("/speaking-image/{id}")
async def get_speaking_image(id: str, use_case: SpeakingImageUseCase = Depends(get_speaking_image_use_case), current_user: User = Depends(get_current_user)):
    return await use_case.get(id)


@router.get("/speaking-image/download/{id}")
async def download_speaking_image(id: str, use_case: SpeakingImageUseCase = Depends(get_speaking_image_use_case), current_user: User = Depends(get_current_user)):
    image_bytes = await use_case.download_image(id)
    if not image_bytes:
        return {"error": "Image not found"}
    return StreamingResponse(iter([image_bytes]), media_type="image/jpeg")

# Evita conflicto con el endpoint de get por ID, usando un path diferente para obtener una imagen aleatoria
@router.get("/speaking-image/random/get")
async def get_random_speaking_image(use_case: SpeakingImageUseCase = Depends(get_speaking_image_use_case), current_user: User = Depends(get_current_user)):
    return await use_case.get_random()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.get("/", response_class=HTMLResponse)
async def template():
    with open("interfaces/upload_test.html", "r", encoding="utf-8") as f:
        return f.read()

@router.post("/register")
async def register_user(name: str, email: str, password: str, use_case: UserUseCase = Depends(get_user_use_case)):
    if await use_case.get_by_email(email):
        raise HTTPException(status_code=400, detail="Email already registered")
    await use_case.create(name=name, email=email, password=password)
    return {"msg": "User registered"}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), use_case: UserUseCase = Depends(get_user_use_case)):
    user = await use_case.get_by_email(form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token({"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer", "email": user.email, "name": user.name, "id": user._id}