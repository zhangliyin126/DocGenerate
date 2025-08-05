import argparse
import os
import re
import subprocess
import sys
import tempfile
import shutil
import uuid

def run_command(command, cwd=None, use_shell=False):
    """Runs a command and checks for errors."""
    try:
        # If using shell, join the command list into a single string
        if use_shell and isinstance(command, list):
            command = ' '.join(command)
            
        result = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8',
            cwd=cwd,
            shell=use_shell  # Set shell=True
        )
        return result
    except subprocess.CalledProcessError as e:
        # For display, join list to string if it's a list
        cmd_str = ' '.join(e.cmd) if isinstance(e.cmd, list) else e.cmd
        print(f"Error executing command: {cmd_str}", file=sys.stderr)
        print(f"Return code: {e.returncode}", file=sys.stderr)
        print(f"Stdout: {e.stdout}", file=sys.stderr)
        print(f"Stderr: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def create_temp_dir_in_project():
    """Create a temporary directory in the project's temp folder."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    temp_dir_path = os.path.join(project_root, 'temp')
    
    # Create temp directory if it doesn't exist
    if not os.path.exists(temp_dir_path):
        os.makedirs(temp_dir_path)
        print(f"Created temp directory: {temp_dir_path}")
    
    # Create a unique temporary subdirectory
    temp_subdir = os.path.join(temp_dir_path, f"temp_{uuid.uuid4().hex[:8]}")
    os.makedirs(temp_subdir)
    return temp_subdir

def cleanup_temp_dir(temp_dir):
    """Clean up the temporary directory."""
    try:
        shutil.rmtree(temp_dir)
        print(f"Cleaned up temporary directory: {temp_dir}")
    except Exception as e:
        print(f"Warning: Could not clean up temporary directory {temp_dir}: {e}")

def main():
    parser = argparse.ArgumentParser(description='Convert Markdown to DOCX, processing Excalidraw and Mermaid diagrams.')
    parser.add_argument('input_file', help='The path to the input Markdown file.')
    parser.add_argument('output_file', help='The path for the output DOCX file.')
    args = parser.parse_args()

    input_file_path = os.path.abspath(args.input_file)
    output_file_path = os.path.abspath(args.output_file)
    project_root = os.path.dirname(os.path.abspath(__file__))

    # Create temporary directory in project's temp folder
    temp_dir = create_temp_dir_in_project()
    print(f"Created temporary directory: {temp_dir}")

    try:
        # Read the original markdown content
        with open(input_file_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()

        # --- The rest of the processing logic will go here ---

        # 1. Process Excalidraw files
        print("Processing Excalidraw diagrams...")
        excalidraw_matches = re.findall(r'!\[(.*?)\]\((.*?\.excalidraw)\)', markdown_content)
        for i, (alt_text, excalidraw_path) in enumerate(excalidraw_matches):
            print(f"  Found Excalidraw: {excalidraw_path}")
            
            # Create absolute path for the source excalidraw file
            abs_excalidraw_path = os.path.abspath(os.path.join(os.path.dirname(input_file_path), excalidraw_path))
            
            # Define the output path for the SVG image in the temp directory
            output_svg_name = f"excalidraw-{i}.svg"
            abs_output_svg_path = os.path.join(temp_dir, output_svg_name)
            
            # Get the relative path for the link in the markdown file
            relative_output_svg_path = output_svg_name

            # Render the excalidraw file to SVG
            render_script_path = os.path.join(project_root, 'render_excalidraw.js')
            print(f"  Rendering to {abs_output_svg_path}...")
            run_command(['node', render_script_path, abs_excalidraw_path, abs_output_svg_path])
            
            # Replace the .excalidraw path with the new .svg path
            original_link = f"![{alt_text}]({excalidraw_path})"
            new_link = f"![{alt_text}]({relative_output_svg_path})"
            markdown_content = markdown_content.replace(original_link, new_link)
            print(f"  Replaced link with: {new_link}")

        # 2. Process Mermaid diagrams
        print("\nProcessing Mermaid diagrams...")
        
        mermaid_counter = 0
        def replace_mermaid_block(match):
            nonlocal mermaid_counter
            mermaid_code = match.group(1).strip()
            print(f"  Found Mermaid diagram {mermaid_counter + 1}")

            # Define paths for temporary mermaid source and output SVG
            temp_mmd_path = os.path.join(temp_dir, f"mermaid-{mermaid_counter}.mmd")
            output_svg_name = f"mermaid-{mermaid_counter}.svg"
            abs_output_svg_path = os.path.join(temp_dir, output_svg_name)
            
            # Write mermaid code to a temporary file
            with open(temp_mmd_path, 'w', encoding='utf-8') as f:
                f.write(mermaid_code)

            # Render the mermaid file to SVG using mmdc
            print(f"  Rendering to {abs_output_svg_path}...")
            mmdc_command = [
                'npx', 'mmdc', '-i', temp_mmd_path, '-o', abs_output_svg_path
            ]
            run_command(mmdc_command, cwd=project_root, use_shell=True)

            # Increment counter for the next diagram
            mermaid_counter += 1

            # Return the new image link
            alt_text = "Mermaid Diagram"
            new_link = f"![{alt_text}]({output_svg_name})"
            print(f"  Replacing block with: {new_link}")
            return new_link

        # Use re.sub with a replacement function to handle all mermaid blocks
        mermaid_pattern = re.compile(r'```mermaid\n(.*?)\n```', re.DOTALL)
        markdown_content = mermaid_pattern.sub(replace_mermaid_block, markdown_content)

        # 3. Write the final processed markdown
        processed_md_path = os.path.join(temp_dir, 'processed.md')
        with open(processed_md_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        # 4. Convert to DOCX using Pandoc
        print("\nConverting to DOCX with Pandoc...")
        pandoc_command = [
            'pandoc',
            processed_md_path,
            '-o',
            output_file_path,
            '--resource-path',
            temp_dir
        ]
        
        run_command(pandoc_command)
        
        print(f"\nSuccessfully created DOCX file at: {output_file_path}")

    finally:
        # Clean up the temporary directory
        print("hold on clearning.")
        # cleanup_temp_dir(temp_dir)

    print("Processing complete.")


if __name__ == '__main__':
    main()
