from backend.rag.text_chunker import split_text_into_chunks

sample_text = "Artificial Intelligence is transforming healthcare. " * 100

chunks = split_text_into_chunks(sample_text)

print("CHUNKING TEST SUCCESSFUL!")
print("-------------------------")
print("Total chunks:", len(chunks))

for i, chunk in enumerate(chunks, start=1):
    print(f"Chunk {i} length:", len(chunk))