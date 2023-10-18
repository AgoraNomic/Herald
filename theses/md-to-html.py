# you need to grab the markdown package from pip or your distro
from markdown import markdown
import os
from datetime import datetime
import re
from hashlib import md5

# config these as please
txt_dir = "md"
post_dir = "html"
post_template = "template.html"

new_posts = os.listdir(txt_dir)

for post in new_posts:
    title = post[:-4]
    print(title)
    
    post_file = f"{title}.md"

    # process the md into html
    f = open(f"{txt_dir}/{post}").read()
    output=markdown(f)
        
    # open the html template and map output to it
    html_doc = open(post_template).read()
    html_mapping = {'post': output, 'title': title}
    html_out = html_doc.format_map(html_mapping)
    with open(f"{post_dir}/{post_file}", 'w') as ofile:
        ofile.write(html_out)
