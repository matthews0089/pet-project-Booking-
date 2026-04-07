from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("room_id, date_from, date_to, expected_total, expected_status", [
    (6, "2030-05-06", "2030-05-10", 3, 201),
    (6, "2030-05-06", "2030-05-10", 4, 201),
    (6, "2030-05-06", "2030-05-10", 5, 201),
    (6, "2030-05-06", "2030-05-10", 6, 201),
    (6, "2030-05-06", "2030-05-10", 7, 201),
    (6, "2030-05-06", "2030-05-10", 8, 201),
    (6, "2030-05-06", "2030-05-10", 8, 409),
    (6, "2030-05-06", "2030-05-10", 8, 409),
])
async def test_add_and_get_booking(
    room_id, date_from, date_to, expected_total, expected_status, aunthenticated_ac: AsyncClient
):
    response = await aunthenticated_ac.post("/bookings", json={
        "room_id": room_id,
        "date_from": date_from,
        "date_to": date_to,
    })
    
    assert response.status_code == expected_status
    

    get_response = await aunthenticated_ac.get("/bookings")
    assert get_response.status_code == 200
    
    assert len(get_response.json()) == expected_total
    
async def test_get_and_delete_all_bookings(aunthenticated_ac: AsyncClient):
    
    response = await aunthenticated_ac.get("/bookings")
    assert response.status_code == 200
    
    bookings = response.json()
    
    assert len(bookings) > 0
    
    for booking in bookings:
        del_response = await aunthenticated_ac.delete(f"/bookings/{booking['id']}")
        assert del_response.status_code == 200
        
    response = await aunthenticated_ac.get("/bookings")
    new_bookings = response.json() 
    
    assert len(new_bookings) == 0
        