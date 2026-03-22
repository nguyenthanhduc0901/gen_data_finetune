"""
Storage handler for saving fine-tuning data to JSON files
"""

import json
import os
import logging
from pathlib import Path
from typing import List, Dict, Any

import config

logger = logging.getLogger(__name__)


class DataStorage:
    """Handle loading and saving fine-tuning data"""
    
    def __init__(self, data_file: str = config.OUTPUT_FILE):
        self.data_file = data_file
        self.use_jsonl = config.USE_JSONL
        
        # Create parent directory if needed
        Path(self.data_file).parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"DataStorage initialized: {self.data_file}")
    
    def load_existing(self) -> List[Dict[str, Any]]:
        """
        Load existing records from file
        
        Returns:
            List of existing records, or empty list if file doesn't exist
        """
        if not os.path.exists(self.data_file):
            logger.info(f"File does not exist: {self.data_file}")
            return []
        
        try:
            if self.use_jsonl:
                # JSON Lines format
                records = []
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.strip():
                            records.append(json.loads(line))
                logger.info(f"Loaded {len(records)} records from JSONL file")
                return records
            else:
                # Standard JSON array
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Handle both direct array or wrapped in object
                    if isinstance(data, list):
                        records = data
                    elif isinstance(data, dict) and "records" in data:
                        records = data["records"]
                    else:
                        records = [data]
                    
                    logger.info(f"Loaded {len(records)} records from JSON file")
                    return records
                    
        except Exception as e:
            logger.error(f"Error loading file: {e}")
            return []
    
    def append_record(self, record: Dict[str, Any]) -> bool:
        """
        Append a single record to file
        
        Args:
            record: Single fine-tuning record
            
        Returns:
            True if successful
        """
        try:
            if self.use_jsonl:
                # JSON Lines: append as new line
                with open(self.data_file, 'a', encoding='utf-8') as f:
                    json.dump(record, f, ensure_ascii=False)
                    f.write('\n')
            else:
                # Standard JSON: load all, append, save
                records = self.load_existing() if os.path.exists(self.data_file) else []
                records.append(record)
                
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(records, f, ensure_ascii=False, indent=2)
            
            return True
            
        except Exception as e:
            logger.error(f"Error appending record: {e}")
            return False
    
    def append_records(self, records: List[Dict[str, Any]]) -> int:
        """
        Append múltiple records to file
        
        Args:
            records: List of fine-tuning records
            
        Returns:
            Number of records successfully appended
        """
        if not records:
            return 0
        
        try:
            if self.use_jsonl:
                # JSON Lines: append each as new line
                with open(self.data_file, 'a', encoding='utf-8') as f:
                    for record in records:
                        json.dump(record, f, ensure_ascii=False)
                        f.write('\n')
                
                logger.info(f"Appended {len(records)} records to JSONL file")
                return len(records)
            else:
                # Standard JSON: load all, extend, save
                existing_records = self.load_existing() if os.path.exists(self.data_file) else []
                existing_records.extend(records)
                
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    json.dump(existing_records, f, ensure_ascii=False, indent=2)
                
                logger.info(f"Appended {len(records)} records to JSON file")
                logger.info(f"Total records now: {len(existing_records)}")
                return len(records)
                
        except Exception as e:
            logger.error(f"Error appending records: {e}")
            return 0
    
    def save_records(self, records: List[Dict[str, Any]], overwrite: bool = False) -> bool:
        """
        Save records to file
        
        Args:
            records: List of records
            overwrite: If True, overwrite existing file; if False, append
            
        Returns:
            True if successful
        """
        try:
            if overwrite:
                logger.info(f"Overwriting file with {len(records)} records")
                with open(self.data_file, 'w', encoding='utf-8') as f:
                    if self.use_jsonl:
                        for record in records:
                            json.dump(record, f, ensure_ascii=False)
                            f.write('\n')
                    else:
                        json.dump(records, f, ensure_ascii=False, indent=2)
            else:
                logger.info(f"Appending {len(records)} records")
                self.append_records(records)
            
            return True
            
        except Exception as e:
            logger.error(f"Error saving records: {e}")
            return False
    
    def get_record_count(self) -> int:
        """Get total number of records in file"""
        try:
            records = self.load_existing()
            return len(records)
        except Exception as e:
            logger.error(f"Error counting records: {e}")
            return 0
    
    def create_backup(self) -> bool:
        """Create backup of current data file"""
        try:
            if not os.path.exists(self.data_file):
                logger.info("No file to backup")
                return True
            
            backup_file = config.BACKUP_FILE
            with open(self.data_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            logger.info(f"Backup created: {backup_file}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return False
    
    def validate_records(self, records: List[Dict[str, Any]]) -> tuple:
        """
        Validate records format
        
        Returns:
            (is_valid, error_message)
        """
        required_keys = {"messages"}
        message_required_keys = {"role", "content"}
        
        for i, record in enumerate(records):
            if not isinstance(record, dict):
                return False, f"Record {i} is not a dict"
            
            if required_keys - set(record.keys()):
                return False, f"Record {i} missing required keys: {required_keys - set(record.keys())}"
            
            messages = record["messages"]
            if not isinstance(messages, list):
                return False, f"Record {i} messages is not a list"
            
            if len(messages) < 2:
                return False, f"Record {i} has less than 2 messages"
            
            for j, msg in enumerate(messages):
                if not isinstance(msg, dict):
                    return False, f"Record {i}, message {j} is not a dict"
                
                if message_required_keys - set(msg.keys()):
                    return False, f"Record {i}, message {j} missing keys"
        
        return True, "All records valid"
