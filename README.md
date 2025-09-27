# Downloads Organizer

An intelligent file organization system that automatically manages your downloads folder, categorizing files, removing duplicates, and maintaining a clean, organized structure.

## Features

- 🗂️ **Automatic File Categorization** - Images, Documents, Software, Archives
- 🏷️ **Smart File Naming** - Intelligent renaming based on content and metadata
- 🔍 **Duplicate Detection** - Find and remove duplicate files
- 🧹 **Automatic Cleanup** - Remove old temporary files
- 📊 **Real-time Dashboard** - Monitor organization activity
- ⚙️ **Custom Rules** - Set your own organization preferences
- 🔄 **Background Processing** - Works automatically without interruption

## Tech Stack

- **Backend**: Python + FastAPI + SQLAlchemy + Celery
- **Frontend**: React + TypeScript + Next.js + Tailwind CSS
- **Database**: PostgreSQL
- **File Monitoring**: Watchdog
- **Deployment**: Docker + Cloud

## Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd downloads-organizer
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn main:app --reload
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Database Setup**
   ```bash
   # Create PostgreSQL database
   createdb downloads_organizer
   
   # Run migrations
   cd backend
   alembic upgrade head
   ```

## Project Structure

```
downloads-organizer/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core business logic
│   │   ├── models/         # Database models
│   │   ├── services/       # Business services
│   │   └── utils/          # Utility functions
│   ├── requirements.txt
│   └── main.py
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   ├── hooks/          # Custom hooks
│   │   └── utils/          # Frontend utilities
│   ├── package.json
│   └── next.config.js
├── docker-compose.yml      # Development environment
└── README.md
```

## Development

### Backend Development
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm run dev
```

### Database Migrations
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## License

MIT License - see LICENSE file for details.
