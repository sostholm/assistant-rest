from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from .database import DSN, register_device_type, register_device
import psycopg

# device_name: str,
# device_type_id: int,
# unique_identifier: str,
# ip_address: str = None,
# mac_address: str = None,
# location: str = None,
# status: str = 'active'
# type_name: str,
# description: str = None

async def register_satellite(request):
    data = await request.json()
    assert "satellite_name" in data, "Satellite name is required"
    assert "unique_identifier" in data, "Unique identifier is required"
    assert "ip_address" in data, "IP address is required"
    assert "mac_address" in data, "MAC address is required"
    assert "location" in data, "Location is required"
    assert "status" in data, "Status is required"
    assert "satellite_type" in data, "Satellite type is required"
    assert "description" in data, "Description is required"

    # Register the satellite type
    async with await psycopg.AsyncConnection.connect(DSN) as conn:
        
        type_id = await register_device_type(
            conn,
            data["satellite_type"],
            data["description"]
        )
        
        await register_device(
            conn,
            data["satellite_name"],
            type_id,
            data["unique_identifier"],
            data["ip_address"],
            data["mac_address"],
            data["location"],
            data["status"]
        )

    # Process the data here
    return JSONResponse({"message": "Satellite registered successfully", "data": data})

routes = [
    Route('/register_satellite', register_satellite, methods=['POST'])
]

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])
]

app = Starlette(debug=True, routes=routes, middleware=middleware)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000)