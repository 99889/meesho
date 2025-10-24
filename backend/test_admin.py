import asyncio
import httpx

async def test_admin_endpoints():
    async with httpx.AsyncClient() as client:
        # First, let's login as admin
        login_data = {
            "email": "admin@meesho.com",
            "password": "admin123"
        }
        
        try:
            response = await client.post("http://localhost:8000/api/auth/login", json=login_data)
            if response.status_code == 200:
                print("Login successful!")
                token_data = response.json()
                token = token_data["token"]
                print(f"Token: {token}")
                
                # Test admin endpoints with the token
                headers = {"Authorization": f"Bearer {token}"}
                
                # Test getting all products (admin endpoint)
                products_response = await client.get("http://localhost:8000/api/admin/products", headers=headers)
                if products_response.status_code == 200:
                    print("Admin products endpoint works!")
                    products_data = products_response.json()
                    print(f"Total products: {products_data['total']}")
                else:
                    print(f"Failed to get products: {products_response.status_code}")
                    print(products_response.text)
            else:
                print(f"Login failed: {response.status_code}")
                print(response.text)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_admin_endpoints())