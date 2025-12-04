#!/usr/bin/env python3
"""Test different queries to show different outputs."""

import asyncio
from src.core.devops_health_bot import DevOpsHealthBot


async def main():
    print("🧪 Testing Different Queries")
    print("=" * 60)
    print()
    
    bot = DevOpsHealthBot()
    
    # Test 1: All containers
    print("📋 Test 1: /ai (all containers)")
    print("-" * 60)
    result = await bot.check_health("")
    print(result)
    print("\n" + "=" * 60 + "\n")
    
    # Test 2: Filter by existing container name
    print("📋 Test 2: /ai goofy (filter by name)")
    print("-" * 60)
    result = await bot.check_health("goofy")
    print(result)
    print("\n" + "=" * 60 + "\n")
    
    # Test 3: Filter by non-existent
    print("📋 Test 3: /ai prod (probably no matches)")
    print("-" * 60)
    result = await bot.check_health("prod")
    print(result)
    print("\n" + "=" * 60 + "\n")
    
    # Test 4: Another non-existent filter
    print("📋 Test 4: /ai staging (probably no matches)")
    print("-" * 60)
    result = await bot.check_health("staging")
    print(result)
    print("\n" + "=" * 60 + "\n")
    
    # Test 5: Web filter
    print("📋 Test 5: /ai web (filter by 'web')")
    print("-" * 60)
    result = await bot.check_health("web")
    print(result)
    print("\n" + "=" * 60 + "\n")
    
    print("✅ Tests complete!")
    print()
    print("💡 Notice:")
    print("- Different queries give different results")
    print("- Filters that don't match show 'No containers matched'")
    print("- Filters that match show only matching containers")
    print()
    print("To see different results:")
    print("1. Start containers with specific names:")
    print("   docker run -d --name prod-web-1 nginx")
    print("2. Then run: /ai prod")
    print("3. You'll see prod-web-1 in the results!")


if __name__ == "__main__":
    asyncio.run(main())
