import subprocess, shutil, sys, os

def build():
    """Build the C++ extension module."""
    print("Building C++ extension module...")
    
    try:
        # Configure with CMake
        python_exe = sys.executable
        subprocess.check_call([
            'cmake',
            '--preset=vcpkg',
            f'-DPython_EXECUTABLE={python_exe}',
            f'-DPython3_EXECUTABLE={python_exe}'
        ])
        
        # Build in Release mode
        subprocess.check_call(['cmake', '--build', 'build', '--config', 'Release'])
        
        # Copy the built extension to the package directory
        # Note: The exact filename may vary based on Python version and platform
        build_dir = './build/cpp/Release'
        target_dir = './src/{{ cookiecutter.module_name }}'
        
        # Find the .pyd or .so file
        for file in os.listdir(build_dir):
            if file.startswith('{{ cookiecutter.module_name }}_core') and (file.endswith('.pyd') or file.endswith('.so')):
                src_file = os.path.join(build_dir, file)
                dst_file = os.path.join(target_dir, '{{ cookiecutter.module_name }}_core.pyd' if file.endswith('.pyd') else '{{ cookiecutter.module_name }}_core.so')
                print(f"Copying {src_file} to {dst_file}")
                shutil.copyfile(src_file, dst_file)
                break
        else:
            print("Warning: Could not find built extension module", file=sys.stderr)
            
        print("Build completed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    success = build()
    sys.exit(0 if success else 1)
