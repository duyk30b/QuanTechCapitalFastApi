*** Old: use python3 + pip3
`python3 --version`
`which python3`
`python3 -m venv venv`

Ubuntu: `source venv/bin/activate`
Window: `venv\Scripts\activate`
Exit: `deactivate`

`pip3 --version`
`pip3 list`
- Export package list: `pip3 freeze > requirements.txt`
- Install package list: `pip3 install -r requirements.txt`

1. Install uv
- Install: `curl -Ls https://astral.sh/uv/install.sh | sh`
- Check: `uv --version`
- Venv: `uv venv`

2. Install fastapi
- `uv init`
- `uv add "fastapi[standard]"`
- `uv pip list`
- `uv pip tree`
- `uv run uvicorn --version`

3. Clone project
```bash
git clone ...
cd project
uv sync
```

4. Run project
`uv run fastapi dev`
`uv run fastapi dev src/main.py`