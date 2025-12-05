#!/usr/bin/env python3
"""
Test script to verify container status is refreshed correctly
"""

import asyncio
import os
from dotenv import load_dotenv
from src.core.mcp_client import MCPClient


async def test_status_command():
    """Test the /ai show status command"""
    print("=" * 60)
    print("Testing /ai show status command")
    print("=" * 60)
    print()
    
    # Initialize MCP client
    client = MCPClient()
    
    # Check if Azure is configured
    if not client.azure_client.is_available():
        print("❌ Azure not configured. This test requires Azure setup.")
        print("   Please configure .env with Azure credentials.")
        return
    
    print("✅ Azure is configured")
    print()
    
    # Test 1: Show status
    print("Test 1: Running '/ai show status'")
    print("-" * 60)
    result = await client.execute("show status")
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
    else:
        print(result.get("message", result))
    
    print()
    print("=" * 60)
    print("Test complete!")
    print()
    print("To verify the fix:")
    print("1. Note the current status of containers above")
    print("2. Stop one or more containers in Azure Portal")
    print("3. Wait a few seconds")
    print("4. Run this test again")
    print("5. The status should reflect the stopped containers")
    print()
    print("Before the fix: Status would show cached data (all running)")
    print("After the fix: Status is refreshed and shows actual state")
    print("=" * 60)


if __name__ == "__main__":
    load_dotenv()
    asyncio.run(test_status_command())
