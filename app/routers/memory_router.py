from fastapi import APIRouter, HTTPException, Path, Query

from app.models.memory import Memory
from app.models.person import Person
from app.utils.api_response import ResponseModel

router = APIRouter()


@router.get("", response_model=ResponseModel)
async def list_memories(
    owner_id: str = Query(None, description="所有者ID"),
    creator_id: str = Query(None, description="创建者ID"),
):
    """获取所有记忆"""
    memory_filter = {}
    if owner_id:
        owner = await Person.get_by_id(owner_id)
        assert owner, f"Owner with ID {owner_id} not found"
        memory_filter["owner_id"] = owner_id
    if creator_id:
        creator = await Person.get_by_id(creator_id)
        assert creator, f"Creator with ID {owner_id} not found"
        memory_filter["creator_id"] = creator_id

    memories = await Memory.list(filter_dict=memory_filter)
    return ResponseModel(
        success=True,
        data=[
            memory.model_dump(
                by_alias=False,
            )
            for memory in memories
        ],
        message="Memories retrieved successfully",
    )


@router.get("/{memory_id}", response_model=ResponseModel)
async def get_memory(memory_id: str = Path(..., description="记忆ID")):
    """获取单条记忆"""
    memory = await Memory.get_by_id(memory_id)
    if not memory:
        raise HTTPException(status_code=404, detail="Memory not found")
    return ResponseModel(
        success=True,
        data=memory.model_dump(
            by_alias=False,
        ),
        message="Memory retrieved successfully",
    )


@router.post("")
async def create_memory(payload: Memory):
    """创建记忆"""
    return HTTPException(status_code=403, detail="Memory creation is disabled")


@router.put("/{memory_id}")
async def update_memory(memory_id: str, payload: Memory):
    """更新记忆"""
    return HTTPException(status_code=403, detail="Memory update is disabled")


@router.delete("/{memory_id}")
async def delete_memory(memory_id: str):
    """删除记忆"""
    return HTTPException(status_code=403, detail="Memory deletion is disabled")
