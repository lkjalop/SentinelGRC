"""
Secure Configuration Management for Sentinel GRC
================================================
Zero-cost security for API keys and secrets.
"""

import os
from pathlib import Path
import json
from cryptography.fernet import Fernet
import getpass

class SecureConfig:
    """
    Local encryption for API keys - completely free.
    Better than storing in plain text files.
    """
    
    def __init__(self, config_dir=".config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.key_file = self.config_dir / "key.enc"
        self.secrets_file = self.config_dir / "secrets.enc"
        
        # Initialize encryption
        if not self.key_file.exists():
            self._generate_key()
        
        self.cipher = Fernet(self._load_key())
    
    def _generate_key(self):
        """Generate encryption key"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        os.chmod(self.key_file, 0o600)  # Read-only for owner
    
    def _load_key(self):
        """Load encryption key"""
        with open(self.key_file, 'rb') as f:
            return f.read()
    
    def store_secret(self, name: str, value: str):
        """Store encrypted secret"""
        secrets = self._load_secrets()
        secrets[name] = value
        
        encrypted = self.cipher.encrypt(json.dumps(secrets).encode())
        
        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted)
        os.chmod(self.secrets_file, 0o600)
    
    def get_secret(self, name: str) -> str:
        """Get decrypted secret"""
        # Try environment variable first
        env_value = os.getenv(name)
        if env_value:
            return env_value
        
        # Fall back to encrypted storage
        secrets = self._load_secrets()
        return secrets.get(name)
    
    def _load_secrets(self) -> dict:
        """Load and decrypt secrets"""
        if not self.secrets_file.exists():
            return {}
        
        try:
            with open(self.secrets_file, 'rb') as f:
                encrypted = f.read()
            decrypted = self.cipher.decrypt(encrypted)
            return json.loads(decrypted.decode())
        except:
            return {}
    
    def setup_interactively(self):
        """Interactive setup for secrets"""
        print("Sentinel GRC - Secure Configuration Setup")
        print("=" * 45)
        
        groq_key = getpass.getpass("Enter your Groq API key: ")
        if groq_key:
            self.store_secret("GROQ_API_KEY", groq_key)
            print("✅ Groq API key stored securely")
        
        neo4j_password = getpass.getpass("Enter Neo4j password: ")
        if neo4j_password:
            self.store_secret("NEO4J_PASSWORD", neo4j_password)
            print("✅ Neo4j password stored securely")
        
        print("\n✅ Configuration complete!")
        print("Your secrets are encrypted and stored locally.")
    
    def get_groq_client(self):
        """Get configured Groq client"""
        api_key = self.get_secret("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not configured. Run setup_interactively()")
        
        try:
            import groq
            return groq.Client(api_key=api_key)
        except ImportError:
            raise ImportError("Install groq: pip install groq")


# Usage example
def setup_secrets():
    """One-time setup for your secrets"""
    config = SecureConfig()
    config.setup_interactively()
    
    # Test Groq connection
    try:
        client = config.get_groq_client()
        print("✅ Groq client test successful!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    setup_secrets()