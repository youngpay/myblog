'''
Created on 2013-6-20

@author: yangpei
'''
import tornado.web
import logging

class ThemeCss(tornado.web.UIModule):
    def render(self, entry, show_comments=False):
        themeFile = "themes/" + entry + ".html"
        try:
            return self.render_string(themeFile)
        except IOError:
            logging.error("No such file:" + themeFile)
            return self.render_string("themes/slate.html")