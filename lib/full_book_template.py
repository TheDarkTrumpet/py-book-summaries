def get_full_book_template(book_name, book_author, full_book_summary, individual_chapters, terminology = None):
    summary = f"""
# {book_name} Summary

# Author: {book_author}

{full_book_summary}

# Individual Chapters

{individual_chapters}

"""
    if terminology:
        summary += f"""

# Book Terminology
{terminology}
"""
    return summary