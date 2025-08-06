# Project: Markdown to DOCX Conversion

This document outlines the tasks required to create a script that automatically converts a Markdown file into a DOCX document, handling embedded Mermaid diagrams and Excalidraw scene files.

## I. Project Initialization
- [x] Create `project.md` to track progress.

## II. Planning & Analysis
- [x] **Analyze Existing Files:**
  - [x] Review `transfer2doc.md` for the agreed-upon implementation plan.
  - [x] Examine `spec.md` to understand the structure of the source Markdown file.
  - [x] Inspect `scenarios/scene_1.excalidraw` to understand the data format.
  - [x] Analyze `render_excalidraw.js` to determine how to execute it for image conversion.
  - [x] Check `package.json` for Node.js dependencies.
- [x] **Finalize Implementation Strategy:**
  - [x] Define the main script language and key libraries (Python seems appropriate).
  - [x] Detail the process for handling Excalidraw files.
  - [x] Detail the process for handling Mermaid diagrams.
  - [x] Select a tool for the final Markdown-to-DOCX conversion (e.g., Pandoc).

## III. Implementation
- [x] **Set up Environment:**
  - [x] Install necessary Node.js packages using `npm install`.
- [x] **Develop the Conversion Script (Python):**
  - [x] **File Parsing:**
    - [x] Read the input Markdown file (`spec.md`).
    - [x] Create a temporary directory for generated images.
  - [x] **Excalidraw Processing:**
    - [x] Find all Markdown image links pointing to `.excalidraw` files.
    - [x] For each file, call `render_excalidraw.js` to generate a PNG image.
    - [x] Replace the `.excalidraw` path in the Markdown content with the path to the generated PNG.
  - [x] **Mermaid Processing:**
    - [x] Find all `mermaid` code blocks.
    - [x] For each block, save the content to a temporary `.mmd` file.
    - [x] Use a command-line tool (like `mmdc`) to convert the `.mmd` file to a PNG image.
    - [x] Replace the Mermaid code block with a Markdown image link to the generated PNG.
  - [x] **Final Document Generation:**
    - [x] Write the modified Markdown content to a temporary file.
    - [x] Use Pandoc to convert the temporary Markdown file to a `.docx` document.
    - [x] Clean up temporary files.

## IV. Testing
- [ ] **Execute the script:**
  - [ ] Run the script with `spec.md` as input.
- [ ] **Verify the output:**
  - [ ] Check the generated `.docx` file to ensure Excalidraw SVGs are embedded correctly.
  - [ ] Verify that Mermaid diagrams are rendered as SVGs and correctly embedded in the final document.
  - [ ] Ensure all other Markdown content is preserved.

**NOTE:** The script execution failed because the `pandoc` command was not found. Pandoc is a required dependency that must be in the system's PATH.

## V. Refinements and Bug Fixes
- [x] **Excalidraw Improvements:**
  - [x] Modify the rendering process to generate SVG (vector graphics) instead of PNG.
  - [x] Adjust the export to ensure the drawing is centered within the SVG canvas.
- [x] **Mermaid Integration (New Approach):**
  - [x] **Abandon `pandoc-mermaid` filter:** The library is outdated and not suitable.
  - [x] **Implement `mermaid-cli` rendering:**
    - [x] Find all `mermaid` code blocks in the Markdown file.
    - [x] For each block, save its content to a temporary `.mmd` file.
    - [x] Use `mmdc` (from `mermaid-cli`) to convert the `.mmd` file to an **SVG** image.
    - [x] In the Markdown content, replace the `mermaid` code block with a standard image link to the generated SVG file.
  - [x] **Update Pandoc command:** Ensure the command can correctly embed SVG images during the final DOCX conversion.