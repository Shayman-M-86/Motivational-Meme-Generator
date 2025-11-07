
class Quote:
    """A class to represent a quote with its author."""

    def __init__(self, body: str, author: str):
        """Initialize a Quote instance.

        Args:
            body (str): The text of the quote.
            author (str): The author of the quote.
        """
        self.body = body
        self.author = author

    def __str__(self):
        """Return a string representation of the quote."""
        return f'"{self.body}" - {self.author}'
    
    def __repr__(self):
        """Return a formal string representation of the quote."""
        return return f'"{self.body}" - {self.author}'