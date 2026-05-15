from pydantic import BaseModel, ConfigDict


class GetAnDbRowSchema(BaseModel):
    id: int


class RedisExmapleJsonSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    example: str


class MyDecoratorSchema(BaseModel):
    id: int
    name: str
