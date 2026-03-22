"""
Format generated data into OpenAI fine-tuning format
"""

import json
import logging
from typing import Dict, Any

from prompts import PERSONAS

logger = logging.getLogger(__name__)


class DataFormatter:
    """Format generated data into fine-tuning conversation format"""
    
    @staticmethod
    def to_fine_tune_format(
        focus_area: str,
        context: str,
        difficulty: str,
        complete_data: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Convert complete unified data to OpenAI fine-tune message format
        
        Args:
            focus_area: DEBUG_FOCUS, OPTIMIZATION_FOCUS, etc.
            context: Problem context
            difficulty: Difficulty level
            complete_data: Output from unified LLM call (8 fields)
            
        Returns:
            Formatted record with "messages" field
        """
        
        # Get appropriate persona for this focus_area and difficulty
        persona = PERSONAS.get(focus_area, {}).get(difficulty, "Gia sư Socratic")
        
        # Build system message
        system_message = f"Persona: {persona}"
        
        # Build user message from complete_data
        user_parts = [
            f"Bối cảnh: [{context}]",
            f"Đề bài: {complete_data.get('problem_description', '')}",
            f"Code:",
            complete_data.get('buggy_code', ''),
            f"Lỗi: {complete_data.get('environment_feedback', '')}",
        ]
        user_message = "\n".join(user_parts)
        
        # Build assistant message (combine all 4 teaching components)
        assistant_parts = [
            complete_data.get('diagnosis', ''),
            complete_data.get('root_cause', ''),
            complete_data.get('related_knowledge', ''),
            complete_data.get('socratic_hint', ''),
        ]
        # Filter out empty parts and join
        assistant_message = "\n\n".join([p for p in assistant_parts if p.strip()])
        
        return {
            "messages": [
                {
                    "role": "system",
                    "content": system_message,
                },
                {
                    "role": "user",
                    "content": user_message,
                },
                {
                    "role": "assistant",
                    "content": assistant_message,
                },
            ]
        }
    
    @staticmethod
    def format_batch(
        generated_records: list,
    ) -> list:
        """
        Format a batch of generated records
        
        Args:
            generated_records: List of dicts from AsyncLLMBatcher.batch_generate()
            
        Returns:
            List of formatted records ready for fine-tuning
        """
        formatted = []
        
        for record in generated_records:
            if record is None:
                continue
            
            try:
                formatted_record = DataFormatter.to_fine_tune_format(
                    focus_area=record["focus_area"],
                    context=record["context"],
                    difficulty=record["difficulty"],
                    complete_data=record["problem_data"],
                )
                formatted.append(formatted_record)
                
            except Exception as e:
                logger.error(f"Failed to format record: {e}")
                continue
        
        logger.info(f"Successfully formatted {len(formatted)} records")
        return formatted

