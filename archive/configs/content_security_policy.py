"""
Content Security Policy (CSP) Implementation for Sentinel GRC
============================================================
Zero-cost CSP headers and security middleware for Streamlit and web deployment.
"""

import os
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

class ContentSecurityPolicy:
    """Content Security Policy header generator and validator"""
    
    def __init__(self, mode: str = "strict"):
        """
        Initialize CSP with security mode
        
        Args:
            mode: 'strict', 'balanced', or 'permissive'
        """
        self.mode = mode
        self.nonce_cache = {}
        
        # Base CSP directives
        self.base_directives = {
            'default-src': ["'self'"],
            'script-src': ["'self'"],
            'style-src': ["'self'", "'unsafe-inline'"],  # Streamlit requires unsafe-inline for styles
            'img-src': ["'self'", "data:", "https:"],
            'font-src': ["'self'", "https://fonts.gstatic.com"],
            'connect-src': ["'self'"],
            'media-src': ["'self'"],
            'object-src': ["'none'"],
            'base-uri': ["'self'"],
            'form-action': ["'self'"],
            'frame-ancestors': ["'none'"],
            'block-all-mixed-content': [],
            'upgrade-insecure-requests': []
        }
        
        # Mode-specific configurations
        self._configure_for_mode()
    
    def _configure_for_mode(self):
        """Configure CSP based on security mode"""
        
        if self.mode == "strict":
            # Strictest security - only essential sources
            self.directives = {
                **self.base_directives,
                'script-src': ["'self'", "'strict-dynamic'"],
                'style-src': ["'self'", "'unsafe-inline'"],  # Required for Streamlit
                'connect-src': [
                    "'self'", 
                    "https://api.groq.com",  # Groq API
                    "https://*.supabase.co",  # Supabase
                    "wss://*.supabase.co"     # Supabase realtime
                ]
            }
            
        elif self.mode == "balanced":
            # Balanced - allows common CDNs
            self.directives = {
                **self.base_directives,
                'script-src': [
                    "'self'", 
                    "'unsafe-inline'",  # Required for Streamlit
                    "https://cdn.jsdelivr.net"
                ],
                'style-src': [
                    "'self'", 
                    "'unsafe-inline'", 
                    "https://fonts.googleapis.com",
                    "https://cdn.jsdelivr.net"
                ],
                'connect-src': [
                    "'self'",
                    "https://api.groq.com",
                    "https://*.supabase.co",
                    "wss://*.supabase.co",
                    "https://cdn.jsdelivr.net"
                ]
            }
            
        else:  # permissive
            # Most permissive - for development
            self.directives = {
                **self.base_directives,
                'script-src': [
                    "'self'", 
                    "'unsafe-inline'", 
                    "'unsafe-eval'",  # For development tools
                    "https:"
                ],
                'style-src': [
                    "'self'", 
                    "'unsafe-inline'", 
                    "https:"
                ],
                'connect-src': [
                    "'self'",
                    "https:",
                    "wss:",
                    "ws:"
                ]
            }
    
    def add_allowed_source(self, directive: str, source: str):
        """Add an allowed source to a CSP directive"""
        if directive not in self.directives:
            self.directives[directive] = []
        
        if source not in self.directives[directive]:
            self.directives[directive].append(source)
            logger.info(f"Added {source} to {directive}")
    
    def remove_allowed_source(self, directive: str, source: str):
        """Remove an allowed source from a CSP directive"""
        if directive in self.directives and source in self.directives[directive]:
            self.directives[directive].remove(source)
            logger.info(f"Removed {source} from {directive}")
    
    def generate_header(self, include_report_uri: bool = False) -> str:
        """Generate CSP header string"""
        csp_parts = []
        
        for directive, sources in self.directives.items():
            if sources:
                directive_string = f"{directive} {' '.join(sources)}"
            else:
                directive_string = directive
            csp_parts.append(directive_string)
        
        # Add report URI if requested (for monitoring)
        if include_report_uri:
            report_uri = os.getenv("CSP_REPORT_URI", "/api/csp-report")
            csp_parts.append(f"report-uri {report_uri}")
        
        return "; ".join(csp_parts)
    
    def get_security_headers(self, include_csp_report: bool = False) -> Dict[str, str]:
        """Get all security headers including CSP"""
        headers = {
            # Content Security Policy
            'Content-Security-Policy': self.generate_header(include_csp_report),
            
            # Additional security headers
            'X-Content-Type-Options': 'nosniff',
            'X-Frame-Options': 'DENY',
            'X-XSS-Protection': '1; mode=block',
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            'Permissions-Policy': (
                'geolocation=(), microphone=(), camera=(), '
                'payment=(), usb=(), magnetometer=(), gyroscope=()'
            ),
            
            # HSTS (if HTTPS)
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload',
            
            # Cache control for sensitive pages
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
        
        return headers
    
    def validate_violation_report(self, report_data: Dict) -> bool:
        """Validate CSP violation report"""
        required_fields = ['document-uri', 'violated-directive', 'blocked-uri']
        
        # Check if all required fields are present
        for field in required_fields:
            if field not in report_data:
                logger.warning(f"CSP violation report missing field: {field}")
                return False
        
        # Log the violation
        logger.warning(
            f"CSP Violation: {report_data.get('violated-directive')} "
            f"blocked {report_data.get('blocked-uri')} "
            f"on {report_data.get('document-uri')}"
        )
        
        return True

class StreamlitSecurityMiddleware:
    """Security middleware for Streamlit applications"""
    
    def __init__(self, csp_mode: str = "balanced"):
        self.csp = ContentSecurityPolicy(mode=csp_mode)
        self.security_stats = {
            'requests_processed': 0,
            'csp_violations': 0,
            'blocked_requests': 0
        }
    
    def add_security_headers(self, response_headers: Dict[str, str]) -> Dict[str, str]:
        """Add security headers to Streamlit response"""
        security_headers = self.csp.get_security_headers()
        
        # Merge with existing headers
        merged_headers = {**response_headers, **security_headers}
        
        self.security_stats['requests_processed'] += 1
        return merged_headers
    
    def create_streamlit_config(self) -> Dict[str, any]:
        """Create Streamlit configuration with security settings"""
        config = {
            # Server configuration
            'server': {
                'port': int(os.getenv('PORT', 8501)),
                'enableCORS': False,
                'enableXsrfProtection': True,
                'maxUploadSize': 10,  # 10MB max upload
                'maxMessageSize': 200,  # 200MB max message
                'enableWebsocketCompression': True
            },
            
            # Browser configuration
            'browser': {
                'gatherUsageStats': False,  # Privacy
                'serverAddress': 'localhost',
                'serverPort': int(os.getenv('PORT', 8501))
            },
            
            # Global configuration
            'global': {
                'developmentMode': os.getenv('DEVELOPMENT', 'false').lower() == 'true',
                'logLevel': 'info',
                'showErrorDetails': os.getenv('DEVELOPMENT', 'false').lower() == 'true'
            },
            
            # Theme (optional)
            'theme': {
                'primaryColor': '#1f77b4',
                'backgroundColor': '#ffffff',
                'secondaryBackgroundColor': '#f0f2f6',
                'textColor': '#262730'
            }
        }
        
        return config
    
    def get_stats(self) -> Dict[str, any]:
        """Get security middleware statistics"""
        return {
            **self.security_stats,
            'csp_mode': self.csp.mode,
            'csp_header_length': len(self.csp.generate_header())
        }

def create_nginx_config(domain: str = "sentinelgrc.com") -> str:
    """Create Nginx configuration with security headers"""
    
    csp = ContentSecurityPolicy(mode="balanced")
    headers = csp.get_security_headers(include_csp_report=True)
    
    nginx_config = f"""
# Nginx configuration for Sentinel GRC with security headers
server {{
    listen 80;
    listen 443 ssl http2;
    server_name {domain} www.{domain};
    
    # SSL configuration (Let's Encrypt)
    ssl_certificate /etc/letsencrypt/live/{domain}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain}/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
"""
    
    for header_name, header_value in headers.items():
        nginx_config += f'    add_header "{header_name}" "{header_value}" always;\n'
    
    nginx_config += f"""
    
    # Rate limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/m;
    limit_req_zone $binary_remote_addr zone=general:10m rate=60r/m;
    
    # Main application
    location / {{
        limit_req zone=general burst=20 nodelay;
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }}
    
    # API endpoints with stricter rate limiting
    location /api/ {{
        limit_req zone=api burst=5 nodelay;
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }}
    
    # CSP violation reporting
    location /api/csp-report {{
        limit_req zone=api burst=10 nodelay;
        proxy_pass http://127.0.0.1:8501;
        proxy_set_header Content-Type application/csp-report;
    }}
    
    # Block common attack paths
    location ~ ^/(admin|phpmyadmin|wp-admin|wp-login) {{
        return 444;
    }}
    
    # Redirect HTTP to HTTPS
    if ($scheme != "https") {{
        return 301 https://$host$request_uri;
    }}
}}
"""
    
    return nginx_config

def create_apache_config(domain: str = "sentinelgrc.com") -> str:
    """Create Apache configuration with security headers"""
    
    csp = ContentSecurityPolicy(mode="balanced")
    headers = csp.get_security_headers(include_csp_report=True)
    
    apache_config = f"""
# Apache configuration for Sentinel GRC with security headers
<VirtualHost *:80>
    ServerName {domain}
    ServerAlias www.{domain}
    
    # Redirect to HTTPS
    Redirect permanent / https://{domain}/
</VirtualHost>

<VirtualHost *:443>
    ServerName {domain}
    ServerAlias www.{domain}
    
    # SSL configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/{domain}/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/{domain}/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/{domain}/chain.pem
    
    # Modern SSL configuration
    SSLProtocol TLSv1.2 TLSv1.3
    SSLCipherSuite ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    
    # Security headers
"""
    
    for header_name, header_value in headers.items():
        apache_config += f'    Header always set "{header_name}" "{header_value}"\n'
    
    apache_config += f"""
    
    # Rate limiting (requires mod_evasive)
    DOSHashTableSize    2048
    DOSPageCount        10
    DOSSiteCount        50
    DOSPageInterval     1
    DOSSiteInterval     1
    DOSBlockingPeriod   600
    
    # Proxy configuration
    ProxyPreserveHost On
    ProxyPass / http://127.0.0.1:8501/
    ProxyPassReverse / http://127.0.0.1:8501/
    
    # WebSocket support
    RewriteEngine On
    RewriteCond %{{HTTP:Upgrade}} websocket [NC]
    RewriteCond %{{HTTP:Connection}} upgrade [NC]
    RewriteRule ^/?(.*) "ws://127.0.0.1:8501/$1" [P,L]
    
    # Block common attack paths
    <LocationMatch "^/(admin|phpmyadmin|wp-admin|wp-login)">
        Require all denied
    </LocationMatch>
    
    # Custom error pages
    ErrorDocument 403 /403.html
    ErrorDocument 404 /404.html
    ErrorDocument 500 /500.html
</VirtualHost>
"""
    
    return apache_config

if __name__ == "__main__":
    # Test CSP implementation
    print("Testing Content Security Policy...")
    
    # Test different modes
    for mode in ["strict", "balanced", "permissive"]:
        print(f"\n{mode.upper()} MODE:")
        csp = ContentSecurityPolicy(mode=mode)
        headers = csp.get_security_headers()
        
        print(f"CSP Header: {csp.generate_header()[:100]}...")
        print(f"Total headers: {len(headers)}")
    
    # Test Streamlit middleware
    print("\nTesting Streamlit Security Middleware:")
    middleware = StreamlitSecurityMiddleware(csp_mode="balanced")
    
    # Simulate processing a request
    response_headers = {"Content-Type": "text/html"}
    secure_headers = middleware.add_security_headers(response_headers)
    
    print(f"Original headers: {len(response_headers)}")
    print(f"Secure headers: {len(secure_headers)}")
    print(f"Middleware stats: {middleware.get_stats()}")
    
    # Generate web server configs
    print("\nGenerating web server configurations...")
    
    # Save Nginx config
    nginx_conf = create_nginx_config("sentinelgrc.com")
    with open("nginx-security.conf", "w") as f:
        f.write(nginx_conf)
    print("Generated: nginx-security.conf")
    
    # Save Apache config
    apache_conf = create_apache_config("sentinelgrc.com")
    with open("apache-security.conf", "w") as f:
        f.write(apache_conf)
    print("Generated: apache-security.conf")
    
    print("\nContent Security Policy implementation ready!")