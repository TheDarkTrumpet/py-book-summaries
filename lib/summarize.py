import os
import re
from dataclasses import dataclass
import PyPDF2 as pdf
import dotenv
import httpx
import pypandoc
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from .full_book_template import get_full_book_template
from .prompts import full_book_prompt, full_terminology_prompt, chapter_prompt

_env = dotenv.dotenv_values("../../.env")

_llm = ChatOpenAI(
    base_url=_env["OPENAI_API_BASE"],
    api_key=_env["OPENAI_API_KEY"],
    model=_env["SUMMARY_MODEL"],
    temperature=0.2, streaming=False, max_tokens=32768,
    http_client=httpx.Client(
        verify="../../ai.pem",
    )
)


def _clean_text(text: str) -> str:
    # Clean up the think tags
    text = re.sub(r'<think>\s*.*?\s*</think>\s*', '', text, flags=re.DOTALL)
    text = re.sub(r'```markdown\n', r'', text, flags=re.DOTALL)
    text = re.sub(r'\n```', r'', text, flags=re.DOTALL)
    text = re.sub(r'---', r'', text, flags=re.DOTALL)
    # text = re.sub(r'\n\n', r'\n', text, flags=re.DOTALL)

    return text.strip()


def _summarize_chapter(chapter: str, book_name, book_author) -> str:
    prompt = ChatPromptTemplate.from_messages(chapter_prompt)
    chain = prompt | _llm

    summary = chain.invoke({"chapter": chapter, "book_name": book_name, "book_author": book_author}).content.strip()

    return _clean_text(summary)


def _summarize_full_book(book_summary, book_name, book_author) -> str:
    prompt = ChatPromptTemplate.from_messages(full_book_prompt)
    chain = prompt | _llm

    master_summary = chain.invoke(
        {"summaries": book_summary, "book_name": book_name, "book_author": book_author}).content.strip()
    return _clean_text(master_summary)


def _get_book_terminology(book_summary, book_name, book_author) -> str | None:
    prompt = ChatPromptTemplate.from_messages(full_terminology_prompt)
    chain = prompt | _llm

    master_summary = chain.invoke(
        {"summaries": book_summary, "book_name": book_name, "book_author": book_author}).content.strip()
    master_summary = _clean_text(master_summary)
    if len(master_summary) == 0:
        return None
    return master_summary


@dataclass
class Section:
    title: str
    number: int


@dataclass
class Chapter:
    title: str
    number: int
    start: int
    end: int
    section: Section = None

    def __str__(self):
        return f"{self.number} - {self.title}"


@dataclass
class Book:
    book_path: str
    name: str
    author: str
    chapters: list[Chapter]
    destination: str


def generate_book_summary(book: Book, make_pdf: bool = False, make_epub: bool = False) -> None:
    os.makedirs(book.destination, exist_ok=True)

    if not os.path.exists(book.book_path):
        raise RuntimeError(f"Book path {book.book_path} does not exist.")

    # Check if it ends in PDF, else raise
    if not book.book_path.endswith(".pdf"):
        raise RuntimeError(f"Book path {book.book_path} does not end in PDF.")

    pdf_reader = pdf.PdfReader(book.book_path)

    running_chapter_summaries = ''
    encountered_section = None

    for chapter in book.chapters:
        print(f"Processing chapter {chapter}")
        start = chapter.start - 1
        end = chapter.end

        chapter_text = ''
        for page_num in range(start, end):
            page = pdf_reader.pages[page_num]
            chapter_text += page.extract_text()
        summary = _summarize_chapter(chapter_text, book.name, book.author)

        with open(f"{book.destination}/{chapter} - {chapter.title}.md", 'w') as f:
            f.write(summary)

        if chapter.section and chapter.section != encountered_section:
            running_chapter_summaries += f"## Part: {chapter}\n"
            encountered_section = chapter.section

        if chapter.section:
            running_chapter_summaries += f"### Part: {chapter.section.number} Chapter: {chapter}\n\n{summary}\n\n"
        else:
            running_chapter_summaries += f"### Chapter: {chapter.number} - {chapter.title}\n\n{summary}\n\n"

    book_summary = _summarize_full_book(running_chapter_summaries, book.name, book.author)
    terminology = _get_book_terminology(running_chapter_summaries, book.name, book.author)

    full_cliffnotes = get_full_book_template(book.name, book.author, book_summary, running_chapter_summaries, terminology)
    with open(f"{book.destination}/full_book_summary.md", 'w') as f:
        f.write(full_cliffnotes)

    if make_pdf:
        pypandoc.convert_file(f"{book.destination}/full_book_summary.md", "pdf", outputfile=f"{book.destination}/{book.name} Summary.pdf")
    if make_epub:
        pypandoc.convert_file(f"{book.destination}/full_book_summary.md", "epub", outputfile=f"{book.destination}/{book.name} Summary.epub")