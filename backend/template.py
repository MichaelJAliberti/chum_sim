from datetime import datetime


DATA_TEMPLATE = {
    "chats": {
        "<id>": {
            "users": ["USER ID"],
            "messages": [
                {"timestamp": datetime.now(), "user": "USER ID", "payload": ""}
            ],
        },
    },
    "devices": {
        "<id>": {
            "timestamp": datetime.now(),
            "mac": "ff-ff-ff-ff-ff-ff",
            "value": 145,
        },
    },
    "users": {
        "<id>": {
            "info": {
                "full_name": "John Doe",
                "email": "example@example.com",
                "dob": "1/1/2000",
                "gender": "male",
            },
            "chats": ["CHAT ID"],
        },
    },
}
