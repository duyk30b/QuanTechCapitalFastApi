\*\*\* Old: use python3 + pip3
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
   1.1. With Ubuntu

- Install: `curl -Ls https://astral.sh/uv/install.sh | sh`

  1.2. With Window: Use PowerShell

- `irm https://astral.sh/uv/install.ps1 -OutFile install.ps1`
- `notepad install.ps1`
- `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
- `.\install.ps1`
- Restart VSCode

  1.3. Check uv

- Check: `uv --version`

2. Init project fastapi

- `uv init`
- `uv venv`
- `uv add "fastapi[standard]"`
- `uv pip list`
- `uv pip tree`
- `uv run uvicorn --version`
- `uv remove bcrypt`

3. Clone project

```bash
git clone ...
cd project
uv sync --reinstall --frozen
```

4. Run project
   `uv run fastapi dev`
   `uv run fastapi dev app/main.py`

5. Windows - Run auto activate
   `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`
   PowerShell: `.venv\Scripts\Activate.ps1`
   CMD: `.venv\Scripts\activate.bat`

6. Migrate
   5.1. Setup
   `uv add alembic`
   `alembic init alembic`
   Sửa ./alembic/env.py

```bash
from app.postgres.postgres_config import postgres_settings
from app.postgres.base_entity import Base

target_metadata = Base.metadata
config.set_main_option(
    "sqlalchemy.url",
    postgres_settings.sqlalchemy_database_uri
)

from app.postgres.entities.user_entity import UserEntity  # noqa
```

5.2. Run migrate generate

- Generate
  `alembic revision --autogenerate -m "init user table"`
- Get SQL
  `alembic upgrade head --sql`
- Run
  `alembic upgrade head`
- Rollback
  `alembic downgrade -1`
