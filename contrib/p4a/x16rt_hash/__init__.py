from pythonforandroid.recipe import CythonRecipe


class X16RTHashRecipe(CythonRecipe):

    url = 'https://files.pythonhosted.org/packages/77/d2/83e12ad85a42859b7d1699180c5d8b39af8689a82ae9aa638e854db3eb53/x16rt_hash-1.0.1.tar.gz'
    version = '1.0.1'
    depends = ['python3']

    def should_build(self, arch):
        """It's faster to build than check"""
        return True


recipe = X16RTHashRecipe()
