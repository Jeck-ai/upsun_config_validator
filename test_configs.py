import os
import shutil
import subprocess
from concurrent.futures import ProcessPoolExecutor, as_completed
from datetime import datetime
import time
import fcntl
import errno

class FileLock:
    def __init__(self, path):
        self.path = path
        self.lockfile = f"{path}.lock"
        self.fd = None

    def __enter__(self):
        while True:
            try:
                self.fd = os.open(self.lockfile, os.O_CREAT | os.O_EXCL | os.O_RDWR)
                break
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
                time.sleep(0.1)
        return self

    def __exit__(self, *args):
        if self.fd:
            os.close(self.fd)
            os.unlink(self.lockfile)

def get_yaml_files(test_dir):
    yaml_files = []
    passing_configs_dir = os.path.join(test_dir, 'passing_configs')
    for root, _, files in os.walk(passing_configs_dir):
        for file in files:
            if file.endswith('.yaml'):
                yaml_files.append(os.path.join(root, file))
    return yaml_files

def divide_files(yaml_files, num_groups=3):
    groups = [[] for _ in range(num_groups)]
    for i, file in enumerate(yaml_files):
        groups[i % num_groups].append(file)
    return groups

def log_to_file(log_dir, upsun_dir, yaml_file, message):
    timestamp = datetime.now().strftime('%H:%M:%S')
    log_file = os.path.join(log_dir, f"{os.path.basename(upsun_dir)}.log")
    with open(log_file, 'a') as f:
        f.write(f"\n=== {yaml_file} ===\n")
        f.write(f"[{timestamp}] {message}\n")

def process_yaml_file(args):
    upsun_dir, yaml_file, log_dir, dir_num = args
    yaml_basename = os.path.basename(yaml_file)
    timestamp = datetime.now().strftime('%H:%M:%S')
    remote_name = f"upsun{dir_num}"
    
    try:
        log_to_file(log_dir, upsun_dir, yaml_basename, f"Starting processing of {yaml_basename}")
        print(f"\n[{timestamp}] {upsun_dir}: Starting {yaml_basename}")
        
        # Create .upsun directory if it doesn't exist
        upsun_config_dir = os.path.join(upsun_dir, '.upsun')
        os.makedirs(upsun_config_dir, exist_ok=True)
        
        # Copy YAML file to config.yaml
        config_path = os.path.join(upsun_config_dir, 'config.yaml')
        shutil.copy2(yaml_file, config_path)
        
        # Git and Upsun operations with lock
        with FileLock(upsun_dir):
            # Git operations
            git_add = subprocess.run(['git', 'add', '.'], cwd=upsun_dir,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True)
            if git_add.stderr:
                log_to_file(log_dir, upsun_dir, yaml_basename, f"Git add stderr:\n{git_add.stderr}")
            
            commit_msg = f"testing {yaml_basename}"
            git_commit = subprocess.run(['git', 'commit', '-m', commit_msg], cwd=upsun_dir,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         text=True)
            if git_commit.stderr:
                log_to_file(log_dir, upsun_dir, yaml_basename, f"Git commit stderr:\n{git_commit.stderr}")
            
            print(f"[{timestamp}] {upsun_dir}: Pushing {yaml_basename}")
            
            # Git push with full output capture
            push = subprocess.run(['git', 'push', '--set-upstream', 'upsun', 'main'], 
                                cwd=upsun_dir,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)
            
            # Log full git push output
            log_to_file(log_dir, upsun_dir, yaml_basename, 
                       f"Git push output:\nstdout:\n{push.stdout}\nstderr:\n{push.stderr}")
            
            # Raise exception if push failed due to invalid config
            if "invalid configuration files" in push.stderr:
                raise Exception("Git push failed due to invalid configuration")
        
        print(f"[{timestamp}] {upsun_dir}: Completed {yaml_basename}")
        log_to_file(log_dir, upsun_dir, yaml_basename, "Completed successfully")
        
        return {
            'file': yaml_file,
            'status': 'success',
            'output': push.stdout,
            'dir': upsun_dir
        }
        
    except subprocess.CalledProcessError as e:
        error_msg = f"Command failed: {e.cmd}\nOutput:\nstdout: {e.stdout}\nstderr: {e.stderr}"
        log_to_file(log_dir, upsun_dir, yaml_basename, f"ERROR: {error_msg}")
        return {
            'file': yaml_file,
            'status': 'failure',
            'error': error_msg,
            'dir': upsun_dir
        }
    except Exception as e:
        error_msg = str(e)
        log_to_file(log_dir, upsun_dir, yaml_basename, f"ERROR: {error_msg}")
        return {
            'file': yaml_file,
            'status': 'failure',
            'error': error_msg,
            'dir': upsun_dir
        }

def main():
    # Base directories
    base_dir = os.getcwd()  # Assuming running from project root
    test_dir = os.path.join(base_dir, 'tests')
    
    # Create logs directory
    log_dir = os.path.join(base_dir, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Clear previous logs
    for file in os.listdir(log_dir):
        os.unlink(os.path.join(log_dir, file))
    
    # The upsun directories are in the project root
    upsun_dirs = [
        os.path.join(base_dir, 'upsun'),
        os.path.join(base_dir, 'upsun2'),
        os.path.join(base_dir, 'upsun3')
    ]

    # Verify directories exist
    for dir_path in upsun_dirs:
        if not os.path.isdir(dir_path):
            print(f"Error: Directory not found: {dir_path}")
            return 1

    # Get all YAML files from passing_configs only
    yaml_files = get_yaml_files(test_dir)
    print(f"Found {len(yaml_files)} valid YAML files to process")
    
    # Divide files into groups
    file_groups = divide_files(yaml_files)
    
    # Create work items
    work_items = []
    for i, (upsun_dir, files) in enumerate(zip(upsun_dirs, file_groups), 1):
        for file in files:
            work_items.append((upsun_dir, file, log_dir, i))
    
    # Clean up any existing lock files
    for upsun_dir in upsun_dirs:
        lockfile = f"{upsun_dir}.lock"
        if os.path.exists(lockfile):
            os.unlink(lockfile)
    
    # Process files in parallel using as_completed for better output handling
    with ProcessPoolExecutor(max_workers=3) as executor:
        future_to_work = {executor.submit(process_yaml_file, item): item for item in work_items}
        for future in as_completed(future_to_work):
            result = future.result()
            if result['status'] == 'failure':
                print(f"\nFailed in {result['dir']}: {result['error']}")
                # Cancel all pending futures
                for f in future_to_work:
                    f.cancel()
                return 1
    
    return 0

if __name__ == '__main__':
    exit(main())