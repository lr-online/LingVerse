from app.models.person import Person


async def create_person():
    # 创建一个人物实例
    await Person.create(
        name="女娲",
        gender="女",
        birthday="1990-01-01",
        email="",
        phone="18888888888",
        access_token="abc123",
        avatar_url="https://www.example.com/avatar.jpg",
        role="admin",
        address="北京市朝阳区",
        language_preference="chinese",
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_person())
