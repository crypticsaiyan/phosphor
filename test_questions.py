#!/usr/bin/env python3
"""Test question handling in MCP client."""

import asyncio
from src.core.mcp_client import MCPClient


async def test_questions():
    """Test different types of questions."""
    print("🧪 Testing Question Handling")
    print("=" * 60)
    
    mcp = MCPClient()
    
    test_cases = [
        ("explain what healthy means", "Health status explanation"),
        ("explain restart counts", "Restart explanation"),
        ("show me logs", "Logs explanation"),
        ("what is docker", "Docker basics"),
        ("how do I check containers", "General question"),
        ("random query", "Ambiguous query"),
        ("check docker health", "Health check"),
        ("prod", "Environment filter"),
    ]
    
    for query, description in test_cases:
        print(f"\n📋 Test: {description}")
        print(f"Query: {query}")
        print("-" * 60)
        
        result = await mcp.execute(query)
        
        if "message" in result:
            # Show first 150 chars
            message = result["message"]
            preview = message[:150] + "..." if len(message) > 150 else message
            print(preview)
        elif "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Result: {result}")
        
        print()
    
    print("=" * 60)
    print("✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_questions())
