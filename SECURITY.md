# Security Policy

## Supported Versions

We provide security updates for the following versions of AstralytiQ:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | ✅ Yes             |
| 1.0.x   | ⚠️ Limited Support |
| < 1.0.0 | ❌ No              |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

If you discover a security vulnerability within AstralytiQ, please send an e-mail to security@astralytiq.com. All security vulnerabilities will be promptly addressed.

Please include the following in your report:
- Type of issue (e.g., SQL injection, XSS, etc.)
- Steps to reproduce the issue
- Potential impact of the vulnerability
- Any suggested fixes (optional)

We will acknowledge receipt of your vulnerability report within 48 hours and send a follow-up response within 72 hours detailing the next steps.

## Security Best Practices for Deployment

- **Environment Variables**: Never commit `.env` files. Use secret managers (GCP Secret Manager, AWS Secrets Manager).
- **TLS/SSL**: Always serve production instances over HTTPS.
- **JWT Secrets**: Use a strong, randomly generated string for `JWT_SECRET_KEY`.
- **Database Access**: Ensure the database is not publicly accessible and uses strong authentication.
