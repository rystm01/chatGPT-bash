from openai import OpenAI
import os
import subprocess 
import json

client = OpenAI()




def bash(command):
  proc = os.popen(command)  
  res = proc.read()
  proc.close()
  return res



tools = [
  {
      "type": "function",
      "function": {
          "name": "bash",
          "parameters": {
              "type": "object",
              "properties": {
                  "command  ": {"type": "string",
                                "description": "The command that will be run on the users bash shell.",},
                  
              },
          },
          "required": ["command"]
      },
  },
]

# system prompt
messages = [
          {"role": "system", 
           "content": "You are a helpful assistant. You can run bash commands on the \
           WSL system a windows 11 laptop you are running on. \
          Be very careful to not do anything reckless or unasked for. ", }
      ]
while True:
  # print('messages at start of loop : ')
  # print(messages)
  print()
  # get user prompt
  msg = messages.append({
              "role": "user",
              "content": input(':'),
          })

  # call gpt
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=messages,
      tools=tools
  )
  
  
  # if gpt called a function  
  if completion.choices[0].message.tool_calls:
   
    args = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)
    # print('here')
    fun = locals()[completion.choices[0].message.tool_calls[0].function.name]
    out = fun(args['command'])
    print("$" + args['command'])
    # print(out)
    # print(completion.choices[0].message)
    
    # print(messages)
   


   
    response = completion
    messages.append(response.choices[0].message)

    tool_msg = {
    "role": "tool",
    "content": json.dumps({
        "command": args['command'],
        "command_output": out,
    }),
    "tool_call_id": response.choices[0].message.tool_calls[0].id
   }
    messages.append(tool_msg)



     # call gpt
    completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=messages,
      tools=tools
    )

    print(completion.choices[0].message.content)
  
   
  else:
    # print('appending \n' + str(completion.choices[0].message))
    print()
    messages.append(completion.choices[0].message)
    print(completion.choices[0].message.content)
    print()