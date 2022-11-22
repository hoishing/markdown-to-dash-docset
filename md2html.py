# %%
from markdown2 import markdown_path
from pathlib import Path
from bs4 import BeautifulSoup as bs
import re, yaml
from collections import namedtuple

src = Path("src")
op_dir = Path("output")
css = "style.css"
pygment = "pygment.css"
config_dict = yaml.safe_load(Path("config.yaml").open())
config = namedtuple("Config", field_names=config_dict)(**config_dict)

# markdown files
mds = sorted(p for p in src.iterdir() if p.suffix == ".md")


# %%
def link_file(file_str):
    path = op_dir / file_str
    if not path.exists():
        path.symlink_to(Path("..") / file_str)


def remove_digits(name):
    return re.sub(r"\d+-", "", name)


def head() -> bs:
    """return BeautifulSoup obj with css files as HTML header"""
    links = [
        f'<link rel="stylesheet" type="text/css" href="{c}">' for c in (css, pygment)
    ]
    head = f'<head><meta charset="utf-8">{"".join(links)}</head>'
    return bs(head, "html.parser")


def nav(md: Path) -> bs:
    """return BeafifulSoup obj for docset navigation"""

    def a_tag(idx):
        """remove digits for html <a> tag"""
        name = mds[idx].stem
        file = name + ".html"
        return f'<a href="{file}">{remove_digits(name)}</a>'

    idx = mds.index(md)
    prev = "" if idx == 0 else a_tag(idx - 1)
    next = "" if idx + 1 == len(mds) else a_tag(idx + 1)
    nav_tpl = """
    <div class="navi">
        <div class="prev">{}</div>
        <div class="idx"><a href="index.html">index</a></div>
        <div class="next">{}</div>
    </div>
    """
    return bs(nav_tpl.format(prev, next), "html.parser")


# %%
# convert md to html
for md in mds:
    md_html = markdown_path(md, extras=["fenced-code-blocks"])
    main = f'<div class="main">{md_html}</div>'
    sp = bs(main, "lxml")
    sp.html.insert(0, head())
    sp.body.insert(0, nav(md))
    sp.body.append(nav(md))
    p = op_dir / (md.stem + ".html")
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(str(sp))

# %%
# create index.html
chapters = "\n".join(
    [
        '<li><a href="{}.html">{}</a></li>'.format(md.stem, remove_digits(md.stem))
        for md in mds
    ]
)

template = """
<html>
{head}
<body>
  <div class="header">
      <h1>{bookname}</h1>
      <div class="author">
          <p>author: <a href="{author_url}">{author}</a></p>
          <p>source: <a href="{source}">{source}</a></p>
      </div>
  </div>
  <div class="main">
      <h2>table of contents</h2>
      <ul class="toc">
          {chapters}
      </ul>
  </div>
  <div class="footer">license: <a href="{license_url}">{license}</a></div>
</body>
</html>
"""

html = template.format(
    bookname=config_dict.bookname,
    author=config_dict.author,
    author_url=config_dict.author_url,
    source=config_dict.source,
    license=config_dict.license,
    license_url=config_dict.license_url,
    head=str(head()),
    chapters=chapters,
)

(op_dir / "index.html").write_text(html)

# %%
# create asset files
import lesscpy

css_content = lesscpy.compile(Path("style.less").open())
(op_dir / css).write_text(css_content)

link_file("icon.png")
link_file(pygment)
link_file("PTMono-Regular.woff")

import json

(op_dir / "dashing.json").write_text(json.dumps(config_dict.dashing, indent=2))
