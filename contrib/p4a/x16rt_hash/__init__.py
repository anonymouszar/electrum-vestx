from pythonforandroid.recipe import CythonRecipe


class X11HashRecipe(CythonRecipe):

    url = 'https://files.pythonhosted.org/packages/76/50/b1bd87b5e4411e177417aff138e7396fc02eee585777f863de2f6e7a706c/x16rt_hash-{version}.tar.gz'
    version = '1.0.0'
    depends = ['python3']

    def should_build(self, arch):
        """It's faster to build than check"""
        return True


recipe = X11HashRecipe()
