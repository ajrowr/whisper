#!/usr/bin/env python

import yaml, datetime, os

env = lambda *a: os.environ.get(*a)
feeddir = lambda feedname: os.path.join(env('FEEDS_ROOT', '/home/alan/projects/_/2017/Whisper/feeds'), feedname)
fpath = lambda feed: lambda fname='': os.path.join(feeddir(feed), fname)


def loadyaml(fname):
    with open(fname) as f:
        return yaml.load(f.read())


def newitem(feed, data={}, fname=None):
    p = fpath(feed)
    fid = datetime.datetime.now().isoformat().split('.')[0].replace(':','_')
    fname = fname or "item_{}.yaml".format(fid)
    data.update({'id': fid})
    with open(p(fname), 'w') as fout:
        yaml.dump(data, stream=fout, default_flow_style=False)
    return p(fname)


def add(feed, fields=['title', 'content_text']):
    dat = dict(
        date_published = datetime.datetime.now().isoformat()
    )
    for f in fields:
        dat[f] = raw_input("{}: ".format(f))
    print
    print newitem(feed, dat)


def loadfeed(feed):
    # feed_dir = feeddir(feed)
    p = fpath(feed)
    feeddata = {}
    
    try:
        with open(p('feedinfo.yaml'), 'r') as metafile:
            feeddata = yaml.load(metafile.read())
    except:
        feeddata['message'] = 'feedinfo.yaml is missing'
        
    feeditems = filter(lambda fn: fn.startswith('item'), os.listdir(p()))
    feeditems.sort(reverse=True) # key= ..
    feeddata['items'] = map(loadyaml, [p(f) for f in feeditems])
    if '_scripts' in feeddata:
        feeddata['_scripts_output'] = dict(map(lambda scr: (scr[0], eval(scr[1])(feeddata)), feeddata['_scripts'].items()))
    return feeddata
