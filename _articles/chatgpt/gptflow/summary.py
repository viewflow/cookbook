import re
import openai
from typing import List, TypedDict, Tuple
from urllib.request import urlopen, Request

SUMMARY_TASK_TEMPLATE = """
1. Analyze the text provided below.
2. Exclude any advertising information from your analysis.
3. Identify a minimum of {min_chapter}-{max_chapter} key sections and provide a detailed and comprehensive analysis of each section, including examples and explanations.
4. Pay special attention to new terms and concepts in the text. If any are encountered, provide a detailed description of them.
5. For each section:
   - Provide the title of the section.
   - Briefly describe the contents of the section, favoring specific parables, stories, examples, tips, instructions, and directions.
   - Highlight {min_quote}-{max_quote} of the most significant quotes that reflect the essence of the discussion in this section.
   - Important: Do not use examples from this PROMPT in your response.

Example response format:

Section: [Section Title]
Description: [Brief description of the section's content with specific examples and tips]
Quotes:
- "[Quote 1]"
- "[Quote 2]"
- "[Quote 3]"
""".strip()


ARTICLE_TASK_TEMPLATE = (
    """
Below is the content of my lecture. Your task is to transform it into a
comprehensive article. Draw from the main themes provided and delve into a
detailed exploration of the subject. Target readers who may be unfamiliar with
the topic, yet are keen to obtain a comprehensive and engaging overview of the
essential details. Your article should consist of at least {chapters_count}
distinct sections.

Make sure to weave the provided quotes extensively into the narrative. Conclude
the article with a succinct summary addressing the key points and arguments
presented. Use clear and concise sentences. The tone and style of the article
should align with the provided quotes. Extensively embed provided quotes as
direct speech. When embedding citations into the article's content, do so
fluidly without the use of quotation marks. Craft the article as if I'm
narrating it directly to the reader. use first-person voice, but do not say "I"
or "My". Do not style as retelling, but as direct narration. Omit any references
to the author's method of conveying information or personal annotations on the
content delivery.

Title: {title}
""".replace(
        "\n", " "
    )
    .replace("  ", "\n\n")
    .strip()
)


class Subtitle(TypedDict):
    start: str
    end: str
    text: str


class Section(TypedDict):
    title: str
    content: str


def load_youtube_data(url: str) -> Tuple[str, List[str]]:
    """
    Fetches and processes YouTube video data given a video URL.

    Args:
        url (str): The YouTube video URL to scrape data from.

    Returns:
        Tuple[str, List[str]]:
            - str: The title of the YouTube video.
            - List[str]: A list of timestamps and their corresponding titles.

    Example:
        >>> load_youtube_data('https://www.youtube.com/watch?v=example')
        ('Video Title', ['00:01 Intro', '01:30 Main Content', '05:00 Outro'])

    """
    request = Request(url)
    with urlopen(request) as response:
        html_content = response.read().decode("utf-8")

    # title
    match = re.search(r"<title>(.*?)<\/title>", html_content, re.IGNORECASE)
    title = match.group(1)[:-10]

    # timestamps
    pattern = r'{"macroMarkersListItemRenderer":{"title":{"simpleText":"(.*?)"},"timeDescription":{"simpleText":"(.*?)"}'
    matches = re.findall(pattern, html_content)
    timestamps = [f"{time} {title}" for title, time in matches]
    timestamps = timestamps[: int(len(timestamps) / 2)]
    return title, timestamps


def parse_srt(filename: str) -> List[Subtitle]:
    """
    Parses an SRT (SubRip Text) file and extracts subtitle information.

    Args:
        filename (str): The path to the SRT file.

    Returns:
        List[Subtitle]: A list of TypedDicts containing subtitle information.
            Each TypedDict has keys 'start', 'end', and 'text' corresponding to
            the start time, end time, and text content of each subtitle.

    Example:
        >>> parse_srt("example.srt")
        [
            {'start': '00:00:01,234', 'end': '00:00:03,345', 'text': 'This is a text.'},
            {'start': '00:01:00,567', 'end': '00:01:03,789', 'text': 'Another text.'}
        ]
    """
    with open(filename, "r", encoding="utf-8") as f:
        srt_content = f.read()

    pattern = re.compile(
        r"(?P<id>\d+)\n(?P<start>\d{2}:\d{2}:\d{2},\d{3}) --> (?P<end>\d{2}:\d{2}:\d{2},\d{3})\n(?P<text>.+?)(?=\n\n|\Z)",
        re.DOTALL,
    )
    return [
        {
            "start": m.group("start"),
            "end": m.group("end"),
            "text": m.group("text").strip(),
        }
        for m in pattern.finditer(srt_content)
    ]


def srt_to_timestamp(timestamp: str) -> float:
    """
    Converts an SRT timestamp to its equivalent duration in seconds.

    Args:
        timestamp (str): The SRT timestamp, which can be in HH:MM:SS,xxx or MM:SS,xxx format.
                         xxx represents milliseconds.

    Returns:
        float: The duration in seconds as a float

    Example:
        >>> srt_to_timestamp('01:10:00,500')
        4200.5
        >>> srt_to_timestamp('10:00,500')
        600.5
    """
    parts = list(map(float, re.split("[:]", timestamp.replace(",", "."))))

    if len(parts) == 3:  # HH:MM:SS
        h, m, s = parts
        return h * 3600 + m * 60 + s
    elif len(parts) == 2:  # MM:SS
        m, s = parts
        return m * 60 + s
    else:
        return -1


def split_into_sections(
    subtitles: List[Subtitle], sections: List[str]
) -> List[Section]:
    """
    Splits subtitles into sections based on provided timestamps and section titles.

    Args:
        subtitles (List[Subtitle]): A list of subtitles where each subtitle is a dictionary with keys 'start' and 'text'.
        sections (List[str]): A list of strings where each string starts with a timestamp and is followed by the section title.

    Returns:
        List[Section]: A list of dictionaries. Each dictionary represents a section and contains the 'title' and 'content'.

    Example:
        >>> split_into_sections([{'start': '00:00:01,000', 'text': 'Hello'}], ['00:00:00 Intro'])
        [{'title': 'Intro', 'content': 'Hello'}]
    """
    result = []
    idx = 0
    for i, section in enumerate(sections):
        _, title = section.split(" ", 1)

        # To hold the next section's timestamp or set to a high value if it's the last section
        next_timestamp = (
            srt_to_timestamp(sections[i + 1].split(" ", 1)[0])
            if i + 1 < len(sections)
            else float("inf")
        )

        content = []
        while (
            idx < len(subtitles)
            and srt_to_timestamp(subtitles[idx]["start"]) < next_timestamp
        ):
            content.append(subtitles[idx]["text"])
            idx += 1

        result.append({"title": title, "content": " ".join(content)})
    return result


def get_section_summary(
    task: str,
    section: Section,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0,
    n: int = 1,
) -> List[str]:
    """

    Generates a summary of a given section using OpenAI's GPT-3.5 model.

    Args:
        task (str): The task that the system should accomplish (e.g., "Summarize the following text").
        section (Section): A TypedDict containing 'title' and 'content' of the section to be summarized.
        model (str, optional): The OpenAI GPT model to use for text completion. Defaults to "gpt-3.5-turbo-16k".
        temperature (float, optional): Sampling temperature to control randomness in the output. Defaults to 0.
        n (int, optional): Number of completions to generate. Defaults to 1.

    Returns:
        List[str]: A list containing the generated summary/summaries.

    Example:
        >>> get_section_summary("Summarize the following text", {"title": "Introduction", "content": "This is an introduction."})
        ["This is an introduction summarized."]
    """
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": task,
            },
            {
                "role": "user",
                "content": f"{section['title'].title()}\n{section['content']}",
            },
        ],
        n=n,
    )
    return [result.message.content for result in completion.choices]


def create_article(
    task: str,
    summary: str,
    model: str = "gpt-3.5-turbo-16k",
    temperature: float = 0.75,
    n: int = 1,
) -> str:
    completion = openai.ChatCompletion.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": task,
            },
            {
                "role": "user",
                "content": summary,
            },
        ],
        n=n,
    )
    return [result.message.content for result in completion.choices][0]
