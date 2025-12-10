# Docker Setup Guide

## Environment Configuration

The `docker-compose.yml` uses environment variables for security. Follow these steps:

### 1. Create `.env.docker` file

```bash
cp .env.docker.example .env.docker
```

### 2. Edit `.env.docker` with your credentials

Replace all placeholder values:
- `your_secure_password_here` - Strong database password
- `your_api_key_here` - Your actual API keys
- `your_news_api_url_here` - Your news API endpoint

### 3. Run Docker Compose with env file

```bash
docker-compose --env-file .env.docker up -d
```

## Security Notes

- ⚠️ **NEVER commit `.env.docker`** - It's in `.gitignore`
- ✅ Only `.env.docker.example` should be committed (with placeholders)
- 🔒 Use strong, unique passwords for production
- 🔄 Rotate credentials regularly

## Default Ports

- Web App: `http://localhost:3000`
- OM1 Runtime: `http://localhost:8000`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
