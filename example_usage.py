"""
Example usage of the modular search engine.
This demonstrates the basic functionality and different search types.
"""

import time
from src.core.search_engine import SearchEngine
from src.utils.config import SearchConfig
from api import SearchEngineAPI


def example_basic_usage():
    """Example of basic search engine usage."""
    print("=== Basic Search Engine Usage ===")
    
    # Create configuration
    config = SearchConfig(data_path="./data")
    
    # Initialize search engine
    search_engine = SearchEngine(config)
    
    # Test query
    query = "how to learn AI"
    
    # Perform clustering search (default)
    print(f"Searching for: '{query}'")
    start_time = time.time()
    results = search_engine.search(query, top_n=5)
    end_time = time.time()
    
    print(f"Found {len(results)} results in {end_time - start_time:.3f} seconds")
    print("\nTop results:")
    for i, (_, row) in enumerate(results.iterrows(), 1):
        title = row['Title'][:100] + "..." if len(str(row['Title'])) > 100 else str(row['Title'])
        print(f"{i}. {title}")
    
    print("\n" + "="*50 + "\n")


def example_api_usage():
    """Example of using the API interface."""
    print("=== API Interface Usage ===")
    
    # Initialize API
    api = SearchEngineAPI()
    
    # Health check
    health = api.health_check()
    print(f"Health Status: {health['status']}")
    if 'message' in health:
        print(f"Message: {health['message']}")
    
    # Get stats
    stats = api.get_stats()
    if stats['success']:
        print(f"Total Posts: {stats['engine_stats']['total_posts']}")
        print(f"Total Topics: {stats['engine_stats']['total_topics']}")
        print(f"CUDA Available: {stats['engine_stats']['cuda_available']}")
    
    # Test different search types
    query = "python programming"
    print(f"\nTesting different search types for: '{query}'")
    
    search_types = ["clustering", "semantic", "vector"]
    
    for search_type in search_types:
        print(f"\n--- {search_type.upper()} Search ---")
        result = api.search(query, top_n=3, search_type=search_type)
        
        if result['success']:
            print(f"Found {result['total_results']} results in {result['execution_time']:.3f}s")
            for i, post in enumerate(result['results'][:2], 1):
                title = post['title'][:80] + "..." if len(post['title']) > 80 else post['title']
                print(f"  {i}. {title}")
        else:
            print(f"Error: {result['error']}")
    
    print("\n" + "="*50 + "\n")


def example_post_retrieval():
    """Example of retrieving specific posts."""
    print("=== Post Retrieval Example ===")
    
    api = SearchEngineAPI()
    
    # First, let's search for some posts to get their IDs
    query = "machine learning"
    result = api.search(query, top_n=3, search_type="clustering")
    
    if result['success'] and result['results']:
        # Get the first result's ID
        post_id = result['results'][0]['id']
        print(f"Retrieving post with ID: {post_id}")
        
        # Retrieve the specific post
        post_result = api.get_post(post_id)
        
        if post_result['success']:
            post = post_result['post']
            print(f"Title: {post['title']}")
            print(f"Body preview: {post['body'][:200]}...")
            print(f"Score: {post['score']}")
            print(f"Creation Date: {post['creation_date']}")
        else:
            print(f"Error retrieving post: {post_result['error']}")
    
    print("\n" + "="*50 + "\n")


def example_configuration():
    """Example of custom configuration."""
    print("=== Custom Configuration Example ===")
    
    # Create custom configuration
    custom_config = SearchConfig(
        data_path="./data",
        coeff1=0.4,  # Increase semantic answer weight
        coeff2=0.1,  # Decrease vector similarity weight
        coeff3=0.5,  # Keep title similarity weight
        batch_size=512,  # Smaller batch size for memory efficiency
        default_top_n=10
    )
    
    # Initialize search engine with custom config
    search_engine = SearchEngine(custom_config)
    
    # Test search
    query = "deep learning"
    results = search_engine.search(query, top_n=3)
    
    print(f"Search with custom config: '{query}'")
    print(f"Found {len(results)} results")
    
    # Show configuration
    print(f"\nConfiguration used:")
    print(f"  Semantic weight (coeff1): {custom_config.coeff1}")
    print(f"  Vector weight (coeff2): {custom_config.coeff2}")
    print(f"  Title weight (coeff3): {custom_config.coeff3}")
    print(f"  Batch size: {custom_config.batch_size}")
    
    print("\n" + "="*50 + "\n")


def main():
    """Run all examples."""
    print("Modular Search Engine Examples")
    print("=" * 50)
    
    try:
        # Run examples
        example_basic_usage()
        example_api_usage()
        example_post_retrieval()
        example_configuration()
        
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"Error running examples: {e}")
        print("\nMake sure you have:")
        print("1. Installed all dependencies: pip install -r requirements.txt")
        print("2. Prepared your data files in the data/ directory")
        print("3. Generated embeddings and models")


if __name__ == "__main__":
    main() 