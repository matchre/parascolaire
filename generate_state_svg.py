#!/usr/bin/env python3
#! coding: utf-8
from __future__ import print_function

import argparse
import xml.dom.minidom
import re

from generate_utils import OutFile

p = argparse.ArgumentParser(description='''
    In a svg file {x}.svg, look for every layer and creates {x}.state-{i}.svg
    for all detected states.
    
    The layers names may have set-pattern like
    {1} (include me in state 1)
    or {1,4,5} (in states 1 4 and 5)
    or {7,8,a} (in states 7 8 and a)
    or {1-5} (in states 1,2,3,4,5)
    or {hello-x, world} (in states "hello-w" and "world")
''')

p.add_argument('svg_file', nargs='+')

g = p.add_mutually_exclusive_group()
g.add_argument('--numeric-layers', action='store_true', help='''
    Overrides the default behaviour, and create states 1 2 3 ... where each layer is a slide''')
g.add_argument('--layer-name', action='store_true', help='''
    Overrides the default behaviour, and create states {name of layer 1} {name of layer 2} {name of layer 3} ... where each layer is a slide''')

a = args = p.parse_args()

# for x in range(150): print(x, '\033[' + str(x) + 'm', 'Hel', '\033[0m')
def print_warning(*args): # orange
    print('\033[33m' + 'Warning:', *(args + ('\033[0m',)))
    
def print_info(*args): # green
    print('\033[32m' + 'Info:', *(args + ('\033[0m',)))
    
def print_error(*args): # error
    print('\033[31m' + 'Error:', *(args + ('\033[0m',)))
    
for svg_file in args.svg_file:
    if not svg_file.endswith('.svg'):
        print_error('filename is not .svg', svg_file)
        continue
    
    svg_filename = svg_file[:-4]
    with open(svg_file) as f:
        doc = xml.dom.minidom.parse(f)
        root = doc.documentElement

    def set_union(iterable):
        it = iter(iterable)
        try:
            S1 = next(it)
        except StopIteration:
            return set()
        return set.union(S1, *it)

    INK = 'http://www.inkscape.org/namespaces/inkscape'

    layers = [x for x in root.childNodes
            if getattr(x, 'tagName', None) == 'g'
            if x.getAttributeNS(INK, 'groupmode') == 'layer']

    R = re.compile('''
        \{(
        \d+ (- \d+)?
        ((\s+|\s*,\s*) \d+ (- \d+)?)*
        (\s+|\s*,\s*)?
        )\}''', re.X)

    all_infos = []
    nexts = {}
    for i,layer in enumerate(layers):
        nexts[layer] = layer.nextSibling
        
        if args.numeric_layers:
            all_infos.append((layer, {str(i+1)}))
            continue
        
        l = layer.getAttributeNS(INK, 'label').strip()
        
        if args.layer_name:
            all_infos.append((layer, {l}))
            continue
        
        m = re.search('\{[^{}]*\}', l)
        if not m:
            print_info('Layer on every slide :', l)
            continue
        
        S = set()
        for I in (s.strip() for s in m.group(1).split(',')):
            if re.match('\d+\s*-\s*\d+', I):
                a,b = tuple(map(int, I.split('-')))
                S |= set(map(str, range(a,b+1)))
            else:
                S.add(I)
            
        all_infos.append((layer, S))
        
    # all_infos : {
    #  DOM Element g[groupmode=layer]: {'1', '5', '6', '7', 'a'},
    #  DOM Element g[groupmode=layer]: {'a'},
    # }
    # first g will be include in slides 1 5 6 7 a
    # 
    # other slides non having S(...) infos will always be included

    if all_infos:
        slides = set_union(info for layer, info in all_infos)

        for slide in slides:
            new = OutFile("{}.state-{}.svg".format(svg_filename, slide))
            with new as f:
                for layer, info in all_infos:
                    if slide not in info:
                        root.removeChild(layer)
                f.write(root.toxml())
                for layer, info in reversed(all_infos):
                    if slide not in info:
                        root.insertBefore(layer, nexts[layer])
            print('Created', new.filename)