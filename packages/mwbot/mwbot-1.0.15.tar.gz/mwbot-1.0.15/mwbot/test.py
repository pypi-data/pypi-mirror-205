from .utils import templates_env

ENV = templates_env()
a = ENV.render(T_NAME="test.jinja")
print(a)
a = ENV.render(T_NAME="test.jinja",my_param="S")
print(a)
