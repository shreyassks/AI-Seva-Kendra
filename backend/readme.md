

# Backend

#### Setup

Go to `backend` folder ->

1. `python3 --version` -- needs 3.9 and above
2. `python3 -m venv env_dev`
3. `source ./env_dev/bin/activate`
4. `pip install -r requirements.txt`
4. Verify detials in `.env` file
5. `python3 -m uvicorn main:app --reload`

make sure after every pip install you do 
`pip freeze > requirements.txt` 

# 

#### Workspace setup

For code formatting use **Black Formatter** (VS code).
Set both auto format on save and strict type checking. Steps -  
1. Install **Black Formatter**
2. cmd + shift + P > `open workspace settings [JSON]`
3. Enter the following fields - 

```
"[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnType": true,
        "editor.formatOnSave": true,
    }, 
"python.analysis.typeCheckingMode": "basic"
```

# 

#### Common issues 

* Pylance's `import not resolved`

1. activate your venv (`env_dev`) in terminal 
2. Check in python - 
```
import sys
print(sys.executable) 
```
3. cmd + shift + P > `Python: select interpreter`
4. Copy the path from 2 here
   
