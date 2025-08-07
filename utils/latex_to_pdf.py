import subprocess
import tempfile
import os
import shutil
from typing import Tuple, Optional

def is_pdflatex_installed() -> bool:
    """Check if pdflatex is installed and available in PATH."""
    return shutil.which('pdflatex') is not None

def install_pdflatex() -> bool:
    """Attempt to install pdflatex using the system package manager."""
    try:
        print("\n⚠️ pdflatex not found. Attempting to install LaTeX...")
        # Try to determine the package manager and install texlive
        if shutil.which('apt-get'):  # Debian/Ubuntu
            subprocess.run(['sudo', 'apt-get', 'update'], check=True)
            subprocess.run(['sudo', 'apt-get', 'install', '-y', 'texlive-latex-base', 'texlive-latex-extra'], check=True)
        elif shutil.which('dnf'):  # Fedora
            subprocess.run(['sudo', 'dnf', 'install', '-y', 'texlive-scheme-basic'], check=True)
        elif shutil.which('pacman'):  # Arch Linux
            subprocess.run(['sudo', 'pacman', '-S', '--noconfirm', 'texlive-core'], check=True)
        else:
            print("⚠️ Could not determine package manager. Please install LaTeX manually.")
            return False
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install LaTeX: {e}")
        return False

def convert_to_pdf(latex_content: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Convert LaTeX content to PDF.
    
    Args:
        latex_content: LaTeX content as a string
        
    Returns:
        Tuple containing (pdf_path, error_message). If successful, error_message is None.
        If failed, pdf_path is None and error_message contains the error details.
    """
    # Check if pdflatex is installed
    if not is_pdflatex_installed():
        if not install_pdflatex():
            return None, "LaTeX (pdflatex) is not installed and could not be installed automatically. " \
                      "Please install it manually and try again."
    
    # Create a temporary directory for LaTeX compilation
    temp_dir = tempfile.mkdtemp()
    tex_path = os.path.join(temp_dir, 'resume.tex')
    
    try:
        # Write the LaTeX content to a file
        with open(tex_path, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        # Compile the LaTeX file to PDF
        result = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", temp_dir, tex_path],
            capture_output=True,
            text=True,
            cwd=temp_dir
        )
        
        # Check if PDF was generated
        pdf_path = os.path.join(temp_dir, 'resume.pdf')
        if not os.path.exists(pdf_path):
            # If no PDF was generated, return the LaTeX log for debugging
            log_path = os.path.join(temp_dir, 'resume.log')
            log_content = ""
            if os.path.exists(log_path):
                with open(log_path, 'r') as f:
                    log_content = f.read()
            
            error_msg = f"Failed to generate PDF. LaTeX compilation failed.\n\n"
            if result.stderr:
                error_msg += f"Error output:\n{result.stderr}\n\n"
            if log_content:
                error_msg += f"LaTeX log:\n{log_content}"
            
            return None, error_msg
        
        return pdf_path, None
        
    except Exception as e:
        return None, f"An error occurred during PDF generation: {str(e)}"
    finally:
        # Clean up temporary files (keeping the PDF if it was generated)
        if os.path.exists(tex_path):
            os.remove(tex_path)
        for ext in ['.aux', '.log', '.out']:
            temp_file = os.path.join(temp_dir, f'resume{ext}')
            if os.path.exists(temp_file):
                os.remove(temp_file)
