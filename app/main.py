from datetime import datetime
from enum import Enum
from fastapi import FastAPI, Query, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="나의 첫 번째 API",
    description="FastAPI로 만든 API입니다.",
    version="1.0.0"
)

# ---- 가상 데이터베이스 ----

fake_items = [
    {"id": 1, "name": "노트북", "category": "electronics", "price": 1500000},
    {"id": 2, "name": "키보드", "category": "electronics", "price": 150000},
    {"id": 3, "name": "청바지", "category": "clothing", "price": 80000},
    {"id": 4, "name": "티셔츠", "category": "clothing", "price": 30000},
    {"id": 5, "name": "사과", "category": "food", "price": 3000},
]

todos_db: dict[int, "Todo"] = {}
todo_id_counter = 1

orders_db: dict[int, "Order"] = {}
order_id_counter = 1

users_db: dict[int, "UserInDB"] = {}
user_id_counter = 1


# ---- Pydantic 모델 ----

class ItemCategory(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    food = "food"


# 사용자 모델 (요청/응답 분리)
class UserCreate(BaseModel):
    """사용자 생성 요청"""
    name: str = Field(min_length=2, max_length=50)
    email: str = Field(pattern=r"^[\w.-]+@[\w.-]+\.\w+$")
    password: str = Field(min_length=8)


class UserUpdate(BaseModel):
    """사용자 수정 요청"""
    name: str | None = Field(default=None, min_length=2, max_length=50)
    email: str | None = Field(default=None, pattern=r"^[\w.-]+@[\w.-]+\.\w+$")


class UserResponse(BaseModel):
    """사용자 응답 (password 제외)"""
    id: int
    name: str
    email: str
    created_at: datetime


class UserDetailResponse(UserResponse):
    """사용자 상세 응답"""
    is_active: bool
    last_login: datetime | None


class UserInDB(BaseModel):
    id: int
    name: str
    email: str
    password: str
    is_active: bool = True
    created_at: datetime
    last_login: datetime | None = None


# TODO 모델
class TodoCreate(BaseModel):
    """할 일 생성 요청"""
    title: str = Field(min_length=1, max_length=100, examples=["FastAPI 공부하기"])
    description: str | None = Field(default=None, max_length=500)


class TodoUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    """할 일 응답"""
    id: int
    title: str
    description: str | None
    completed: bool = False
    created_at: datetime

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 1,
                    "title": "FastAPI 공부하기",
                    "description": "PART 04까지 완료하기",
                    "completed": False,
                    "created_at": "2024-01-01T10:00:00"
                }
            ]
        }
    }


# 주문 모델 (중첩)
class OrderItem(BaseModel):
    """주문 항목"""
    product_name: str
    quantity: int = Field(ge=1)
    unit_price: float = Field(ge=0)

    @property
    def subtotal(self) -> float:
        return self.quantity * self.unit_price


class ShippingAddress(BaseModel):
    """배송 주소"""
    recipient: str = Field(description="수령인")
    phone: str = Field(description="연락처")
    address: str = Field(description="주소")
    memo: str | None = Field(default=None, description="배송 메모")


class OrderCreate(BaseModel):
    """주문 생성 요청"""
    items: list[OrderItem] = Field(min_length=1)
    shipping: ShippingAddress


class Order(BaseModel):
    """주문 응답"""
    id: int
    items: list[OrderItem]
    shipping: ShippingAddress
    total: float
    status: str
    created_at: datetime


# ---- API 엔드포인트 ----

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}

@app.get("/hello")
def say_hello():
    return {"greeting": "안녕하세요!"}

@app.get(
    "/items",
    summary="아이템 목록 조회",
    description="저장된 모든 아이템의 목록을 반환합니다.",
    tags=["items"]
)
def read_items(
    skip: int = 0,
    limit: int = Query(default=10, le=100),
    q: str | None = Query(default=None, min_length=1, description="검색어"),
    category: str | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
):
    results = fake_items

    if q:
        results = [item for item in results if q in item["name"]]
    if category:
        results = [item for item in results if item["category"] == category]
    if min_price is not None:
        results = [item for item in results if item["price"] >= min_price]
    if max_price is not None:
        results = [item for item in results if item["price"] <= max_price]

    return {
        "total": len(results),
        "items": results[skip:skip + limit]
    }

@app.get("/items/{category}", tags=["items"])
def read_items_by_category(category: ItemCategory):
    return {"category": category, "message": f"{category.value} 카테고리 아이템"}

@app.get("/search", tags=["items"])
def search_items(q: str | None = None):
    if q:
        return {"query": q, "results": [f"{q} 검색 결과"]}
    return {"query": None, "results": []}

@app.get("/files/{file_path:path}", tags=["files"])
def read_file(file_path: str):
    return {"file_path": file_path}

# 사용자 API (response_model 사용)

@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["users"])
def create_user(user: UserCreate):
    """사용자 생성"""
    global user_id_counter

    hashed_password = f"hashed_{user.password}"

    new_user = UserInDB(
        id=user_id_counter,
        name=user.name,
        email=user.email,
        password=hashed_password,
        created_at=datetime.now()
    )

    users_db[user_id_counter] = new_user
    user_id_counter += 1

    return new_user  # password가 있어도 response_model이 제외

@app.get("/users", response_model=list[UserResponse], tags=["users"])
def read_users():
    """사용자 목록"""
    return list(users_db.values())

@app.get("/users/me", tags=["users"])
def read_current_user():
    return {"user": "현재 사용자"}

@app.get("/users/{user_id}", response_model=UserDetailResponse, tags=["users"])
def read_user(user_id: int):
    """사용자 상세"""
    if user_id not in users_db:
        return {"error": "사용자를 찾을 수 없습니다"}
    return users_db[user_id]

@app.patch("/users/{user_id}", response_model=UserResponse, tags=["users"])
def update_user(user_id: int, user: UserUpdate):
    """사용자 수정"""
    if user_id not in users_db:
        return {"error": "사용자를 찾을 수 없습니다"}

    stored_user = users_db[user_id]

    if user.name is not None:
        stored_user.name = user.name
    if user.email is not None:
        stored_user.email = user.email

    return stored_user

@app.get("/users/{user_id}/items", tags=["users"])
def read_user_items(user_id: int, skip: int = 0, limit: int = 10):
    return {
        "user_id": user_id,
        "skip": skip,
        "limit": limit
    }

@app.get("/users/{user_id}/posts/{post_id}", tags=["users"])
def read_user_post(user_id: int, post_id: int):
    return {
        "user_id": user_id,
        "post_id": post_id
    }

# TODO CRUD

@app.post("/todos", response_model=Todo, tags=["todos"])
def create_todo(todo: TodoCreate):
    """할 일 생성"""
    global todo_id_counter

    new_todo = Todo(
        id=todo_id_counter,
        title=todo.title,
        description=todo.description,
        completed=False,
        created_at=datetime.now()
    )
    todos_db[todo_id_counter] = new_todo
    todo_id_counter += 1

    return new_todo

@app.get("/todos", tags=["todos"])
def read_todos():
    """할 일 목록 조회"""
    return list(todos_db.values())

@app.get("/todos/{todo_id}", tags=["todos"])
def read_todo(todo_id: int):
    """특정 할 일 조회"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}
    return todos_db[todo_id]

@app.put("/todos/{todo_id}", tags=["todos"])
def update_todo(todo_id: int, todo: TodoUpdate):
    """할 일 수정"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}

    stored_todo = todos_db[todo_id]

    if todo.title is not None:
        stored_todo.title = todo.title
    if todo.description is not None:
        stored_todo.description = todo.description
    if todo.completed is not None:
        stored_todo.completed = todo.completed

    return stored_todo

@app.delete("/todos/{todo_id}", tags=["todos"])
def delete_todo(todo_id: int):
    """할 일 삭제"""
    if todo_id not in todos_db:
        return {"error": "할 일을 찾을 수 없습니다"}

    deleted = todos_db.pop(todo_id)
    return {"message": "삭제되었습니다", "deleted": deleted}

# 주문 API (중첩 모델)

@app.post("/orders", response_model=Order, tags=["orders"])
def create_order(order: OrderCreate):
    """주문 생성"""
    global order_id_counter

    total = sum(item.quantity * item.unit_price for item in order.items)

    new_order = Order(
        id=order_id_counter,
        items=order.items,
        shipping=order.shipping,
        total=total,
        status="pending",
        created_at=datetime.now()
    )

    orders_db[order_id_counter] = new_order
    order_id_counter += 1

    return new_order

@app.get("/orders/{order_id}", response_model=Order, tags=["orders"])
def read_order(order_id: int):
    """주문 조회"""
    if order_id not in orders_db:
        return {"error": "주문을 찾을 수 없습니다"}
    return orders_db[order_id]
