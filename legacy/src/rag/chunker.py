'''
range(start=0, stop=len(lines), step=chunk_size - overlap)

It starts at 0, and increments by chunk_size - overlap (i.e. 300 - 50 = 250 by default).

So, the chunks slide forward by 250 lines, and each chunk contains 300 lines, meaning the

last 50 lines of one chunk overlap with the first 50 lines of the next.
'''

def chunk(text,chunk_size=300,overlap=50):
    lines=text.splitlines()
    chunks=[]

    for i in range(0,len(lines),chunk_size-overlap):
        chunk = "\n".join(lines[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

