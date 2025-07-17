from fastapi import Request, HTTPException, status, Depends

def login_required(request: Request):
    if not request.session.get("authenticated"):
        raise HTTPException(
            status_code=status.HTTP_302_FOUND,
            headers={"Location": "/login"}
        )
    return True
