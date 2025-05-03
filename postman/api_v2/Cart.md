Here are Postman requests for testing the cart functionality in your Django REST API, covering the operations from your `CartView`, `CartItemView`, and `ClearCartView`:

### 1. **Get Cart Items**
   **Method:** `GET`  
   **URL:** `/cart/`  
   **Headers:**  
   - `Authorization: Token <your-token>`

   **Example Response:**
   ```json
   {
       "data": [
           {
               "id": 1,
               "product": {
                   "id": 1,
                   "name": "Product Name",
                   "price": "100.00"
               },
               "qty": 2,
               "total_price": "200.00"
           },
           {
               "id": 2,
               "product": {
                   "id": 2,
                   "name": "Another Product",
                   "price": "50.00"
               },
               "qty": 1,
               "total_price": "50.00"
           }
       ],
       "grand_total": 250.00
   }
   ```

### 2. **Add Product to Cart**
   **Method:** `POST`  
   **URL:** `/cart/`  
   **Headers:**  
   - `Authorization: Token <your-token>`  
   - `Content-Type: application/json`

   **Body (JSON):**
   ```json
   {
       "product_id": 1
   }
   ```

   **Example Response:**
   ```json
   {
       "message": "Product Name added to your cart."
   }
   ```

### 3. **Update Cart Item (Increase/Decrease Quantity)**
   **Method:** `PATCH`  
   **URL:** `/cart/item/`  
   **Headers:**  
   - `Authorization: Token <your-token>`  
   - `Content-Type: application/json`

   **Body (Increase Quantity Example - JSON):**
   ```json
   {
       "cart_id": 1,
       "action": "increase"
   }
   ```

   **Body (Decrease Quantity Example - JSON):**
   ```json
   {
       "cart_id": 1,
       "action": "decrease"
   }
   ```

   **Example Response (Increase):**
   ```json
   {
       "message": "Quantity updated in your cart."
   }
   ```

### 4. **Remove Item from Cart**
   **Method:** `DELETE`  
   **URL:** `/cart/item/`  
   **Headers:**  
   - `Authorization: Token <your-token>`  
   - `Content-Type: application/json`

   **Body (JSON):**
   ```json
   {
       "cart_id": 1
   }
   ```

   **Example Response:**
   ```json
   {
       "message": "Item removed from your cart."
   }
   ```

### 5. **Clear Cart**
   **Method:** `DELETE`  
   **URL:** `/clear-cart/`  
   **Headers:**  
   - `Authorization: Token <your-token>`

   **Example Response:**
   ```json
   {
       "message": "Cart cleared successfully."
   }
   ```

### Authorization
Ensure you use a valid token in the `Authorization` header in each request. You can obtain a token using the `/token/` endpoint by sending the username and password:
- **Method:** `POST`
- **URL:** `/token/`
- **Body:**
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```

This should allow you to test the cart functionality fully.