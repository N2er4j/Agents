#!/usr/bin/env python
import asyncio

from typing import List

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel


from write_a_book_with_flows.crews.write_book_chapter_crew.write_book_chapter_crew import (
    WriteBookChapterCrew,
)
from write_a_book_with_flows.types import Chapter, ChapterOutline

from .crews.outline_book_crew.outline_crew import OutlineCrew
from langtrace_python_sdk import langtrace

langtrace.init(api_key = 'a2887f4825fa6962040dc026ba0db00c20aaa534eccca49698bf73b941c78aa3')

class BookState(BaseModel):
    title: str = "The Algorithmic Classroom: How AI is Reshaping Education"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = (
        "Explores the transformative impact of AI on various aspects of education, including personalized learning, automated grading, intelligent tutoring systems, adaptive assessments, and accessibility for diverse learners"
    )
    goal: str = "To provide a comprehensive overview of the current state of AI in education and its potential to revolutionize teaching and learning."


class BookFlow(Flow[BookState]):
    initial_state = BookState

    @start()
    def generate_book_outline(self):
        print("Kickoff the Book Outline Crew")
        output = (
            OutlineCrew()
            .crew()
            .kickoff(inputs={"topic": self.state.topic, "goal": self.state.goal})
        )

        chapters = output["chapters"]
        print("Chapters:", chapters)

        self.state.book_outline = chapters
        return chapters

    @listen(generate_book_outline)
    async def write_chapters(self):
        print("Writing Book Chapters")
        tasks = []

        async def write_single_chapter(chapter_outline):
            output = (
                WriteBookChapterCrew()
                .crew()
                .kickoff(
                    inputs={
                        "goal": self.state.goal,
                        "topic": self.state.topic,
                        "chapter_title": chapter_outline.title,
                        "chapter_description": chapter_outline.description,
                        "book_outline": [
                            chapter_outline.model_dump_json()
                            for chapter_outline in self.state.book_outline
                        ],
                    }
                )
            )
            title = output["title"]
            content = output["content"]
            chapter = Chapter(title=title, content=content)
            return chapter

        for chapter_outline in self.state.book_outline:
            print(f"Writing Chapter: {chapter_outline.title}")
            print(f"Description: {chapter_outline.description}")
            # Schedule each chapter writing task
            task = asyncio.create_task(write_single_chapter(chapter_outline))
            tasks.append(task)

        # Await all chapter writing tasks concurrently
        chapters = await asyncio.gather(*tasks)
        print("Newly generated chapters:", chapters)
        self.state.book.extend(chapters)

        print("Book Chapters", self.state.book)

    @listen(write_chapters)
    async def join_and_save_chapter(self):
        print("Joining and Saving Book Chapters")
        # Combine all chapters into a single markdown string
        book_content = ""

        for chapter in self.state.book:
            # Add the chapter title as an H1 heading
            book_content += f"# {chapter.title}\n\n"
            # Add the chapter content
            book_content += f"{chapter.content}\n\n"

        # The title of the book from self.state.title
        book_title = self.state.title

        # Create the filename by replacing spaces with underscores and adding .md extension
        md_filename = f"./{book_title.replace(' ', '_')}.md"
        html_filename = f"./{book_title.replace(' ', '_')}.html"

        # Save the combined content into the file
        with open(md_filename, "w", encoding="utf-8") as file:
            file.write(book_content)

        print(f"Book saved as {md_filename}")
        '''
        def convert_md_to_html(md_file, html_file):
            #Converts a Markdown file to HTML.
            with open(md_file, "r", encoding="utf-8") as f:
                md_text = f.read()
            
            html_text = markdown.markdown(md_text)

            with open(html_file, "w", encoding="utf-8") as f:
                f.write(html_text)

        convert_md_to_html(md_filename, html_filename)
        '''
        return book_content


def kickoff():
    poem_flow = BookFlow()
    poem_flow.kickoff()


def plot():
    poem_flow = BookFlow()
    poem_flow.plot()


if __name__ == "__main__":
    kickoff()
