from fastapi import APIRouter, HTTPException, Path

from app.models.memory import Memory
from app.models.person import Person
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_persons(page: int = 1, limit: int = 100, role: str = None):
    """获取所有人物"""
    filter_dict = {}
    if role:
        filter_dict["role"] = role
    persons = await Person.list(
        filter_dict=filter_dict, skip=(page - 1) * limit, limit=limit
    )
    return ResponseModel(
        success=True,
        data=[
            person.model_dump(
                exclude={"access_token"},
                by_alias=False,
            )
            for person in persons
        ],
        message="Persons retrieved successfully",
    )


@router.get("/{person_id}", response_model=ResponseModel)
async def get_person(person_id: str):
    """获取单个人物"""
    person = await Person.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=404, detail="Person not found")
    memories = await Memory.list({"owner_id": person_id}, limit=100)
    return ResponseModel(
        success=True,
        data={
            "person": person.model_dump(
                exclude={"access_token"},
                by_alias=False,
            ),
            "memories": [
                memory.model_dump(
                    by_alias=False,
                )
                for memory in memories
            ],
        },
        message="Person retrieved successfully",
    )


@router.post("", response_model=ResponseModel)
async def create_person(payload: Person):
    """创建人物"""
    new_person = await Person.create(**payload.model_dump(exclude={"access_token"}))
    return ResponseModel(
        success=True,
        data=new_person.model_dump(exclude={"access_token"}, by_alias=False),
        message="Person created successfully",
    )


@router.put("/{person_id}", response_model=ResponseModel)
async def update_person(person_id: str, payload: Person):
    """更新人物信息"""
    try:
        success = await Person.update_by_id(
            id=person_id, data=payload.model_dump(exclude={"access_token"})
        )
        message = "Person updated successfully"
    except Exception as e:
        success = False
        message = str(e)
    return ResponseModel(success=success, data={}, message=message)


@router.delete("/{person_id}", response_model=ResponseModel)
async def delete_person(person_id: str):
    """删除人物"""
    success = await Person.delete_by_id(person_id)
    return ResponseModel(
        success=success, data={"id": person_id}, message="Person deleted successfully"
    )
