"""Basic tests for pycnblogs (requires valid PAT in ~/.cnbrc)."""

import asyncio
import pytest
from pycnblogs import CnblogsClient, AuthenticationError


@pytest.mark.asyncio
async def test_user_info():
    """Test getting user information."""
    async with CnblogsClient() as client:
        user_info = await client.user.get_info()
        assert user_info.display_name
        assert user_info.blog_app
        print(f"User: {user_info.display_name}")


@pytest.mark.asyncio
async def test_list_posts():
    """Test listing posts."""
    async with CnblogsClient() as client:
        posts, total = await client.post.get_list(skip=0, take=5)
        assert isinstance(posts, list)
        assert isinstance(total, int)
        print(f"Found {total} posts")


@pytest.mark.asyncio
async def test_list_ings():
    """Test listing ings."""
    async with CnblogsClient() as client:
        ings = await client.ing.get_list(skip=0, take=5)
        assert isinstance(ings, list)
        print(f"Found {len(ings)} ings")


@pytest.mark.asyncio
async def test_list_news():
    """Test listing news."""
    async with CnblogsClient() as client:
        news_list = await client.news.get_list(skip=0, take=5)
        assert isinstance(news_list, list)
        print(f"Found {len(news_list)} news items")


if __name__ == "__main__":
    # Run tests manually
    print("Running basic tests...\n")
    
    async def run_all():
        await test_user_info()
        await test_list_posts()
        await test_list_ings()
        await test_list_news()
        print("\n✓ All tests passed!")
    
    asyncio.run(run_all())
