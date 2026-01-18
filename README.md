---

## 📚 Table of Contents
1. [What is MCP?](#what-is-mcp)
2. [MCP Architecture & Layers (Deep Dive)](#mcp-architecture--layers-the-deep-dive)
3. [Why is MCP Needed?](#why-is-mcp-needed)
4. [Advantages of MCP](#advantages-of-mcp)
5. [Disadvantages of MCP](#disadvantages-of-mcp)
6. [Use Cases for MCP](#use-cases-for-mcp)
7. [MCP vs. REST vs. GraphQL](#mcp-vs-rest-vs-graphql)
8. [Best Practices](#best-practices-for-mcp)
9. [Expense Tracker MCP Server (Project)](#expense-tracker-mcp-server)
10. [Setup & Usage](#how-to-run-the-project)
11. [Future Enhancements](#future-enhancements)
12. [License](#license)

---

## What is MCP?

The **Model Context Protocol (MCP)** is a modern architectural approach designed to simplify and enhance the interaction between clients and servers in distributed systems. It focuses on providing a structured way to manage **models** (data), **contexts** (state or environment), and **protocols** (communication rules). MCP is designed to provide a **tool-first API** approach, where the focus is on exposing tools (functions or commands) that operate on models within specific contexts.

For more details, see the [MCP Overview](#model-context-protocol-mcp---in-depth-explanation).

MCP stands for **Model Context Protocol**. It is a framework designed to standardize how AI agents and tools interact. It emphasizes:

1. **Model**: The data entities being managed (e.g., database records).
2. **Context**: The state or environment (e.g., user sessions, current date).
3. **Protocol**: The rules of communication (JSON-RPC 2.0).

MCP is designed to provide a **tool-first API** approach. Unlike REST, which exposes resources (`GET /users`), MCP exposes tools (`find_user`) that operate on models within specific contexts.

---

## MCP Architecture & Layers (The Deep Dive)

To fully understand *how* MCP works, we must look at its layered architecture. This separates the application consuming the data (the Host) from the application providing the data (the Server).



### 1. The Host Layer (The Client)
This is the application "consuming" your API (e.g., Claude Desktop, Cursor IDE, or a custom frontend).
* **Role**: It provides the User Interface. It does not know the business logic (e.g., how to calculate tax); it simply asks the Server, "What tools do you have?" and "Please execute this tool."

### 2. The Protocol Layer (JSON-RPC 2.0)
MCP uses **JSON-RPC 2.0** for all communication.
* **Why JSON-RPC instead of REST?**
    * **Transport Agnostic**: REST requires HTTP. JSON-RPC allows MCP to work over **Standard Input/Output (Stdio)** for local desktop apps *or* **HTTP/SSE** for remote servers.
    * **Stateful & Async**: JSON-RPC uses IDs (`id: 1`) to track requests. The client can send 10 requests at once without waiting for the first to finish, which is crucial for AI agents that "think" fast.
    * **Action-Oriented**: REST is resource-oriented. AI agents are action-oriented. RPC (Remote Procedure Call) fits this mental model perfectly.
    * **Supports Batching**: Mutiple request can be sent in a batch and response will also be recieved in a batch accordingly.

 #### 📨 JSON-RPC Message Examples

**Request (Client -> Server):**
The client asks to execute the `add_expense` tool. Note how the arguments are passed in the `params` object.
```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 1,
  "params": {
    "name": "add_expense",
    "arguments": {
      "amount": 50,
      "category": "Food",
      "note": "Lunch at cafe"
    }
  }
}
```
***Response (Server -> Client): The server processes the logic and returns a structured result matching the ID 1.***

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Successfully added expense ID #42: $50 (Food)."
      }
    ]
  }
}
```
***Error Response (Server -> Client): If the input is invalid (e.g., missing amount), the server returns a standard error object.***

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params: 'amount' is required."
  }
}
```

### 3. The Transport Layer
This determines *how* the messages are sent.
* **Stdio (Standard Input/Output)**:
    * **Usage**: Local processes. The Host launches your `main.py` script directly.
    * **Benefit**: Extremely fast, secure (no open network ports), and zero-configuration.
* **SSE (Server-Sent Events) over HTTP**:
    * **Usage**: Remote servers.
    * **Benefit**: Allows the server to "push" updates (like a progress bar) to the client.

### 4. The Server Application Layer
This is where your code lives. In MCP, your logic is divided into three specific primitives:
* **Resources (Passive Data)**: File-like data that clients can read (e.g., a list of expense categories).
* **Tools (Active Actions)**: Functions that modify state (e.g., `add_expense`).
* **Prompts (Templated Context)**: Reusable templates that help LLMs use your tools better.

---

## Why is MCP Needed?

Traditional API paradigms like REST and GraphQL have served well for web apps, but they have limitations for AI Agents:

### Limitations of Traditional APIs
1. **Verbosity in REST**: Requires multiple endpoints to perform related operations.
2. **Over/Under-fetching**: REST returns fixed data structures, often requiring client-side filtering.
3. **State Management**: Traditional APIs don't inherently share "context" (like cursor position in an editor).
4. **GraphQL Complexity**: Introduces complexity in query design and schema management.

### How MCP Solves These Issues
1. **Tool-Centric Design**: Exposes commands that encapsulate full operations.
2. **Context Awareness**: Integrates runtime state directly into the request flow.
3. **Structured Communication**: Enforces strict typing, preventing "hallucinated" parameters from AI models.
4. **Simplified Integration**: Clients interact with tools directly without constructing complex queries.

---

## Advantages of MCP

1. **Simplified API Design**: Tools are self-contained and single-purpose.
2. **Context-Aware**: Adapts behavior based on user role or environment.
3. **Type Safety**: Strict validation reduces runtime errors.
4. **Developer Experience**: Built-in tooling for debugging and documentation.
5. **Flexibility**: Works locally (Stdio) or remotely (HTTP/WebSocket).
6. **Reduced Overhead**: Clients call tools directly without managing complex endpoints.

---

## Disadvantages of MCP

1. **Learning Curve**: New concepts (Contexts, Prompts) compared to standard REST.
2. **Limited Ecosystem**: Newer than REST/GraphQL, so fewer third-party libraries exist.
3. **Overhead**: Can be overkill for simple CRUD apps.
4. **Complexity**: Managing stateful contexts in multi-user environments can be difficult.
5. **Performance**: Strict validation adds slight processing time.

---

## Use Cases for MCP

1. **Complex Business Logic**: Financial systems, expense trackers.
2. **Context-Dependent Operations**: Admin dashboards, multi-tenant apps.
3. **Real-Time Applications**: Chat apps, live dashboards.
4. **Microservices**: Structured communication between internal services.
5. **AI Integration**: The primary use case—connecting LLMs to your data securely.

---

## MCP vs. REST vs. GraphQL

| Feature | MCP | REST | GraphQL |
| :--- | :--- | :--- | :--- |
| **Design Paradigm** | Tool-centric | Resource-centric | Query-centric |
| **Context Awareness** | Built-in | Manual | Manual |
| **Type Safety** | Enforced | Optional | Optional |
| **Real-Time Support** | Built-in (WebSocket/SSE) | Custom implementation | Built-in (subscriptions) |
| **Ease of Use** | Moderate | Easy | Complex |
| **Flexibility** | High | Moderate | High |
| **Ecosystem** | Growing | Mature | Growing |

---

## Best Practices for MCP

1. **Design Tools Carefully**: Keep tools focused. Use descriptive names (LLMs rely on them).
2. **Leverage Context**: Don't force the user to provide data you already have in context.
3. **Validate Inputs**: Use schemas to catch errors before execution.
4. **Optimize Performance**: Use caching where possible.
5. **Monitor and Debug**: Use built-in logging tools.

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

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

