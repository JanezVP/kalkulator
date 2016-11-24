#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class RezultatHandler(BaseHandler):
    def post(self):
        stevilkaena = self.request.get("steviloena")
        stevilkadve = self.request.get("stevilodve")

        sestevek = int(stevilkaena) + int(stevilkadve)

        params = {"plus": sestevek}
        return self.render_template("rezultat.html", params=params)



class ZmnozekHandler(BaseHandler):
    def post(self):
        stevilkaena = self.request.get("steviloena")
        stevilkadve = self.request.get("stevilodve")

        zmnozek = int(stevilkaena) * int(stevilkadve)

        params = {"krat": zmnozek}
        return self.render_template("zmnozek.html", params=params)

class IndexHandler(BaseHandler):
    def post(self):
        stevilkaena = self.request.get("steviloena")
        stevilkadve = self.request.get("stevilodve")

        index = int(stevilkadve) / ((float(stevilkaena) / 100) ** 2.00)

        params = {"kilo": index}
        return self.render_template("index.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/zmnozek', ZmnozekHandler),
    webapp2.Route('/index', IndexHandler),
], debug=True)