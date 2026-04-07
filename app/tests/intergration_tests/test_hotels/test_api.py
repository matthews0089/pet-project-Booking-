from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("location, date_from, date_to, status_code", [
    ("Hilton Kyiv", "2030-05-01", "2030-05-10", 200),
    ("Hilton Kyiv", "2030-05-20", "2030-05-29", 200),
    ("Hilton Kyiv", "2030-05-20", "2030-05-10", 400),
    ("Hilton Kyiv", "2030-05-12", "2030-05-02", 400),
    ("Hilton Kyiv", "2030-05-12", "2030-09-02", 400),
])
async def test_get_hotels(location,date_from, date_to, status_code, ac: AsyncClient):
     response = await ac.get("/hotels/", params={
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
    })
     
     assert response.status_code == status_code
    