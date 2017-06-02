# Whisper
Whisper is a straightforward and convenient publishing tool for personal JSON Feeds. It is made with Python, and has the following parts:

- A CGI script that assembles feeds from directories of Yaml files
- A source-able bash file that contains functions for publishing to the above feeds
- A Python library that contains utilities used by the above
- Some apache configuration to make the CGI work.

Publication of blogs is just one of many use cases for simple feeds of serialised items. Inspired by the recent introduction of the JSON Feed standard, I started work on a WebVR client for JSON feeds - [which can be found here](http://ajrowr.github.com/gadabout/) - and came to realise that having a super-simple means of publishing something to a feed could be not only a great way of expressing my thoughts, but also a very useful organisational tool. 

### Parameters:
- Must be simple to use
- Any required processing must be self-containable in a Python CGI
- No database or other non-optional daemon dependencies
- Data files are YAML
- Data files are scriptable

### Setup
- Git clone this repo to your preferred location on your system (in a virtualenv if that's how you roll)
- `pip install requests && pip install PyYAML`
- Create a folder for your feeds (we'll call it `$FEEDS_ROOT`) and mkdir subfolders for feeds you want
- Adapt the apache config to your needs and system layout (including changing `SetEnv FEEDS_ROOT ...` to the feeds path you created above) and install it in your Apache using your preferred means
- Likewise the project.sh file
- `service apache2 reload`
- `source project.sh`

.. and you should be ready to go, if your setup is similar to mine. You may need to fiddle with your apache config and some other things. (I write a lot of CGIs in Python; if you don't then there might be some tweaks needed to your apache conf for that).

To test it, make at least one subdir in your `$FEEDS_ROOT` - let's use `todo` as an example.
````
mkdir $FEEDS_ROOT/todo
whisper todo
````

This will bring up a prompt - `title:` - so enter the title you want for this entry in the feed.
Then you will be prompted for `content_text:` - enter some content text.
Now, have a look in the `$FEEDS_ROOT/todo` - there should be a Yaml file named for the date and time. `cat` it to have a look at its structure - it's deliberately simple, but it contains all the required fields for an item in a JSON Feed.

Next, check that the feed assembler is working by visiting `http://your-vhost-name.domain.tld/feed/todo` in a browser. You should see a JSON representation of your single-entry todo feed. As you add more items to your feed, they will appear at the top of the feed.

One more step to create formally-correct JSON Feeds. Add a file in your feed dir called `feedinfo.yaml`. It should look something like this:

````
version: https://jsonfeed.org/version/1
title: Title of my Feed
````

Whisper will still generate a feed if this file is missing, but it won't be conformant to the JSON Feed standard.

### Scripts

The JSON Feed standard provides for third-party extensions by adding keys prefixed with an underscore. Whisper has a simple scripting interface that lives in the `_script` key of the `feedinfo.yaml` file. This key contains a dictionary mapping of names to scripts.

In Python terms, these scripts are lambdas (or, any expression resulting in a function) expressed as a string that is fed to `eval()` at runtime. The resulting function is then called with a single argument; the entire feed as a dictionary. When a feed is assembled, all the functions are called in this way, and the results are assembled into a dictionary in the `_scripts_output` key of the feed. Let's look at an example.

__*TODO add an example*__



Now, go forth and make feeds, and populate them!


