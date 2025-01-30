
import googlesearch

QUERY_FORMAT = "I will give you a question. I want a short google query using only keywords and words from the question: {q}"


def search(query: str, n_results: int = 2) -> list[str]:
    # ignore duplicated links
    return list(set(googlesearch.search(query, num_results=n_results))) # type: ignore

def create_partial_query(query: str) -> str:
    return QUERY_FORMAT.format(q=query)

