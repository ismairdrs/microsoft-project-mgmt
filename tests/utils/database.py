class DatabaseUtils:
    @classmethod
    async def create(cls, db_session, data) -> None:
        db_session.add(data)
        await db_session.commit()

    @classmethod
    def expire_session_objects(cls, db_session) -> None:
        # expire all objects in the current session to fetch
        # Learn more:
        # https://stackoverflow.com/questions/19143345/about-refreshing-objects-in-sqlalchemy-session
        db_session.expire_all()

    @classmethod
    async def update(cls, db_session, data) -> None:
        model_class = type(data)
        data.__dict__.pop("_sa_instance_state")
        update_class_model = (
            model_class.__table__.update()
            .where(model_class.id == data.id)
            .values(**data.__dict__)
        )
        await db_session.execute(update_class_model)
        await db_session.commit()

    @classmethod
    async def create_many(cls, db_session, objects) -> None:
        for obj in objects:
            db_session.add(obj)
        await db_session.commit()
