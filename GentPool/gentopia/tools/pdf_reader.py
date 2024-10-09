from typing import AnyStr
import PyPDF2  # type: ignore
from gentopia.tools.basetool import *
import requests
import os

class PdfReaderArgs(BaseModel):
    query: str = Field(..., description="A pdf url to download and read its contents. You must make sure that the url is real and correct.")

class PdfReader(BaseTool):
    """Tool that adds the capability to download a pdf and read its contents."""
    name = "pdf_reader"
    description = ("A pdf reader tool that can read pages in a pdf. "
                  "Input should be a pdf url.")

    args_schema: Optional[Type[BaseModel]] = PdfReaderArgs

    def _run(self, query: AnyStr) -> str:
        temp_file = 'downloaded.pdf'
        try:
            response = requests.get(query, timeout=10)        
            with open(temp_file, 'wb') as f:
                f.write(response.content)
        except requests.exceptions.RequestException as e:
            return f"Error downloading PDF: {str(e)}"
        text = ""

        try:
            with open(temp_file, "rb") as file_pointer:
                pdf_reader = PyPDF2.PdfReader(file_pointer)
                print("\nNo of pages :\n",len(pdf_reader.pages))
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
            
        except PyPDF2.errors.PdfReadError as e:
            return f"Error reading PDF: {str(e)}"
        
        finally:
            if os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError


if __name__ == "__main__":
    ans = PdfReader()("Attention for transformer")
    print(ans)
