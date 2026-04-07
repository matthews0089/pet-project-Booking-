from fastapi import HTTPException, status

UserAlreadyExistException = HTTPException (
    status_code=status.HTTP_409_CONFLICT,
    detail="User already exists",
)

IncorrectEmailOrPasswordException = HTTPException (
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect email or password,please try again",
)

ExpiredTokenException = HTTPException (
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has been expired",
)

TokenAbsent = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token absent",
)


JWTIssue = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="JWT has some issue",
)

User_ID_Exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="ID absent",
)

RoomCannotBeBooked = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="We dont have a free room"
)

Incorrect_Data = HTTPException(
     status_code = status.HTTP_400_BAD_REQUEST,
    detail="Wrong data"
)


Booking_Too_Long = HTTPException(
    status_code = status.HTTP_400_BAD_REQUEST,
    detail="Booking too long"
)