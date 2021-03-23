
Intro
=====
The lack of standard terminology in industry experimentation is a pedantic but real
obstacle to building a strong data-driven culture. This repo has a very modest goal: to
compile the terms used by various sources and organizations, and to provide a very
lightweight tool for querying that data easily.

What can I do with it?
----------------------
This project is inteneded to answer questions like:
- Company X is using the term T in its experimentation blog post/product documentation -
  **what do they mean when they use that term?** Google Optimize, for example, uses the
  term `variant` to refer to what other people call a `level`. Netflix blog posts, for
  another example, often mention `cells`, which (at least to our knowledge) is entirely
  unique to them.
  
- I'm interviewing or giving a talk at Company X soon, give me a list of **all of
  Company X's experimentation vernacular.**

- I want to use term T to mean something specific, is that standard? Tell me **what
  various organizations mean when they use term T.**

What does this tool not do?
--------------
This tool is *not* meant to be a glossary of all A/B testing terms. It does not include
terms that have a precise statistical definition, like `p-value`. It also does not
include terms that are universally agreed upon. Lastly, it is restricted to
experimentation; let's not creep into optimization or machine learning.

ABGlossary does not define its own standard terminology, at least for now. That means
you can't look up the terms that relate to a particular *concept*, e.g. "give me all the
terms that refer to the concept of assignment of subjects to variants".

Installation
============
ABGlossary is tested on Python 3.8. We cannot confirm that it works with other Python
versions.

With a bash(-like) terminal:

1. Clone the repo locally and navigate to the local repo folder.
    ```bash
    $ git clone git@github.com:CrosstabKite/ABGlossary.git
    $ cd ABGlossary
    ```

2. Install the required packages in a Python virtual environment (e.g. Conda) and
   activate the environment. Let's say we have a conda environment named `abgloss-test`.
    ```bash
    $ conda activate abgloss-test
    $ pip install -r requirements.txt
    ```
  
Usage
=====
There are two modes of usage: 1. the command line utility, and 2. simply opening the
data file `terminology.yaml` in a text editor and using Ctrl+f to search for interesting
things.

Command line utility
--------------
The CLI is the python script `abglossary.py`. It has two subcommands: `list`, which
lists all the terms, organizations, or sources that are in the data file, and `query`,
which filters the data to a specified organization and/or term and sorts according to
any of the output fields.

To see the CLI documentation:
```bash
$ python abglossary.py --help
$ python abglossary.py list --help
$ python abglossar.py query --help
```

To list all organizations with at least one entry in the data file:
```bash
$ python abglossary.py list orgs
```

Also try listing `sources` and `terms` in place of `orgs`.

To query all entries for a particular organization, let's say Amazon:
```bash
$ python abglossary.py query -o Amazon
```

And to sort these results alphabetically by term:
```bash
$ python abglossary.py query -o Amazon -s terms
```

To see the full entries for the query results in dictionary instead of table form:
```bash
$ python abglossary.py query -o Amazon --verbose
```

Note that sorting has no effect with verbose printing.

Suppose we want to find how various organizations use a particular term, let's say
`variant`. To get that info:
```bash
$ python abglossary.py query -t variant
```

Finally, we can filter by both organization and term to answer the first question in the
intro:
```bash
$ python abglossary.py query -o Google -t variant
```

Note that ABGlossary is not (yet?) a search engine; filtering arguments must match the
data exactly to be retrieved.

The data file
-------------
Skimming or searching for the text in the data file (`terminology.yaml`) is also a good
way to use the data.

The data is organized by source, e.g. a blog post, product documentation, book chapter.
Each source has a *title*, URL *link*, organizations involved (*orgs*), authors if
named, and the map of terms to definitions.

Definitions pulled verbatim from a source are enclosed in double quotes, as are
synonyms. If a definition does not have quotes, it is our best attempt to paraphrase the
meaning of the term from the source. Many terms have no definition at all; we think it's
worth knowing a particular term is used, even if not accompanied by the definition.
