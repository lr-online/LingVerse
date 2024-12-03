from typing import Annotated

from fastapi import Depends, HTTPException, Request

from app.models.person import Person


async def get_current_user(request: Request) -> Person:
    """获取当前登录用户"""
    return request.state.person


# 创建类型注解别名，使用更简洁
CurrentUser = Annotated[Person, Depends(get_current_user)]


async def get_admin_user(current_user: CurrentUser) -> Person:
    """获取管理员用户"""
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403, detail="Only admin users can perform this operation"
        )
    return current_user


AdminUser = Annotated[Person, Depends(get_admin_user)]
