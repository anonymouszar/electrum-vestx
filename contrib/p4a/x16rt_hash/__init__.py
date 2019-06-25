from pythonforandroid.recipe import CythonRecipe


class X16RTHashRecipe(CythonRecipe):

    url = 'https://github.com/anonymouszar/x16rt_hash/releases/download/v1.0.2/x16rt_hash-1.0.2.tar.gz'
    version = '1.0.2'
    depends = ['python3']

    def should_build(self, arch):
        """It's faster to build than check"""
        return True


recipe = X16RTHashRecipe()
