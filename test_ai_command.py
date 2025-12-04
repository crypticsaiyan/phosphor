#!/usr/bin/env python3
"""Test the /ai command behavior."""

import asyncio
from src.core.mcp_client import MCPClient


async def test_ai_commands():
    """Test different /ai command variations."""
    print("🧪 Testing /ai Command Behavior")
    print("=" * 60)
    
    mcp = MCPClient()
    
    # Test 1: Basic health check
    print("\n📋 Test 1: /ai (basic health check)")
    print("-" * 60)
    result = await mcp.execute("")
    if "message" in result:
        print(result["message"][:200] + "...")
    else:
        print(result)
    
    # Test 2: With query
    print("\n📋 Test 2: /ai check docker health")
    print("-" * 60)
    result = await mcp.execute("check docker health")
    if "message" in result:
        print(result["message"][:200] + "...")
    else:
        print(result)
    
    # Test 3: Filter by prod
    print("\n📋 Test 3: /ai prod")
    print("-" * 60)
    result = await mcp.execute("prod")
    if "message" in result:
        print(result["message"][:200] + "...")
    else:
        print(result)
    
    # Test 4: Private query (should work the same in MCP)
    print("\n📋 Test 4: /ai private explain health checks")
    print("-" * 60)
    result = await mcp.execute("explain health checks")
    if "message" in result:
        print(result["message"][:200] + "...")
    else:
        print(result)
    
    # Test 5: Help
    print("\n📋 Test 5: /ai help")
    print("-" * 60)
    result = await mcp.execute("help")
    if "message" in result:
        print(result["message"][:200] + "...")
    else:
        print(result)
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print()
    print("💡 In the TUI:")
    print("- /ai <query>         → Sends to IRC channel (if connected)")
    print("- /ai private <query> → Shows only to you (local)")
    print()
    print("If not connected to IRC, results show locally only.")


if __name__ == "__main__":
    asyncio.run(test_ai_commands())
