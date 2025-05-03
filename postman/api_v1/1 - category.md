To send requests to the Django API you've implemented via Postman, follow these examples:

### 1. **GET Request**: List categories with pagination
**Endpoint**: `/categories/`  
**Method**: `GET`

#### Postman setup:
- **URL**: `http://localhost:8000/categories/?page=1` (adjust `localhost:8000` to your actual domain if needed)
- **Params**: You can add a query parameter `page` to specify which page you want, and the `perPage` is handled in the Django pagination class itself (defaults to 2 items per page).
  - Example: `?page=1`
- **Headers**: No additional headers are needed, but the `Content-Range` header will be included in the response.

#### Example response:
```json
{
    "count": 5,
    "next": "http://localhost:8000/categories/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Electronics"
        },
        {
            "id": 2,
            "name": "Furniture"
        }
    ]
}
```

---

### 2. **POST Request**: Create a new category
**Endpoint**: `/categories/`  
**Method**: `POST`

#### Postman setup:
- **URL**: `http://localhost:8000/categories/`
- **Headers**: 
  - `Content-Type`: `application/json`
- **Body**: 
  - Select **raw** and **JSON** as the format.
  - Provide the category data in JSON format:
    ```json
    {
        "name": "New Category"
    }
    ```

#### Example response (201 Created):
```json
{
    "id": 6,
    "name": "New Category"
}
```

---

### 3. **GET Request**: Retrieve a single category
**Endpoint**: `/categories/<id>/`  
**Method**: `GET`

#### Postman setup:
- **URL**: `http://localhost:8000/categories/1/` (Replace `1` with the actual category ID you want to retrieve.)

#### Example response:
```json
{
    "id": 1,
    "name": "Electronics"
}
```

---

### 4. **PUT Request**: Update a category
**Endpoint**: `/categories/<id>/`  
**Method**: `PUT`

#### Postman setup:
- **URL**: `http://localhost:8000/categories/1/` (Replace `1` with the actual category ID.)
- **Headers**:
  - `Content-Type`: `application/json`
- **Body**: 
  - Select **raw** and **JSON** as the format.
  - Provide the updated category data:
    ```json
    {
        "name": "Updated Category"
    }
    ```

#### Example response:
```json
{
    "id": 1,
    "name": "Updated Category"
}
```

---

### 5. **DELETE Request**: Delete a category
**Endpoint**: `/categories/<id>/`  
**Method**: `DELETE`

#### Postman setup:
- **URL**: `http://localhost:8000/categories/1/` (Replace `1` with the actual category ID you want to delete.)
- **Headers**: No additional headers are needed.

#### Example response (204 No Content):
There will be no body returned, but the response code will be `204` indicating successful deletion.

---

These Postman requests allow you to interact with the Django REST API for categories just like you would in your Laravel setup. Be sure to replace the domain or port as necessary based on your local development environment.