# Markdown to Dash Docset

[Dash](https://kapeli.com/dash) was my favorite documentation app on macOS. Besides reading tech docs, I also use it for reading tech books due to its handy search functionalities.

This python utils was created for converting ebook written in markdown to HTML files, that are suitable for generating Dash docset later on. It's written in jupyter format for easy debugging and exploratory coding. So you have to run with VSCode instead of running directly with python.

## Tooling

- jupyter in vscode for exploratory dev style
- YAML for configuration
- [Pygments](https://pygments.org/) as syntax highlighter
- [less css](https://lesscss.org/) as css preprocessor
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/) for manipulating HTML elements (insert, append...etc)

After creating the HTML files, generate Dash docset with [dashing](https://github.com/technosophos/dashing) CLI.

# Required Python Packages

```toml
bs4 = "^0.0.1"
pyyaml = "^6.0"
markdown2 = "^2.4.6"
jupyter = "^1.0.0"
lesscpy = "^0.15.1"
```

# Usage

- put markdown files in `src` folder
- edit config.yaml to suit your package
- replace icon.png
- run all cells in md2html.py in VSCode
- in terminal
  - cd output
  - run `dashing build <package_name>`