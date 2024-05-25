class MongoDBLockFactory:
    """
    Factory for value of the lock field in the MongoDB
    collections.

    See [this article](https://www.mongodb.com/blog/post/how-to-select-\
-for-update-inside-mongodb-transactions) for details.

    Basic usage::

        class FooMapper:
            def __init__(
                self,
                collection: AsyncIOMotorCollection,
                lock_factory: MongoDBLockFactory,
            ):
                self._collection = collection
                self._lock_factory = lock_factory

            async def acquire_with_id(self, id: int):
                foo = await self._collection.find_one_and_update(
                    {"id": id},
                    {"$set": {"lock": self._lock_factory()}},
                )
                ...
    """

    def __call__(self) -> str:
        return "0_o"
