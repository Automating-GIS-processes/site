# -*- coding: utf-8 -*-
"""
    sphinxcontrib.slide
    ~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2012 by Takeshi KOMIYA
    :license: BSD, see LICENSE for details.
"""

import re
import urllib as urllib2
from docutils import nodes
from sphinx.util.compat import Directive


class slide(nodes.General, nodes.Element):
    pass


class SlideDirective(Directive):
    """Directive for embedding slide"""

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True
    option_spec = {
    }

    def run(self):
        try:
            node = slide()
            node['url'] = self.arguments[0]
            node['slide_options'] = get_slide_options(self.arguments[0])

            return [node]
        except Exception as e:
            reporter = self.state.document.reporter
            return [reporter.warning(str(e), line=self.lineno)]


def get_slide_options(url):
    if re.match('https://docs.google.com/presentation/(pub\?|d/)', url):
        return get_slide_options_for_googledocs(url)
    elif re.match('http://www.slideshare.net/', url):
        return get_slide_options_for_slideshare(url)
    elif re.match('https://speakerdeck.com/', url):
        return get_slide_options_for_speakerdeck(url)
    elif re.match('https?://slides.com/', url):
        return get_slide_options_for_slides_com(url)
    else:
        msg = 'unknown slide URL: %s' % url
        raise Exception(msg)


def get_slide_options_for_googledocs(url):
    options = {}
    options['type'] = 'googledocs'
    if re.search('/presentation/pub', url):
        options['embed_url'] = re.sub('/pub\?', '/embed?', url)
    elif re.search('/presentation/d/', url):
        options['embed_url'] = re.sub('/edit.*', '', re.sub('/d/', '/embed?id=', url))

    content = urllib2.urlopen(url).read()
    matched = re.search('<title>(.*?)</title>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    return options


def get_slide_options_for_slideshare(url):
    options = {}
    options['type'] = 'slideshare'

    content = urllib2.urlopen(url).read()
    matched = re.search('http://www.slideshare.net/slideshow/embed_code/\d+', content)
    if matched:
        options['embed_url'] = matched.group(0)

    matched = re.search('<title>(.*?)</title>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    matched = re.search('<meta name="slideshow_author".*? content="(.*?)" />', content)
    if matched:
        options['author_url'] = matched.group(1)

    matched = re.search('<img class="h-author-image".*? alt="(.*?)" width="50" />', content)
    if matched:
        options['author_name'] = matched.group(1).decode('utf-8')

    return options


def get_slide_options_for_speakerdeck(url):
    options = {}
    options['type'] = 'speakerdeck'

    content = urllib2.urlopen(url).read()
    matched = re.search('<h1>(.*?)</h1>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    matched = re.search('data-id="(.*?)"', content)
    if matched:
        options['data_id'] = matched.group(1).decode('utf-8')

    matched = re.search('data-ratio="(.*?)"', content)
    if matched:
        options['data_ratio'] = matched.group(1).decode('utf-8')

    return options


def get_slide_options_for_slides_com(url):
    options = {}
    options['type'] = 'slides.com'
    options['embed_url'] = re.sub('https?:', '', re.sub('#/$', '', url)) + '/embed'

    content = urllib2.urlopen(url).read()
    matched = re.search('<h4>(.*?)</h4>', content)
    if matched:
        options['title'] = matched.group(1).decode('utf-8')

    return options


def html_visit_slide_node(self, node):
    options = node['slide_options']

    if options['type'] == 'googledocs':
        template = """<iframe src="%s" frameborder="0" width="480" height="375" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"> </iframe>"""
        self.body.append(template % options.get('embed_url'))
    elif options['type'] == 'slideshare':
        template = """<iframe src="%s" width="427" height="356" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC;border-width:1px 1px 0;margin-bottom:5px" allowfullscreen="true"> </iframe> <div style="margin-bottom:5px"> <strong> <a href="%s" title="%s" target="_blank">%s</a> </strong> from <strong><a href="%s" target="_blank">%s</a></strong> </div>"""
        self.body.append(template % (options.get('embed_url'),
                                     node.get('url'),
                                     options.get('title', ""),
                                     options.get('title', ""),
                                     options.get('author_url'),
                                     options.get('author_name', "")))
    elif options['type'] == 'speakerdeck':
        template = """<script async="async" class="speakerdeck-embed" data-id="%s" data-ratio="%s" src="//speakerdeck.com/assets/embed.js"> </script>"""
        self.body.append(template % (options.get('data_id'), options.get('data_ratio')))
    elif options['type'] == 'slides.com':
        template = ('<iframe src="%s" width="576" height="420" scrolling="no"'
                    ' frameborder="0" webkitallowfullscreen mozallowfullscreen'
                    ' allowfullscreen></iframe>')
        self.body.append(template % options.get('embed_url'))


def latex_visit_slide_node(self, node):
    title = node['slide_options'].get('title')

    if title:
        self.body.append("\\href{%s}{%s}" % (self.encode_uri(node['url']), self.encode(title)))
    else:
        self.body.append("\\url{%s}" % self.encode_uri(node['url']))


def depart_slide_node(self, node):
    pass


def setup(app):
    app.add_node(slide,
                 html=(html_visit_slide_node, depart_slide_node),
                 latex=(latex_visit_slide_node, depart_slide_node))
    app.add_directive('slide', SlideDirective)
