**Follow these rules strictly. Do not deviate.**

## Project Name - **Arun-Code**

## Coding Guidelines

[Coding Guidelines](../skills/coding-guidlines/SKILL.md).** - These guidelines are strict and must be followed without exception. They cover important aspects of software development such as thinking before coding, simplicity, surgical changes, and goal-driven execution.  

## Requirement

1. **You are an expert software engineer with 10+ years of experience in building production-grade applications.** - Your code should reflect this expertise by following best practices, writing clean, maintainable, and efficient code, and making sound architectural decisions.
2. **You are building a project called "Arun-Code".** - This name should be used as the project name in all relevant places, such as `package.json`, `pom.xml`, `Cargo.toml`, etc. Build project using uv package manager.
3. **Coding Assistant** - You have to build coding assistant tool to run locally using nvidia nim sample hello world code can be found in exmaple folder - file `hello_agent.py`.
- Create plan for building coding assistant tool. This tool will be running in my local machine for local AI development. It will have webinterface/plugin for vs code and antigravity where user will be able to chat with the coding assistant and get code suggestions run in agent mode.
- Coding assistant will provide best possible coding experience to user and will have access for all tools in agent mode for building complex features similiar to other coding assist .e.g. Copilot, Antigravity, Cursors etc. 
- This tools will primary focused for code generation, code completion, code refactoring, code review and quick prototyping of application.
- Coding assistant will work seemless in sending prompt request to nvidia endpoint and geting response from the model in clear human readable format.
- Use less emoji's and human friendly language
- Do not assume anything ask for clarification if needed
- Do not write code if not sure about the implementation ask for clarification
- This project will be open source to help fellow developer to build applicaiton in local using this arun-code assistant.
4. **GITHUB REPOSITORY** - [arunCSK](https://github.com/ArunCSK/arun-code.git). This project should help myself to stand out and gain more recognition in the open source community.


## Known Issues

1. Following error occured in vs code copilot chat.

```json
Sorry, your request failed. Please try again.

Client Request Id: d872dbc5-9dfa-4641-b90f-6999aed845b9

Reason: NVIDIA NIM API error: 404 Not Found {"status":404,"title":"Not Found","detail":"Function 'e2d298c5-204e-4213-b921-9f492cc9011b': Not found for account '4HIw6rV_Jsmqpzrr5pb6iq9OyynWll7NFrpgABkG1wg'"}: Error: NVIDIA NIM API error: 404 Not Found {"status":404,"title":"Not Found","detail":"Function 'e2d298c5-204e-4213-b921-9f492cc9011b': Not found for account '4HIw6rV_Jsmqpzrr5pb6iq9OyynWll7NFrpgABkG1wg'"} at streamChatCompletion (c:\Users\Arun.vscode\extensions\hidenobunagai.nvidia-nim-provider-0.2.2\out\api.js:131:15) at process.processTicksAndRejections (node:internal/process/task_queues:104:5) at async processOpenAIStream (c:\Users\Arun.vscode\extensions\hidenobunagai.nvidia-nim-provider-0.2.2\out\streaming\openai.js:141:30) at async NvidiaNimChatModelProvider.provideLanguageModelChatResponse (c:\Users\Arun.vscode\extensions\hidenobunagai.nvidia-nim-provider-0.2.2\out\provider.js:468:13)
```




