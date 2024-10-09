## Order Service

Denne microservice håndterer ordrer, herunder oprettelse, opdatering og hentning af ordredata. Den behandler ordrers livscyklus fra oprettelse til ændring af status (f.eks. "shipped" eller "completed").

### Installation

Clone dette repository:
```
git clone https://github.com/SushiGirrl/Order-service.git
cd order_service
docker build -t order_service_image .
docker run -d --name order-service -e DATABASE_DIR=/data -v orders_data:/data -p 5000:5000 order_service_image
```
## API Endpoints

### Opret en ny ordre

- **URL:** `/orders`
- **Method:** `POST`
- **Request Body:** JSON

  ```json
  {
      "product_id": "1",
      "quantity": "2"
  }
  ```

- **Response:**

  - **201 Created:** Returnerer detaljer om den oprettede ordre.
  - **400 Bad Request:** Hvis product_id eller quantity mangler.

### Hent en specifik ordre

- **URL:** `/orders/{order_id}`
- **Method:** `GET`
- **Response:**

  - **200 OK:** Returnerer detaljer om den oprettede ordre.
  - **404 Not Found:** Hvis ordren ikke findes.

### Opdater status ordre

- **URL:** `/orders/{order_id}/status`
- **Method:** `PUT`
- **Request Body:** JSON

  ```json
  {
    "status": "shipped"
  }
  ```

- **Response:**

  - **200 OK:** Bekræfter, at status er blevet opdateret.
  - **400 Bad Request:** Hvis status ikke er angivet i request body.
  - **404 Not Found:** Hvis ordren ikke findes.

## Notes

- **Persistent Data:** Applikationen bruger en SQLite-database for at gemme ordredata. 
Dataen gemmes i en ekstern mappe via Docker-volumes for at sikre persistens.

- **Environment Variables:** Du kan ændre databasens gemmesti ved hjælp af miljøvariablen `DATABASE_DIR`.

## License

MIT License
