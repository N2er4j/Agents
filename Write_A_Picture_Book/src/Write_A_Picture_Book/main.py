#!/usr/bin/env python
import asyncio
import json
import os

from typing import List
from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel
from crewai_tools import SerperDevTool
from openai import OpenAI

'''
from Write_A_Picture_Book.crews.write_book_chapter_crew.write_book_chapter_crew import (
    WriteBookChapterCrew,
)
'''

from Write_A_Picture_Book.types import Chapter, ChapterOutline

from .crews.outline_book_crew.outline_crew import OutlineCrew
from langtrace_python_sdk import langtrace

langtrace.init(api_key = 'a2887f4825fa6962040dc026ba0db00c20aaa534eccca49698bf73b941c78aa3')
client = OpenAI()

class BookState(BaseModel):
    #title: str = "The Algorithmic Classroom: How AI is Reshaping Education"
    title: str = "The Amazing Adventures of Barnaby the Bear"
    book: list = [] 
    book_outline: list[ChapterOutline] = []
    topic: str = (
        "Friendship between animals from different backgrounds. "
        "Learning about different habitats and animal behaviors. "
        "The importance of teamwork and helping others."
    )
    goal: str = (
        "To introduce 2nd graders to the wonders of the animal kingdom. "
        "To spark their curiosity about different species and their environments. "
        "To teach valuable life lessons like friendship, cooperation, and helping those in need."
    )
    '''
    title: str = "Education 2_0: The AI-Powered Future of Learning"
    book: List[Chapter] = []
    book_outline: List[ChapterOutline] = []
    topic: str = (
        "Examines the future of education in the age of AI, exploring emerging trends such as virtual and augmented reality in education, AI-driven curriculum development, and the role of AI in fostering creativity and critical thinking."
    )
    goal: str = "To paint a vision of the future of education and inspire educators, policymakers, and technologists to embrace the potential of AI to create a more equitable and effective learning ecosystem."
    '''

    '''
    topic: str = (
        "Explores the transformative impact of AI on various aspects of education, including personalized learning, automated grading, intelligent tutoring systems, adaptive assessments, and accessibility for diverse learners"
    )
    goal: str = "To provide a comprehensive overview of the current state of AI in education and its potential to revolutionize teaching and learning."
    '''

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

        def generate_dalle_image(prompt):
            """
            Generates an image using the DALL-E 2 API.

            Args:
            prompt: The text description of the image to generate.

            Returns:
            The URL of the generated image.
            """
            try:
                response = client.images.generate(prompt=prompt)
                image_url = response.data[0].url
                return image_url
            except Exception as e:
                print(f"Error generating image: {e}")
                return None
  
        async def write_single_chapter(chapter_outline):
            
            prompt =f"{chapter_outline.title}: {chapter_outline.description}"
            print(f"Generating image for prompt: {prompt}")
            image_url = generate_dalle_image(prompt)
            image_description = f"Image for {chapter_outline.title}"

            print("##############################################################################")
            print(f"Image URL: {image_url}")

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
                        "image_url": image_url,
                        "image_description": image_description,

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
