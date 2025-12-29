# GitHub Actions CI/CD Deployment

This repository includes automated deployment workflows for staging and production environments.

## Workflows

### 1. `deploy-production.yml` - Automatic Production Deployment
- **Trigger**: Automatically runs on push to `main` branch
- **Method**: Full stack restart (docker stack rm + deploy)
- **Use case**: Standard deployments with brief downtime

### 2. `deploy-production-manual.yml` - Manual Production Deployment
- **Trigger**: Manual trigger from GitHub Actions UI
- **Methods**: 
  - **Rolling Update**: Zero-downtime deployment (default)
  - **Full Restart**: Complete stack restart
- **Use case**: Controlled deployments with choice of method

### 3. `deploy.yml` - Staging Deployment
- **Trigger**: Automatically runs on push to `staging` branch
- **Method**: AWS SSM-based deployment

## Required GitHub Secrets

To enable production deployments, add these secrets to your GitHub repository:

### Navigate to: Repository → Settings → Secrets and variables → Actions → New repository secret

| Secret Name | Description | Example Value |
|------------|-------------|---------------|
| `PROD_SSH_HOST` | Production server hostname or IP | `odoo.robobo.org` |
| `PROD_SSH_USER` | SSH username for production server | `root` |
| `PROD_SSH_KEY` | Private SSH key for authentication | (your private key content) |
| `PROD_SSH_PORT` | SSH port (optional, defaults to 22) | `22` |

### Setting up SSH Key

1. **Generate SSH key pair** (if you don't have one):
   ```bash
   ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/github_deploy
   ```

2. **Add public key to production server**:
   ```bash
   ssh-copy-id -i ~/.ssh/github_deploy.pub root@odoo.robobo.org
   ```
   
   Or manually:
   ```bash
   cat ~/.ssh/github_deploy.pub
   # Copy the output and add to /root/.ssh/authorized_keys on the server
   ```

3. **Add private key to GitHub**:
   ```bash
   cat ~/.ssh/github_deploy
   # Copy the entire content (including -----BEGIN/END lines)
   # Add as PROD_SSH_KEY secret in GitHub
   ```

## Deployment Methods Comparison

### Rolling Update (Zero Downtime)
- ✅ No service interruption
- ✅ Faster deployment
- ✅ Gradual rollout
- ⚠️ Requires Docker Swarm
- ⚠️ Not suitable for database migrations

```bash
docker service update --force odoo_web
```

### Full Restart
- ✅ Clean state
- ✅ Suitable for major updates
- ✅ Applies all configuration changes
- ⚠️ Brief downtime (10-30 seconds)

```bash
docker stack rm odoo
docker stack deploy -c docker-compose.yml odoo
```

## Usage

### Automatic Deployment (Main Branch)
Simply push or merge to `main` branch:
```bash
git checkout main
git pull
git merge feature-branch
git push origin main
```

The workflow will automatically:
1. SSH into production server
2. Pull latest changes from `linhafala_odoo` directory
3. Restart Docker Swarm stack
4. Report deployment status

### Manual Deployment
1. Go to GitHub repository → Actions tab
2. Select "Deploy to Production (Fast)" workflow
3. Click "Run workflow"
4. Choose deployment method:
   - **rolling**: Zero-downtime update
   - **full_restart**: Complete restart

## Monitoring Deployments

### View Deployment Status
- Go to repository → Actions tab
- Click on latest workflow run
- View logs for each step

### Check Production Status
SSH into server and run:
```bash
# List all services
docker service ls --filter name=odoo

# View service logs
docker service logs odoo_web --tail 100 -f

# Check service health
docker service ps odoo_web
```

## Troubleshooting

### Deployment Fails
1. Check GitHub Actions logs
2. Verify SSH connectivity:
   ```bash
   ssh -i ~/.ssh/github_deploy root@odoo.robobo.org
   ```
3. Check server disk space:
   ```bash
   df -h
   ```
4. Review Docker logs:
   ```bash
   docker service logs odoo_web --tail 100
   ```

### Services Won't Start
1. Check Docker Swarm status:
   ```bash
   docker node ls
   docker stack ps odoo
   ```
2. Inspect service errors:
   ```bash
   docker service ps odoo_web --no-trunc
   ```

### Rollback
If deployment fails, rollback to previous version:
```bash
cd /root/odoo_docker/addons-extra/linhafala_odoo/
git log --oneline -10  # Find previous commit
git checkout <previous-commit-hash>
cd /root/odoo_docker
docker service update --force odoo_web
```

## Best Practices

1. **Test in Staging First**: Always test changes in staging before deploying to production
2. **Use Rolling Updates**: Prefer rolling updates for zero-downtime deployments
3. **Monitor After Deploy**: Check logs and service health after deployment
4. **Backup Database**: Ensure regular database backups are in place
5. **Use Environments**: Configure GitHub environments for additional protection rules

## Security Notes

- ✅ SSH keys are stored as encrypted GitHub Secrets
- ✅ Private keys never appear in logs
- ✅ Use dedicated deployment keys (not personal keys)
- ✅ Restrict SSH key to specific IP if possible
- ✅ Enable GitHub environment protection rules for production

## Support

For issues or questions:
1. Check GitHub Actions workflow logs
2. Review server logs
3. Contact DevOps team
