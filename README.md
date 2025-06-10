## 🔧 Setup Instructions

### ✅ 1. Clone the Repository

```bash
git clone myproject repo

cd my-repo
python -m venv venv
venv\Scripts\activate  # Use `source venv/bin/activate` on Mac/Linux

pip install -r requirements.txt

# Create a `.env` file and add your environment variables (e.g., SECRET_KEY, DB configs)

cd my_project
# Apply migrations
python manage.py migrate

# Run the Django server
python manage.py runserver
```
