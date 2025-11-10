# Rift Rewind - Deployment Guide

This guide walks you through deploying the Rift Rewind application to AWS.

## Table of Contents
1. [Security Setup](#security-setup)
2. [Prerequisites](#prerequisites)
3. [Backend Deployment](#backend-deployment)
4. [Frontend Deployment](#frontend-deployment)
5. [Environment Configuration](#environment-configuration)
6. [AWS Setup](#aws-setup)
7. [Troubleshooting](#troubleshooting)

## Security Setup

⚠️ **CRITICAL**: Before deploying, you must:

### 1. Rotate Your Credentials

Your credentials have been exposed in the repository. **You MUST rotate them immediately**:

- **Riot API Key**: Go to https://developer.riotgames.com and regenerate your API key
- **AWS Credentials**:
  - Go to AWS IAM Console
  - Find the access key
  - Deactivate the old key
  - Create a new access key

### 2. Never Commit `.env` Files

- The `.env` file has been added to `.gitignore`
- Always use `.env.example` as a template for documentation
- Use GitHub Secrets for CI/CD pipelines
- Use AWS Secrets Manager for production runtime secrets

### 3. Clean Git History (Optional but Recommended)

To remove the old `.env` file from git history:

```bash
# Using BFG Repo-Cleaner (easiest method)
bfg --delete-files backend/.env

# Or using git filter-branch (more complex)
git filter-branch --tree-filter 'rm -f backend/.env' HEAD
```

## Prerequisites

Before deployment, ensure you have:

- [ ] AWS Account with appropriate permissions
- [ ] Docker and Docker Compose installed locally (for testing)
- [ ] PostgreSQL database (or use AWS RDS)
- [ ] Riot API Key
- [ ] AWS Access Key and Secret Access Key
- [ ] AWS Bedrock Knowledge Base ID

## Backend Deployment

### Option 1: AWS Elastic Container Service (ECS) - Recommended

#### Step 1: Create ECR Repository

```bash
# Login to AWS
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# Create ECR repository
aws ecr create-repository --repository-name rift-rewind-backend --region us-east-1

# Build and push image
docker build -t rift-rewind-backend:latest ./backend
docker tag rift-rewind-backend:latest YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rift-rewind-backend:latest
docker push YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rift-rewind-backend:latest
```

#### Step 2: Set Up RDS PostgreSQL Database

```bash
# Using AWS CLI
aws rds create-db-instance \
  --db-instance-identifier rift-rewind-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password YOUR_PASSWORD \
  --allocated-storage 20 \
  --region us-east-1
```

**Or use AWS Console:**
- Go to RDS → Create Database
- Choose PostgreSQL 15
- Use db.t3.micro (free tier eligible)
- Set master username/password
- Enable Public Accessibility (for initial setup) or configure security groups
- Note the endpoint URL

#### Step 3: Create ECS Cluster

1. Go to AWS ECS Console
2. Create new cluster (Fargate capacity)
3. Name it `rift-rewind`

#### Step 4: Create Task Definition

```bash
# Create task-definition.json
{
  "family": "rift-rewind-backend",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "containerDefinitions": [
    {
      "name": "backend",
      "image": "YOUR_AWS_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/rift-rewind-backend:latest",
      "portMappings": [
        {
          "containerPort": 5000,
          "hostPort": 5000,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {
          "name": "FLASK_ENV",
          "value": "production"
        },
        {
          "name": "AWS_DEFAULT_REGION",
          "value": "us-east-1"
        }
      ],
      "secrets": [
        {
          "name": "DATABASE_URL",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/db-url"
        },
        {
          "name": "RIOT_API_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/riot-api-key"
        },
        {
          "name": "AWS_ACCESS_KEY_ID",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/aws-access-key"
        },
        {
          "name": "AWS_SECRET_ACCESS_KEY",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/aws-secret-key"
        },
        {
          "name": "KNOWLEDGE_BASE_ID",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/knowledge-base-id"
        },
        {
          "name": "MODEL_ARN",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/model-arn"
        },
        {
          "name": "AGENT_MODEL_ID",
          "valueFrom": "arn:aws:secretsmanager:us-east-1:YOUR_ACCOUNT_ID:secret:rift-rewind/agent-model-id"
        }
      ],
      "logConfiguration": {
        "logDriver": "awslogs",
        "options": {
          "awslogs-group": "/ecs/rift-rewind-backend",
          "awslogs-region": "us-east-1",
          "awslogs-stream-prefix": "ecs"
        }
      }
    }
  ]
}

# Register task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json
```

#### Step 5: Store Secrets in AWS Secrets Manager

```bash
# Store each secret
aws secretsmanager create-secret --name rift-rewind/db-url --secret-string "postgresql://user:password@host:5432/dbname"
aws secretsmanager create-secret --name rift-rewind/riot-api-key --secret-string "YOUR_RIOT_API_KEY"
aws secretsmanager create-secret --name rift-rewind/aws-access-key --secret-string "YOUR_AWS_ACCESS_KEY"
aws secretsmanager create-secret --name rift-rewind/aws-secret-key --secret-string "YOUR_AWS_SECRET_KEY"
aws secretsmanager create-secret --name rift-rewind/knowledge-base-id --secret-string "YOUR_KB_ID"
aws secretsmanager create-secret --name rift-rewind/model-arn --secret-string "arn:aws:bedrock:us-east-1::foundation-model/..."
aws secretsmanager create-secret --name rift-rewind/agent-model-id --secret-string "us.anthropic.claude-sonnet-4-20250514-v1:0"
```

#### Step 6: Create ECS Service

1. Go to ECS Cluster → Services → Create
2. Select Fargate launch type
3. Select task definition: `rift-rewind-backend`
4. Set desired count: 2 (for HA)
5. Configure network settings (VPC, subnets, security groups)
6. Enable load balancer (Application Load Balancer)
7. Set health check path: `/health`

#### Step 7: Get Backend URL

Once the service is running:
```bash
aws elbv2 describe-load-balancers --query 'LoadBalancers[?contains(LoadBalancerName, `rift-rewind`)].DNSName'
```

This gives you the backend URL (e.g., `http://rift-rewind-backend-1234567890.us-east-1.elb.amazonaws.com`)

### Option 2: AWS Elastic Beanstalk (Simpler)

```bash
# Install EB CLI
pip install awsebcli

# Initialize Elastic Beanstalk
eb init -p "Python 3.12 running on 64bit Amazon Linux 2" rift-rewind

# Create environment
eb create rift-rewind-env

# Deploy
eb deploy

# Get URL
eb open
```

### Option 3: Docker Compose (Local Testing)

```bash
# Copy environment template
cp .env.docker.example .env

# Edit with your actual values
nano .env

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## Frontend Deployment

The frontend is automatically deployed to GitHub Pages when you push to `main`.

### Configure Backend URL for Production

1. Go to GitHub Repository → Settings → Secrets and variables → Actions
2. Add secret: `PRODUCTION_API_URL` = `https://your-backend-url.com`
3. This will be used during build time to set the API endpoint

### Example Secret Values

```
PRODUCTION_API_URL=https://rift-rewind-backend-abc123.us-east-1.elb.amazonaws.com
```

## Environment Configuration

### Backend `.env` File

Create `backend/.env` with:

```bash
# Database (RDS)
DATABASE_URL="postgresql://postgres:password@rift-rewind-db.abc123.us-east-1.rds.amazonaws.com:5432/rift_rewind"

# Riot API
RIOT_API_KEY="YOUR_RIOT_API_KEY"

# AWS
AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
AWS_DEFAULT_REGION="us-east-1"

# Bedrock
KNOWLEDGE_BASE_ID="YOUR_KB_ID"
MODEL_ARN="arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-haiku-20240307-v1:0"
AGENT_MODEL_ID="us.anthropic.claude-sonnet-4-20250514-v1:0"

# Flask
FLASK_ENV="production"
SECRET_KEY="YOUR_SECRET_KEY_CHANGE_THIS"
```

### Frontend `.env` File

Create `rift-rewind/.env` with:

```bash
VITE_API_URL=https://your-backend-url.com
```

## AWS Setup

### 1. Create IAM User for CI/CD

1. Go to AWS IAM Console
2. Create new user: `rift-rewind-ci`
3. Attach policies:
   - AmazonEC2ContainerRegistryPowerUser (for ECR)
   - AmazonECS_FullAccess (for ECS)
   - IAMReadOnlyAccess

4. Create access keys and add to GitHub Secrets:
   - `AWS_ACCESS_KEY_ID`
   - `AWS_SECRET_ACCESS_KEY`

### 2. Create ECR Repository

```bash
aws ecr create-repository --repository-name rift-rewind-backend --region us-east-1
```

### 3. Set Up Security Groups

**Backend Security Group:**
- Inbound: Port 5000 from ALB security group
- Outbound: All to anywhere (needed for API calls)

**RDS Security Group:**
- Inbound: Port 5432 from Backend security group
- Outbound: All to anywhere

**ALB Security Group:**
- Inbound: Port 80, 443 from 0.0.0.0/0
- Outbound: Port 5000 to Backend security group

## Troubleshooting

### Backend not responding

1. Check CloudWatch logs:
```bash
aws logs tail /ecs/rift-rewind-backend --follow
```

2. Verify environment variables in ECS task
3. Check security group rules
4. Test database connectivity:
```bash
psql -h YOUR_RDS_ENDPOINT -U postgres -d rift_rewind
```

### Frontend API errors

1. Check browser console for CORS errors
2. Verify `VITE_API_URL` is set correctly
3. Ensure backend health check passes:
```bash
curl https://your-backend-url/health
```

### Database connection errors

1. Verify DATABASE_URL format
2. Check RDS security group allows your IP
3. Verify database and user exist:
```bash
psql -h HOST -U postgres -l
```

### Docker build failures

```bash
# Build locally first
docker build -t rift-rewind-backend:latest ./backend

# Debug with interactive shell
docker run -it rift-rewind-backend:latest /bin/sh
```

## Monitoring & Logs

### CloudWatch

```bash
# View logs
aws logs tail /ecs/rift-rewind-backend --follow

# Create alarms
aws cloudwatch put-metric-alarm \
  --alarm-name rift-rewind-backend-cpu \
  --alarm-description "Alert when CPU > 80%" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

### Health Checks

Backend health endpoint: `GET /health`

This is checked by the load balancer every 30 seconds.

## Next Steps

1. Deploy backend to AWS ECS
2. Get backend URL
3. Add `PRODUCTION_API_URL` to GitHub Secrets
4. Push to main to trigger frontend build
5. Test frontend at GitHub Pages URL
6. Monitor logs and set up alarms

## Support

For issues:
1. Check CloudWatch logs
2. Review environment variables
3. Test locally with docker-compose
4. Check AWS service quotas
