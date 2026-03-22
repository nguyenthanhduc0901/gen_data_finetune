"""
Main script to generate fine-tuning data using LLM
"""

import asyncio
import logging
import random
import sys
from datetime import datetime
from typing import List, Tuple

import config
from llm_client import LLMClient, AsyncLLMBatcher
from data_formatter import DataFormatter
from data_storage import DataStorage

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT,
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler(),
    ],
)
logger = logging.getLogger(__name__)


def generate_record_specs(
    num_records: int,
    focus_distributions: dict = None,
) -> List[Tuple[str, str, str]]:
    """
    Generate record specifications (focus_area, context, difficulty)
    
    Args:
        num_records: Total number of records to generate
        focus_distributions: Distribution of focus areas
        
    Returns:
        List of tuples: (focus_area, context, difficulty)
    """
    
    if focus_distributions is None:
        focus_distributions = config.FOCUS_DISTRIBUTIONS
    
    focus_areas = list(focus_distributions.keys())
    weights = list(focus_distributions.values())
    
    specs = []
    for _ in range(num_records):
        focus_area = random.choices(focus_areas, weights=weights)[0]
        context = random.choice(config.CONTEXTS)
        difficulty = random.choice(config.DIFFICULTIES)
        
        specs.append((focus_area, context, difficulty))
    
    logger.info(f"Generated {num_records} record specifications")
    return specs


async def generate_batch(
    specs: List[Tuple[str, str, str]],
    batch_size: int = config.BATCH_SIZE,
) -> List:
    """
    Generate a batch of records
    
    Args:
        specs: List of record specifications
        batch_size: Size of each batch
        
    Returns:
        List of generated records
    """
    
    try:
        client = LLMClient(api_key=config.API_KEY, model=config.MODEL_NAME)
    except ValueError as e:
        logger.error(f"Failed to initialize LLM client: {e}")
        logger.error("Please set ANTHROPIC_API_KEY environment variable")
        sys.exit(1)
    
    batcher = AsyncLLMBatcher(client, max_concurrent=config.CONCURRENT_REQUESTS)
    
    all_records = []
    num_batches = (len(specs) + batch_size - 1) // batch_size
    
    for batch_num in range(num_batches):
        start_idx = batch_num * batch_size
        end_idx = min((batch_num + 1) * batch_size, len(specs))
        batch_specs = specs[start_idx:end_idx]
        
        logger.info(f"Processing batch {batch_num + 1}/{num_batches} ({len(batch_specs)} records)")
        
        # Generate records concurrently
        generated = await batcher.batch_generate(batch_specs)
        
        # Format to fine-tune format
        formatted = DataFormatter.format_batch(generated)
        all_records.extend(formatted)
        
        logger.info(f"Batch {batch_num + 1} complete. Generated {len(formatted)} valid records")
    
    # Log token usage
    usage = client.get_token_usage()
    logger.info(f"Token usage: {usage['total_tokens']} tokens (~${usage['estimated_cost_usd']})")
    
    return all_records


async def main(
    num_records: int = config.NUM_RECORDS,
    output_file: str = config.OUTPUT_FILE,
    batch_size: int = config.BATCH_SIZE,
    backup: bool = True,
):
    """
    Main generation pipeline
    
    Args:
        num_records: Number of records to generate
        output_file: Output file path
        batch_size: Batch size for concurrent generation
        backup: Whether to create backup before saving
    """
    
    logger.info("="*60)
    logger.info("Starting Fine-tuning Data Generation")
    logger.info("="*60)
    logger.info(f"Target records: {num_records}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Batch size: {batch_size}")
    logger.info(f"Focus distributions: {config.FOCUS_DISTRIBUTIONS}")
    logger.info("="*60)
    
    # Initialize storage
    storage = DataStorage(output_file)
    
    # Create backup if file exists
    if backup:
        storage.create_backup()
    
    # Get current record count
    existing_count = storage.get_record_count()
    logger.info(f"Existing records: {existing_count}")
    
    # Generate record specifications
    specs = generate_record_specs(num_records, config.FOCUS_DISTRIBUTIONS)
    
    # Generate records in batches
    try:
        generated_records = await generate_batch(specs, batch_size)
    except Exception as e:
        logger.error(f"Generation failed: {e}")
        sys.exit(1)
    
    if not generated_records:
        logger.warning("No records were generated")
        sys.exit(1)
    
    # Validate records
    valid, msg = storage.validate_records(generated_records)
    if not valid:
        logger.error(f"Validation failed: {msg}")
        sys.exit(1)
    
    logger.info(f"Validation passed: {msg}")
    
    # Save records
    num_saved = storage.append_records(generated_records)
    logger.info(f"Successfully saved {num_saved} records")
    
    # Final summary
    total_count = storage.get_record_count()
    logger.info("="*60)
    logger.info("Generation Complete!")
    logger.info(f"Total records in file: {total_count}")
    logger.info(f"Generation time: {datetime.now().isoformat()}")
    logger.info("="*60)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate fine-tuning data for 8B model")
    parser.add_argument(
        "--num-records",
        type=int,
        default=config.NUM_RECORDS,
        help="Number of records to generate",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=config.OUTPUT_FILE,
        help="Output file path",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=config.BATCH_SIZE,
        help="Batch size for concurrent generation",
    )
    parser.add_argument(
        "--no-backup",
        action="store_true",
        help="Don't create backup before saving",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Run async main function
    asyncio.run(main(
        num_records=args.num_records,
        output_file=args.output,
        batch_size=args.batch_size,
        backup=not args.no_backup,
    ))
