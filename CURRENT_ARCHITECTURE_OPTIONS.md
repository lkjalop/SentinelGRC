# secure_config.py - Zero-cost security for API keys

import os
from pathlib import Path
import json
from cryptography.fernet import Fernet
import base64

class SecureConfig:
    """
    Zero-cost security for API keys and secrets.
    Uses local encryption and environment variables.
    """
    
    def __init__(self, config_dir=".config"):
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(exist_ok=True)
        self.key_file = self.config_dir / "key.enc"
        self.secrets_file = self.config_dir / "secrets.enc"
        
        # Initialize encryption key
        if not self.key_file.exists():
            self._generate_key()
        
        self.cipher = Fernet(self._load_key())
    
    def _generate_key(self):
        """Generate encryption key for secrets"""
        key = Fernet.generate_key()
        with open(self.key_file, 'wb') as f:
            f.write(key)
        
        # Make key file read-only
        os.chmod(self.key_file, 0o400)
    
    def _load_key(self):
        """Load encryption key"""
        with open(self.key_file, 'rb') as f:
            return f.read()
    
    def store_secret(self, name: str, value: str):
        """Store encrypted secret"""
        secrets = self._load_secrets()
        secrets[name] = value
        
        encrypted_data = self.cipher.encrypt(json.dumps(secrets).encode())
        
        with open(self.secrets_file, 'wb') as f:
            f.write(encrypted_data)
        
        # Make secrets file read-only
        os.chmod(self.secrets_file, 0o400)
    
    def get_secret(self, name: str) -> str:
        """Get decrypted secret"""
        # Try environment variable first
        env_value = os.getenv(name.upper())
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
                encrypted_data = f.read()
            
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return json.loads(decrypted_data.decode())
        
        except Exception:
            return {}
    
    def setup_from_text_file(self, text_file_path: str):
        """Setup secrets from your secrets.txt file"""
        if not Path(text_file_path).exists():
            print(f"File {text_file_path} not found")
            return
        
        with open(text_file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if '=' in line and not line.startswith('#'):
                    key, value = line.split('=', 1)
                    self.store_secret(key.strip(), value.strip())
                    print(f"Stored secret: {key.strip()}")
    
    def get_groq_client(self):
        """Get configured Groq client"""
        api_key = self.get_secret('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in secrets")
        
        try:
            import groq
            return groq.Client(api_key=api_key)
        except ImportError:
            raise ImportError("Please install groq: pip install groq")

# Usage example:
if __name__ == "__main__":
    config = SecureConfig()
    
    # Setup from your secrets.txt file
    config.setup_from_text_file("secrets.txt")
    
    # Test Groq connection
    try:
        client = config.get_groq_client()
        print("Groq client configured successfully!")
    except Exception as e:
        print(f"Error: {e}")