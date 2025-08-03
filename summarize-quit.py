from lib.summarize import Book, Chapter, Section, generate_book_summary

sections = [
    Section(number=1, title="The Case for Quitting"),
    Section(number=2, title="In the Losses"),
    Section(number=3, title="Identity and Other Impediments"),
    Section(number=4, title="Opportunity Cost")
]

chapters = [
    Chapter(title="The Opposite of a Great Virtue Is Also a Great Virtue",
            number=1,
            section=sections[0],
            start=20,
            end=35),
    Chapter(title="Quitting On Time Usually Feels like Quitting Too Early",
            section=sections[0],
            number=2,
            start=36,
            end=55),
    Chapter(title="Should I Stay, or Should I Go?",
            section=sections[0],
            number=3,
            start=56,
            end=72),
    Chapter(title="Escalating Commitment",
            section=sections[1],
            number=4,
            start=74,
            end=83),
    Chapter(title="Sunk Costs and the Fear of Waste",
            section=sections[1],
            number=5,
            start=84,
            end=101),
    Chapter(title="Moneys and Pedestals",
            section=sections[1],
            number=6,
            start=102,
            end=122),
    Chapter(title="You Own What You've Bought and What You've Thought: Endowment and Status Quo Bias",
            section=sections[2],
            number=7,
            start=124,
            end=141),
    Chapter(title="The Hardest Thing to Quit Is Who you Are: Identity and Dissonance",
            section=sections[2],
            number=8,
            start=142,
            end=159),
    Chapter(title="Find Someone Who Loves You but Doesn't Care about Hurt Feelings'",
            section=sections[2],
            number=9,
            start=160,
            end=176),
    Chapter(title="Lessons from Forced Quitting",
            section=sections[3],
            number=10,
            start=178,
            end=196),
    Chapter(title="The Myopia of Goals",
            section=sections[3],
            number=11,
            start=197,
            end=212)
]

book = Book(
    name='Quit',
    author='Annie Duke',
    destination='summaries/quit',
    book_path='/Volumes/8TBNVME/Books - Calibre/Annie Duke/Quit_ The Power of Knowing When to Walk Away (143)/Quit_ The Power of Knowing When to Walk Aw - Annie Duke.pdf',
    chapters=chapters
)

generate_book_summary(book, make_pdf=True)
