## **Gender Prediction API**

### **Overview**

This project is a simple REST API that predicts the gender associated with a given name by querying an external service — Genderize.io. The API accepts a name as input, forwards the request to the external API, processes the response, and returns a structured, enhanced result. It transforms parts of the response and adds useful metadata for better usability.

### **Key Features**

* **Gender Prediction**: Determines likely gender based on a given name
* **External API Integration**: Fetches real-time data from Genderize.io
* **Response Transformation**:
  * Renames count → sample_size
  * Adds is_confident flag based on internal logic
* **Timestamping**: Adds processed_at field in ISO 8601 format
* **Lightweight & Fast**: Single endpoint powered by FastAPI

 ### **How to Run**

**1. Clone the Repository**

```git clone https://github.com/C0deWeather/hng_task_0.git```
```cd hng_task_0```

**2. Run with Docker**

* Build the Docker Image

  ```docker build -t gender-api .```

* Run the Container

  ```docker run -p 80:8000 gender-api```

> The application will be available on http://localhost:80


### **How to Use This API**

**Endpoint**

GET /api/classify?name=\<name\>

**Example Request**

```curl "http://localhost:80/api/classify?name=john"```

**Example Response**
```
{
  "status": "success",
  "data": {
    "name": "john",
    "gender": "male",
    "probability": 0.99,
    "sample_size": 1234,
    "is_confident": true,
    "processed_at": "2026-04-01T12:00:00Z"
  }
}
```

**Another Example**

```curl "http://localhost:80/api/classify?name=alex"```

```
{
  "status": "success",
  "data": {
    "name": "alex",
    "gender": "male",
    "probability": 0.65,
    "sample_size": 80,
    "is_confident": false,
    "processed_at": "2026-04-01T12:05:00Z"
  }
}
```
You can try out your examples interactively via the Swagger Docs:
```http://localhost:80/docs```

**Tech Stack**

* Python 3.12
* FastAPI
* Docker
* External API: Genderize.io

⚠️ Notes

* The accuracy of results depends on the external API.
* Network issues or API limits from Genderize.io may affect responses.
