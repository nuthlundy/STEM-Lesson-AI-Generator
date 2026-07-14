import os
import json
from typing import Dict, Any, Optional
from core.config.settings import Settings
from core.config.validator import ConfigValidator

class ConfigLoader:
    """Loads configuration settings from defaults, environment variables, or files."""
    
    _cached_settings: Dict[str, Settings] = {}

    @staticmethod
    def load(file_path: Optional[str] = None) -> Settings:
        env_state = tuple(sorted((k, v) for k, v in os.environ.items() if k.startswith("STEM_")))
        cache_key = (file_path or "default", env_state)
        if cache_key in ConfigLoader._cached_settings:
            return ConfigLoader._cached_settings[cache_key]


        config_dict: Dict[str, Any] = {}
        
        if file_path and os.path.exists(file_path):
            try:
                with open(file_path, "r") as f:
                    file_data = json.load(f)
                    if isinstance(file_data, dict):
                        config_dict.update(file_data)
            except Exception:
                pass
                
        for field in Settings.model_fields:
            env_key = f"STEM_{field.upper()}"
            if env_key in os.environ:
                val = os.environ[env_key]
                field_type = Settings.model_fields[field].annotation
                if field_type == bool:
                    config_dict[field] = val.lower() in ("true", "1", "yes")
                elif field_type == int:
                    config_dict[field] = int(val)
                elif field_type == float:
                    config_dict[field] = float(val)
                elif field_type == dict or field_type == Dict[str, bool]:
                    try:
                        config_dict[field] = json.loads(val)
                    except Exception:
                        pass
                else:
                    config_dict[field] = val
                    
        settings = Settings(**config_dict)
        ConfigValidator.validate_settings(settings)
        ConfigLoader._cached_settings[cache_key] = settings
        return settings

