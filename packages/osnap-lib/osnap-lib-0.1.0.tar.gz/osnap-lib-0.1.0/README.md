# OSNAP Library

OSNAP (Open Standard Network Agent Protocol) Library is a Python package for implementing OSNAP Agents in a standardized way, making it easier to create, manage and communicate between agents in a network.

This library provides an easy-to-use framework for creating OSNAP Agents, handling requests and responses, and managing agent tasks.

## Installation

To install the OSNAP Library, simply run:

```
pip install osnap-lib
```

## Usage

Here's a quick guide to get started with the OSNAP Library:

1. Import the required classes and functions:

```python
from osnap_lib import OSNAPAgent, OSNAPRequest, OSNAPResponse, OSNAPAgentTool, OSNAPAgentTask
```

2. Create a custom agent class by extending the `OSNAPAgent` class and implementing the necessary methods:

```python
class CustomAgent(OSNAPAgent):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Implement custom agent methods here
```

3. Initialize your agent:

```python
agent = CustomAgent(name="Custom Agent", description="An example custom agent", scope="public", info_endpoint="http://localhost:8080/info", registry_url="http://osnap-registry.example.com")
```

4. Create OSNAP tools by extending the `OSNAPAgentTool` class and implementing the necessary methods:

```python
class CustomTool(OSNAPAgentTool):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # Implement custom tool methods here
```

5. Add tools to your agent:

```python
tool = CustomTool(name="Custom Tool", description="An example custom tool")
agent.add_tool(tool)
```

6. Send a request to another agent:

```python
request = OSNAPRequest(request_type="info", priority="low", request_metadata={"key": "value"})
response = agent.send_request_to_agent(target_agent_id="agent_id", request=request)
```

7. Register, update tools, and unregister your agent with the registry:

```python
agent.register()
agent.update_tools_on_registry()
agent.unregister()
```

For more detailed information on each class and method, please refer to the source code and comments.

## Contributing

Feel free to contribute to this project by submitting issues, pull requests or helping with documentation.

## License

This project is licensed under the MIT License.
