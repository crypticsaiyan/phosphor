#!/usr/bin/env python3
"""
Demo: Container Status Refresh Fix

This script demonstrates the difference between cached and refreshed status.
"""

import asyncio
import time
from dotenv import load_dotenv
from src.azure_container_manager import AzureContainerManager
import os


async def demo_status_refresh():
    """Demonstrate the status refresh fix"""
    
    print("=" * 70)
    print("Container Status Refresh Demo")
    print("=" * 70)
    print()
    
    # Check Azure configuration
    load_dotenv()
    required_vars = [
        'AZURE_SUBSCRIPTION_ID',
        'AZURE_CLIENT_ID', 
        'AZURE_CLIENT_SECRET',
        'AZURE_TENANT_ID',
        'AZURE_RESOURCE_GROUP'
    ]
    
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print("❌ Azure not configured. Missing variables:")
        for var in missing:
            print(f"   - {var}")
        print()
        print("Please configure .env with Azure credentials.")
        return
    
    # Initialize Azure manager
    print("Initializing Azure Container Manager...")
    manager = AzureContainerManager(
        subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
        client_id=os.getenv('AZURE_CLIENT_ID'),
        client_secret=os.getenv('AZURE_CLIENT_SECRET'),
        tenant_id=os.getenv('AZURE_TENANT_ID'),
        resource_group=os.getenv('AZURE_RESOURCE_GROUP')
    )
    print()
    
    # Demo 1: Show cached behavior
    print("Demo 1: Cached Status (OLD BEHAVIOR)")
    print("-" * 70)
    print("Fetching containers (first call - no cache)...")
    containers1 = manager.get_all_containers()
    print(f"Found {len(containers1)} containers")
    for c in containers1:
        print(f"  • {c['name']}: {c['status']}")
    print()
    
    print("Fetching again immediately (uses cache)...")
    containers2 = manager.get_all_containers()
    print(f"Found {len(containers2)} containers (from cache)")
    print()
    
    print("⚠️  Problem: If a container was stopped between calls,")
    print("   the cached version would still show it as running!")
    print()
    
    # Demo 2: Show refresh behavior
    print("Demo 2: Forced Refresh (NEW BEHAVIOR)")
    print("-" * 70)
    print("Fetching with force_refresh=True...")
    containers3 = manager.get_all_containers(force_refresh=True)
    print(f"Found {len(containers3)} containers (fresh from Azure API)")
    for c in containers3:
        print(f"  • {c['name']}: {c['status']}")
    print()
    
    print("✅ Solution: Status queries now use force_refresh=True")
    print("   This ensures real-time accuracy for critical operations")
    print()
    
    # Demo 3: Show the fix in action
    print("Demo 3: Status Query (FIXED)")
    print("-" * 70)
    answer = manager.answer_question("show status")
    print(answer)
    print()
    
    print("=" * 70)
    print("Demo Complete!")
    print()
    print("Key Takeaways:")
    print("  1. Cache improves performance for non-critical queries")
    print("  2. Status queries bypass cache for accuracy")
    print("  3. Health checks also use fresh data")
    print("  4. Other queries (IPs, ports) can still use cache")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(demo_status_refresh())
