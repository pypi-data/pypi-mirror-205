<div align="center">
  <h1>anydoc</h1>
  <p>
    <em>🔌 Turn your GitHub Markdown documentation into a Q&A bot for Slack (more integrations to come soon!)</em>
  </p>
</div>

---

`anydoc` is a Python package to easily generate a Q&A bot from your GitHub Markdown
documentation. It is built on top of [🤗 HuggingFace Transformers](https://github.com/huggingface/transformers)
for the embedding generation, [FAISS from Meta Research](https://github.com/facebookresearch/faiss) for the indexing
and search, and [🦜⛓️ LangChain](https://github.com/hwchase17/langchain) (what a surprise huh?) for the
question-answering generation using the vector store as context. Additionally, it uses
[Slack Bolt for Python](https://github.com/slackapi/bolt-python) for the Slack integration, and 
[GitHub FileSystem](https://github.com/fsspec/filesystem_spec/blob/master/fsspec/implementations/github.py) for
pulling the Markdown files from GitHub.
