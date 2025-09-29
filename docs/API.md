# API Documentation

Overview
- Base URL (development): http://localhost:5000
- Authentication: none
- Content types: application/json for JSON endpoints
- Error format: { "error": "..." }

Health
- GET /
  - 200: text/plain "✅ Upskill Advisor API is running!"

Roles
- POST /roles
  - Description: Add a user role.
  - Request (application/json):
    - role (string, required): User role
  - Response (application/json):
    - status (string): "success"
    - role (string): Added role
  - Status codes:
    - 201: Role added successfully
    - 400: Validation error
    - 500: Server error
  - Example request (curl):
    ```bash
    curl -s -X POST http://localhost:5000/roles \
      -H "Content-Type: application/json" \
      -d '{"role":"Data Scientist"}'
    ```
  - Example response:
    ```json
    {
      "status": "success",
      "role": "Data Scientist"
    }
    ```

Skills
- POST /skills
  - Description: Add user skills.
  - Request (application/json):
    - skills (array of strings, required): List of user skills
  - Response (application/json):
    - status (string): "success"
    - skills (array of strings): Added skills
  - Status codes:
    - 201: Skills added successfully
    - 400: Validation error
    - 500: Server error
  - Example request (curl):
    ```bash
    curl -s -X POST http://localhost:5000/skills \
      -H "Content-Type: application/json" \
      -d '{"skills":["Python","Data Analysis"]}'
    ```
  - Example response:
    ```json
    {
      "status": "success",
      "skills": ["Python", "Data Analysis"]
    }
    ```

Recommendations
- POST /recommendations
  - Description: Get course recommendations based on user role and skills.
  - Request (application/json):
    - role (string, required): User role
    - skills (array of strings, required): List of user skills
  - Response (application/json):
    - courses (array of objects): List of recommended courses
      - course (string): Course name
      - provider (string): Course provider
      - url (string): Course URL
  - Status codes:
    - 200: Recommendations generated successfully
    - 400: Validation error
    - 500: Server error
  - Example request (curl):
    ```bash
    curl -s -X POST http://localhost:5000/recommendations \
      -H "Content-Type: application/json" \
      -d '{"role":"Data Scientist","skills":["Python","Data Analysis"]}'
    ```
  - Example response:
    ```json
    [
      {
        "course": "Advanced Python Programming",
        "provider": "Coursera",
        "url": "https://coursera.org/advanced-python"
      },
      {
        "course": "Data Science with Python",
        "provider": "edX",
        "url": "https://edx.org/data-science-python"
      }
    ]
    ```
