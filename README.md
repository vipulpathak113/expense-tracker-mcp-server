# Model Context Protocol (MCP)

The **Model Context Protocol (MCP)** is a modern architectural approach designed to simplify and enhance the interaction between clients and servers in distributed systems. It focuses on providing a structured way to manage **models** (data), **contexts** (state or environment), and **protocols** (communication rules). Below is a detailed theoretical explanation of MCP, including its purpose, advantages, disadvantages, and use cases.

---

## What is MCP?

MCP stands for **Model Context Protocol**, and it is a framework or protocol that emphasizes the following:

1. **Model**: Represents the data or entities being managed by the system. Models are typically structured and validated to ensure consistency.
2. **Context**: Refers to the state or environment in which the models operate. Contexts can include user sessions, application states, or any runtime information that influences the behavior of the system.
3. **Protocol**: Defines the rules and mechanisms for communication between different components of the system. This includes how data is exchanged, how tools (or commands) are executed, and how errors are handled.

MCP is designed to provide a **tool-first API** approach, where the focus is on exposing tools (functions or commands) that operate on models within specific contexts, rather than relying on traditional resource-based APIs like REST.

---

## Why is MCP Needed?

Traditional API paradigms like REST and GraphQL have served well for many use cases, but they come with limitations that MCP aims to address:

### Limitations of Traditional APIs
1. **Verbosity in REST**:
   - REST APIs often require multiple endpoints to perform related operations, leading to increased complexity.
   - Example: To fetch a user, update their profile, and retrieve their activity log, you might need three separate endpoints.

2. **Over-fetching or Under-fetching in REST**:
   - REST endpoints often return either too much or too little data, requiring additional requests or client-side filtering.

3. **GraphQL Complexity**:
   - While GraphQL solves some REST issues, it introduces complexity in query design and server-side schema management.
   - It also lacks built-in mechanisms for handling commands or actions (e.g., "reset password").

4. **State Management Challenges**:
   - Traditional APIs do not inherently manage context (e.g., user sessions, runtime state), leaving developers to implement this manually.

### How MCP Solves These Issues
1. **Tool-Centric Design**:
   - MCP focuses on exposing tools (commands) that encapsulate specific operations, reducing the need for multiple endpoints.
   - Example: A single tool can handle "fetch user data and update profile" in one call.

2. **Context Awareness**:
   - MCP integrates context into its design, allowing tools to operate based on the current state or environment.
   - Example: A tool can behave differently for authenticated vs. unauthenticated users.

3. **Structured Communication**:
   - MCP enforces strict input/output validation using type systems, reducing errors and improving developer productivity.

4. **Simplified Client Integration**:
   - Clients interact with tools directly, without worrying about constructing complex queries or managing multiple endpoints.

---

## Advantages of MCP

### 1. **Simplified API Design**
- Tools are self-contained and focused, making APIs easier to design, document, and maintain.
- No need to manage multiple endpoints for related operations.

### 2. **Context-Aware Operations**
- Tools can adapt their behavior based on the current context (e.g., user roles, session state).
- This reduces the need for additional logic on the client side.

### 3. **Type Safety**
- MCP enforces strict type validation for inputs and outputs, reducing runtime errors.
- Example: If a tool expects a `date` parameter, it will reject invalid formats before execution.

### 4. **Improved Developer Experience**
- Built-in tooling for documentation, testing, and debugging.
- Developers can focus on implementing business logic rather than managing API infrastructure.

### 5. **Flexibility**
- MCP supports multiple transport layers (e.g., HTTP, WebSocket), making it suitable for both synchronous and asynchronous operations.

### 6. **Reduced Overhead**
- Clients can call tools directly without worrying about constructing complex queries or managing multiple endpoints.

---

## Disadvantages of MCP

### 1. **Learning Curve**
- MCP introduces new concepts (tools, contexts, protocols) that may be unfamiliar to developers accustomed to REST or GraphQL.

### 2. **Limited Ecosystem**
- MCP is relatively new, so it may lack the extensive libraries, tools, and community support available for REST and GraphQL.

### 3. **Overhead for Simple Use Cases**
- For simple CRUD operations, MCP may introduce unnecessary complexity compared to REST.

### 4. **State Management Complexity**
- While MCP supports context-aware operations, managing complex contexts (e.g., multi-user sessions) can become challenging.

### 5. **Performance Overhead**
- MCP's strict type validation and context management can introduce slight performance overhead compared to lightweight REST APIs.

---

## Use Cases for MCP

### 1. **Complex Business Logic**
- Applications with complex workflows (e.g., financial systems, expense trackers) benefit from MCP's tool-centric design.

### 2. **Context-Dependent Operations**
- Systems where operations depend on user roles, permissions, or runtime state (e.g., admin dashboards, multi-tenant applications).

### 3. **Real-Time Applications**
- MCP's support for WebSocket transport makes it ideal for real-time systems (e.g., chat applications, live dashboards).

### 4. **Microservices**
- MCP's structured communication and context management make it suitable for microservice architectures.

### 5. **Developer-Focused APIs**
- MCP is ideal for internal APIs where developer productivity and type safety are priorities.

---

## MCP vs. REST vs. GraphQL

| Feature                | MCP                          | REST                         | GraphQL                     |
|------------------------|------------------------------|------------------------------|-----------------------------|
| **Design Paradigm**    | Tool-centric                | Resource-centric             | Query-centric               |
| **Context Awareness**  | Built-in                    | Manual                      | Manual                      |
| **Type Safety**        | Enforced                    | Optional                     | Optional                    |
| **Real-Time Support**  | Built-in (WebSocket)        | Requires custom implementation | Built-in (subscriptions)   |
| **Ease of Use**        | Moderate                    | Easy                         | Complex                     |
| **Flexibility**        | High                        | Moderate                     | High                        |
| **Ecosystem**          | Growing                     | Mature                       | Growing                     |

---

## Best Practices for MCP

1. **Design Tools Carefully**:
   - Keep tools focused and single-purpose.
   - Use descriptive names and document inputs/outputs.

2. **Leverage Context**:
   - Use context to simplify client-side logic.
   - Example: A tool can return different data for admins vs. regular users.

3. **Validate Inputs and Outputs**:
   - Use strict type validation to catch errors early.

4. **Optimize Performance**:
   - Use caching and batching to reduce latency.
   - Avoid unnecessary context lookups.

5. **Monitor and Debug**:
   - Use built-in logging and debugging tools to monitor tool performance.

---

# Expense Tracker MCP Server

The **Expense Tracker MCP Server** is a backend application built using the **Model Context Protocol (MCP)**. It provides APIs and tools to manage expenses, budgets, and categories efficiently. This project demonstrates the practical application of MCP in a real-world scenario, focusing on structured communication, context-aware operations, and developer-friendly APIs.

---

## What Does This Project Do?

The **Expense Tracker MCP Server** helps users track and manage their financial activities. It provides the following core functionalities:

1. **Expense Management**:
   - Add, update, delete, and retrieve expenses.
   - Categorize expenses (e.g., food, travel, utilities) for better organization.

2. **Expense Summarization**:
   - Summarize expenses by category within a specific date range.
   - Optionally filter summaries by a specific category.

3. **Category Management**:
   - Expose predefined categories and subcategories (e.g., food, transport, housing) via an MCP resource.
   - Categories are dynamically fetched from a JSON file.

4. **Date-Based Filtering**:
   - Retrieve expenses within a specific date range for better analysis.

5. **Real-Time Notifications**:
   - Built-in support for WebSocket-based real-time updates (future scope).

6. **Context-Aware Operations**:
   - Tailor responses and operations based on user roles, preferences, and session context.

---

## Key Features

### 1. **MCP Tools**
The project implements several tools using the MCP framework:
- **`add_expense`**: Adds a new expense record to the database.
- **`list_expenses`**: Lists all expense records in ascending order of their IDs.
- **`list_expenses_bydate`**: Retrieves expenses within a specified date range.
- **`summarize`**: Summarizes expenses by category within a date range.

### 2. **MCP Resource**
- **`categories`**: Exposes a JSON file containing predefined categories and subcategories, allowing clients to fetch and use them dynamically.

### 3. **Database Integration**
- Uses SQLite to store expense records with fields like `amount`, `category`, `date`, `subcategory`, and `note`.

---

## Technology Stack

- **Backend Framework**: Python with MCP architecture.
- **Database**: SQLite for storing user, expense, and category data.
- **Transport Protocols**: HTTP for synchronous communication (WebSocket support planned).
- **Validation**: MCP's built-in type validation for strict input/output handling.

---

## How to Run the Project

1. **Install Dependencies**:
   Ensure you have Python installed. Then, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. **Initialize the Database**:
   Run the application to automatically create the SQLite database (`expenses.db`) and the `expenses` table.

3. **Start the MCP Server**:
   Start the server using the following command:
   ```bash
   python main.py
   ```
   The server will be available at `http://0.0.0.0:8000`.

4. **Access MCP Tools**:
   Use an HTTP client (e.g., Postman, cURL) to interact with the MCP tools and resources.

---

## Example Usage

### Add an Expense
```bash
POST /tools/add_expense
{
  "amount": 100,
  "category": "food",
  "date": "2025-10-22",
  "subcategory": "groceries",
  "note": "Weekly shopping"
}
```

### List All Expenses
```bash
GET /tools/list_expenses
```

### Summarize Expenses by Category
```bash
POST /tools/summarize
{
  "start_date": "2025-10-01",
  "end_date": "2025-10-22"
}
```

### Fetch Categories
```bash
GET /resources/categories
```

---

## Project Goals

- **Simplify Expense Tracking**: Provide an intuitive and efficient way for users to manage their finances.
- **Demonstrate MCP Architecture**: Showcase the practical application of MCP in a real-world project.
- **Scalability and Flexibility**: Build a backend that can scale with user growth and adapt to new features easily.
- **Developer-Friendly API**: Expose a tool-centric API that is easy to use and integrate with frontend applications.

---

## Future Enhancements

1. **User Authentication**:
   - Add support for user authentication and role-based access control.

2. **Real-Time Updates**:
   - Implement WebSocket-based notifications for budget thresholds and unusual spending patterns.

3. **Advanced Analytics**:
   - Provide more detailed insights into spending habits, including trends and forecasts.

4. **Multi-User Support**:
   - Enable multi-user functionality with separate expense tracking for each user.

---

## About MCP

The **Model Context Protocol (MCP)** is a modern architectural approach designed to simplify and enhance the interaction between clients and servers in distributed systems. It focuses on providing a structured way to manage **models** (data), **contexts** (state or environment), and **protocols** (communication rules). MCP is designed to provide a **tool-first API** approach, where the focus is on exposing tools (functions or commands) that operate on models within specific contexts.

For more details, see the [MCP Overview](#model-context-protocol-mcp---in-depth-explanation).

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

