from typing import AnyStr
from gentopia.tools.basetool import *
import requests

class NewsAggregatorArgs(BaseModel):
    query: str = Field(..., description="This tool is to query latest news articles, it can have input parameters such as article category, country etc, if user wishes to specify.")

class NewsAggregator(BaseTool):
    """Tool that adds the capability to query latest news articles and summarize their contents."""
    name = "news_aggregator"
    description = ("A News Aggregator tool that can query and summarize news articles."
                  "Input can be a few parameters or None at all.")

    args_schema: Optional[Type[BaseModel]] = NewsAggregatorArgs

    def _run(self, query: AnyStr) -> str:
        apiEndpoint = 'https://newsapi.org/v2/top-headlines?'
        headers = {'X-Api-Key':'4efd81054ee1481b99092811ddcb6e87'}
        params = {'country':'us', 
                    'category': 'technology'
                    }
        response = requests.get(apiEndpoint, headers=headers, params=params)
        responseJson = response.json()
        articlesAll = responseJson['articles']
        formatted_output = []
        for item in articlesAll:
            title = item.get('title', 'No Title')
            author = item.get('author', 'Unknown Author')
            url = item.get('url', 'No URL')
            description = item.get('description', 'No Description')
            formatted_item = f"**Title**: {title}\n**Author**: {author}\n**Description**: {description}\n**URL**: {url}\n"
            formatted_output.append(formatted_item)
        return '\n\n'.join(formatted_output)

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = NewsAggregator()("Attention for transformer")
    print(ans)
