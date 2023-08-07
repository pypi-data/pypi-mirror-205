# inworld_python

Under construction! Not ready for production use. Currently experimenting and planning!

Developed by Edgelord and ChatGPT (c) 2023

## Examples of How To Use (Buggy Alpha Version)

Installation
```python
pip install inworld-python
```
Note: If you don't have node js installed also do the following
```python
pip install 'nodejs-bin[cmd]'
```

Usage for dummies even.

```python
from inworld_python import inworld_chat

chat_app = inworld_chat.InWorldChat('inworld_key', 
                       'inworld_secret', 
                       'inworld_scene'
                      )

# installs the inworld command in the current directory as iw.js
chat_app.setup()

# enter query, user_name, channel_id, and user_id
out = chat_app.chat("What did I just ask?", "blowhard", "3232323", "23232323")
print(out)
```
