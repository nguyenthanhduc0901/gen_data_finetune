"""
LLM Client for calling Claude API or Gemini API
Handles retries, rate limiting, and JSON parsing
"""

import asyncio
import json
import logging
from typing import Dict, Optional, Any
import httpx

import config
from prompts import PROMPTS, PERSONAS

logger = logging.getLogger(__name__)

# Try to import Google GenAI
try:
    from google import genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    logger.warning("google-genai not installed. Gemini provider will not be available.")


class LLMClient:
    """Client for calling LLM APIs (Claude, Gemini, etc)"""
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = config.MODEL_NAME,
        provider: str = config.LLM_PROVIDER,
        timeout: int = config.API_TIMEOUT,
    ):
        self.api_key = api_key or config.API_KEY
        self.model = model
        self.provider = provider.lower()
        self.timeout = timeout
        
        if not self.api_key:
            raise ValueError(f"API_KEY not provided in config or environment (provider: {self.provider})")
        
        # Provider-specific setup
        if self.provider == "gemini":
            if not HAS_GEMINI:
                raise ImportError("google-genai not installed. Run: pip install google-genai")
            # Initialize Gemini client
            self.client = genai.Client(api_key=self.api_key)
            logger.info(f"Initialized Gemini LLMClient with model: {self.model}")
        
        elif self.provider == "anthropic":
            self.base_url = "https://api.anthropic.com/v1"
            logger.info(f"Initialized Claude LLMClient with model: {self.model}")
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}. Supported: anthropic, gemini")
        
        self.token_count = 0
    
    def _call_gemini_api(self, prompt_text: str, max_tokens: int = 2000) -> str:
        """
        Call Gemini API with retry logic (synchronous wrapper)
        
        Args:
            prompt_text: The prompt text to send
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from Gemini
        """
        import time
        
        for attempt in range(config.MAX_RETRIES):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt_text
                )
                
                content = response.text
                
                # Track tokens (estimate if not provided)
                if hasattr(response, 'usage_metadata') and response.usage_metadata:
                    metadata = response.usage_metadata
                    # Try different attribute names for Gemini API
                    try:
                        input_tokens = getattr(metadata, 'prompt_token_count', getattr(metadata, 'input_tokens', 0))
                        output_tokens = getattr(metadata, 'candidates_token_count', getattr(metadata, 'output_tokens', 0))
                        self.token_count += input_tokens + output_tokens
                    except Exception:
                        # Fallback to estimation if attributes don't match
                        self.token_count += (len(prompt_text) + len(content)) // 4
                else:
                    # Rough estimate: ~4 chars per token
                    self.token_count += (len(prompt_text) + len(content)) // 4
                
                logger.debug(f"Gemini API call successful. Total tokens used: {self.token_count}")
                return content
                
            except Exception as e:
                wait_time = config.RETRY_BACKOFF ** attempt
                if attempt < config.MAX_RETRIES - 1:
                    logger.warning(f"Gemini API error (attempt {attempt + 1}): {e}. Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Gemini API error (final attempt): {e}")
                    raise
        
        raise Exception("Max retries exceeded for Gemini API")
    
    async def _call_anthropic_api(self, messages: list, max_tokens: int = 2000) -> str:
        """
        Call Anthropic Claude API with retry logic
        
        Args:
            messages: List of message dicts with role and content
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from Claude
        """
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        
        payload = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": messages,
        }
        
        for attempt in range(config.MAX_RETRIES):
            try:
                async with httpx.AsyncClient(timeout=self.timeout) as client:
                    response = await client.post(
                        f"{self.base_url}/messages",
                        json=payload,
                        headers=headers,
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        # Track tokens
                        self.token_count += data.get("usage", {}).get("input_tokens", 0)
                        self.token_count += data.get("usage", {}).get("output_tokens", 0)
                        
                        content = data["content"][0]["text"]
                        logger.debug(f"Claude API call successful. Total tokens used: {self.token_count}")
                        return content
                    
                    elif response.status_code == 429:
                        wait_time = config.RETRY_BACKOFF ** attempt
                        logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                        continue
                    
                    else:
                        logger.error(f"API Error: {response.status_code} - {response.text}")
                        raise Exception(f"API Error {response.status_code}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Timeout on attempt {attempt + 1}/{config.MAX_RETRIES}")
                if attempt < config.MAX_RETRIES - 1:
                    await asyncio.sleep(config.RETRY_BACKOFF ** attempt)
                else:
                    raise
            
            except Exception as e:
                logger.error(f"Error on attempt {attempt + 1}: {e}")
                if attempt < config.MAX_RETRIES - 1:
                    await asyncio.sleep(config.RETRY_BACKOFF ** attempt)
                else:
                    raise
        
        raise Exception("Max retries exceeded")
    
    async def _call_api(self, messages: list, max_tokens: int = 2000) -> str:
        """
        Route to the appropriate LLM API based on provider
        
        Args:
            messages: List of message dicts with role and content
            max_tokens: Maximum tokens in response
            
        Returns:
            Response text from LLM
        """
        if self.provider == "gemini":
            # Convert messages to prompt text for Gemini
            prompt_text = "\n".join([f"{m['role']}: {m['content']}" for m in messages])
            # Call Gemini synchronously and wrap in async
            loop = asyncio.get_event_loop()
            return await loop.run_in_executor(None, self._call_gemini_api, prompt_text, max_tokens)
        
        elif self.provider == "anthropic":
            return await self._call_anthropic_api(messages, max_tokens)
        
        else:
            raise ValueError(f"Unknown provider: {self.provider}")
    
    async def generate_complete_record(
        self,
        focus_area: str,
        context: str,
        difficulty: str,
    ) -> Dict[str, Any]:
        """
        Generate complete training record (problem + teaching response) in ONE LLM call
        
        Args:
            focus_area: One of DEBUG_FOCUS, OPTIMIZATION_FOCUS, etc.
            context: Problem context (Bank, Game, etc.)
            difficulty: Trình độ (Mới bắt đầu, Trung bình, Giỏi)
            
        Returns:
            Parsed JSON with all 8 fields from unified call
        """
        logger.info(f"Generating complete record: {focus_area} / {context} / {difficulty}")
        
        # Build prompt using unified template
        template = PROMPTS[focus_area]["unified"]
        
        # Add optional params
        params = {
            "focus_area": focus_area,
            "context": context,
            "difficulty": difficulty,
        }
        
        if focus_area == "DEBUG_FOCUS":
            import random
            params["bug_type"] = random.choice(config.BUG_TYPES)
        
        if focus_area == "OPTIMIZATION_FOCUS":
            params["size"] = "100,000"
        
        prompt = template.format(**params)
        
        # Call API (1 call duy nhất)
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_api(messages, max_tokens=2000)
        
        # Parse JSON from response
        try:
            json_str = self._extract_json(response)
            complete_data = json.loads(json_str)
            
            # Validate all required fields exist
            required_fields = [
                "problem_description",
                "buggy_code",
                "environment_feedback",
                "hidden_teacher_context",
                "diagnosis",
                "root_cause",
                "related_knowledge",
                "socratic_hint",
            ]
            
            missing_fields = [f for f in required_fields if f not in complete_data]
            if missing_fields:
                raise ValueError(f"Missing fields: {missing_fields}")
            
            logger.debug("Successfully generated complete record")
            return complete_data
            
        except Exception as e:
            logger.error(f"Failed to parse complete record response: {e}")
            logger.debug(f"Raw response: {response[:500]}")
            raise
    
    @staticmethod
    def _extract_json(text: str) -> str:
        """
        Extract JSON object from text that might contain other content
        
        Args:
            text: Response text from Claude
            
        Returns:
            JSON string
        """
        # Try to find JSON object in the text
        start = text.find('{')
        if start == -1:
            raise ValueError("No JSON object found in response")
        
        # Find matching closing brace
        brace_count = 0
        for i in range(start, len(text)):
            if text[i] == '{':
                brace_count += 1
            elif text[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    return text[start:i+1]
        
        raise ValueError("JSON object not properly closed")
    
    def get_token_usage(self) -> Dict[str, int]:
        """Get total token usage"""
        estimated_cost = (self.token_count / 1000) * 0.003  # Rough estimate for Claude
        return {
            "total_tokens": self.token_count,
            "estimated_cost_usd": round(estimated_cost, 2),
        }


class AsyncLLMBatcher:
    """Batch manage múltiple concurrent LLM requests"""
    
    def __init__(self, client: LLMClient, max_concurrent: int = config.CONCURRENT_REQUESTS):
        self.client = client
        self.semaphore = asyncio.Semaphore(max_concurrent)
    
    async def generate_record(
        self,
        focus_area: str,
        context: str,
        difficulty: str,
    ) -> Dict[str, Any]:
        """
        Generate a complete training record (1 unified LLM call)
        """
        async with self.semaphore:
            try:
                # 1 LLM call - sinh toàn bộ
                complete_data = await self.client.generate_complete_record(
                    focus_area, context, difficulty
                )
                
                return {
                    "focus_area": focus_area,
                    "context": context,
                    "difficulty": difficulty,
                    "problem_data": complete_data,
                }
                
            except Exception as e:
                logger.error(f"Failed to generate record: {e}")
                return None
    
    async def batch_generate(
        self,
        records: list,
    ) -> list:
        """
        Generate múltiple records concurrently
        
        Args:
            records: List of tuples (focus_area, context, difficulty)
            
        Returns:
            List of generated records
        """
        tasks = [
            self.generate_record(focus_area, context, difficulty)
            for focus_area, context, difficulty in records
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=False)
        
        # Filter out None results (failed generations)
        valid_results = [r for r in results if r is not None]
        logger.info(f"Successfully generated {len(valid_results)}/{len(records)} records")
        
        return valid_results
