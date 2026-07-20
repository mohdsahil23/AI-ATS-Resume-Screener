import PyPDF2

# Resume PDF Path
file_path = "resumes/resume.pdf"

# Open PDF
with open(file_path, "rb") as file:
    reader = PyPDF2.PdfReader(file)

    print("Total Pages:", len(reader.pages))
    print("=" * 50)

    # Read every page
    for i, page in enumerate(reader.pages):
        text = page.extract_text()

        print(f"\nPage {i+1}\n")

        if text:
            print(text)
        else:
            print("❌ No text found. This PDF may be scanned.")
            print("❌ No text found. This PDF may be scanned.")