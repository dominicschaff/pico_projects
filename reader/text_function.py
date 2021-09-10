from random import choice

def split(text, width=49, lines=27):
    raw_lines = text.split('\n')
    output_lines = []
    for line in raw_lines:
        l2 = chunks(line, width)
        for l in l2:
            output_lines.append(l)
    
    
    return chunks(output_lines, lines)
    
def chunks(chunk_list, size=10):
    """
    Given a list like object break it up into chunks.

    Args:
        chunk_list: a list like object
        size: the size of the chunks

    Returns:
        A new list of lists, with the sub list being at most `size` long
    """
    return [chunk_list[i * size:(i + 1) * size] for i in range((len(chunk_list) + size - 1) // size )]

def random_hex(length=49, lines=1):
    a = "0123456789ABCDEF"
    return ["".join(choice(a) for x in range(length)) for y in range(lines)]
