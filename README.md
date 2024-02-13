# Flokerr
Flokerr is a server app for real-time communication and data management via HTTP and WS. It supports CRUD, data exchange, and monitoring across WebSocket clients.

# Flokerr Project Overview
Flokerr is a comprehensive server application designed to facilitate real-time communication and data management through both HTTP and WebSocket (WS) protocols. This project is structured to support a variety of operations, including data creation, reading, updating, and deletion (CRUD), alongside real-time data exchange and monitoring across different clients connected through WebSockets.

## Key Features
* HTTP Server: Handles traditional HTTP requests, enabling CRUD operations through RESTful endpoints. It's built to support operations such as authentication, data manipulation, and server health checks.

* WebSocket Server: Offers real-time, bidirectional communication between the server and clients. It supports a wide range of operations, including live data feeds, client management, and notifications. The WebSocket server uses custom protocols and includes mechanisms for client authentication, connection management, and data transmission.

* Dynamic Topic Management: Through both HTTP and WS, clients can subscribe to specific topics for updates or publish data to these topics, allowing for a flexible and dynamic data exchange system. Topics are managed in a database, and their states are synchronized across clients in real time.

* Database Integration: Utilizes SQLAlchemy for database management, ensuring robust data handling and persistence. The database schema includes tables for topics, performances, and warnings, among others, facilitating comprehensive data storage and retrieval.

* Configuration and Security: The server configuration is managed through a JSON file, allowing for easy customization of server parameters. Additionally, sensitive information is handled through a separate secrets file, enhancing security.

* Decorator and Endpoint Structure: The codebase makes extensive use of Python decorators to streamline the handling of requests and responses, error management, and data parsing. Endpoints are organized into modules within the http and ws directories for clear separation of concerns.

## How It Works
* Initialization: The server starts by setting up the database connection and ensuring that all required tables are present. It then launches the HTTP and WebSocket servers based on the configurations provided.

* HTTP Operations: Clients can perform CRUD operations through HTTP endpoints, interacting with the server for tasks like data manipulation and querying server status. The server processes these requests, interacts with the database as needed, and returns appropriate responses.

* WebSocket Communication: For real-time communication, clients connect to the WebSocket server. Once connected, they can subscribe to topics, receive live updates, and publish data to these topics. The WebSocket server manages client connections, authenticates users, and routes messages to the appropriate topics and subscribers.

* Security and Authentication: The server includes mechanisms for authenticating users and securing data transmission, ensuring that only authorized clients can publish or subscribe to specific topics.

## Getting Started
* Requirements: Make sure Python 3.x is installed along with the necessary packages listed in requirements.txt.
* Configuration: Adjust configuration.json and secrets.json to match your server and security settings. Or, use dokcer-compose file to set all environnement variables.
* Running the Server: Execute main.py to start the server. It listens for HTTP and WebSocket connections as configured.
## Conclusion
Flokerr is designed to be a versatile backend solution for applications requiring real-time data exchange and robust data management capabilities. Its architecture supports scalable and secure communications, making it suitable for a wide range of applications, from IoT devices to real-time messaging systems.