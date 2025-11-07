## 1. Project Init

#### 1.1 Create project folder
```bash
mkdir sgjob_v2 && cd sgjob_v2
```

#### 1.2 Initialize new project (creates pyproject.toml and .venv)
```bash
uv init
```

#### 1.3 Add dependencies
```bash
uv add pandas numpy matplotlib seaborn streamlit
```

#### 1.4 (Optional) Add dev tools
```bash
uv add --dev black ruff ipykernel jupyter
```

#### 1.5 Verify everything is installed (or if pyproject.toml exist, run this to create the env and install dependencies)
```bash
uv sync
```

## 2. Activate project environment
```bash
source .venv/bin/activate
```
add .vscode/settings.json

#### 3. Create requirements.txt for some environment
```bash
uv export -o requirements.txt
```
#### 4. Run individual phase
```bash
# Phase 1
uv run python -m src.data_ingestion

# Phase 2
uv run python -m src.data_cleaning
```

#### 5. Run a stramlite app
```bash
cd streamlit_app
uv run streamlit run streamlit_app/app.py
```

#### 6. Git
```
git init
git add .
git commit -m "Initial commit"
git branch -M main
git push -f origin main
git remote add origin https://github.com/Learnfa/Mod1-SGJob.git
git push -u origin main
