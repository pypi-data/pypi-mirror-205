# Scribber

---

A simple document generator with not very rich functionality that can export a document to some formats such 
as text, docx, xlsx and markdown.

## Installation
```shell
pip install scribber
```

## Usage

```python
from scribber import (
    SimpleDocument,
    Title,
    EmptyLine,
    Paragraph,
    Table,
    Director,
    CodeBlock,
    DocumentBuilder,
    ExcelDocument,
    MarkdownDocument,
    TextDocument,
    WordDocument
)

CODE_EXAMPLE = """
import platform

def main():
    print("Hello World!")
    print(f"OS: {platform.system()}")
    
if __name__ == "__main__":
    main()             
"""

CODE_RESULT = """Hello World!
OS: Linux"""


if __name__ == "__main__":
    # Create abstract document
    doc = SimpleDocument()
    doc.add(Title(title="Funny report"))
    doc.add(EmptyLine())
    doc.add(Paragraph(text="Let me show you report"))
    doc.add(
        Table(
            headers=["one", "two", "three", "four"],
            content=[
                (1, 2, 3, 4),
                ("234", 345, 986, ""),
                (89, 35, 587643, 8675),
            ],
        )
    )
    doc.add(EmptyLine())
    doc.add(Title(title="Code block", level=2))
    doc.add(CodeBlock(style="python", code=CODE_EXAMPLE))
    doc.add(CodeBlock(style="console", code=CODE_RESULT))
    doc.add(Paragraph(text="It's Ok!"))

    director = Director()
    text_report_builder = DocumentBuilder(doc=TextDocument())
    word_report_builder = DocumentBuilder(doc=WordDocument())
    excel_report_builder = DocumentBuilder(doc=ExcelDocument())
    marckdown_report_builder = DocumentBuilder(doc=MarkdownDocument())

    print("Make a Text Document")
    director.builder = text_report_builder
    director.build_report_from_doc(doc)
    text_report_builder.parts.save("test.txt")

    print("Make a Word Document")
    director.builder = word_report_builder
    director.build_report_from_doc(doc)
    word_report_builder.parts.save("test.docx")

    print("Make a Excel Document")
    director.builder = excel_report_builder
    director.build_report_from_doc(doc)
    excel_report_builder.parts.save("test.xlsx")

    print("Make a Marckdown Document")
    director.builder = marckdown_report_builder
    director.build_report_from_doc(doc)
    marckdown_report_builder.parts.save("test.md")

    print()
    print("Build without Director")
    text_report_builder.add_title(Title(title="Next report"))
    text_report_builder.add_paragraph(Paragraph(text="That is all!"))
    print(text_report_builder.parts.get_result())

```

The text file example
```text
Funny report
============

Let me show you report
---------------------------
 one | two | three  | four 
---------------------------
  1  |  2  |   3    |  4   
 234 | 345 |  986   |      
 89  | 35  | 587643 | 8675 
---------------------------
Total
=====
It's Ok!
```

## requirements

- lxml>=4.9.1<5.0.0
- pydantic>=1.10.2<2.0.0
- python-docx>=0.8.11<1.0.0
- typing_extensions>=4.4.0<5.0.0
- XlsxWriter>=3.0.3<4.0.0
