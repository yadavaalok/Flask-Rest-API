GET -> /students  

Get all students records

```json
[
    {
        "roll_no": 1,
        "name": "ABCD",
        "gender": "M",
        "dob": "01/01/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "Delhi",
        "subjects": [
            {
                "sub_id": 1,
                "name": "Mathematics",
                "marks": 92
            },
            {
                "sub_id": 2,
                "name": "English",
                "marks": 86
            }
        ]
    },
    {
        "roll_no": 2,
        "name": "XYZ",
        "gender": "F",
        "dob": "02/02/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "Delhi",
        "subjects": [
            {
                "sub_id": 1,
                "name": "Mathematics",
                "marks": 93
            },
            {
                "sub_id": 3,
                "name": "Science",
                "marks": 89
            }
        ]
    }
]
```

GET -> students?city=Delhi&name=XYZ

```json
[
	{
        "roll_no": 2,
        "name": "XYZ",
        "gender": "F",
        "dob": "02/02/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "Delhi",
        "subjects": [
            {
                "sub_id": 1,
                "name": "Mathematics",
                "marks": 93
            },
            {
                "sub_id": 3,
                "name": "Science",
                "marks": 89
            }
        ]
    }
]
```

GET -> students/ID

Get record of 1 student

EX -> students/1

```json
{
        "roll_no": 1,
        "name": "ABCD",
        "gender": "M",
        "dob": "01/01/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "Delhi",
        "subjects": [
            {
                "sub_id": 1,
                "name": "Mathematics",
                "marks": 92
            },
            {
                "sub_id": 2,
                "name": "English",
                "marks": 86
            }
        ]
    }
```

GET -> /subjects

Get list of all subjects

```json
[
    {
        "sub_id": 1,
        "name": "Mathematics",
    },
    {
        "sub_id": 3,
        "name": "Science"
    }
]
```

GET -> subjects/sub_id

Get record of 1 subject

```json
{
    "sub_id": 1,
    "name": "Mathematics",
}
```

POST -> students

Create students record

Request BODY:

```json
{
        "roll_no": 1,
        "name": "ABCD",
        "gender": "M",
        "dob": "01/01/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "Delhi",
        "subjects": [
            {
                "sub_id": 1,
                "marks": 92
            },
            {
                "sub_id": 2,
                "marks": 86
            }
        ]
    }
```

POST -> subject

Create subject record

```json
{
    "sub_id": 1,
    "name": "Mathematics",
}
```

PUT -> students/id

Update students record

Request BODY:

```json
{
        
        "name": "ABCDEF",
        "gender": "M",
        "dob": "01/01/2001",
        "contact_no.": "+91xxxxxxxxx",
        "city": "MUMBAI",
        "subjects": [
            {
                "sub_id": 1,
                "marks": 45
            },
            {
                "sub_id": 2,
                "marks": 80
            }
        ]
}
```

DELETE -> students/id
Delete student record
