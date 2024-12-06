import os

import pytest

from language_model_gateway.gateway.tools.scraping_bee_web_scraper_tool import (
    ScrapingBeeWebScraperTool,
)


@pytest.mark.skipif(
    os.getenv("RUN_TESTS_WITH_REAL_LLM") != "1",
    reason="Requires ScrapingBee API key",
)
async def test_scraping_bee_tool_tool_async() -> None:
    print("")
    tool = ScrapingBeeWebScraperTool(api_key=os.environ["SCRAPING_BEE_API_KEY"])
    result = await tool._arun(url="https://www.example.com")
    print(result)
    assert "This domain is for use in illustrative examples in documents." in result


@pytest.mark.skipif(
    os.getenv("RUN_TESTS_WITH_REAL_LLM") != "1",
    reason="Requires ScrapingBee API key",
)
async def test_scraping_bee_tool_tool_complex_async() -> None:
    print("")
    tool = ScrapingBeeWebScraperTool(
        api_key=os.environ["SCRAPING_BEE_API_KEY"],
        premium_proxy=True,
        return_markdown=True,
    )
    result = await tool._arun(
        url="https://www.johnmuirhealth.com/doctor/David-Chang-MD/1174545909"
    )
    print(result)
    assert "1812" in result


@pytest.mark.skipif(
    os.getenv("RUN_TESTS_WITH_REAL_LLM") != "1",
    reason="Requires ScrapingBee API key",
)
async def test_scraping_bee_tool_tool_complex_answer_query_async() -> None:
    print("")
    tool = ScrapingBeeWebScraperTool(
        api_key=os.environ["SCRAPING_BEE_API_KEY"],
        premium_proxy=True,
        return_markdown=True,
    )
    result = await tool._arun(
        url="https://www.johnmuirhealth.com/doctor/David-Chang-MD/1174545909",
        query="Address",
    )
    print(result)
    assert "1812" in result


@pytest.mark.skipif(
    os.getenv("RUN_TESTS_WITH_REAL_LLM") != "1",
    reason="Requires ScrapingBee API key",
)
async def test_scraping_bee_tool_tool_printable_async() -> None:
    print("")
    tool = ScrapingBeeWebScraperTool(api_key=os.environ["SCRAPING_BEE_API_KEY"])
    result = await tool._arun(
        url="https://www.johnmuirhealth.com/fad/doctor/profilePrintable/1174545909"
    )
    print(result)
    assert "Chang" in result
