import jinja2


from .config import blog_config as config
from .constants import *  # noqa


template_loader = jinja2.PackageLoader(
    APPLICATION_NAME,
    TEMPLATE_DIR)
if config.TEMPLATE_DIR is not None:
    template_loader = jinja2.ChoiceLoader([
        jinja2.FileSystemLoader(config.TEMPLATE_DIR),
        template_loader])
env = jinja2.Environment(loader=template_loader)


def jinja_template_writer(template, content, fh):
    """
    Render the given jinja template and write the
    output to fh.
    """
    template = env.get_template(template)
    template_stream = template.stream(content=content)
    template_stream.dump(fh)
