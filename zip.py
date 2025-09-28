import shutil

# Replace 'project_folder' with the path to your project folder
project_folder = 'path_to_your_project_folder'
output_zip = 'project.zip'

# Create a ZIP file
shutil.make_archive('project', 'zip', project_folder)

print(f"Project has been zipped as {output_zip}")