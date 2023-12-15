"""
Module for define API endpoints
"""

from typing import Optional
from fastapi import FastAPI, Body, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from hypercorn.asyncio import serve
from hypercorn.config import Config as HyperCornConfig
from pydantic import BaseModel, Field, EmailStr
from bson import ObjectId

app = FastAPI()


class PyObjectId(ObjectId):
    """
    PyObjectId define id of students
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        """Check if a student id is valid
        Parameters
        ----------
        cls
          Type of id
        value
          Value used for define id
        Returns
        -------
        Representation of id using ObjectId
        """
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectid")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class StudentModel(BaseModel):
    """
    StudentModel define attributes of students used for creaton
    """

    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)

    class Config:
        """
        Configure access to MongoDB using StudentsModel class
        """

        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


class UpdateStudentModel(BaseModel):
    """
    UpdateStudentModel define attributes of students used for update
    """

    name: Optional[str]
    email: Optional[EmailStr]
    course: Optional[str]
    gpa: Optional[float]

    class Config:
        """
        Configure access to MongoDB using UpdateStudentModel class
        """

        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }


app = FastAPI()


class StudentsServer:
    """
    StudentsServer class define fastapi configuration using StudentsAction to access
    internal API
    """

    _hypercorn_config = None

    def __init__(self, config, db_handler):
        self._hypercorn_config = HyperCornConfig()
        self._config = config
        self._db_handler = db_handler

    async def run_server(self):
        """Starts the server with the config parameters"""

        self._hypercorn_config.bind = [f'0.0.0.0:{self._config.FASTAPI_CONFIG["port"]}']
        self._hypercorn_config.keep_alive_timeout = 90
        self.add_routes()
        await serve(app, self._hypercorn_config)

    def add_routes(self):
        """Maps the endpoint routes with their methods."""

        app.add_api_route(path="/health", endpoint=self.health_check, methods=["GET"])

        app.add_api_route(
            path="/api/student",
            endpoint=self.create_student,
            summary="Add a new student",
            methods=["POST"],
            response_model=StudentModel,
            response_description="Create a new student",
        )

        app.add_api_route(
            path="/api/student",
            endpoint=self.get_students,
            summary="Get all students",
            methods=["GET"],
            response_model=StudentModel,
            response_description="Get all students",
        )

        app.add_api_route(
            path="/api/student/{id}",
            endpoint=self.delete_student,
            summary="Delete a student",
            methods=["DELETE"],
            response_description="Delete a student",
        )

        app.add_api_route(path="/", endpoint=self.read_main, methods=["GET"])

    async def read_main(self):
        """Simple main endpoint"""
        return JSONResponse(
            status_code=status.HTTP_200_OK, content={"msg": "Hello World"}
        )

    async def health_check(self):
        """Simple health check."""

        return JSONResponse(status_code=status.HTTP_200_OK, content={"health": "ok"})

    async def create_student(self, student: StudentModel = Body(...)):
        """Add a new student
        Parameters
        ----------
        student
          Student representation
        Returns
        -------
        Response from the action layer
        """
        student = jsonable_encoder(student)
        new_student = await self._db_handler[
            self._config.MONGODB_COLLECTION
        ].insert_one(student)
        created_student = await self._db_handler[
            self._config.MONGODB_COLLECTION
        ].find_one({"_id": new_student.inserted_id})
        return JSONResponse(
            status_code=status.HTTP_201_CREATED, content=created_student
        )

    async def get_students(self):
        """Get all students
        Returns
        -------
        Response from the action layer
        """
        students = []
        for student in (
            await self._db_handler[self._config.MONGODB_COLLECTION]
            .find()
            .to_list(length=100)
        ):
            students.append(student)
        return JSONResponse(status_code=status.HTTP_200_OK, content=students)

    async def delete_student(self, id: str):
        """Delete a student
        Parameters
        ----------
        id
          Student id
        Returns
        -------
        Response from the action layer
        """
        student = await self._db_handler[self._config.MONGODB_COLLECTION].find_one(
            {"_id": id}
        )
        if student:
            await self._db_handler[self._config.MONGODB_COLLECTION].delete_one(
                {"_id": id}
            )
            return JSONResponse(
                status_code=status.HTTP_204_NO_CONTENT,
            )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": "Student not found"},
        )
