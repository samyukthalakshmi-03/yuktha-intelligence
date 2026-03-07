import app
import json

with app.app.test_client() as c:
    response = c.post('/generate', json={
        "business": "Tech",
        "task": "Develop app",
        "details": "make an app"
    })
    print(response.json)
