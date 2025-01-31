from typing import Annotatedfrom pydantic import BaseModel

# How to add a new AI Agent

## What is an AI Agent
An AI Agent is just code that can be called by an LLM to do external tasks such as querying databases, calling APIs, running Python code etc.

There is no data science knowledge needed to write an AI Agent.  
An AI Agent is just a Python class that derives from a `BaseTool` class and implements a function to do the task.

Note: "tools" was the old name for this functionality in OpenAI.  Then OpenAI renamed it to "functions".  But nowadays people call these "AI Agents".  So all three are synonymous in this context.


## Examples
Simple example of an AI Agent that just returns the current date and time:
[language_model_gateway/gateway/tools/current_time_tool.py](language_model_gateway/gateway/tools/current_time_tool.py)

Example of an AI Agent that talks to Jira to get list of issues: 
[language_model_gateway/gateway/tools/jira_issues_analyzer_tool.py](language_model_gateway/gateway/tools/jira_issues_analyzer_tool.py)

Example of an AI Agent that talks to Provider Search Service: 
[language_model_gateway/gateway/tools/provider_search_tool.py](language_model_gateway/gateway/tools/provider_search_tool.py)


## Creating the AI Agent
### Step 1: Add a new file to hold your AI Agent class
Create a new Python file in [language_model_gateway/gateway/tools](language_model_gateway/gateway/tools).  

### Step 2: Define a Pydantic model class to specify the input parameters for your AI Agent
This class should inherit from Pydantic's BaseModel class.  This class should have a list of input parameters that you want the LLM to pass to your AI Agent.

```python
from pydantic import BaseModel, Field
from typing import Type, Optional, List, Tuple, Literal

class JiraIssuesAnalyzerAgentInput(BaseModel):
    """
    Input model for configuring GitHub Pull Request extraction and analysis.
    """

    project_name: Optional[str] = Field(
        default=None,
        description=(
            "Optional specific project name to analyze. "
            "PARSING INSTRUCTION: Extract exact project name from the query if query specifies a project name. "
        ),
    )
```
- Mark it as Optional if this is an optional parameter
- Set default if the parameter is Optional
- Provide a description to aid the LLM in knowing what to pass for this parameter
- Add any additional parameters


### Step 3: Define your AI Agent class
This class should inherit from `ResilientBaseTool`. ResilientBaseTool is our subclass of LangChain's BaseTool.  Our subclass handles parameter naming issue.

```python
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from typing import Type, Optional, List, Tuple, Literal
from pydantic import BaseModel, Field

class JiraIssuesAnalyzerTool(ResilientBaseTool):
    """
    A LangChain-compatible tool for comprehensive Jira issue analysis.

    This tool can be used to extract and analyze Jira issues across projects and assignees.

    """

    name: str = "Replace with name of your AI agent"
    description: str = (
        "Description of your AI Agent so the LLM knows when to call it."
        "----  Sample below -----"
        "Advanced Jira Issue analysis tool. "
        "USAGE TIPS: "
        "- Specify assignee with username "
        "- If querying for a specific date range, include 'from [date] to [date]' "
        "- Set 'counts_only' if you want to get counts only"
        "- Set include_full_description to get full issue description"
        "- Set 'sort_by' to sort by 'created', 'updated', 'popularity', or 'long-running' "
        "- Set 'sort_by_direction' to 'asc' or 'desc' "
        "- Set use_verbose_logging to get verbose logs"
        "- Example queries: "
        "'Pull issues in EFS', "
        "'Issues assigned to johndoe in EFS', "
        "'What issues assigned to imranq2 in EFS project'"
        "'Get last 10 issues'"
    )

    args_schema: Type[BaseModel] = JiraIssuesAnalyzerAgentInput  # Should be the input parameters class you created above
    response_format: Literal["content", "content_and_artifact"] = "content_and_artifact"

    # You can define any other initialization parameters to your class.  These are not passed by the LLM but we can pass them 
    # during initialization
```
IMPORTANT: Your description is really important because that's what tells the LLM when and how to use your AI Agent.
If needed, just ask our AI tool what description to use for your class.

Now implement the `_arun` method to do the actual work.
```python
from typing import Type, Optional, List, Tuple, Literal
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool

class JiraIssuesAnalyzerTool(ResilientBaseTool):
    async def _arun(
        self,
        # add parameters here that mirror the fields in your input parameters class
        # For example:
        project_name: Optional[str] = None
    ) -> Tuple[str, str]:
        # do your actual work here
        return "response to LLM", "artifact that is not given to LLM but shown in the UI"
```
IMPORTANT: This function should take the same parameters as the fields in your input parameters class.

You also have to implement the synchronous version of this method but you can just return `NotImplementedError`.
```python
from typing import Type, Optional, List, Tuple, Literal
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool

class JiraIssuesAnalyzerTool(ResilientBaseTool):
    def _run(
        self,
        # add parameters here that mirror the fields in your input parameters class
        # For example:
        project_name: Optional[str] = None
    ) -> Tuple[str, str]:
        """
        Synchronous version of the tool (falls back to async implementation).

        Raises:
            NotImplementedError: Always raises to enforce async usage
        """
        raise NotImplementedError("Use async version of this tool")

```

Recommendation: Separate your actual code into a utility class that you can test directly without having to go through the LLM.
As an example, see how `language_model_gateway/gateway/tools/jira_issues_analyzer_tool.py` uses 
the `language_model_gateway/gateway/utilities/jira/jira_issues_helper.py` class to handle all the communication with Jira.

This allows us to test the latter with unit tests without using the LLM:
`tests/gateway/utilities/jira/test_jira_issues_helper.py`

### Step 4: Add your new AI Agent to the tool_provider.py
Add your new AI Agent to the tool_provider.py file in the same directory: `language_model_gateway/gateway/tools/tool_provider.py`.  This is where the LLM will look for all available AI Agents.

```python
from typing import Dict
from langchain_core.tools import BaseTool
from language_model_gateway.gateway.tools.jira_issues_analyzer_tool import (
    JiraIssuesAnalyzerTool,
)
from language_model_gateway.gateway.utilities.jira.jira_issues_helper import (
    JiraIssueHelper,
)

class ToolProvider:
    def __init__(
        self,
        *,
        jira_issues_helper: JiraIssueHelper,
    ) -> None:
        self.tools: Dict[str, BaseTool] = {
            "jira_issues_analyzer": JiraIssuesAnalyzerTool(
                jira_issues_helper=jira_issues_helper
            )
        }
 ```
Match the name here with the name defined in your AI Agent class

### Step 5: Register your agent in the container_factory
Add your new AI Agent to the container_factory.py file in the same directory: `language_model_gateway/container/container_factory.py`.  This is where the LLM will look for all available AI Agents.

```python
container.register(
    JiraIssueHelper,
    lambda c: JiraIssueHelper(
        http_client_factory=c.resolve(HttpClientFactory),
        jira_base_url=c.resolve(EnvironmentVariables).jira_base_url,
        access_token=c.resolve(EnvironmentVariables).jira_token,
        username=c.resolve(EnvironmentVariables).jira_username,
    ),
)
```
You may also need to register any dependencies that your AI Agent needs to the container_factory.py file.  For example, the JiraIssueHelper needs a HttpClientFactory class to do the actual work.
```python
container.register(HttpClientFactory, lambda c: HttpClientFactory())
```


### Step 6: Add your agent to the configuration for task models
You can now add this to any task model configurations where you want this tool available: `language_model_gateway/configs/chat_completions/testing`

```json
{
  "tools": [
    {
      "name": "current_date"
    },
    {
      "name": "jira_issues_analyzer"
    }
  ]
}
```

## Unit testing your AI Agent

### Step 1: Create unit tests for your utility class
If you created a separate utility class, as recommended above, then you can just write unit tests as normal.


### Step 2: Create unit test for your AI Agent
Take a look at this example unit test: `tests/gateway/tools/test_jira_issues_analyzer_tool.py`.

Since we use Dependency Injection (DI) containers, you can override any class by supplying a new implementation in the container.

When `RUN_TESTS_WITH_REAL_LLM` environment variable is not set, you can mock various parts of the code.  
When `RUN_TESTS_WITH_REAL_LLM` is set then you can test against the real LLMs with the same code.

## Integration testing your AI Agent using real LLMs
Change the `RUN_TESTS_WITH_REAL_LLM` environment variable to "1" in docker-compose.yml.  
Now your unit tests will run using real LLMs so you can add breakpoints and step through your code.


## Adding Authentication
If your AI Agent needs access to the bearer token of the user, you do the following.

Add auth_token as an input parameter to your AI Agent input model.  This will be injected by our code.
```python
from langgraph.prebuilt import InjectedState
from typing import Type, Optional, List, Tuple, Literal, Dict, Annotated
from pydantic import BaseModel, Field

class GitHubPullRequestAnalyzerAgentInput(BaseModel):
    auth_token: Annotated[Optional[str], InjectedState("auth_token")] = Field(
        default=None,
        description="Injected state",
    )
```

Now you can add auth_token as a parameter to your `_arun` method and it will be passed to your code when present.
```python
from language_model_gateway.gateway.tools.resilient_base_tool import ResilientBaseTool
from typing import Type, Optional, List, Tuple, Literal, Dict, Annotated

class GitHubPullRequestAnalyzerTool(ResilientBaseTool):
    async def _arun(
        self,
        *,
        auth_token: Optional[str] = None,
    ) -> Tuple[str, str]:
        pass
```

This will be the auth_token that was passed to our language model gateway when the user authenticated.  

In the case of the OpenWebUI this is the Okta access token generated when the user authenticated.

In the case of API, this is whatever Bearer token the was passed in the Authorization header.

```
