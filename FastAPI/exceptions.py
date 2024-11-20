from fastapi import HTTPException, status as st


class JWTDecodeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_401_UNAUTHORIZED, detail="Please log in again")


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")


class UserNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_404_NOT_FOUND, detail="User not found")


class PasswordVerificationError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")


class UnsupportedFileTypeError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_400_BAD_REQUEST, detail="Unsupported file type")


class UnableToProcessInputError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_400_BAD_REQUEST, detail="Input processing error")


class PostNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_404_NOT_FOUND, detail="Post not found")


class UnauthorizedAccessError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_403_FORBIDDEN, detail="Access denied")


class ImageNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_404_NOT_FOUND, detail="Image not found")


class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(status_code=st.HTTP_409_CONFLICT, detail="Email already in use. Please log in")