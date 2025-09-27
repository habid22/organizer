# Downloads Organizer - Setup Guide

## Quick Start

### Option 1: Docker (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd downloads-organizer

# Make scripts executable
chmod +x start.sh

# Start the application
./start.sh
```

### Option 2: Development Mode
```bash
# Clone the repository
git clone <repository-url>
cd downloads-organizer

# Make scripts executable
chmod +x start-dev.sh

# Start in development mode
./start-dev.sh
```

## Manual Setup

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- Redis (optional, for background tasks)

### Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp ../env.example .env
# Edit .env with your database settings

# Run database migrations
alembic upgrade head

# Start the backend
uvicorn app.main:app --reload
```

### Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start the frontend
npm run dev
```

## Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/downloads_organizer

# Redis Configuration (optional)
REDIS_URL=redis://localhost:6379/0

# File System Configuration
DOWNLOADS_PATH=~/Downloads

# API Configuration
API_URL=http://localhost:8000
SECRET_KEY=your-secret-key-change-in-production
```

### Downloads Folder
The application will monitor your downloads folder for new files. Make sure the path is correct in your `.env` file.

## Features

### 🗂️ Automatic File Organization
- **Images**: JPG, PNG, GIF, SVG → `Images/2024-01/`
- **Documents**: PDF, DOC, TXT → `Documents/PDFs/`, `Documents/Word/`
- **Software**: EXE, MSI, DMG → `Software/Installers/`
- **Archives**: ZIP, RAR, 7Z → `Archives/`

### 🏷️ Smart File Naming
- **Screenshots**: `screenshot_2024-01-15_14-30.png`
- **Photos**: `photo_2024-01-15_14-30.jpg`
- **Documents**: `invoice_2024-01-15.pdf`
- **Software**: `software_installer_2024-01-15.exe`

### 🔍 Duplicate Detection
- Identifies duplicate files by content
- Shows duplicates in the dashboard
- Allows manual cleanup

### 🧹 Automatic Cleanup
- Removes temporary files after 7 days
- Archives old files after 30 days
- Configurable cleanup rules

## API Documentation

Once running, visit:
- **API Docs**: http://localhost:8000/api/docs
- **Frontend**: http://localhost:3000

## Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure PostgreSQL is running
   - Check database credentials in `.env`
   - Run migrations: `alembic upgrade head`

2. **File Permission Error**
   - Check downloads folder permissions
   - Ensure the application has write access

3. **Port Already in Use**
   - Change ports in `docker-compose.yml` or `.env`
   - Kill existing processes on ports 3000/8000

### Logs
- **Backend logs**: Check terminal output
- **Frontend logs**: Check browser console
- **Docker logs**: `docker-compose logs [service]`

## Development

### Project Structure
```
downloads-organizer/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configuration
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── tasks/          # Background tasks
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Next.js pages
│   │   └── lib/            # API client
│   └── package.json
├── docker-compose.yml      # Development environment
└── README.md
```

### Adding New Features

1. **Backend**: Add new API routes in `backend/app/api/`
2. **Frontend**: Add new components in `frontend/src/components/`
3. **Database**: Create migrations with `alembic revision --autogenerate`

### Testing
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Deployment

### Production Deployment
1. Set up production database
2. Configure environment variables
3. Build and deploy with Docker
4. Set up reverse proxy (nginx)
5. Configure SSL certificates

### Cloud Deployment
- **AWS**: Use ECS or EKS
- **Google Cloud**: Use Cloud Run or GKE
- **Azure**: Use Container Instances or AKS

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.
